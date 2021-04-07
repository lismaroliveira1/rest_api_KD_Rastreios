from sql_alchemy import database


class TrackingModel(database.Model):
    __tablename__: 'trackings'

    date = database.Column(database.String(10), required=True)
    destiny = database.Column(database.String(80))
    hour = database.Column(database.String(10))
    origin = database.Column(database.String(80))
    status = database.Column(database.String(80))

    def __init__(self, date, destiny, hour, origin, status):
        self.date = date
        self.destiny = destiny
        self.hour = hour
        self.origin = origin
        self.status = status

    def toJson(self):
        return {
            "date": self.date,
            "destiny": self.destiny,
            "hour": self.hour,
            "origin": self.origin,
            "status": self.status
        }

    def saveTracking(self):
        database.session.save(self)
        database.session.commit()

    def updateTracking(self):
        self.date = date
        self.destiny = destiny
        self.hour = hour
        self.origin = origin
        self.status = status

    def deletetracking(self):
        database.session.delete(self)
        database.session.commit()
