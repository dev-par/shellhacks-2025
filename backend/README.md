## Backend Run

```
npm install express body-parser cors dotenv
npm install passport passport-auth0 express-session
npm install @veramo/core @veramo/cli @veramo/did-resolver @veramo/credential-w3c
```

## Agent Testing

```bash

# Create
python -m venv .venv
# Activate (each new terminal)
# macOS/Linux:
source .venv/bin/activate

# Windows CMD:
.venv\Scripts\activate.bat

# Windows PowerShell:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt

python main.py
```
