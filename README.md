# 🎓 AI Campus Issue Triage System

An automated campus ticket classification, prioritization, and resolution management web application built with Python, Streamlit, SQLite, and a Rule-Based AI Classifier.

---

## 🚀 Key Features

1. **Student Issue Submission:**
   - Simple form for submitting issue reports with student name, location, and details.
   - Real-time automatic AI classification preview before submission.

2. **Automated AI Triage Engine:**
   - **Category Classification:** Network, Equipment, Infrastructure, General.
   - **Priority Matrix:** HIGH (red), MEDIUM (yellow), LOW (green).
   - **Department Assignment:** IT Support, Maintenance, Facilities, Campus Admin.
   - **Suggested Action:** Actionable recommendation generated per issue type.

3. **Admin Dashboard:**
   - Visual metric cards (Total Issues, High Priority, Medium Priority, Low Priority, Open Tickets).
   - Expandable ticket view with status management (OPEN → IN PROGRESS → RESOLVED).

4. **Search & Multi-Filter:**
   - Filter issues by Category, Priority, and Status.
   - Live search keyword filter across student names, locations, and descriptions.

---

## 🛠️ Tech Stack & Architecture

- **Language:** Python 3.9+
- **Frontend UI:** Streamlit (interactive web app framework)
- **Database:** SQLite3 (embedded SQL database)
- **Classifier:** Keyword & Pattern-based Rule-based AI Engine

```text
  [ Student Input ] 
         ↓
  [ Streamlit UI (app.py) ]
         ↓
  [ Rule-based AI Classifier (classifier.py) ]
         ↓
  [ SQLite Database (database.py) ]
         ↓
  [ Admin Dashboard & Metrics ]
```

---

## 📦 How to Install and Run Locally

### Step 1: Open Terminal / Command Prompt in Project Folder
```bash
cd "e:\AI Campus Issue Triage System"
```

### Step 2: Install Required Libraries
```bash
pip install -r requirements.txt
```

### Step 3: Run the Streamlit Web Application
```bash
python -m streamlit run app.py
```

The application will automatically open in your web browser at `http://localhost:8501`.

---

## 📚 Interview Preparation Guide
See the included `interview_prep.md` file for full Accenture ASE/AAE HR and Technical Q&As, architecture explanations, and tips on how to present this project.
