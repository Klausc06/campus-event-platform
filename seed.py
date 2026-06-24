from datetime import datetime, timedelta, timezone

from app import create_app
from app.extensions import db
from app.models import User, Event, Registration

app = create_app()

with app.app_context():
    db.create_all()

    admin = User(username='admin', email='admin@campus.edu', is_admin=True)
    admin.set_password('admin123456')
    db.session.add(admin)

    students = []
    for i in range(1, 6):
        s = User(username=f'student{i}', email=f'student{i}@campus.edu')
        s.set_password('12345678')
        db.session.add(s)
        students.append(s)

    db.session.flush()

    now = datetime.now(timezone.utc)
    events = [
        Event(
            title='新学期迎新晚会',
            description='欢迎新同学加入校园大家庭',
            location='大礼堂',
            start_time=now + timedelta(days=7),
            end_time=now + timedelta(days=7, hours=3),
            max_participants=200,
            checkin_code='WELCOME2024',
            creator_id=admin.id,
        ),
        Event(
            title='Python 编程工作坊',
            description='从零开始学习 Python 编程',
            location='计算机实验室 A301',
            start_time=now + timedelta(days=14),
            end_time=now + timedelta(days=14, hours=2),
            max_participants=50,
            checkin_code='PYTHON123',
            creator_id=admin.id,
        ),
        Event(
            title='校园马拉松',
            description='第五届校园马拉松比赛',
            location='校田径场',
            start_time=now + timedelta(days=21),
            end_time=now + timedelta(days=21, hours=4),
            max_participants=500,
            checkin_code='RUN2024',
            creator_id=admin.id,
        ),
        Event(
            title='职业规划讲座',
            description='企业 HR 分享求职经验',
            location='学术报告厅',
            start_time=now + timedelta(days=30),
            end_time=now + timedelta(days=30, hours=2),
            max_participants=100,
            checkin_code='CAREER',
            creator_id=admin.id,
        ),
        Event(
            title='电影放映之夜',
            description='本周放映经典影片',
            location='多功能厅',
            start_time=now + timedelta(days=3),
            end_time=now + timedelta(days=3, hours=3),
            max_participants=0,
            checkin_code='MOVIE',
            creator_id=admin.id,
        ),
    ]
    for e in events:
        db.session.add(e)

    db.session.flush()

    for s in students[:3]:
        db.session.add(Registration(user_id=s.id, event_id=events[0].id, status='confirmed'))

    db.session.add(Registration(user_id=students[0].id, event_id=events[1].id, status='confirmed', checked_in=True, checked_in_at=now))

    db.session.commit()

    print('Seed data created successfully!')
    print('Admin login:  admin / admin123456')
    print('Student logins: student1-5 / 12345678')
