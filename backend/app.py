from flask import Flask, request, jsonify
from flask_cors import CORS
import random
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
import sqlite3
import os
app = Flask(__name__)

CORS(app)  # THIS ENABLES CORS FOR ALL ROUTES

# Basic home route test
@app.route('/')
def home():
    return "MoodBoost AI Backend is Running!"

# Simple mental health chatbot API (placeholder)
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message', '')

    # For now, dummy response
    reply = "I'm here to listen! You said: " + user_message

    return jsonify({'reply': reply})


@app.route('/career', methods=['POST'])
def career_recommend():
    data = request.get_json()
    interests = data.get('interests', '')  # Example: "AI, coding, design"
    # Simple rule-based example, recruiter-impress fallback (expandable)
    if 'ai' in interests.lower():
        career = "AI Engineer"
    elif 'design' in interests.lower():
        career = "UI/UX Designer"
    elif 'cloud' in interests.lower():
        career = "Cloud Solutions Architect"
    elif 'security' in interests.lower():
        career = "Cybersecurity Analyst"
    else:
        career = "Software Developer"
    return jsonify({'career': career})

@app.route('/music', methods=['POST'])
def music_recommend():
    data = request.get_json()
    mood = data.get('mood', '').lower()
    # Simple mood to music mapping
    mood_map = {
        "happy":  ["Happy - Pharrell Williams", "On Top of the World - Imagine Dragons"],
        "sad":    ["Someone Like You - Adele", "Let Her Go - Passenger"],
        "angry":  ["Stronger - Kanye West", "Castle of Glass - Linkin Park"],
        "relaxed":["Weightless - Marconi Union", "Sunflower - Post Malone"],
        "motivated":["Hall of Fame - The Script", "Believer - Imagine Dragons"]
    }
    playlist = mood_map.get(mood, ["Adventure of a Lifetime - Coldplay", "Let Me Down Slowly - Alec Benjamin"])
    return jsonify({'playlist': playlist})

quotes = [
    "Believe you can and you're halfway there.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Sometimes later becomes never. Do it now.",
    "Great things never come from comfort zones.",
    "Dream it. Wish it. Do it.",
    "Success doesn't just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it."
]

@app.route('/motivational', methods=['GET'])
def motivational_quote():
    quote = random.choice(quotes)
    return jsonify({"quote": quote})


app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'  # Change this!
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

# Database setup
DATABASE = 'moodboost.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  message TEXT,
                  reply TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

init_db()

# Home route
@app.route('/')
def home():
    return "MoodBoost AI Backend is Running!"

# Signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    
    try:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Signup successful!'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user and bcrypt.check_password_hash(user[1], password):
        session['user_id'] = user[0]
        session['username'] = username
        return jsonify({'message': 'Login successful!', 'username': username}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

# Chatbot (save to history if logged in)
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    user_message = data.get('message', '')
    reply = "I'm here to listen! You said: " + user_message
    
    if 'user_id' in session:
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO chat_history (user_id, message, reply) VALUES (?, ?, ?)",
                  (session['user_id'], user_message, reply))
        conn.commit()
        conn.close()
    
    return jsonify({'reply': reply})

# Career recommendation
@app.route('/career', methods=['POST'])
def career_recommend():
    data = request.get_json()
    interests = data.get('interests', '').lower()
    
    career_map = {
        "ai": "AI Engineer", "ml": "Machine Learning Engineer",
        "design": "UI/UX Designer", "cloud": "Cloud Solutions Architect",
        "security": "Cybersecurity Analyst", "data": "Data Scientist",
        "blockchain": "Blockchain Developer", "mobile": "Mobile App Developer",
        "devops": "DevOps Engineer", "game": "Game Developer"
    }
    
    career = career_map.get(interests, "Software Developer")
    return jsonify({'career': career})

# Music recommender
@app.route('/music', methods=['POST'])
def music_recommend():
    data = request.get_json()
    mood = data.get('mood', '').lower()
    
    mood_map = {
        "happy": ["Happy - Pharrell Williams", "On Top of the World - Imagine Dragons"],
        "sad": ["Someone Like You - Adele", "Let Her Go - Passenger"],
        "angry": ["Stronger - Kanye West", "Castle of Glass - Linkin Park"],
        "relaxed": ["Weightless - Marconi Union", "Sunflower - Post Malone"],
        "motivated": ["Hall of Fame - The Script", "Believer - Imagine Dragons"]
    }
    
    playlist = mood_map.get(mood, ["Adventure of a Lifetime - Coldplay"])
    return jsonify({'playlist': playlist})

# Motivational quotes

@app.route('/history', methods=['GET'])
def get_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""SELECT message, reply, timestamp FROM chat_history 
                 WHERE user_id = ? ORDER BY timestamp DESC LIMIT 10""", 
              (session['user_id'],))
    history = c.fetchall()
    conn.close()
    
    history_list = [{'message': h[0], 'reply': h[1], 'timestamp': h[2]} for h in history]
    return jsonify({'history': history_list})

# Check if user is logged in
@app.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({'logged_in': True, 'username': session.get('username')})
    return jsonify({'logged_in': False})
@app.route('/life-support', methods=['POST'])
def life_support():
    data = request.get_json()
    situation = data.get('situation', '').lower()
    
    support_map = {
        "love_failure": {
            "message": "Love failure hurts, but it's not the end. You deserve someone who sees your worth. Time heals everything.",
            "steps": [
                "Allow yourself to feel the pain, don't suppress it",
                "Focus on self-care and personal growth",
                "Reconnect with friends and hobbies you love",
                "Remember: the right person will come at the right time"
            ]
        },
        "job_rejection": {
            "message": "Rejection is redirection. Every 'no' brings you closer to the right 'yes'. Keep going!",
            "steps": [
                "Review and improve your resume/portfolio",
                "Practice mock interviews",
                "Network with professionals in your field",
                "Stay consistent - success takes time"
            ]
        },
        "exam_failure": {
            "message": "Failure is not final. It's feedback. Learn from it and come back stronger!",
            "steps": [
                "Analyze what went wrong without self-blame",
                "Create a realistic study schedule",
                "Seek help from teachers or mentors",
                "Remember: one exam doesn't define your future"
            ]
        },
        "family_issues": {
            "message": "Family conflicts are tough, but communication and patience can heal wounds. You're not alone.",
            "steps": [
                "Try calm, open conversations when emotions settle",
                "Seek to understand before being understood",
                "Set healthy boundaries if needed",
                "Consider family counseling if helpful"
            ]
        },
        "financial_stress": {
            "message": "Money problems are temporary. With planning and effort, you can overcome this challenge.",
            "steps": [
                "List your expenses and create a budget",
                "Look for side income opportunities",
                "Cut non-essential expenses temporarily",
                "Seek financial advice if needed"
            ]
        },
        "loneliness": {
            "message": "Feeling alone doesn't mean you are alone. Reach out, connect, and remember you matter.",
            "steps": [
                "Join communities or groups with shared interests",
                "Volunteer or help others - it builds connection",
                "Reach out to old friends or family",
                "Consider therapy or support groups"
            ]
        }
    }
    
    response = support_map.get(situation, {
        "message": "Whatever you're going through, remember: this too shall pass. You are stronger than you think.",
        "steps": [
            "Take one day at a time",
            "Talk to someone you trust",
            "Focus on small wins daily",
            "Believe in yourself - you've got this!"
        ]
    })
    
    return jsonify(response)
quotes_with_video = [
    {
        "quote": "Push yourself, because no one else is going to do it for you.",
        "youtube": "https://www.youtube.com/watch?v=mgmVOuLgFB0"  # Unstoppable - Motivational Speech
    },
    {
        "quote": "Great things never come from comfort zones.",
        "youtube": "https://www.youtube.com/watch?v=sTANio_2E0Q"  # Elon Musk Motivation
    },
    {
        "quote": "Dream it. Wish it. Do it.",
        "youtube": "https://www.youtube.com/watch?v=r5vZ3l6cE0g"  # Study Motivation
    },
    {
        "quote": "Believe you can and you're halfway there.",
        "youtube": "https://www.youtube.com/watch?v=wnHW6o8WMas"  # You Are Limitless
    }
]

@app.route('/motivational', methods=['GET'])
def motivational_quote():
    item = random.choice(quotes_with_video)
    return jsonify({"quote": item["quote"], "youtube": item["youtube"]})


if __name__ == '__main__':
    app.run(debug=True)
