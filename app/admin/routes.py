import os

from flask import current_app, render_template
from flask_login import login_required, current_user
from sqlalchemy import func

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

    stats = db.session.query(
        Event,
        func.count(Registration.id).filter(Registration.status == 'confirmed').label('registered'),
        func.count(Registration.id).filter(Registration.status == 'confirmed', Registration.checked_in == True).label('checked_in'),
    ).outerjoin(Registration).group_by(Event.id).order_by(Event.created_at.desc()).all()

    event_stats = []
    for event, registered, checked_in in stats:
        rate = round(checked_in / registered * 100, 1) if registered > 0 else 0
        event_stats.append({'event': event, 'registered': registered, 'checked_in': checked_in, 'rate': rate})

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
    log_file = current_app.config['LOG_FILE']

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
