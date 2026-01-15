# ChatGPT-like Web Chat Application

A full-stack Python project with a modern ChatGPT-like web interface, featuring Flask backend and a beautiful HTML/CSS/JavaScript frontend.

## Project Structure

```
.
├── web_server.py              # Flask backend server
├── templates/
│   └── index.html             # Main chat UI
├── static/
│   ├── style.css              # Styling
│   └── script.js              # Client-side logic
└── requirements.txt           # Python dependencies
```

## Quick Start

### 1. Create Virtual Environment

```bash
python -m venv venv
```

Then activate it:

```bash
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
python ./server-side/web_server.py
```

### 4. Open in Browser

Navigate to:
```
http://localhost:5000
```

That's it! The chat interface will load and you can start chatting.

