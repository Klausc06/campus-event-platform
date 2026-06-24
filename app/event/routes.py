from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.event import event_bp
from app.extensions import db
from app.models import Event, Registration
from app.forms import EventForm


@event_bp.route('/')
def list_events():
    q = request.args.get('q', '').strip()
    query = Event.query
    if q:
        escaped_q = q.replace('%', '\\%').replace('_', '\\_')
        query = query.filter(
            (Event.title.ilike(f'%{escaped_q}%')) | (Event.location.ilike(f'%{escaped_q}%'))
        )
    events = query.order_by(Event.start_time.desc()).all()
    return render_template('event/list.html', events=events, q=q)


@event_bp.route('/<int:id>')
def detail(id):
    event = db.get_or_404(Event, id)
    registration = None
    if current_user.is_authenticated:
        registration = Registration.query.filter_by(
            user_id=current_user.id, event_id=event.id, status='confirmed'
        ).first()
    return render_template('event/detail.html', event=event, registration=registration)


@event_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(creator_id=current_user.id)
        form.populate_obj(event)
        db.session.add(event)
        db.session.commit()
        flash('活动创建成功', 'success')
        return redirect(url_for('event.detail', id=event.id))
    return render_template('event/create.html', form=form)


@event_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    event = db.get_or_404(Event, id)
    if event.creator_id != current_user.id and not current_user.is_admin:
        flash('无权编辑此活动', 'danger')
        return redirect(url_for('event.detail', id=event.id))
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        db.session.commit()
        flash('活动更新成功', 'success')
        return redirect(url_for('event.detail', id=event.id))
    return render_template('event/edit.html', form=form, event=event)


@event_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    event = db.get_or_404(Event, id)
    if event.creator_id != current_user.id and not current_user.is_admin:
        flash('无权删除此活动', 'danger')
        return redirect(url_for('event.detail', id=event.id))
    db.session.delete(event)
    db.session.commit()
    flash('活动已删除', 'success')
    return redirect(url_for('event.list_events'))


@event_bp.route('/<int:id>/register', methods=['POST'])
@login_required
def register(id):
    event = db.get_or_404(Event, id)
    existing = Registration.query.filter_by(user_id=current_user.id, event_id=event.id).first()
    if existing:
        if existing.status == 'cancelled':
            if event.is_full:
                flash('名额已满，无法重新报名', 'warning')
                return redirect(url_for('event.detail', id=event.id))
            existing.status = 'confirmed'
            db.session.commit()
            flash('已重新报名', 'success')
        else:
            flash('您已报名此活动', 'info')
    else:
        if event.is_full:
            flash('名额已满，无法报名', 'warning')
            return redirect(url_for('event.detail', id=event.id))
        reg = Registration(user_id=current_user.id, event_id=event.id)
        db.session.add(reg)
        db.session.commit()
        flash('报名成功', 'success')
    return redirect(url_for('event.detail', id=event.id))


@event_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel(id):
    event = db.get_or_404(Event, id)
    reg = Registration.query.filter_by(
        user_id=current_user.id, event_id=event.id, status='confirmed'
    ).first()
    if not reg:
        flash('未找到报名记录', 'warning')
        return redirect(url_for('event.detail', id=event.id))
    reg.status = 'cancelled'
    db.session.commit()
    flash('已取消报名', 'info')
    return redirect(url_for('event.detail', id=event.id))
