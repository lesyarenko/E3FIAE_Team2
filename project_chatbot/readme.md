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
│     ├─ catalog.html       # Katalog für Chatbots
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
Wenn `python` bereits installiert ist, kann es sein, dass der Befehl statt python auch `py` oder `python3` lautet.
#### Virtuelle Umgebung aktivieren
Windows
```bash
venv\Scripts\activate
```
Falls sich dieses Skript in PowerShell unter Windows nicht ausführen lässt, musst du die Ausführungsrichtlinie anpassen, damit lokal erstellte und signierte Skripte erlaubt sind.
Öffne dazu PowerShell als Administrator und gib folgenden Befehl ein:
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
### 4. Umgebungsvariablen konfigurieren
Für die OpenAI-Integration wird ein API-Schlüssel benötigt. Setze die Umgebungsvariable `OPEN_AI_API_SECRET`:

#### Temporär (nur für aktuelle Sitzung)
Windows
```bash
set OPEN_AI_API_SECRET=your_api_key_here
```
Linux/macOS
```bash
export OPEN_AI_API_SECRET=your_api_key_here
```

#### Persistent (über Neustarts hinweg)
**Windows:**
```bash
setx OPEN_AI_API_SECRET "your_api_key_here"
```
Nach dem Ausführen von `setx` musst du eine neue PowerShell/CMD-Sitzung öffnen, damit die Variable verfügbar ist.

**Linux:**
Füge folgende Zeile in `~/.bashrc` oder `~/.bash_profile` ein:
```bash
export OPEN_AI_API_SECRET="your_api_key_here"
```
Danach ausführen:
```bash
source ~/.bashrc
```

**macOS:**
Füge folgende Zeile in `~/.zshrc` (oder `~/.bash_profile` für ältere Versionen) ein:
```bash
export OPEN_AI_API_SECRET="your_api_key_here"
```
Danach ausführen:
```bash
source ~/.zshrc
```

Ersetze `your_api_key_here` mit deinem tatsächlichen OpenAI API-Schlüssel von [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys).

### 5. Projekt starten
```bash
python scripts/main.py # Startet Flask auf http://localhost:5050
```
### 6. Webseite öffnen
Browser öffnen → [http://localhost:5050](http://localhost:5050)
