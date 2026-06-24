import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask

def _create():
    try:
        from app import create_app
        return create_app()
    except Exception:
        fallback = Flask(__name__)
        import traceback
        @fallback.route("/")
        def err():
            return f"<pre>{traceback.format_exc()}</pre>", 500
        return fallback

app = _create()
