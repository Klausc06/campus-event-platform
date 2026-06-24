import sys
import os
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import create_app
    app = create_app()
except Exception:
    from flask import Flask
    app = Flask(__name__)

    @app.route("/")
    def show_error():
        return f"<pre>{traceback.format_exc()}</pre>", 500
