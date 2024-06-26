from models import *
from sqlalchemy.orm import Session
import numpy as np

from random import randrange
from datetime import datetime, timedelta

def random_date_normal_exp(start, end):
    """
    This function will return a random datetime between two datetime 
    objects. The day is generated using a normal distribution and the
    time is generated using an exponential distribution.
    """
    # Parameters for normal distribution of days
    mean = (d2 - d1).days / 2
    sigma = (d2 - d1).days / 4

    # Scale parameter for exponential distribution (in hours)
    scale = 1.0  # Mean of 1 hour

    delta = end - start
    int_delta_days = delta.days
    
    # Generate a random day using normal distribution
    random_day = np.random.normal(mean, sigma)
    random_day = int(random_day)  # Convert to integer days
    
    # Ensure the random day is within the range
    random_day = max(0, min(int_delta_days, random_day))
    
    # Generate a random time using exponential distribution
    start_time = 1  # Start at 8:00 AM
    end_time = 23  # End at 6:00 PM
    while True:
        random_time = np.random.exponential(scale)
        if start_time <= random_time <= end_time:
            break
    
    random_hours = int(random_time)
    random_minutes = int((random_time - random_hours) * 60)
    
    # Calculate the final random datetime
    random_date = start + timedelta(days=random_day, hours=random_hours, minutes=random_minutes)
    
    return random_date

def poisson_random_date(start, end, lam):
    """
    This function will return a random datetime between two datetime 
    objects using a Poisson distribution for the intervals.
    """
    delta = end - start
    int_delta = delta.total_seconds()
    
    current_time = start
    while True:
        # Generate a Poisson-distributed interval (in seconds)
        interval = np.random.exponential(lam)
        
        # Add the interval to the current time
        current_time += timedelta(seconds=interval)
        
        # If the new time exceeds the end time, break the loop
        if current_time > end:
            break
            
    return current_time

d1 = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')

# Lambda for the Poisson distribution (average interval in seconds)
lam = 3600  # 1 hour on average

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

d1 = datetime.strptime('1/1/2008 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2009 4:50 AM', '%m/%d/%Y %I:%M %p')

def gen_users():
    with Session(engine) as session:
        spongebob = User(
            id=1,
            login="spongebob",
            password="Spongebob Squarepants",
            last_activity=random_date_normal_exp(d1, d2)
        )
        sandy = User(
            id=2,
            login="sandy",
            password="Sandy Cheeks",
            last_activity=random_date_normal_exp(d1, d2)
        )
        patrick = User(
            id=3,
            login="patrick", 
            password="Patrick Star",
            last_activity=random_date_normal_exp(d1, d2)
        )

        session.add_all([
            User(
                id=i,
                login=f"patrick{i}", 
                password=f"Patrick Star{i}",
                last_activity=random_date_normal_exp(d1, d2)
            ) for i in range(4, 2000)
        ])


        session.add_all([spongebob, sandy, patrick])
        session.commit()

def gen_drivers():
    with Session(engine) as session:
        session.add_all([
            Driver(
                id=driver_id,
                phone="1234567890",
                contact_email="Sandy Cheeks",
                last_name="Sandy",
                first_name="Cheeks",
            ) for driver_id in range(1, 2000)
        ])
        session.commit()

def gen_trucks():
    with Session(engine) as session:
        session.add_all([
            Truck(
                id=i,
                name = f"Truck{i}",
                year = f"{i}00",
                color =  ["RED", "GREEN", "YELLOW", "BLUE"][i % 4],
                vin_number = f"{i}-{i}",
            ) for i in range(1, 2000)
        ])
        session.commit()

def gen_trips():
    with Session(engine) as session:
        session.add_all([
            TripReport(
                url = "https://www.tripsreport.com/" + "".join(["abcdefghijklmnopqrstuvwxyz0123456789"[(i + j * i) % 17] for j in range(10)]),
                driver_id=i
            ) for i in range(1, 2000)
        ])
        session.commit()

def gen_companies():
    with Session(engine) as session:
        session.add_all([
            OfficialCompany(
                id=i,
                name = f"Name{i}",
                owner = f"NameOwner{i}",
            ) for i in range(1, 2000)
        ])
        session.commit()

def gen_tickets():
    tickets = []
    ticket_id = 1
    for driver_id in range(1, 2000):
        for _ in range(1, int(np.random.normal(loc=40, scale=10))):
            ticket = Ticket(
                        id=ticket_id,
                        driver_id=driver_id,
                        amount=np.random.normal(loc=483.324, scale=49.334)
                    ) 
            ticket_id += 1
            tickets.append(ticket)

    with Session(engine) as session:
        session.add_all(tickets)
        session.commit()

def gen_services():
    services = []
    service_id = 1
    for driver_id in range(1, 2000):
        for _ in range(1, max(0, int(np.random.normal(loc=5, scale=3)))):
            service = Service(
                    id=service_id,
                    driver_id=driver_id,
                    date_of_service=random_date(d1, d2),
                    sum_of_outlays=np.random.normal(loc=1010.324, scale=300.334)
                )
            service_id += 1
            services.append(service)

    with Session(engine) as session:
        session.add_all(services)
        session.commit()

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    gen_users()
    gen_drivers()
    gen_services()
    gen_trucks()
    gen_trips()
    gen_companies()
    gen_tickets()