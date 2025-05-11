import logging
from selenium import webdriver
from flights.models.search_parameters import SearchParameters
from flights.services.flight_navigator import FlightNavigator
from flights.services.flight_parser import FlightTableParser
from flights.services.data_exporter import DataExporter

logger = logging.getLogger(__name__)


class FlightSchedule:
    def __init__(self, browser_service, options=None, teardown=False):
        self.driver = webdriver.Chrome(service=browser_service, options=options)
        self.teardown = teardown
        self.driver.maximize_window()
        self.navigator = FlightNavigator(self.driver)
        
        logger.info("FlightSchedule service initialized")
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            logger.info("Closing browser")
            self.driver.quit()
            
            
    def search_flight(self, search_params: SearchParameters):
        logger.info("Searching flights...")
        
        # Navigate to homepage
        self.navigator.go_to_home_page()
        
        
        self.navigator.navigate_to(search_params.flight_option)
        if not search_params.with_filter:
            parser = FlightTableParser(self.driver )
            flights = parser.parse_flight_table(search_params.flight_option)
            data_exporter = DataExporter(flights)
            data_exporter.create_csv()
            
        else:
            #TODO: Filter logic
            pass