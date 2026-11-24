import pytest

from app.main import create_app


@pytest.fixture
def client(tmp_path):
    # chaque test utilise sa propre base vide
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()
