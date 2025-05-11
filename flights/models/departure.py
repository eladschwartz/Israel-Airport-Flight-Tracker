from flights.models.flight import Flight, FlightStatus
from datetime import datetime, time

class Departure(Flight):
   def __init__(self, airline: str, flight_number: str, from_city: str, 
                 terminal_num: int, scheduled_time: datetime, 
                 estimated_time: time, status: FlightStatus,
                 to_city: str, counter_area: str):
        super().__init__(airline, flight_number, from_city, terminal_num, 
                         scheduled_time, estimated_time, status)
        
        self.to_city = to_city
        self.counter_area = counter_area