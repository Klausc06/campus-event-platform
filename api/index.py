import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import create_app
    app = create_app()
except Exception as e:
    from flask import Flask
    app = Flask(__name__)
    @app.route("/")
    def error():
        return f"Error: {str(e)}", 500
