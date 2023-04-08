class User:
    def __init__(self, id, active, username, timestamp):
        self.id = id
        self.username = username
        self.active = active
        self.timestamp = timestamp

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'active': self.active,
            'timestamp':self.timestamp
        }