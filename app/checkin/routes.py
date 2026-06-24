import base64
import io
import hmac
from datetime import datetime, timezone

import qrcode
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.checkin import checkin_bp
from app.extensions import db
from app.models import Event, Registration
from app.forms import CheckinForm


def get_qr_code(url):
    img = qrcode.make(url, box_size=10, border=2)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return f'data:image/png;base64,{b64}'


@checkin_bp.route('/<int:event_id>', methods=['GET', 'POST'])
@login_required
def checkin(event_id):
    event = db.get_or_404(Event, event_id)

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
        if hmac.compare_digest(form.code.data.strip(), event.checkin_code):
            reg.checked_in = True
            reg.checked_in_at = datetime.now(timezone.utc)
            db.session.commit()
            flash('签到成功！', 'success')
            return redirect(url_for('event.detail', id=event_id))
        else:
            flash('签到码错误', 'danger')

    return render_template('checkin/checkin.html', form=form, event=event)


@checkin_bp.route('/<int:event_id>/qr')
@login_required
def qr(event_id):
    event = db.get_or_404(Event, event_id)

    if event.creator_id != current_user.id and not current_user.is_admin:
        flash('无权查看签到二维码', 'danger')
        return redirect(url_for('event.detail', id=event_id))

    checkin_url = request.url_root.rstrip('/') + url_for('checkin.checkin', event_id=event_id)
    qr_data_uri = get_qr_code(checkin_url)

    return render_template('checkin/qr.html', event=event, qr_data_uri=qr_data_uri)
