from db import db

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    tickets = db.relationship('Ticket', backref='show', cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Show {self.title}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    tickets = db.relationship('Ticket', backref='user')
    def __repr__(self):
        return f"<User {self.username}>"

    def get_id(self):
        return str(self.id)  # Return a string representation of the user's ID

    def is_authenticated(self):
        return True  # All users are authenticated

    def is_active(self):
        return True  # All users are considered active

    def is_anonymous(self):
        return False  # Regular users are not anonymous

class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    theatre = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    shows = db.relationship('Show', backref='venue', cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Venue {self.theatre}>"

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(5), nullable=False)
    num_tickets = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"<Ticket {self.name}>"