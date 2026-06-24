import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models import Event, Registration, User
from datetime import datetime, timedelta, timezone

app = create_app()


def seed_if_empty():
    with app.app_context():
        if User.query.count() > 0:
            return
        db.create_all()
        admin = User(username="admin", email="admin@campus.edu", is_admin=True)
        admin.set_password("admin123456")
        db.session.add(admin)
        students = []
        for i in range(1, 6):
            s = User(username=f"student{i}", email=f"student{i}@campus.edu")
            s.set_password("12345678")
            db.session.add(s)
            students.append(s)
        db.session.flush()
        now = datetime.now(timezone.utc)
        events = [
            Event(title="新学期迎新晚会", description="欢迎新同学加入校园大家庭", location="大礼堂",
                  start_time=now + timedelta(days=7), end_time=now + timedelta(days=7, hours=3),
                  max_participants=200, checkin_code="WELCOME", creator_id=admin.id, category="社交"),
            Event(title="Python编程工作坊", description="从零开始学习Flask Web开发", location="计算机实验室A301",
                  start_time=now + timedelta(days=14), end_time=now + timedelta(days=14, hours=2),
                  max_participants=50, checkin_code="PYTHON", creator_id=admin.id, category="学术"),
            Event(title="校园马拉松", description="第五届校园马拉松比赛", location="校田径场",
                  start_time=now + timedelta(days=21), end_time=now + timedelta(days=21, hours=4),
                  max_participants=500, checkin_code="RUN2024", creator_id=admin.id, category="体育"),
            Event(title="职业规划讲座", description="企业HR分享求职经验", location="学术报告厅",
                  start_time=now + timedelta(days=30), end_time=now + timedelta(days=30, hours=2),
                  max_participants=100, checkin_code="CAREER", creator_id=admin.id, category="学术"),
            Event(title="电影放映之夜", description="本周放映经典影片", location="多功能厅",
                  start_time=now + timedelta(days=3), end_time=now + timedelta(days=3, hours=3),
                  max_participants=0, checkin_code="MOVIE", creator_id=admin.id, category="文艺"),
        ]
        for e in events:
            db.session.add(e)
        db.session.flush()
        for s in students[:3]:
            db.session.add(Registration(user_id=s.id, event_id=events[0].id))
        db.session.add(Registration(user_id=students[0].id, event_id=events[1].id,
                                     checked_in=True, checked_in_at=now))
        db.session.commit()
        print("Vercel: seed data created")


seed_if_empty()
