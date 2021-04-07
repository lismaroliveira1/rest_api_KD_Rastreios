from flask_restful import Resource, reqparse
from models.tracking_model import TrackingModel


class Trackings(Resource):
    def get(self):
        return {"trackings": [tracking.toJson() for tracking in TrackingModel.query.all()]}
