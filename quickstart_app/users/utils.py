from quickstart_app.models import User

def get_user_by_username(name):
    return User.query.filter_by(username=name).first()
