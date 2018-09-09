from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.username = None
        self.password = None
        self.active = False
        self.thread = None
        self.busy = False
        self.script = ''

    def manager(self, username, password):
        self.username = username
        self.password = password
        return self

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.password)