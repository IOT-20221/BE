from .model_mixin import ModelMixin
from main import db
from .user_device import user_device


class Device(ModelMixin, db.Model):
    __tablename__ = "device"
    code = db.Column(db.String(8), index=True, unique=True,
                     nullable=False)
    device_name = db.Column(db.String(255), index=True, nullable=False)
    date_of_manufacture = db.Column(db.DateTime, nullable=False)
    place_of_manufacture = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(10), nullable=False, default="1.0.0")
    users = db.relationship("User", secondary=user_device,
                            lazy="dynamic", backref=db.backref("devices", lazy=True))

    def __repr__(self) -> str:
        return "<Device {}>".format(self.code)
