import pytest

from app.server import MainApp

@pytest.fixture
def app(mocker):
    with mocker.patch('app.server.MainApp._init_rabbit') as patched:
        app = MainApp()

    flask_app = app.get_app()
    flask_app.debug = True
    return flask_app.test_client()

@pytest.fixture
def article():
    return {
        "id": "1",
    }

def test_get_price(app, article):
    import ipdb; ipdb.set_trace()
    res = app.get("/v1/pricing/{}".format(article.get("id")))
    assert res.status_code == 200


# Test caso base de pedido de precio por id_article
# Test caso no hay precio con id_article
