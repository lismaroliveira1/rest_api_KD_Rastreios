from sql_alchemy import database


class PackageModel(database.Model):
    __tablename__ = 'packages'

    package_code = database.Column(database.String, primary_key=True)
    name = database.Column(database.String(20))
    user_id = database.Column(database.String(20))
    trackings = database.relationship('TrackingModel')

    def __init__(self, package_code, name, user_id):
        self.package_code = package_code
        self.name = name
        self.user_id = user_id

    def toJson(self):
        return {
            "package_code": self.package_code,
            "name": self.name,
            "user_id": self.user_id,
            "trackings": [tracking.toJson() for tracking in self.trackings]
        }

    @classmethod
    def findPackage(cls, package_code):
        package = cls.query.filter_by(package_code=package_code).first()
        if package:
            return package
        return None

    def savePackage(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()

    def updatePackage(self, package_code, name, user_id):
        self.package_code = package_code
        self.name = name
        self.user_id = user_id

    def deletePackage(self):
        database.session.delete(self)
        database.session.commit()
