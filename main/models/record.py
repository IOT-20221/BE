from .model_mixin import ModelMixin
from main import db


class Record(ModelMixin, db.Model):
    device_code = db.Column(db.String(8), db.ForeignKey(
        "device.code"), nullable=False)
    data = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return "<Record of {}>".format(self.device_code)
