from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Scooter(db.Model):
    __tablename__ = 'scooters'
    id = db.Column(db.String, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    is_reserved = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self):
        return {'id': self.id, 'lat': self.lat, 'lng': self.lng, 'is_reserved': self.is_reserved}
