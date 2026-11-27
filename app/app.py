import json, os, sqlite3, uuid
from datetime import datetime, timezone
from flask import Flask, render_template, request, jsonify
from chatbot import respond, CAFE

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, 'data', 'app.sqlite3')
app = Flask(__name__)
app.json.ensure_ascii = False

def connect():
    db = sqlite3.connect(DB, timeout=10)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with connect() as db:
        db.executescript('''CREATE TABLE IF NOT EXISTS conversations (id TEXT PRIMARY KEY, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY AUTOINCREMENT, conversation_id TEXT, message TEXT NOT NULL, rating TEXT NOT NULL, created_at TEXT NOT NULL);''')

def now(): return datetime.now(timezone.utc).isoformat()

@app.get('/')
def home(): return render_template('index.html')

@app.get('/api/info')
def info(): return jsonify(CAFE)

@app.post('/api/chat')
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get('message', '')
    if not isinstance(message, str) or not message.strip(): return jsonify(error='Please enter a question.'), 400
    if len(message) > 1500: return jsonify(error='Question must be 1500 characters or fewer.'), 400
    cid = data.get('conversation_id')
    if not isinstance(cid, str) or len(cid) > 100: cid = None
    reply = respond(message)
    with connect() as db:
        if not cid or not db.execute('SELECT id FROM conversations WHERE id=?', (cid,)).fetchone():
            cid = str(uuid.uuid4())
            db.execute('INSERT INTO conversations VALUES (?,?)', (cid, now()))
        db.executemany('INSERT INTO messages (conversation_id,role,content,created_at) VALUES (?,?,?,?)', [(cid,'user',message.strip(),now()),(cid,'assistant',reply,now())])
    return jsonify(reply=reply, conversation_id=cid)

@app.get('/api/history/<cid>')
def history(cid):
    with connect() as db:
        rows = db.execute('SELECT role,content,created_at FROM messages WHERE conversation_id=? ORDER BY id LIMIT 200', (cid,)).fetchall()
    return jsonify(messages=[dict(x) for x in rows])

@app.post('/api/feedback')
def feedback():
    data=request.get_json(silent=True) or {}
    rating=data.get('rating')
    if rating not in ('helpful','not_helpful'): return jsonify(error='Invalid rating'),400
    message=str(data.get('message',''))[:1500]
    with connect() as db:
        db.execute('INSERT INTO feedback (conversation_id,message,rating,created_at) VALUES (?,?,?,?)', (str(data.get('conversation_id',''))[:100],message,rating,now()))
    return jsonify(ok=True)

@app.get('/api/health')
def health(): return jsonify(status='ok', service='Campus Brew FAQ Assistant')

if __name__ == '__main__':
    init_db()
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5000)), debug=False)
else:
    init_db()
