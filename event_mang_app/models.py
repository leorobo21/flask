from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from event_mang_app import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    data_rel = db.relationship('Data', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email},'{self.image_file}')"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(20), nullable=False)
    system_name = db.Column(db.String(20), nullable=False)
    loop_num = db.Column(db.Integer, nullable=False)
    type_file = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    sender = db.Column(db.String(20), nullable=False)
    #last_date_modified = db.Column(db.DateTime, nullable=False, default=datetime.now)
    file_path = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    identity_p = db.relationship('ProjectData', backref='project_identity', lazy=True)
    identity_s = db.relationship('SystemData', backref='system_identity', lazy=True)
    identity_l = db.relationship('LoopData', backref='loop_identity', lazy=True)
    identity_t = db.relationship('TypeData', backref='type_identity', lazy=True)

    def __repr__(self):
        return f"Data('{self.project_name}','{self.date_posted},'{self.file_path}', '{self.sender}')"

class ProjectData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(20), nullable=False)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

    def __repr__(self):
        return f"ProjectData('{self.project}')"

class SystemData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(20), nullable=False)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

    def __repr__(self):
        return f"ProjectData('{self.project}', '{self.data_id}')"

class LoopData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.Integer, nullable=False)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

    def __repr__(self):
        return f"ProjectData('{self.project}')"

class TypeData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String(20), nullable=False)
    data_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

    def __repr__(self):
        return f"ProjectData('{self.project}')"