
# 🛍️ AI Shopping Chat Agent

An **AI‑powered conversational shopping assistant** that allows users to search, compare, and get product recommendations using natural language.

---

## 🚀 Features
- Conversational product search
- AI-based recommendations
- Backend + Frontend architecture
- Dataset-driven responses
- Docker support

---

## 📁 Project Structure
```
AI_shopping_chat_agent/
├── backend/
├── frontend/
├── dataset/
├── dockerfile
├── run_app.sh
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### Clone Repo
```bash
git clone https://github.com/Nirzar-shah-11/AI_shopping_chat_agent.git
cd AI_shopping_chat_agent
```

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

---

## 🧠 Example Queries
- "Compare iPhone vs Samsung"

---

## 🐳 Docker
```bash
docker build -t ai_shopping_agent .
docker run -p 5000:5000 ai_shopping_agent
```