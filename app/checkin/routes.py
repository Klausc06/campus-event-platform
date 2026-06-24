from datetime import datetime, timezone

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app.checkin import checkin_bp
from app.extensions import db
from app.models import Event, Registration
from app.forms import CheckinForm


@checkin_bp.route('/<int:event_id>', methods=['GET', 'POST'])
@login_required
def checkin(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash('活动不存在', 'warning')
        return redirect(url_for('event.list_events'))

    reg = Registration.query.filter_by(
        user_id=current_user.id,
        event_id=event_id,
        status='confirmed',
    ).first()

    if not reg:
        flash('你尚未报名此活动，无法签到', 'warning')
        return redirect(url_for('event.detail', id=event_id))

    if reg.checked_in:
        flash('你已经签到过了', 'info')
        return redirect(url_for('event.detail', id=event_id))

    form = CheckinForm()
    if form.validate_on_submit():
        if form.code.data.strip() == event.checkin_code:
            reg.checked_in = True
            reg.checked_in_at = datetime.now(timezone.utc)
            db.session.commit()
            flash('签到成功！', 'success')
            return redirect(url_for('event.detail', id=event_id))
        else:
            flash('签到码错误', 'danger')

    return render_template('checkin/checkin.html', form=form, event=event)
