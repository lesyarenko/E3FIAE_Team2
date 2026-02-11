from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import os
from db import init_db, db, User, ChatBot, ChatBotTextFile, ChatBotCssFile
from utils import hash_password, verify_password, get_git_info
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, jsonify
from flask import jsonify

app = Flask(
    __name__,
    template_folder="../app/templates",
    static_folder="../app/static",
)

# Secret key for session and flashing; prefer environment variable.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'dev-secret'

# Database configuration (can be overridden by environment variable)
app.config.setdefault(
    'SQLALCHEMY_DATABASE_URI', os.environ.get('DATABASE_URL', 'sqlite:///chatbot.db')
)
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)

# Initialize the database
init_db(app, create_tables=True)

def _chat_key(chatbot_id: str) -> str:
    return f"chat_history_{chatbot_id}"

def get_chat_history(chatbot_id: str):
    return session.get(_chat_key(chatbot_id), [])

def append_chat(chatbot_id: str, role: str, text: str):
    key = _chat_key(chatbot_id)
    history = session.get(key, [])
    history.append({"role": role, "text": text})
    session[key] = history
    session.modified = True


@app.context_processor
def inject_git_info():
    """Inject git info into all templates."""
    commit_id, git_tag = get_git_info()
    return {
        'version': git_tag or (commit_id[:7] if commit_id else 'dev'),
        'git_tag': git_tag,
        'git_commit': commit_id,
    }

@app.before_request
def load_logged_in_user():
    """Load user object into `g.user` if logged in via session."""
    g.user = None
    user_id = session.get('user_id')
    if user_id and User is not None:
        try:
            g.user = User.query.get(user_id)
        except Exception:
            g.user = None

@app.route('/')
def home():
    # require authentication
    user = g.get('user')
    if not user:
        return redirect(url_for('login'))

    return render_template(
        'index.html',
        title='YourChatbot',
        username=user.username,
    )


@app.route('/cb/<string:chatbot_id>')
def cb(chatbot_id):
    """Zeigt die Chat-Seite für einen spezifischen Chatbot"""
    # require authentication
    user = g.get('user')
    if not user:
        return redirect(url_for('login'))

    chatbot = ChatBot.query.get(chatbot_id)
    if not chatbot:
        flash('Chatbot nicht gefunden.', 'error')
        return redirect(url_for('catalog'))

    # Berechtigung: Admin darf alle, sonst nur eigene
    if user.username != 'admin' and chatbot.user_id != user.id:
        flash('Keine Berechtigung für diesen Chatbot.', 'error')
        return redirect(url_for('catalog'))

    history = get_chat_history(chatbot_id)

    return render_template(
        'chat.html',
        title=chatbot.name or 'Chat',
        username=user.username,
        chatbot=chatbot,
        history=history
    )

@app.route('/cb/<string:chatbot_id>/send_json', methods=['POST'])
def cb_send_json(chatbot_id):
    user = g.get('user')
    if not user:
        return jsonify({"ok": False, "error": "not_logged_in"}), 401

    chatbot = ChatBot.query.get(chatbot_id)
    if not chatbot:
        return jsonify({"ok": False, "error": "not_found"}), 404

    if user.username != 'admin' and chatbot.user_id != user.id:
        return jsonify({"ok": False, "error": "forbidden"}), 403

    data = request.get_json(silent=True) or {}
    msg = (data.get('message') or '').strip()
    if not msg:
        return jsonify({"ok": False, "error": "empty_message"}), 400

    # save user message (session)
    append_chat(chatbot_id, "user", msg)

    # simple bot answer (demo)
    bot_answer = f"Antwort: Ich habe verstanden: {msg}"
    append_chat(chatbot_id, "bot", bot_answer)

    return jsonify({
        "ok": True,
        "user": {"role": "user", "text": msg},
        "bot": {"role": "bot", "text": bot_answer}
    })

@app.route('/cb/<string:chatbot_id>/reset', methods=['POST'])
def cb_reset(chatbot_id):
    user = g.get('user')
    if not user:
        return jsonify({"ok": False, "error": "not_logged_in"}), 401

    chatbot = ChatBot.query.get(chatbot_id)
    if not chatbot:
        return jsonify({"ok": False, "error": "not_found"}), 404

    if user.username != 'admin' and chatbot.user_id != user.id:
        return jsonify({"ok": False, "error": "forbidden"}), 403

    # delete ONLY this chatbot session history
    session.pop(_chat_key(chatbot_id), None)
    session.modified = True

    return jsonify({"ok": True})


@app.route('/catalog')
def catalog():
    # require authentication
    user = g.get('user')
    if not user:
        return redirect(url_for('login'))

    try:
        if user.username == 'admin':
            # Admin sieht ALLE Chatbots
            chatbots = ChatBot.query.order_by(ChatBot.created.desc()).all()
            is_admin = True
        else:
            # Normale User sehen NUR ihre eigenen
            chatbots = user.chatbots
            is_admin = False
    except Exception:
        chatbots = []
        is_admin = False

    return render_template(
        'catalog.html',
        title='Katalog',
        username=user.username,
        chatbots=chatbots,
        is_admin=is_admin
    )
# eigene Profile-Seite
@app.route('/profile')
def profile():
    # require authentication
    user = g.get('user')
    if not user:
        return redirect(url_for('login'))

    # Anzahl der eigenen Chatbots
    try:
        bot_count = len(user.chatbots)
    except Exception:
        bot_count = 0

    return render_template(
        'profile_user.html',    # neues Template, musst du noch anlegen
        title='Profil',
        username=user.username,
        user=user,
        bot_count=bot_count
    )


@app.route('/chatbot/new', methods=['GET', 'POST'])
def chatbot_new():
    # require authentication
    user = g.get('user')
    if not user:
        return redirect(url_for('login'))

    if request.method == 'GET':
        return render_template('chatbot_form.html', title='Neuen Chatbot erstellen', username=user.username, chatbot=None)

    # POST: create chatbot
    name = (request.form.get('name') or '').strip()
    systemprompt = request.form.get('systemprompt') or ''
    welcomemessage = request.form.get('welcomemessage') or ''

    chatbot = ChatBot(user_id=user.id, name=name, systemprompt=systemprompt, welcomemessage=welcomemessage)
    try:
        db.session.add(chatbot)
        db.session.flush()  # flush to get the chatbot ID
        
        # Handle text file uploads
        text_files = request.files.getlist('text_files')
        for text_file in text_files:
            if text_file and text_file.filename:
                content = text_file.read().decode('utf-8', errors='replace')
                text_file_obj = ChatBotTextFile(
                    chatbot_id=chatbot.id,
                    filename=text_file.filename,
                    content=content
                )
                db.session.add(text_file_obj)
        
        # Handle CSS file upload
        css_file = request.files.get('css_file')
        if css_file and css_file.filename:
            content = css_file.read().decode('utf-8', errors='replace')
            css_file_obj = ChatBotCssFile(
                chatbot_id=chatbot.id,
                filename=css_file.filename,
                content=content
            )
            db.session.add(css_file_obj)
        
        db.session.commit()
        flash('Chatbot erstellt.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Erstellen des Chatbots: {str(e)}', 'error')

    return redirect(url_for('catalog'))

@app.route('/chatbot/<string:chatbot_id>/edit', methods=['GET', 'POST'])
def chatbot_edit(chatbot_id):
    # require authentication
    user = g.get('user')
    if not user:
        return redirect(url_for('login'))

    chatbot = ChatBot.query.get(chatbot_id)
    if not chatbot or chatbot.user_id != user.id:
        flash('Chatbot nicht gefunden oder keine Berechtigung.', 'error')
        return redirect(url_for('catalog'))

    if request.method == 'GET':
        return render_template('chatbot_form.html', title='Chatbot bearbeiten', username=user.username, chatbot=chatbot)

    # POST: update chatbot
    chatbot.name = (request.form.get('name') or '').strip()
    chatbot.systemprompt = request.form.get('systemprompt') or ''
    chatbot.welcomemessage = request.form.get('welcomemessage') or ''
    
    try:
        # Handle text file uploads
        text_files = request.files.getlist('text_files')
        for text_file in text_files:
            if text_file and text_file.filename:
                content = text_file.read().decode('utf-8', errors='replace')
                text_file_obj = ChatBotTextFile(
                    chatbot_id=chatbot.id,
                    filename=text_file.filename,
                    content=content
                )
                db.session.add(text_file_obj)
        
        # Handle CSS file upload (replace existing if present)
        css_file = request.files.get('css_file')
        if css_file and css_file.filename:
            content = css_file.read().decode('utf-8', errors='replace')
            # Delete existing CSS file if present
            if chatbot.css_file:
                db.session.delete(chatbot.css_file)
                db.session.flush()  # flush to delete old css file
            # Create new CSS file
            css_file_obj = ChatBotCssFile(
                chatbot_id=chatbot.id,
                filename=css_file.filename,
                content=content
            )
            db.session.add(css_file_obj)
        
        db.session.commit()
        flash('Änderungen gespeichert.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Speichern der Änderungen: {str(e)}', 'error')

    return redirect(url_for('catalog'))

@app.route('/chatbot/<string:chatbot_id>/textfile/<string:textfile_id>/delete', methods=['POST'])
def textfile_delete(chatbot_id, textfile_id):
    # require authentication
    user = g.get('user')
    if not user:
        return redirect(url_for('login'))

    chatbot = ChatBot.query.get(chatbot_id)
    if not chatbot or chatbot.user_id != user.id:
        flash('Chatbot nicht gefunden oder keine Berechtigung.', 'error')
        return redirect(url_for('catalog'))

    text_file = ChatBotTextFile.query.get(textfile_id)
    if not text_file or text_file.chatbot_id != chatbot_id:
        flash('Text Datei nicht gefunden oder keine Berechtigung.', 'error')
        return redirect(url_for('chatbot_edit', chatbot_id=chatbot_id))

    try:
        db.session.delete(text_file)
        db.session.commit()
        flash('Text Datei gelöscht.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen der Datei: {str(e)}', 'error')

    return redirect(url_for('chatbot_edit', chatbot_id=chatbot_id))

@app.route('/chatbot/<string:chatbot_id>/delete', methods=['POST'])
def chatbot_delete(chatbot_id):
    # require authentication
    user = g.get('user')
    if not user:
        return redirect(url_for('login'))

    chatbot = ChatBot.query.get(chatbot_id)
    # Basic validation
    if not chatbot or chatbot.user_id != user.id:
        flash('Chatbot nicht gefunden oder keine Berechtigung.', 'error')
        return redirect(url_for('catalog'))

    try:
        db.session.delete(chatbot)
        db.session.commit()
        flash('Chatbot gelöscht.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler beim Löschen des Chatbots: {str(e)}', 'error')

    return redirect(url_for('catalog'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', title='Registrieren')

    # POST: handle registration
    username = (request.form.get('username') or '').strip()
    password = request.form.get('password') or ''
    repeat_password = request.form.get('repeat_password') or ''

    # Basic validation
    if not username or not password:
        flash('Benutzername und Passwort sind erforderlich.', 'error')
        return render_template('register.html', title='Registrieren', username=username)

    # Check if passwords match
    if password != repeat_password:
        flash('Passwörter stimmen nicht überein.', 'error')
        return render_template('register.html', title='Registrieren', username=username)

    # Check for existing user
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash('Benutzername existiert bereits. Bitte wähle einen anderen.', 'error')
        return render_template('register.html', title='Registrieren', username='')

    # Hash the password (generates a new salt)
    password_hash, salt = hash_password(password)

    # Create and save the user
    new_user = User(username=username, password=password_hash, salt=salt)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Fehler bei der Registrierung: {str(e)}', 'error')
        return render_template('register.html', title='Registrieren', username=username)

    # log the user in immediately after registering
    session['user_id'] = new_user.id
    session.permanent = True
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', title='Login')

    # POST: handle login
    username = (request.form.get('username') or '').strip()
    password = request.form.get('password') or ''

    # Basic validation
    if not username or not password:
        flash('Benutzername und Passwort sind erforderlich.', 'error')
        return render_template('login.html', title='Login', username=username)

    # Check if user exists and password is correct
    user = User.query.filter_by(username=username).first()
    if not user or not verify_password(user.password, user.salt or '', password):
        flash('Ungültiger Benutzername oder Passwort.', 'error')
        return render_template('login.html', title='Login')

    session['user_id'] = user.id
    session.permanent = True
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5050)
