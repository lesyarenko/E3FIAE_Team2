# Chatbot-Projekt – E3FIAE_Team2

## Projektstruktur
```plaintext
├─ app/                     # Haupt-Anwendung
│  ├─ static/
│  │  ├─ style.css          # Design der Webseite
│  │  ├─ script.js          # Optional: Chatfunktionen
│  │  ├─ logo.svg           # Logos & Hintergründe
│  │  └─ bg.svg
│  └─ templates/
│     ├─ base.html          # Template was als Basis für alle anderen Templates verwendet wird. Variablen: title, username. Platzhalter: content
│     ├─ chatbot_form.html  # Template zum erstellen und bearbeiten von Chatbots. Variablen: chatbot
│     ├─ index.html         # Template für Chat. Variablen: -
│     ├─ login.html         # Template für Login mit Benutzername und Passwort. Variablen: username
│     ├─ profile.html       # Template für Benutzerprofil mit Liste der vom Benutzer erstellten Chatbots. Variablen: chatbots
│     └─ register.html      # Template für Registrierung mit Erstellung Benutzername und Passwort. Variablen: username
├─ venv/                    # Virtuelle Umgebung (nicht in GitHub hochladen!)
├─ scripts/
|  ├─ db.py                 # Datenbank Modelle für Benutzer und Chatbots
|  ├─ main.py               # Startpunkt der App → `python main.py`
|  └─ utils.py              # Utilities wie passwort hashen, ids generieren.
├─ requirements.txt         # Notwendige Python-Bibliotheken (Flask usw.)
└─ readme.md                # Dokumentation
```

## Anleitung zur Nutzung

### 0. Benötigte Werkzeuge

Zur Nutzung werden `git` und `Python` benötigt.

Windows
```bash
winget install --id Git.Git -e --source winget
winget install --id Python.Python.3.11 -e --source winget
```
Linux
```bash
apt install git-all
apt install python3.13-venv
```
macOS
```bash
brew install git
brew install python
```

### 1. Repository klonen

```bash
git clone https://github.com/NuraiymSadyrbaeva/E3FIAE_Team2.git
```

### 2. Virtuelle Umgebung anlegen und aktivieren

#### Virtuelle Umgebung anlegen
```bash
cd project_chatbot
python -m venv venv
```
If python is already installed it might be called `py` or `python3` instead of `python`.
#### Virtuelle Umgebung aktivieren
Windows
```bash
venv\Scripts\activate
```
If this script can not be executed in PowerShell on Windows then change the execution policy to allow remotly signed code. By executing the following command in an elevated (administrator) PowerShell:
```bash
Set-ExecutionPolicy RemoteSigned
```
Linux/macOS
```bash
source venv/bin/activate
```
### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```
### 4. Projekt starten
```bash
python scripts/main.py   # Startet Flask auf http://localhost:5050
```
### 5. Webseite öffnen
Browser öffnen → [http://localhost:5050](http://localhost:5050)
