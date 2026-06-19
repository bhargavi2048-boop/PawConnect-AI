# 🐾 PawConnect AI
### *Connecting Citizens, Volunteers & NGOs to Protect Stray Dogs*

> **1M1B Initiative Project** · Built for SDG Impact · Developed by **Bhargavi N**

---

Demo Link: "https://pawconnect-ai-powered-dpe8.onrender.com"
## 📌 Table of Contents

- [About the Project](#-about-the-project)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Key Features](#-key-features)
- [SDG Alignment](#-sdg-alignment)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Pages & Routes](#-pages--routes)
- [AI Chatbot](#-ai-chatbot--pawbot)
- [Screenshots](#-screenshots)
- [Expected Impact](#-expected-social-impact)
- [Responsible AI](#-responsible-ai)
- [Developer](#-developer)

---

## 🌟 About the Project

**PawConnect AI** is a sustainability-focused web platform that leverages technology to protect India's stray dog population. It bridges the gap between compassionate citizens and the animals that desperately need their help — by creating a unified digital ecosystem for reporting, tracking, volunteering, and AI-guided rescue coordination.

India has an estimated **62 million stray dogs** — the highest in the world. Yet there is no centralized, accessible platform for citizens to report cases and get help. PawConnect AI changes that.

---

## 🚨 Problem Statement

| Problem | Impact |
|---|---|
| No easy reporting channel for citizens | Injured/sick dogs go unreported for days |
| Delayed response from authorities | Preventable suffering and deaths |
| Disconnected volunteers & NGOs | Wasted capacity and duplication of effort |
| No data or transparency | No accountability or improvement over time |
| Lack of public awareness | Citizens don't know how or where to help |

---

## 💡 Solution

PawConnect AI provides a **4-pillar solution**:

1. **📝 Instant Reporting** — Citizens submit complaints in under 2 minutes with photo upload and GPS location, receiving a unique Complaint ID (e.g. `PC001`) for tracking.

2. **🤝 Volunteer Network** — Citizens register as Food Providers, Rescue Volunteers, or Medical Helpers and are matched with nearby complaints.

3. **🤖 AI Chatbot (PawBot)** — A 24/7 intelligent assistant guiding users on feeding, first aid, emergency contacts, and how to report.

4. **📊 Admin Analytics Dashboard** — Charts, maps, and complaint management tools give NGOs and coordinators full visibility and control.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🚨 Complaint Reporting | Submit stray dog cases with photo, type, and location |
| 🔍 Real-Time Tracking | Track complaint status from Submitted → In Progress → Rescued → Closed |
| 🤝 Volunteer Registration | Register as food provider, rescue volunteer, or medical helper |
| 🤖 PawBot AI Chatbot | Instant guidance on feeding, first aid, and emergency contacts |
| 📊 Analytics Dashboard | Charts for complaints by category, resolved vs pending, monthly trends |
| 🗺️ Interactive Map | Live map of complaint locations using OpenStreetMap + Leaflet.js |
| 📋 Admin Panel | Full complaint management with status update controls |
| 📱 Responsive Design | Mobile-friendly across all devices |

---

## 🌍 SDG Alignment

PawConnect AI is aligned with **5 UN Sustainable Development Goals**:

| SDG | Goal | How PawConnect Contributes |
|---|---|---|
| 🏥 **SDG 3** | Good Health & Well-Being | Reduces zoonotic disease risks (rabies) by enabling faster treatment of sick/injured strays |
| ⚙️ **SDG 9** | Industry, Innovation & Infrastructure | Builds digital infrastructure for animal welfare where none existed — AI chatbot, real-time tracking, data analytics |
| 🏙️ **SDG 11** | Sustainable Cities & Communities | Makes urban environments safer and more compassionate through humane stray management |
| 🌿 **SDG 15** | Life on Land | Directly protects terrestrial animal life through rescue coordination and ABC program support |
| 🤝 **SDG 17** | Partnerships for the Goals | Connects citizens, volunteers, NGOs, and government bodies on one collaborative platform |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask |
| **Frontend** | HTML5, CSS3, Bootstrap 5.3, Jinja2 |
| **Database** | CSV-based flat file storage (no setup required) |
| **Charts** | Chart.js 4.4 |
| **Maps** | Leaflet.js + OpenStreetMap |
| **Icons** | Font Awesome 6.5 |
| **Fonts** | Google Fonts — Nunito, Playfair Display |
| **AI Chatbot** | Rule-based NLP (extensible to OpenAI / IBM Granite) |

---

## 📁 Project Structure

```
pawconnect_final/
│
├── app.py                    # Flask backend — routes, CSV logic, chatbot engine
├── requirements.txt          # Python dependencies
│
├── data/
│   ├── complaints.csv        # Auto-created — stores all complaint records
│   └── volunteers.csv        # Auto-created — stores all volunteer registrations
│
├── static/
│   ├── css/
│   │   └── style.css         # All custom styling & theme
│   └── uploads/              # Auto-created — complaint photo uploads
│
└── templates/
    ├── base.html             # Shared layout (navbar, footer, flash messages)
    ├── home.html             # Landing page with live stats
    ├── report.html           # Dog complaint submission form
    ├── track.html            # Complaint tracking by ID
    ├── volunteer.html        # Volunteer registration + directory
    ├── chatbot.html          # PawBot AI chat interface
    ├── admin.html            # Admin dashboard (charts, map, tables)
    ├── about.html            # Project info, SDG alignment, developer
    └── contact.html          # Contact cards + message form
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python **3.8 or higher**
- pip (comes with Python)

### Step 1 — Clone / Extract the project
```bash
# If using git:
git clone https://github.com/bhargavi2048-boop/pawconnect-ai.git
cd pawconnect-ai

# Or simply extract the ZIP and open the folder in terminal
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

> If `pip` doesn't work, try `pip3`. On Windows, use `py -m pip install -r requirements.txt`.

### Step 3 — Run the application
```bash
python app.py
```

> On Mac/Linux: `python3 app.py`

### Step 4 — Open in browser
```
http://localhost:5000
```

That's it! No database setup, no environment variables, no configuration needed.

---

### 🔧 Changing the Port

If port 5000 is already in use, open `app.py` and change the last line:

```python
app.run(debug=True, port=5001)  # Use any available port
```

---

## 🌐 Pages & Routes

| Route | Page | Description |
|---|---|---|
| `/` | Home | Landing page with live platform statistics |
| `/report` | Report | Submit a stray dog complaint with photo |
| `/track` | Track | Track complaint status by Complaint ID |
| `/volunteer` | Volunteer | Register as a volunteer; view volunteer directory |
| `/chatbot` | AI Chat | Chat with PawBot for animal welfare guidance |
| `/admin` | Admin | Dashboard with charts, map, and complaint management |
| `/about` | About | Project overview, SDGs, developer info |
| `/contact` | Contact | Developer contact cards + message form |
| `/api/chat` | API | POST endpoint for chatbot (JSON) |
| `/admin/update_status` | API | POST endpoint to update complaint status |

---

## 🤖 AI Chatbot — PawBot

PawBot is a rule-based intelligent assistant that responds to natural language queries about animal welfare.

**Supported Topics:**

| Topic | Example Query |
|---|---|
| 🍖 Feeding | *"What should I feed a stray dog?"* |
| 🚨 Injured Dog | *"There's a dog bleeding on the street"* |
| 🏥 Sick Dog | *"The dog looks sick and is not eating"* |
| 📞 Contacts | *"Which NGO should I call for help?"* |
| 💪 Volunteering | *"How can I help stray dogs?"* |
| 📝 Reporting | *"How do I report a stray dog case?"* |

### Upgrading to a Real AI Model

Replace `get_chatbot_response()` in `app.py` with an API call:

```python
import openai
openai.api_key = "YOUR_API_KEY"

def get_chatbot_response(user_message):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are PawBot, a compassionate animal welfare assistant for PawConnect AI. Help users with stray dog care, reporting, and rescue."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content
```

---

## 📈 Expected Social Impact

| Metric | Target |
|---|---|
| 🐾 Animals rescued annually | 500+ |
| 🏙️ Indian cities covered | 10+ |
| 🤝 Volunteer network | 1,000+ registered volunteers |
| 🏥 NGO partnerships | 15+ organizations |
| ⏱️ Average response time | Under 2 hours |
| 🦠 Rabies risk reduction | Measurable reduction via ABC program support |

---

## 🛡️ Responsible AI

- 📵 Mobile numbers are **masked** in all public-facing views
- 🩺 PawBot **does not provide medical diagnoses** — always recommends professional veterinary care
- ✅ All AI recommendations encourage **human verification**
- 🔒 No personal data is sold, shared, or used for advertising
- 🌐 Platform is open and free for all citizens to use

---

## 👩‍💻 Developer

<table>
  <tr>
    <td><strong>Name</strong></td>
    <td>Bhargavi N</td>
  </tr>
  <tr>
    <td><strong>Email</strong></td>
    <td><a href="mailto:bhargavi2048@gmail.com">bhargavi2048@gmail.com</a></td>
  </tr>
  <tr>
    <td><strong>LinkedIn</strong></td>
    <td><a href="https://www.linkedin.com/in/bhargavi-nagaraj-967811381">linkedin.com/in/bhargavi-nagaraj-967811381</a></td>
  </tr>
  <tr>
    <td><strong>GitHub</strong></td>
    <td><a href="https://github.com/bhargavi2048-boop">github.com/bhargavi2048-boop</a></td>
  </tr>
  <tr>
    <td><strong>Initiative</strong></td>
    <td>1 Million for 1 Billion (1M1B) · SDG Impact Platform</td>
  </tr>
</table>

---

## 📄 License

This project is developed for the **1M1B Initiative** as a social impact submission. Free to use for educational, welfare, and non-commercial purposes.

---

<div align="center">

Made with ❤️ for every stray dog that deserves a chance

**🐾 PawConnect AI · © 2026 · Bhargavi N**

*Connecting Hearts. Saving Lives.*

</div>
