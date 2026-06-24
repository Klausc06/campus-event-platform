from flask import render_template
from flask_login import login_required, current_user

from app.admin import admin_bp
from app.decorators import admin_required
from app.extensions import db
from app.models import User, Event, Registration


@admin_bp.before_request
@login_required
@admin_required
def require_admin():
    pass


@admin_bp.route('/')
def dashboard():
    total_users = User.query.count()
    total_events = Event.query.count()
    total_registrations = Registration.query.filter_by(status='confirmed').count()
    total_checkins = Registration.query.filter_by(status='confirmed', checked_in=True).count()

    events = Event.query.order_by(Event.created_at.desc()).all()
    event_stats = []
    for event in events:
        registered = event.registered_count
        checked = event.checked_in_count
        rate = round(checked / registered * 100, 1) if registered > 0 else 0
        event_stats.append({
            'event': event,
            'registered': registered,
            'checked_in': checked,
            'rate': rate,
        })

    return render_template(
        'admin/dashboard.html',
        total_users=total_users,
        total_events=total_events,
        total_registrations=total_registrations,
        total_checkins=total_checkins,
        event_stats=event_stats,
    )
