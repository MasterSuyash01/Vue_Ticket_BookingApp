from celery import shared_task
import requests
import json
from datetime import datetime
from models import User,Venue



@shared_task
def monthly_report():
    print("This is a monthly report")
    return True


# working fine
@shared_task
def Daily_remainder():
    # query all users who have not booked today
    users = User.query.all()
    # for u in User.query.all():
    #     for ticket in u.tickets:
    #         if ticket.date == datetime.now().date():
    #             break
    #     else:
    #         users.append(u)
    for user in users:
        response=requests.post("https://chat.googleapis.com/v1/spaces/AAAA5gMBqaU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=x2yWid_LEstaf-Ns-7wfeGL2ulr3ms23Gmc7nBaoFyg",data=json.dumps({"text": f"Hi {user.name}, Have you visited bookings today ?"}))
    return response.ok

@shared_task
def UserTriggerd_Job():
    venues = Venue.query.all()
    # create csv file
    with open('venues.csv', 'w') as f:
        f.write("Name,Address,City,Number of Shows\n")
        for venue in venues:
            f.write(f"{venue.theatre},{venue.place},{venue.city},{len(venue.shows)}\n")
    return True