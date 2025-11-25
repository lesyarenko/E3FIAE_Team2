from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from utils import hash_password, generate_id6, generate_id8

# Flask-SQLAlchemy instance (call `init_db(app)` in your application factory)
db = SQLAlchemy()


def init_db(app, create_tables: bool = False):
    db.init_app(app)
    if create_tables:
        with app.app_context():
            # db.drop_all()
            db.create_all()

    # Ensure default admin exists (username: 'admin', password: 'hss')
    try:
        with app.app_context():
            if not User.query.filter_by(username='admin').first():
                pwd_hash, pwd_salt = hash_password('hss')
                admin = User(username='admin', password=pwd_hash, salt=pwd_salt)
                db.session.add(admin)
                db.session.commit()
    except Exception:
        # If creation fails, skip silently (don't crash startup)
        pass


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(6), primary_key=True, default=generate_id6, unique=True)
    username = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255), nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    # Relationship: one user -> many chatbots
    chatbots = db.relationship('ChatBot', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"


class ChatBot(db.Model):
    __tablename__ = 'chatbots'

    id = db.Column(db.String(8), primary_key=True, default=generate_id8, unique=True)
    user_id = db.Column(db.String(6), db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(255), nullable=True)
    systemprompt = db.Column(db.Text, nullable=True)
    welcomemessage = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    user = db.relationship('User', back_populates='chatbots')

    def __repr__(self):
        return f"<ChatBot id={self.id} name={self.name} username={self.username}>"


