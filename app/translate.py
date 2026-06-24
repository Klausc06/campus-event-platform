from flask import Blueprint, jsonify, request
from app.models import Event

translate_bp = Blueprint("translate", __name__, url_prefix="/api")


@translate_bp.route("/translate", methods=["POST"])
def translate():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "missing 'text' field"}), 400

    text = data["text"]
    target = data.get("target", "en")

    zh_en = {
        "学术": "Academic",
        "体育": "Sports",
        "文艺": "Arts",
        "社交": "Social",
        "志愿服务": "Volunteer",
        "其他": "Other",
        "全部": "All",
        "报名中": "Open",
        "名额已满": "Full",
        "即将满员": "Almost Full",
        "查看详情": "View Details",
        "创建新活动": "Create Event",
        "搜索活动名称或地点...": "Search events or locations...",
        "活动列表": "Event List",
        "活动详情": "Event Detail",
        "登录": "Login",
        "注册": "Register",
        "退出": "Logout",
        "管理": "Admin",
        "日志": "Logs",
        "我的": "My",
        "签到": "Check In",
        "立即报名": "Register Now",
        "取消报名": "Cancel Registration",
        "已报名": "Registered",
        "签到成功": "Check-in Successful",
        "签到码错误": "Invalid Check-in Code",
        "页面不存在": "Page Not Found",
        "服务器内部错误": "Internal Server Error",
        "返回首页": "Back to Home",
    }

    en_zh = {v: k for k, v in zh_en.items()}

    if target == "en":
        result = zh_en.get(text, text)
    else:
        result = en_zh.get(text, text)

    return jsonify({"original": text, "translated": result, "target": target})


@translate_bp.route("/events")
def events_bilingual():
    events = Event.query.order_by(Event.start_time.desc()).all()
    return jsonify([
        {
            "id": e.id,
            "title": {"zh": e.title, "en": e.title_en or e.title},
            "description": {"zh": e.description, "en": e.description_en or e.description},
            "location": {"zh": e.location, "en": e.location_en or e.location},
            "category": {"zh": e.category, "en": e.category},
            "max_participants": e.max_participants,
            "registered_count": e.registered_count,
        }
        for e in events
    ])
