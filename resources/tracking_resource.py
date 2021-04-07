from flask_restful import Resource, reqparse
from models.tracking_model import TrackingModel


class Trackings(Resource):
    def get(self):
        return {"trackings": [tracking.toJson() for tracking in TrackingModel.query.all()]}


class Trackings(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument('date', type=str, required=True)
    arguments.add_argument('destiny', type=str)
    arguments.add_argument('hour', type=str)
    arguments.add_argument('origin', type=str)
    arguments.add_argument('status', type=str)

    def get(self, tracking_id):
        tracking = TrackingModel.findTracking(tracking_id)
        if tracking:
            return tracking.toJson()
        return {"message": "tracking not found"}
