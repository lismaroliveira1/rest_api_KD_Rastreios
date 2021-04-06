from sql_alchemy import database


class PackageModel(database.Model):
    __tablename__ = 'packages'

    packageCode = database.Column(database.String, primary_key=True)
    name = database.Column(database.String, primary_key=True)

    def __init__(self, packageCode, name):
        self.packageCode = packageCode
        self.name = name

    def saveTracking(self):
        database.session.add(self)
        database.session.commit()

    def toJson(self):
        return {
            "packageCode": self.packageCode,
            "name": self.name
            "trackings": []
        }

    @classmethod
    def findPackage(cls, packageCode):
        package = cls.query.filter_by(packageCode=packageCode).first()
        if package:
            return package
        return None

    def delete(self):
        database.session.delete(self)
        database.session.commit()
