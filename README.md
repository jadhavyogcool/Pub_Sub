# 🚀 Flask + Redis Pub/Sub Demo

This project is a simple **Flask web app** that integrates with **Redis Pub/Sub** hosted on [Redis Cloud](https://redis.com/).  
It allows users to **publish messages** to a Redis channel and view all subscribed messages through a **web interface**.

---

## 📌 Features
- Publish messages to a Redis channel via **web UI** or Postman.
- Background subscriber listens for messages in Redis.
- Messages are saved in Redis (`messages_list`) and displayed on the UI.
- Option to **clear all messages**.
- Simple **auto-refresh frontend** (upgradeable to WebSockets for real-time).

---

## 🛠️ Tech Stack
- [Flask](https://flask.palletsprojects.com/) – Python web framework
- [Redis](https://redis.io/) – In-memory data store (Pub/Sub)
- HTML + JavaScript frontend (served via Flask)

---

## 📂 Project Structure
```
flask-redis-pubsub/
│── app.py              # Flask backend
│── templates/
│    └── index.html     # Web UI
│── README.md           # Documentation
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/your-username/flask-redis-pubsub.git
cd flask-redis-pubsub
```

### 2. Create Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies
```bash
pip install flask redis
```

> For **real-time WebSocket support**, also install:
```bash
pip install flask-socketio eventlet
```

### 4. Configure Redis
- Create a free Redis DB on [Redis Cloud](https://redis.com/try-free/).  
- Copy **host, port, and password**.  
- Update in `app.py`:
```python
redis_client = redis.StrictRedis(
    host="your-redis-host",
    port=your_port,
    password="your_password",
    decode_responses=True
)
```

### 5. Run App
```bash
python app.py
```
App runs at 👉 `http://127.0.0.1:5000`

---

## 🖥️ Usage

### 1. Web UI
- Open `http://127.0.0.1:5000`
- Enter a message → Click **Publish**
- Messages appear in the list (auto-refresh every 2s)
- Click **Clear All** to reset messages

### 2. Postman / cURL

**Publish a Message**
```bash
curl -X POST http://127.0.0.1:5000/publish -H "Content-Type: application/json" -d '{"message":"Hello from Postman!"}'
```

**Fetch All Messages**
```bash
curl http://127.0.0.1:5000/messages
```

**Clear Messages**
```bash
curl -X POST http://127.0.0.1:5000/clear
```

---

## 🛑 Common Issue: Duplicate Messages
When running with `debug=True`, Flask restarts your app twice → two subscriber threads.  
Fix: Run with `debug=False` or add this check before starting subscriber:

```python
import os

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=subscribe_to_channel, daemon=True).start()
    app.run(debug=True)
```

---

## 🚀 Future Improvements
- Upgrade frontend to **WebSockets (Flask-SocketIO + Redis pub/sub)** for instant updates.
- Add user authentication.
- Deploy to **Heroku/Docker** with Redis Cloud.

---

## 📜 License
MIT License – free to use and modify.
