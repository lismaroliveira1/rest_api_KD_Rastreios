from flask_restful import Resource, reqparse
from models.tracking_model import TrackingModel


class Trackings(Resource):
    def get(self):
        return {"trackings": [tracking.toJson() for tracking in TrackingModel.query.all()]}


class Tracking(Resource):

    arguments = reqparse.RequestParser()
    arguments.add_argument('date', type=str, required=True)
    arguments.add_argument('destiny', type=str)
    arguments.add_argument('hour', type=str)
    arguments.add_argument('origin', type=str)
    arguments.add_argument('status', type=str)
    arguments.add_argument('package_code', type=str)

    def get(self, tracking_id):
        tracking = TrackingModel.findTracking(tracking_id)
        if tracking:
            return tracking.toJson(), 200
        return {"message": "tracking not found"}, 404

    def post(self, tracking_id):
        trackingData = Tracking.arguments.parse_args()
        if TrackingModel.findTracking(tracking_id):
            return {"message": "Tracking already exists"}
        tracking = TrackingModel(**trackingData)
        try:
            tracking.saveTracking()
            return tracking.toJson(), 201
        except:
            return {"message": "Internal server error"}, 500

    def put(self, tracking_id):
        tracking = TrackingModel.findTracking(tracking_id)
        tracking_data = Tracking.arguments.parse_args()
        if tracking:
            tracking.updateTracking(**tracking_data)
            try:
                tracking.saveTracking()
                return tracking.toJson(), 200
            except:
                return {"message": "Internal server error"}, 500
        new_tracking = TrackingModel(**tracking_data)
        try:
            new_tracking.saveTracking()
            return new_tracking.toJson(), 201
        except:
            return {"message": "Internal server error"}, 500

    def delete(self, tracking_id):
        tracking = TrackingModel.findTracking(tracking_id)
        if tracking:
            tracking.deleteTracking()
            return {"message": "Tracking deleted successfully"}, 200
        return {"message": "Tracking not found"}
