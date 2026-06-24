from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    registrations = db.relationship('Registration', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    max_participants = db.Column(db.Integer, default=0)
    checkin_code = db.Column(db.String(50))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    creator = db.relationship('User', backref='created_events')
    registrations = db.relationship('Registration', backref='event', lazy='dynamic',
                                    cascade='all, delete-orphan')

    @property
    def registered_count(self):
        return self.registrations.filter_by(status='confirmed').count()

    @property
    def checked_in_count(self):
        return self.registrations.filter_by(checked_in=True).count()

    @property
    def is_full(self):
        if self.max_participants == 0:
            return False
        return self.registered_count >= self.max_participants

    def __repr__(self):
        return f'<Event {self.title}>'


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    status = db.Column(db.String(20), default='confirmed')
    registered_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    checked_in = db.Column(db.Boolean, default=False)
    checked_in_at = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint('user_id', 'event_id'),)

    def __repr__(self):
        return f'<Registration user={self.user_id} event={self.event_id}>'
