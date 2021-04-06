from sql_alchemy import database


class PackageModel(database.Model):
    __tablename__ = 'packages'

    packageCode = database.Column(database.String, primary_key=True)
    name = database.Column(database.String(20))
    user_id = database.Column(database.String)

    def __init__(self, packageCode, name, user_id):
        self.packageCode = packageCode
        self.name = name
        self.user_id = user_id

    def toJson(self):
        return {
            "packageCode": self.packageCode,
            "name": self.name,
            "user_id": self.user_id,
            "trackings": []
        }

    @classmethod
    def findPackage(cls, packageCode):
        package = cls.query.filter_by(packageCode=packageCode).first()
        if package:
            return package
        return None

    def saveTracking(self):
        database.session.add(self)
        database.session.commit()

    def delete(self):
        database.session.delete(self)
        database.session.commit()
