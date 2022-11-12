from main import db

user_device = db.Table(
    "user_device",
    db.Column("user_id", db.Integer, db.ForeignKey(
        "user.id"), primary_key=True),
    db.Column("device_code", db.String(8), db.ForeignKey(
        "device.code"), primary_key=True)
)
