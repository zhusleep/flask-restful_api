# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS
import json
import os


app = Flask(__name__)
CORS(app)
api = Api(app)


# global infer variable
table_warehouse = {}
table_shipment = {}
table_order = {}
infer_report = {}
infer_status = ["2017-11-01","2017-11-02","2017-11-03"]
infer_range = {"start_date":"1979-01-01","end_date":"1979-01-01"}
infer_lock = False
infer_request = {"request": False}
#global truth data
table_warehouse_truth = {}
table_shipment_truth = {}
table_order_truth = {}


# loading truth data
with open('truth_data/warehouse.json', 'r') as f:
    table_warehouse_truth = json.load(f)
    table_warehouse = table_warehouse_truth

with open('truth_data/shipment.json', 'r') as f:
    table_shipment_truth = json.load(f)
    table_shipment = table_shipment_truth

with open('truth_data/order.json', 'r') as f:
    table_order_truth = json.load(f)
    table_order = table_order_truth


def abort_if_todo_not_exist(date, wh_id):
    if wh_id not in table_warehouse[date]:
        abort(404, message = "warehouse {} doesn't exist".format(wh_id))


# warehouse list
# shows a list of all warehouse, and lets you POST to add new tasks
class WarehouseList(Resource):
    def get(self, date):
        return dict([(key, table_warehouse[date][key]["position"]) for key in table_warehouse[date]])

    def put(self, date):
        global table_warehouse
        args=request.json
        table_warehouse[date] = args[date]

    def post(self, date):
        global table_warehouse
        args=request.json
        table_warehouse[date] = args

    def delete(self):
        global table_warehouse
        table_warehouse = table_warehouse_truth


# one warehouse detail
class WarehouseDetail(Resource):
    def get(self, date, wh_id):
        abort_if_todo_not_exist(date, wh_id)
        return table_warehouse[date][wh_id]

    def delete(self, date, wh_id):
        global table_warehouse
        abort_if_todo_not_exist(date, wh_id)
        del table_warehouse[date][wh_id]
        return '', 204

    def put(self, date, wh_id):
        global table_warehouse
        args = request.json
        table_warehouse[date][wh_id] = args
        return args, 201

    def post(self, date, wh_id):
        global table_warehouse
        args = request.json
        table_warehouse[date][wh_id] = args
        return args, 201


# warehouse position list
# return warehouse list and position
class WarehousePositionList(Resource):
    def get(self, date):
        return dict([(key, table_warehouse[date][key]["position"]) for key in table_warehouse[date] if table_warehouse[date][key]["node_type"] != "经销商"])


# dealer position list
# return dealer list and position
class DealerPositionList(Resource):
    def get(self, date):
        return dict([(key, table_warehouse[date][key]["position"]) for key in table_warehouse[date] if table_warehouse[date][key]["node_type"] == "经销商"])


# order list
class OrderList(Resource):
    def put(self, date):
        global table_order
        args = request.json
        table_order[date] = args[date]

    def delete(self):
        global table_order
        table_order = table_order_truth


# order detail of one warehouse
class OrderDetail(Resource):
    def get(self, date, wh_id):
        return table_order[date][wh_id]

    def delete(self, date, wh_id):
        del table_order[date][wh_id]

    def post(self, date, wh_id):
        args = request.json
        table_order[date][wh_id] = args


# shipment list
class ShipmentList(Resource):
    def put(self,date):
        global table_shipment
        args = request.json
        table_shipment[date] = args[date]

    def delete(self):
        global table_shipment
        table_shipment = table_shipment_truth


# shipment detail of one wh
class ShipmentDetail(Resource):
    def get(self, date, wh_id):
        return table_shipment[date][wh_id]

    def delete(self, date, wh_id):
        del table_shipment[date][wh_id]

    def post(self, date, wh_id):
        args = request.json
        table_shipment[date][wh_id] = args


# infer request
class InferRequest(Resource):
    def get(self):
        return infer_request

    def put(self):

        global infer_request
        infer_request["request"] = True

    def delete(self):
        global infer_request
        infer_request["request"] = False


# infer range
class InferRange(Resource):
    def get(self):
        return {'start_date': infer_range["start_date"], 'end_date':infer_range["end_date"]}

    def put(self):
        global infer_range
        args = request.json
        infer_range["start_date"] = args["start_date"]
        infer_range["end_date"] = args["end_date"]
        return '', 201

    def delete(self):
        global infer_range
        infer_range["start_date"] = "1979-01-01"
        infer_range["end_date"] = "1979-01-01"


# infer lock
class InferLock(Resource):
    def get(self):
        return {"infer_lock":infer_lock}

    def put(self):
        global infer_lock
        infer_lock = True
        print(infer_lock)

    def delete(self):
        global infer_lock
        infer_lock = False


# infer status
class InferStatus(Resource):
    def get(self, date):
        if date in infer_status:
            return {"status":True}
        else:
            return {"status":False}

    def put(self, date):
        global infer_status
        infer_status.append(date)
        print(infer_status)
        print(infer_lock)

    def delete(self):
        global infer_status
        infer_status = ["2017-11-01","2017-11-02","2017-11-03"]


# infer report
class InferReport(Resource):
    def get(self):
        return infer_report

    def put(self):
        global infer_report
        args = request.json
        infer_report = args

    def delete(self):
        global infer_report
        infer_report = {}


##
## Actually setup the Api resource routing hear
##
api.add_resource(DealerPositionList, '/dealer_position_list/<date>')
api.add_resource(WarehousePositionList, '/warehouse_position_list/<date>')

api.add_resource(WarehouseList, '/warehouse', '/warehouse/<date>')
api.add_resource(WarehouseDetail, '/warehouse/<date>/<wh_id>')

api.add_resource(OrderList, '/order', '/order/<date>')
api.add_resource(OrderDetail, '/order/<date>/<wh_id>')
api.add_resource(ShipmentList, '/shipment', '/shipment/<date>')
api.add_resource(ShipmentDetail, '/shipment/<date>/<wh_id>')

api.add_resource(InferLock, '/infer/lock')
api.add_resource(InferRange, '/infer/range')
api.add_resource(InferRequest, '/infer/request')
api.add_resource(InferStatus, '/infer/status', '/infer/status/<date>')
api.add_resource(InferReport, '/infer/report')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
