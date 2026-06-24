class TestErrorPages:
    def test_404_page(self, client):
        r = client.get("/nonexistent")
        assert r.status_code == 404
        assert "404" in r.data.decode()

    def test_500_page(self, app, client):
        @app.route("/test-error")
        def test_error():
            raise RuntimeError("Test error")

        r = client.get("/test-error")
        assert r.status_code == 500
        page = r.data.decode()
        assert "500" in page

    def test_request_id_in_response(self, client):
        r = client.get("/event/")
        assert "X-Request-ID" in r.headers

    def test_log_file_created(self, app):
        import os
        log_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "logs", "app.log"
        )
        with app.app_context():
            app.logger.info("test log entry")
        assert os.path.exists(log_file)
