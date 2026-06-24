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
            title_en='Welcome Party for New Students',
            description='欢迎新同学加入校园大家庭，现场音乐、美食与互动游戏',
            description_en='Welcome new students with live music, food and interactive games',
            category='文艺',
            location='大礼堂',
            location_en='Main Auditorium',
            start_time=now + timedelta(days=7),
            end_time=now + timedelta(days=7, hours=3),
            max_participants=200,
            checkin_code='WELCOME2024',
            creator_id=admin.id,
        ),
        Event(
            title='Python 编程工作坊',
            title_en='Python Programming Workshop',
            description='从零开始学习 Python 编程，动手构建你的第一个应用',
            description_en='Learn Python programming from scratch and build your first application',
            category='学术',
            location='计算机实验室 A301',
            location_en='Computer Lab A301',
            start_time=now + timedelta(days=14),
            end_time=now + timedelta(days=14, hours=2),
            max_participants=50,
            checkin_code='PYTHON123',
            creator_id=admin.id,
        ),
        Event(
            title='校园马拉松',
            title_en='Campus Marathon',
            description='第五届校园马拉松比赛，5公里/10公里两个组别',
            description_en='5th Annual Campus Marathon, 5km and 10km categories',
            category='体育',
            location='校田径场',
            location_en='Campus Track Field',
            start_time=now + timedelta(days=21),
            end_time=now + timedelta(days=21, hours=4),
            max_participants=500,
            checkin_code='RUN2024',
            creator_id=admin.id,
        ),
        Event(
            title='职业规划讲座',
            title_en='Career Planning Seminar',
            description='企业 HR 分享求职经验与职场建议',
            description_en='Corporate HR shares job hunting experience and career advice',
            category='学术',
            location='学术报告厅',
            location_en='Academic Lecture Hall',
            start_time=now + timedelta(days=30),
            end_time=now + timedelta(days=30, hours=2),
            max_participants=100,
            checkin_code='CAREER',
            creator_id=admin.id,
        ),
        Event(
            title='电影放映之夜',
            title_en='Movie Night',
            description='本周放映经典影片，免费爆米花',
            description_en='Classic movie screening this week, free popcorn',
            category='社交',
            location='多功能厅',
            location_en='Multi-function Hall',
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
