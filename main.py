from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import random
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# --- Load API key safely ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY is missing. Please set it in your .env file.")

# Configure Gemini
genai.configure(api_key=api_key)

# --- Disease Database (10 illnesses + symptom sets) ---
diseases = [
    {"name": "Influenza", "symptoms": ["fever", "cough", "sore throat", "headache", "muscle pain"]},
    {"name": "Gastritis", "symptoms": ["stomach pain", "nausea", "vomiting", "loss of appetite"]},
    {"name": "Migraine", "symptoms": ["throbbing headache", "light sensitivity", "nausea", "blurred vision"]},
    {"name": "Diabetes", "symptoms": ["thirst", "frequent urination", "fatigue", "unexplained weight loss"]},
    {"name": "Hypertension", "symptoms": ["headache", "dizziness", "chest discomfort", "blurred vision"]},
    {"name": "Anemia", "symptoms": ["fatigue", "pale skin", "shortness of breath", "dizziness"]},
    {"name": "Asthma", "symptoms": ["wheezing", "shortness of breath", "chest tightness", "coughing at night"]},
    {"name": "Food Poisoning", "symptoms": ["nausea", "vomiting", "diarrhea", "abdominal cramps"]},
    {"name": "Common Cold", "symptoms": ["runny nose", "sore throat", "sneezing", "mild cough"]},
    {"name": "COVID-19", "symptoms": ["fever", "dry cough", "loss of smell", "fatigue"]}
]

# --- Extra “distractor” symptoms to confuse the player ---
distractor_symptoms = [
    "mild back pain", "slight rash", "ear ringing", "occasional dizziness",
    "dry mouth", "trouble sleeping", "stiff neck", "mild nausea",
    "chills", "random muscle twitching", "minor toothache"
]

def generate_case():
    """Randomly choose a disease and add a few distractor symptoms, with progressive reveal."""
    case = random.choice(diseases)
    fake_symptoms = random.sample(distractor_symptoms, k=random.randint(1, 3))
    all_symptoms = list(set(case["symptoms"] + fake_symptoms))
    random.shuffle(all_symptoms)
    initial_reveal = all_symptoms[:random.randint(1, 2)]
    return {
        "name": case["name"],
        "symptoms": all_symptoms,
        "true_symptoms": case["symptoms"],  # used in the result card
        "extra": fake_symptoms,
        "revealed_symptoms": initial_reveal
    }

# --- Initialize global state ---
current_case = generate_case()
conversation_history = [
    {
        "role": "system",
        "content": (
            f"You are a patient diagnosed with {current_case['name']}. "
            f"You currently experience these symptoms: {', '.join(current_case['revealed_symptoms'])}. "
            "Speak naturally, casually, and do NOT list all symptoms at once. "
            "You may mention only 1–2 symptoms per answer, unless the doctor specifically asks for more. "
            "Never reveal the disease name."
        )
    }
]

def get_model():
    """Use latest available Gemini 2.5 model."""
    try:
        return genai.GenerativeModel("models/gemini-2.5-flash")
    except Exception as e:
        print("⚠️ gemini-2.5-flash not found, using fallback:", e)
        return genai.GenerativeModel("models/gemini-2.5-pro")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Handles doctor questions and patient replies."""
    user_message = request.json.get("message", "")
    conversation_history.append({"role": "user", "content": user_message})

    try:
        # Reveal 1 new symptom per chat round (if any remain)
        if len(current_case["revealed_symptoms"]) < len(current_case["symptoms"]):
            unrevealed = [s for s in current_case["symptoms"] if s not in current_case["revealed_symptoms"]]
            if unrevealed:
                new_symptom = random.choice(unrevealed)
                current_case["revealed_symptoms"].append(new_symptom)

        # Update system prompt to reflect current symptoms
        conversation_history[0] = {
            "role": "system",
            "content": (
                f"You are a patient diagnosed with {current_case['name']}. "
                f"You currently experience these symptoms: {', '.join(current_case['revealed_symptoms'])}. "
                "Speak naturally, casually, and do NOT list all symptoms at once. "
                "You may mention only 1–2 symptoms per answer, unless the doctor specifically asks for more. "
                "Never reveal the disease name."
            )
        }

        model = get_model()
        messages = [msg["content"] for msg in conversation_history]
        response = model.generate_content(messages)

        reply = response.text.strip() if response and hasattr(response, "text") else \
            "Sorry, I’m having trouble responding right now."

        conversation_history.append({"role": "assistant", "content": reply})

        # Return only currently revealed symptoms to the UI
        return jsonify({
            "reply": reply,
            "symptoms": current_case["revealed_symptoms"]
        })

    except Exception as e:
        print("Error in chat:", e)
        return jsonify({"reply": f"Error: {str(e)}"})

@app.route("/api/guess", methods=["POST"])
def guess():
    """Doctor guesses the diagnosis. Return details for the result card (no reset here)."""
    guess = request.json.get("guess", "")
    name = current_case["name"]

    if guess.lower() == name.lower():
        prevention_tips = {
            "Influenza": "Wash hands often, get vaccinated, avoid close contact with sick people.",
            "Gastritis": "Avoid spicy food, reduce stress, eat small meals, and limit alcohol.",
            "Migraine": "Reduce screen time, avoid loud noise, stay hydrated, rest in a quiet room.",
            "Diabetes": "Balanced diet, regular exercise, monitor blood sugar.",
            "Hypertension": "Reduce salt, exercise regularly, manage stress.",
            "Anemia": "Eat iron-rich foods (spinach, red meat), consider supplements.",
            "Asthma": "Avoid allergens, follow inhaler plan, avoid smoke.",
            "Food Poisoning": "Food hygiene, stay hydrated, avoid suspicious food.",
            "Common Cold": "Rest, warm fluids, avoid sudden temperature changes.",
            "COVID-19": "Vaccination, mask in crowded spaces, isolate when symptomatic."
        }
        treatment_tips = {
            "Influenza": "Rest, fluids, antiviral if prescribed.",
            "Gastritis": "Avoid caffeine/alcohol; antacids or medication if needed.",
            "Migraine": "Migraine meds, dark quiet room, avoid triggers.",
            "Diabetes": "Follow insulin/medication plan, regular glucose checks.",
            "Hypertension": "Antihypertensives as prescribed; low-salt diet; stress reduction.",
            "Anemia": "Iron/B12 supplements as prescribed.",
            "Asthma": "Bronchodilators, corticosteroids, follow action plan.",
            "Food Poisoning": "Oral rehydration, rest; seek care if severe.",
            "Common Cold": "OTC meds, hydration, rest.",
            "COVID-19": "Manage symptoms, rest, hydrate, follow public guidance."
        }

        return jsonify({
            "result": f"✅ Correct! The patient has {name}.",
            "disease_name": name,
            "true_symptoms": current_case["true_symptoms"],  # no distractors
            "prevention": prevention_tips.get(name, "General hygiene and healthy lifestyle."),
            "treatment": treatment_tips.get(name, "Consult your doctor for specific treatment.")
        })
    else:
        return jsonify({"result": "❌ Incorrect. Keep asking questions!"})

@app.route("/api/reset", methods=["POST"])
def reset():
    """Start a new patient case."""
    global current_case, conversation_history
    current_case = generate_case()
    conversation_history = [
        {
            "role": "system",
            "content": (
                f"You are a patient diagnosed with {current_case['name']}. "
                f"You currently experience these symptoms: {', '.join(current_case['revealed_symptoms'])}. "
                "Speak naturally, casually, and do NOT list all symptoms at once. "
                "You may mention only 1–2 symptoms per answer, unless the doctor specifically asks for more. "
                "Never reveal the disease name."
            )
        }
    ]
    return jsonify({"message": "New case generated!"})

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
