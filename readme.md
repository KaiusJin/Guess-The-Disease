# 🩺 Guess The Disease — Learn Medicine, Play Doctor

An AI-powered medical reasoning game that teaches health awareness through play. Built with **Python (Flask)** + **Gemini 2.5 AI** + **HTML/CSS/JS**, designed to make healthcare education accessible, empathetic, and fun.

## 🎯 Inspiration

Access to reliable healthcare knowledge is still limited in many parts of the world. We wanted to create a project that bridges this gap — **teaching people how diagnosis works** while also **building empathy for doctors**. Most people only see the outcome of a diagnosis, not the reasoning behind it. With *Guess The Disease*, we let players experience that reasoning process themselves — by **asking, interpreting, and diagnosing** a virtual patient powered by AI.

## 💡 What It Does

**Guess The Disease** is an interactive AI simulation where you play as a doctor trying to diagnose a patient. The AI, powered by **Google Gemini 2.5**, plays the role of a natural, conversational patient.

* Start a case → the patient describes a few initial symptoms
* Ask questions to reveal more clues
* Try to identify the illness
* When you guess correctly, a **diagnosis card** appears showing:

  * ✅ Official disease name
  * 💬 Verified symptoms (without distractors)
  * 💡 Prevention and treatment tips (from **NHS Inform**)
    It’s a fun way to **learn common diseases, understand medical logic, and practice critical reasoning** — all in a safe, gamified environment.

## ⚙️ Tech Stack

**Frontend:** HTML, CSS, and Vanilla JavaScript — dynamic chat interface between Doctor (user) and Patient (AI), glassmorphism-styled diagnosis modal with blur background, real-time symptom updates per AI response.
**Backend:** Python + Flask — integrated **Google Gemini 2.5 API** (`google-generativeai` SDK), controlled prompt system for symptom progression and realistic responses, randomized symptom distractors to simulate real clinical uncertainty.
**Data Sources:** Common disease symptoms and prevention info were **cross-referenced with [NHS Inform]（https://www.nhsinform.scot/illnesses-and-conditions/a-to-z/)**. Medical language was simplified for educational clarity. The AI model never generates real medical advice — prevention/treatment info is **predefined** and displayed only after correct diagnosis.

## 🧠 Ethical Design

We understand the sensitivity of healthcare-related AI. To ensure **responsible AI use**, we followed these principles:

* ❌ The model **never** provides medical or treatment advice.
* ✅ All medical facts (symptoms, prevention tips) come from **trusted open sources (NHS Inform)**.
* 🧩 The AI’s role is purely educational — it acts as a storytelling and reasoning simulator.
* ⚖️ Every diagnosis outcome includes a disclaimer emphasizing that this is a **learning experience, not a diagnostic tool**.

## 🚀 How to Run Locally

1️⃣ **Clone the repository:**

git clone https://github.com/<your-username>/Guess-The-Disease.git
cd Guess-The-Disease


2️⃣ **Set up your environment:**

python3 -m venv .venv
source .venv/bin/activate  # (Mac/Linux)
.venv\Scripts\activate     # (Windows)
pip install -r requirements.txt


3️⃣ **Add your Gemini API key:**

Create a `.env` file in the project root and add:
GEMINI_API_KEY=your_api_key_here


4️⃣ **Run the backend:**

python main.py

The Flask server will start at **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.
5️⃣ **Open the frontend:**

Open `index.html` in your browser (or serve it with any static web server).

## 🧩 Challenges We Faced

* Keeping AI responses realistic while avoiding oversharing symptoms too early.
* Preventing hallucinated or unsafe medical statements.
* Designing human-like dialogue through controlled prompt engineering.
* Verifying that all diseases and symptoms aligned with NHS Inform data.

## 🏆 Accomplishments

* Fully functional **AI doctor-patient simulation** built within one hackathon weekend.
* Achieved realistic patient dialogue using Gemini 2.5 API.
* Created a system that balances **education, empathy, and entertainment**.
* Demonstrated responsible AI design principles in a healthcare context.

## 📚 What We Learned

* Prompt design can make or break realism in AI conversation.
* Gamification greatly increases engagement with health literacy topics.
* Building with empathy leads to more socially impactful technology.
* Verified data sources (like NHS Inform) are essential for public trust.

## 🔮 What’s Next

We plan to turn *Guess The Disease* into a **mobile-first educational platform**.
Next steps include:

* Adding disease modules for regional health education (e.g., malaria, dengue, heatstroke).
* Developing a multiplayer or classroom mode where students compete to diagnose faster.
* Partnering with **health educators and NGOs** for verified learning content.
* Enabling voice-based interaction for accessibility in low-literacy regions.

## 🧩 Example Diseases (from NHS Inform)

| Disease   | Typical Symptoms                                    |
| --------- | --------------------------------------------------- |
| Influenza | Fever, cough, sore throat, muscle pain, fatigue     |
| Gastritis | Stomach pain, nausea, vomiting, loss of appetite    |
| Migraine  | Headache, nausea, light sensitivity, blurred vision |
| Diabetes  | Thirst, fatigue, frequent urination, weight loss    |
| Asthma    | Wheezing, chest tightness, coughing at night        |

## ❤️ Authors

**Kaius Jin**, *University of Waterloo*
@Hack The Valley X 2025

## ⚠️ Disclaimer

This project is intended **for educational and research purposes only**. It is **not a medical device** and should not be used for real diagnosis or treatment. All medical information is derived from public educational sources such as NHS Inform.

## 🌐 Demo

🎮 Try the demo locally or deploy using Render / Vercel / Replit. *(Live link coming soon)*

> *“Learn medicine. Feel empathy. One diagnosis at a time.”*
---
