from datetime import datetime, time
from enum import Enum


class FlightStatus(Enum):
    CANCELED = "מבוטלת"
    LANDED = "נחתה"
    LANDING = "בנחיתה"
    FINAL = "סופי"
    DELAYED = "עיכוב"
    DEPARTED = "המריאה"
    
class Flight:
   def __init__(self, airline: str, flight_number: str, from_city: str, 
                 terminal_num: int, scheduled_time: datetime, 
                 estimated_time: time, status: FlightStatus):
        self.airline = airline
        self.flight_number = flight_number
        self.from_city = from_city
        self.terminal_num = terminal_num
        self.scheduled_time = scheduled_time
        self.estimated_time = estimated_time
        self.status = status
    
    



    
