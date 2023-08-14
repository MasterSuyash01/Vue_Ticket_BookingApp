from flask import Flask, jsonify, request,session,request,send_file
from flask_cors import CORS
import os
from datetime import datetime
from flask_bcrypt import check_password_hash,Bcrypt
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager
)
from workers import celery_init_app
import task
from celery.schedules import crontab 
from db import db

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Add this line
app.config['JWT_SECRET_KEY'] = 'abcajdhfjkahdflsjd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    from models import User, Show, Venue, Ticket
    db.create_all()

    bcrypt = Bcrypt(app)
    celery = celery_init_app(app)
    admin_username="admin"
    admin_pwd="admin123"
    CORS(app)
    jwt = JWTManager(app)
    if not User.query.filter_by(username=admin_username).first():
        
        hashed_password = bcrypt.generate_password_hash(admin_pwd).decode('utf-8')
        new_user = User(name='admin', username='admin', password=hashed_password, is_admin=True)
        db.session.add(new_user)
        db.session.commit()

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=23, minute=24),
        task.Daily_remainder.s()
    )

def user_loader(user_id):
    if User.query.get(int(user_id)) is not None:
        return User.query.get(int(user_id))
    else:
        return None

@app.route('/shows', methods=['GET', 'POST'])
@jwt_required()
def all_shows():
    if request.method == "POST":
        current_user = user_loader(get_jwt_identity())
        if not current_user.is_admin:
            return jsonify({'status': 'error', 'message': 'User not authorized'}), 401
        post_data = request.get_json()
        new_show = Show(
            title=post_data.get('title'),
            genre=post_data.get('genre'),
            date=post_data.get('date'),
            time=post_data.get('time'),
            venue_id=post_data.get('venue'),
            num_tickets=post_data.get('num_tickets')
        )
        db.session.add(new_show)
        db.session.commit()
        new_show = Show.query.get(new_show.id)
        return jsonify({
            'status': 'success',
            'message': 'Show Added!',
            'show': {
                "title" : new_show.title,
                "genre" : new_show.genre,
                "date" : new_show.date,
                "time" : new_show.time ,
                "num_tickets" : new_show.num_tickets,
                "venue" : {
                    "id" : new_show.venue.id,
                    "theatre" : new_show.venue.theatre,
                    "place" : new_show.venue.place,
                    "city" : new_show.venue.city
                }
                }
        })
    else:
        shows = Show.query.all()
        shows_data = []
        for show in shows:
            if show is not None:
                shows_data.append({
                    'id': show.id,
                    'title': show.title,
                    'genre': show.genre,
                    'date': datetime.strptime(show.date, '%Y-%m-%d').strftime('%Y-%m-%d'),
                    'time': datetime.strptime(show.time, '%H:%M').strftime('%H:%M'),
                    'num_tickets': show.num_tickets,
                    "venue" : {
                        "id" : show.venue.id,
                        "theatre" : show.venue.theatre,
                        "place" : show.venue.place,
                        "city" : show.venue.city
                    }
                })
        return jsonify({'status': 'success', 'shows': shows_data})

@app.route('/shows/<show_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def single_show(show_id):
    current_user = user_loader(get_jwt_identity())
    if not current_user.is_admin:
        return jsonify({'status': 'error', 'message': 'User not authorized'}), 401
    if request.method == "PUT":
        post_data = request.get_json()
        show = Show.query.get(show_id)
        print("Retrieved show:", show)
        if show:
            show.title = post_data.get('title')
            show.genre = post_data.get('genre')
            show.date = post_data.get('date')
            show.time = post_data.get('time')
            show.venue_id = post_data.get('venue')
            show.num_tickets = post_data.get('num_tickets')
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Show Updated!'})
        else:
            return jsonify({'status': 'error', 'message': 'Show not found'}), 404
    elif request.method == "DELETE":
        show = Show.query.get(show_id)
        print("Retrieved show:", show)
        if show:
            db.session.delete(show)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Show removed!'})
        else:
            return jsonify({'status': 'error', 'message': 'Show not found'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'}), 405

@app.route('/venues', methods=['GET', 'POST'])
@jwt_required()
def all_venues():
    if request.method == "POST":
        current_user = user_loader(get_jwt_identity())
        if not current_user.is_admin:
            return jsonify({'status': 'error', 'message': 'User not authorized'}), 401
        post_data = request.get_json()
        new_venue = Venue(
            theatre=post_data.get('theatre'),
            place=post_data.get('place'),
            city=post_data.get('city'),
        )
        db.session.add(new_venue)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Venue Added!', 'venue' : {"theatre" : new_venue.theatre, "place" : new_venue.place, "city" : new_venue.city}})
    else:
        venues = Venue.query.all()
        venues_data = []
        for venue in venues:
            if venue is not None:
                venues_data.append({
                    'id': venue.id,
                    'theatre': venue.theatre,
                    'place': venue.place,
                    'city': venue.city,
                })
        return jsonify({'status': 'success', 'venues': venues_data})

@app.route('/venues/<venue_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def single_venue(venue_id):
    current_user = user_loader(get_jwt_identity())
    if not current_user.is_admin:
        return jsonify({'status': 'error', 'message': 'User not authorized'}), 401
    if request.method == "PUT":
        post_data = request.get_json()
        venue = Venue.query.get(venue_id)
        if venue:
            venue.theatre = post_data.get('theatre')
            venue.place = post_data.get('place')
            venue.city = post_data.get('city')
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Venue Updated!'})
        else:
            return jsonify({'status': 'error', 'message': 'Venue not found'}), 404
    elif request.method == "DELETE":
        venue = Venue.query.get(venue_id)
        if venue:
            db.session.delete(venue)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Venue removed!'})
        else:
            return jsonify({'status': 'error', 'message': 'Venue not found'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'}), 405



@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if not name or not username or not password or not confirm_password:
        return jsonify({'status': 'error', 'message': 'Please provide name, username, password, and confirmPassword'}), 400

    if password != confirm_password:
        return jsonify({'status': 'error', 'message': 'Passwords do not match'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash the password

    new_user = User(name=name, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Please provide username and password'}), 400

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                access_token = create_access_token(identity=user.id)
                session['user_id'] = user.id
                return jsonify({'status': 'success', 'message': 'User logged in successfully', 'access_token': access_token, 'is_admin' : user.is_admin}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        else:
            return jsonify({'status': 'error', 'message': 'User not found'}), 401
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request method'}), 405

@app.route('/check_login', methods=['GET'])
@jwt_required()
def check_login():
    if user_loader(get_jwt_identity()):
        return jsonify({'status': 'success', 'message': 'User is logged in', 'is_admin':user_loader(get_jwt_identity()).is_admin}), 200
    else:
        return jsonify({'status': 'error', 'message': 'User is not logged in'}), 401


@app.route('/bookings', methods=['GET','POST'])
@jwt_required()
def create_booking():
    if request.method == "GET":
        current_user = user_loader(get_jwt_identity())
        if not current_user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        bookings = current_user.tickets
        bookings_data = []
        for booking in bookings:
            if booking is not None:
                bookings_data.append({
                    'id': booking.id,
                    'name': booking.name,
                    'date': booking.date,
                    'time': booking.time,
                    'num_tickets': booking.num_tickets,
                    'venuename': booking.show.venue.theatre,
                    'showname': booking.show.title
                })
        return jsonify({'status': 'success', 'bookings': bookings_data})
    elif request.method == "POST":
        data = request.get_json()
        name = data.get('name')
        date = data.get('date')
        time = data.get('time')
        num_tickets = data.get('num_tickets')
        show_id = data.get('showname')

        # Check if the show exists and if enough tickets are available
        show = Show.query.get(show_id)
        if not show:
            return jsonify({'status': 'error', 'message': 'Show not found'}), 404
        if show.num_tickets < int(num_tickets):
            return jsonify({'status': 'error', 'message': 'Not enough tickets available'}), 400

        new_booking = Ticket(
            name=name,
            date=date,
            time=time,
            num_tickets=num_tickets,
            show_id=show_id
        )
        current_user = user_loader(get_jwt_identity())
        current_user.tickets.append(new_booking)
        db.session.add(new_booking)
        
        # Update the num_tickets value for the show
        show.num_tickets -= int(num_tickets)
        
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Booking created successfully'}), 201

@app.route('/export/theatres')
def export_job():
    job = task.UserTriggerd_Job()
    return send_file('venues.csv', download_name='theatres.csv', as_attachment=True)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # create admin
        admin_username="admin"
        admin_pwd="admin123"
        if not User.query.filter_by(username=admin_username).first():
            
            hashed_password = bcrypt.generate_password_hash(admin_pwd).decode('utf-8')
            new_user = User(name='admin', username='admin', password=hashed_password, is_admin=True)
            db.session.add(new_user)
            db.session.commit()
    app.run(debug=True)