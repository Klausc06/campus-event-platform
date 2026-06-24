import csv
import io
import os
from urllib.parse import quote

from flask import current_app, render_template, Response
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


@admin_bp.route('/export/<int:event_id>')
def export_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        return 'Event not found', 404

    registrations = Registration.query.filter_by(
        event_id=event_id, status='confirmed'
    ).all()

    output = io.StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    writer.writerow(['username', 'email', 'registered_at', 'checked_in', 'checked_in_at'])

    for r in registrations:
        writer.writerow([
            r.user.username,
            r.user.email,
            r.registered_at.strftime('%Y-%m-%d %H:%M:%S') if r.registered_at else '',
            'Yes' if r.checked_in else 'No',
            r.checked_in_at.strftime('%Y-%m-%d %H:%M:%S') if r.checked_in_at else '',
        ])

    output.seek(0)
    filename = f'{event.title}_registrations.csv'
    encoded = quote(filename)
    return Response(
        output.getvalue(),
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': f"attachment; filename=\"{filename}\"; filename*=UTF-8''{encoded}"},
    )


@admin_bp.route('/export/all')
def export_all():
    regs = db.session.query(Registration, Event.title).join(Event).filter(
        Registration.status == 'confirmed'
    ).all()

    output = io.StringIO()
    output.write('\ufeff')
    writer = csv.writer(output)
    writer.writerow(['event_title', 'username', 'email', 'registered_at', 'checked_in', 'checked_in_at'])

    for r, title in regs:
        writer.writerow([
            title,
            r.user.username,
            r.user.email,
            r.registered_at.strftime('%Y-%m-%d %H:%M:%S') if r.registered_at else '',
            'Yes' if r.checked_in else 'No',
            r.checked_in_at.strftime('%Y-%m-%d %H:%M:%S') if r.checked_in_at else '',
        ])

    output.seek(0)
    filename = 'all_events_registrations.csv'
    encoded = quote(filename)
    return Response(
        output.getvalue(),
        mimetype='text/csv; charset=utf-8',
        headers={'Content-Disposition': f"attachment; filename=\"{filename}\"; filename*=UTF-8''{encoded}"},
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
