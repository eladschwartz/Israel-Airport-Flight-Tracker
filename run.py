import logging
from flights.utils.browser_factory import BrowserFactory
from flights.utils.input_collector import UserInputCollector
from flights.services.flight_schedule import FlightSchedule
from selenium.common.exceptions import WebDriverException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("flights_automation.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    try:
        # Get user input for search parameters
        collector = UserInputCollector()
        search_params = collector.collect_search_parameters()
        
        # Setup browser using the factory
        browser_factory = BrowserFactory()
        browser_service, browser_options = browser_factory.prepare_browser("chrome")
        
        # Initialize the flights automation and perform search
        with FlightSchedule(browser_service, browser_options) as flight_schedule:
            flight_schedule.search_flight(search_params)
            
    except WebDriverException as e:
        logger.error(f"WebDriver error: {e}")
        print("\nBrowser automation failed. Please try again.")
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        print(f"\nInput validation failed: {e}")
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
        print("\nProcess interrupted. Exiting...")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()