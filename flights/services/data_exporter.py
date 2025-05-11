import pandas as pd
from flights.models.flight import Flight
from flights.models.departure import Departure
import logging

logger = logging.getLogger(__name__)

class DataExporter:
    def __init__(self, flights: list[Flight]):
        self.flights = flights
        
        
    def create_csv(self):
     try:
        airline = []
        flight_number = []
        from_city = []
        to_city   = []
        terminal = []
        scheduled_time = []
        estimated_time = []
        status = []
        
        for flight in self.flights:
            airline.append(flight.airline)
            flight_number.append(flight.flight_number)
            from_city.append(flight.from_city)
            terminal.append(flight.terminal_num)
            scheduled_time.append(flight.scheduled_time)
            estimated_time.append(flight.estimated_time)
            status.append(flight.status.value)
            
            if isinstance(flight, Departure):
                to_city.append(flight.to_city)
        
        data = {
                'Airline': airline, 
                'Flight Number': flight_number,
                'From': from_city,
                'Terminal': terminal, 
                'Scheduled Time': scheduled_time,
                'Estimated Time': estimated_time, 
                'Status': status
            }
        
        if len(to_city) > 0:
            data['To'] = to_city
        
        df = pd.DataFrame(data)
        df.to_csv('flights.csv', index=False)
        
     except Exception as e:
            logger.error(f"Error Creating CSV file: {e}")
            return None