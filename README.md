# CAMPUS BREW — Full Café Chatbot Application

**CS-2 | The Café Chatbot: Build It, Then Break It**

A full-screen responsive web application with a working FAQ chatbot, menu explorer, café hours, location/contact view, persistent chat history, and feedback collection. No API key is required.

## RUN ON WINDOWS (EASIEST)

1. Install Python 3.10+ from https://www.python.org/downloads/ (check **Add Python to PATH**).
2. Extract the ZIP file completely.
3. Double-click **run_windows.bat**. The first run installs dependencies; internet is required for that step.
4. Open **http://127.0.0.1:5000** if your browser did not open automatically.
5. Leave the black terminal window running. Close it to stop the app.

## MANUAL RUN (WINDOWS CMD)

```bat
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app\app.py
```

## MAC / LINUX

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python app/app.py
```

## TESTS

```bat
.venv\Scripts\python.exe -m pytest -q
```

## FEATURES

- Attractive, responsive app UI with four working views: Assistant, Menu, Hours & Location, Project About.
- Chatbot answers hours, menu prices, item allergens, dietary labels, and location using a local JSON knowledge base.
- SQLite persistence for conversation messages and feedback; browser remembers the current conversation.
- Safe allergy handling: no promises of allergen-free food; staff referral for severe allergies.
- Unknown questions produce a grounded refusal rather than invented facts.
- Input validation and automated API/logic tests.
- Structured failure log with 12 adversarial test cases and diagnoses in `docs/failure_log.md`.

## PROJECT FILES

- `app/app.py`: Flask server and SQLite REST API
- `app/chatbot.py`: deterministic FAQ engine
- `app/templates/index.html`: complete interface
- `app/static/style.css`: responsive visual design
- `app/static/app.js`: working navigation, chat, persistence, feedback and menu filters
- `data/cafe_data.json`: editable café information
- `docs/PROJECT_REPORT.md`: written report
- `docs/failure_log.md`: 12-question failure analysis
- `tests/test_app.py`: automated tests


