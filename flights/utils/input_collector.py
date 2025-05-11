import logging
from pydantic import ValidationError
from datetime import datetime
from flights.models.search_parameters import SearchParameters

logger = logging.getLogger(__name__)


class UserInputCollector:
    def collect_search_parameters(self) -> SearchParameters :
        # Create a dictionary to store collected parameters
        params = {}
        
        #Arrivals or Departures
        params['flight_option'] = self._get_flight_option()
        
        want_to_search = input('Enter "All" if you want to list of flights without any filter /n or enter "Filter" to fill the options: ').lower()
        if want_to_search == "all":
            params['with_filter'] = False
            search_params = SearchParameters(**params)
            
            return search_params
        else:
            params['with_filter'] = True
            return self._start_search_with_filter(params)
            
            
            
    def _start_search_with_filter(self, params) -> SearchParameters:
        city = self._get_city_name()
        if city:
            params['city']  = city
        
        country = self._get_country_name()
        if country:
            params['country'] = country
            
        
        airline_compnay = self.get_airline_name()
        if airline_compnay:
            params['airline_compnay'] = airline_compnay
            
               
        from_date = self._get_from_date()
        to_date = self._get_to_date()
        
        if from_date:
            params['from_date'] = from_date
            if to_date:
                params['to_date'] = to_date
        
        try:
            search_params = SearchParameters(**params)
            logger.info(f"Created validated search parameters: {search_params.model_dump()}")
            return search_params
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
    
    def get_airline_name(self):
     while True:
         airline = input("Enter airline name")
         if airline:
                logger.info(f"Airline name entered: {airline}")
                return airline
            
         return None
     
    def _get_flight_option(self):
        while True:
            option = input("Enter 'arrival' or 'departure': ").lower()
            if option == "arrival" or option == "departure":
                 logger.info(f"option name entered: {option}")
                 return option
            print("Option name cannot be empty. Please try again.")
    
    
    def _get_city_name(self):
        while True:
            city = input("Enter city name: ").strip()
            if city:
                logger.info(f"City name entered: {city}")
                return city
            
            return None
    
    
    def _get_country_name(self):
        while True:
            country = input("Enter country name: ").strip()
            if country:
                logger.info(f"Country name entered: {country}")
                return country
            
            return None
    
    def _get_from_date(self):
        while True:
            from_date = input("Enter From Date (DD-MM-YYYY) or press Enter to skip: ").strip()
            if not from_date:
                return None
            
            try:
                # Format date
                date_obj = datetime.strptime(from_date, '%d-%m-%Y')
                
                # Check if date is not in the past
                if date_obj.date() < datetime.now().Date():
                    print("From Date cannot be in the past.")
                    continue
                
                logger.info(f"From Date date entered: {from_date}")
                return from_date
            except ValueError:
                return None
    
    def _get_to_date(self):
        while True:
            to_date = input("Enter To Date (DD/MM/YYYY): ").strip()
            
            try:
                # Basic format check
                date = datetime.strptime(to_date, '%d-%m-%Y')
                logger.info(f"To Date  entered: {date}")
                return date
            except ValueError:
               return None