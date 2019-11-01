# from datetime import datetime
# import pytest
# from mockupdb import * #noqa
# from pymongo import MongoClient
# from app.utils import mongo
# from app.server import MainApp
#
# @pytest.fixture
# def app(mocker):
#     with mocker.patch('app.server.MainApp._init_rabbit') as patched:
#         main_app = MainApp()
#
#     flask_app = main_app.get_flask_app()
#     flask_app.debug = True
#     return flask_app.test_client()
#
# #
# # @pytest.fixture
# # def patch_price(monkeypatch):
# #     import ipdb; ipdb.set_trace()
# #     # setUp
# #     server = MockupDB()
# #     port = server.run()
# #     def mongo_client():
# #         return MongoClient(server.uri)
# #
# #     monkeypatch.setattr(mongo, "client", mongo_client)
# #
# #     collection = mongo.client.db.prices
# #     data = {
# #         '_id': 346346,
# #         'price_id': 5,
# #         'created': datetime.now(),
# #         'state': 'ACTIVE',
# #         'max_price':  30.0,
# #         'min_price':  15.0,
# #         'price': 25.0,
# #         'price_currency': 'ARS',
# #         'formated_price': 'ARS 25.0',
# #         'article_id': '1'
# #     }
# #     future = go(collection.insertOne, data)
# #     import ipdb; ipdb.set_trace()
# #
# #     # TearDown
# #     yield patch_price
# #     import ipdb; ipdb.set_trace()
# #     go(collection.deleteOne, {'price_id': data.get('price_id')})
# #     client.close()
#
# def test_get_price_by_article_id(app, mocker):
#     server = MockupDB()
#     port = server.run()
#     mongo_client = MongoClient(server.uri)
#     with mocker.patch('app.utils.mongo.get_mongo_client', return_value=mongo_client):
#         import ipdb; ipdb.set_trace()
#         data = {
#             '_id': 346346,
#             'price_id': 5,
#             'created': datetime.now(),
#             'state': 'ACTIVE',
#             'max_price':  30.0,
#             'min_price':  15.0,
#             'price': 25.0,
#             'price_currency': 'ARS',
#             'formated_price': 'ARS 25.0',
#             'article_id': '1'
#         }
#         mongo_client.insertOne(data)
#
#     response = app.get('v1/pricing/1')
#     assert res.status_code == 200
#
# # Test caso base de pedido de precio por article_id
# # Test caso no hay precio con article_id
#
#
# # db.collection.deleteOne(
# #    <filter>,
# #    {
# #       writeConcern: <document>,
# #       collation: <document>
# #    }
# # )
#
# # yield nombre del metodo para el teaardown
