from sql_alchemy import database


class TrackingModel(database.Model):
    __tablename__ = 'trackings'

    tracking_id = database.Column(database.Integer, primary_key=True)
    date = database.Column(database.String(10))
    destiny = database.Column(database.String(80))
    hour = database.Column(database.String(10))
    origin = database.Column(database.String(80))
    status = database.Column(database.String(80))
    package_code = database.Column(
        database.String, database.ForeignKey('packages.package_code'))

    def __init__(self, date, destiny, hour, origin, status, package_code):
        self.date = date
        self.destiny = destiny
        self.hour = hour
        self.origin = origin
        self.status = status
        self.package_code = package_code

    def toJson(self):
        return {
            "date": self.date,
            "destiny": self.destiny,
            "hour": self.hour,
            "origin": self.origin,
            "status": self.status
        }

    @classmethod
    def findTracking(cls, tracking_id):
        tracking = cls.query.filter_by(tracking_id=tracking_id).first()
        if tracking:
            return tracking
        return None

    def saveTracking(self):
        database.session.add(self)
        database.session.commit()

    def updateTracking(self, date, destiny, hour, origin, status):
        self.date = date
        self.destiny = destiny
        self.hour = hour
        self.origin = origin
        self.status = status

    def deleteTracking(self):
        database.session.delete(self)
        database.session.commit()
