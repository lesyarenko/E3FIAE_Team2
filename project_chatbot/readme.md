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
│     └─ index.html         # Templates
├─ venv/                    # Virtuelle Umgebung (nicht in GitHub hochladen!)
├─ scripts/
|  └─ main.py               # Startpunkt der App → `python main.py`
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
#### Virtuelle Umgebung aktivieren
Windows
```bash
venv\Scripts\activate
```
Linux/macOS
```bash
source venv/bin/activate
```
### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```
oder
```bash
pip install flask
```
### 4. Projekt starten
```bash
python scripts/main.py   # Startet Flask auf http://localhost:5050
```
### 5. Webseite öffnen
Browser öffnen → [http://localhost:5050](http://localhost:5050)
