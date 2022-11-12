from main import db
from .model_mixin import ModelMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(ModelMixin, db.Model):
    __tablename__ = "user"
    username = db.Column(db.String(64), index=True,
                         unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    display_name = db.Column(db.String(64), nullable=True, unique=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
