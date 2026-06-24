import os

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


@admin_bp.route("/logs")
def logs():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
    log_file = os.path.join(log_dir, "app.log")

    log_content = ""
    error_lines = ""
    total_lines = 0

    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()
            total_lines = len(lines)
            log_content = "".join(lines[-200:])
            error_lines = "".join(
                l for l in lines if "ERROR" in l or "CRITICAL" in l or "Traceback" in l
            )[-3000:]

    return render_template(
        "admin/logs.html",
        log_content=log_content,
        error_lines=error_lines,
        total_lines=total_lines,
    )
