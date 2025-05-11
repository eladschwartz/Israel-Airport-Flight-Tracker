import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from flights.models.flight import Flight, FlightStatus
from flights.models.arrival import Arrival
from flights.models.departure import Departure
import flights.constants as const


class FlightTableParser:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)
        self.wait = WebDriverWait(self.driver, const.CONFIG["WAIT_TIMEOUT"])
    
    def parse_flight_table(self, flight_type: str) -> list[Flight]:
        self.logger.info(f"Parsing {flight_type} flight table")
        
        flight_type_str = "flight_board-arrivel_table" if flight_type == 'arrival' else 'flight_board-departures_table'
        
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, flight_type_str)))
            flights_talbe = self.driver.find_element(By.ID, flight_type_str)
            flight_rows = flights_talbe.find_elements(By.TAG_NAME, "tr")[1:]
            self.logger.info(f"Found {len(flight_rows)} flights in the table")
            
            flights = []
            for row in flight_rows:
                try:
                    if flight_type.lower() == 'arrival':
                        flight = self._create_arrival(row)
                    else:
                        flight = self._create_departure(row)
                    
                    if flight:
                        flights.append(flight)
                except Exception as e:
                    self.logger.error(f"Error parsing flight row: {e}")
            
            return flights
        except Exception as e:
              self.logger.error(f"Error find element: {e}")
        
    
    
    def _create_flight(self, row: WebElement) -> Flight | None:
        try:
            airline = self._extract_text(row, "td-airline")
            flight_number = self._extract_text(row, "td-flight")
            from_city = self._extract_text(row, "td-city")
            terminal_str = self._extract_text(row, "td-terminal")
            terminal = int(terminal_str) if terminal_str and terminal_str.isdigit() else None     
            
            # Extract scheduled time
            scheduled_time = self._extract_scheduled_datetime(row)
            # Extract estimated time
            estimated_time_str = self._extract_time(row, "td-updatedTime")
            estimated_time = datetime.strptime(estimated_time_str, '%H:%M').time() if estimated_time_str else None
            
            # Extract status
            status_text = self._extract_status(row)
            status = self._map_status(status_text)
    
            return Flight(
                    airline=airline,
                    flight_number=flight_number,
                    from_city=from_city,
                    terminal_num=terminal,
                    scheduled_time=scheduled_time,
                    estimated_time=estimated_time,
                    status=status
                )
        except Exception as e: 
            self.logger.error(f"Failed to create Arrival object: {e}")
            return None
    
    def _create_arrival(self, row: WebElement) -> Arrival | None:
        try:
            flight = self._create_flight(row)
    
            # Create and return Arrival object
            return Arrival(
                airline=flight.airline,
                flight_number=flight.flight_number,
                from_city=flight.from_city,
                terminal_num=flight.terminal_num,
                scheduled_time=flight.scheduled_time,
                estimated_time=flight.estimated_time,
                status=flight.status
            )
        except Exception as e:
            self.logger.error(f"Failed to create Arrival object: {e}")
            return None
    
    def _create_departure(self, row: WebElement) -> Departure | None:
        try:
            flight = self._create_flight(row)
            
            from_city = "TLV"
            to_city = self._extract_text(row, "td-city")
            
            # Extract counter area
            counter_area = self._extract_text(row, "td-counter")
            
            # Create and return Departure object
            return Departure(
                airline=flight.airline,
                flight_number=flight.flight_number,
                from_city=from_city,
                terminal_num=flight.terminal_num,
                scheduled_time=flight.scheduled_time,
                estimated_time=flight.estimated_time,
                status=flight.status,
                to_city=to_city,
                counter_area=counter_area
            )
        except Exception as e:
            self.logger.error(f"Failed to create Departure object: {e}")
            return None
    
    def _extract_text(self, element: WebElement, class_name: str) -> str:
        try:
            div = element.find_element(By.CLASS_NAME, class_name)
            return div.text.strip()
        except NoSuchElementException:
            return ""
        except Exception as e:
            self.logger.error(f"Error extracting text from {class_name}: {e}")
            return ""
    
    def _extract_time(self, element: WebElement, class_name: str) -> str:
        try:
            div = element.find_element(By.CLASS_NAME, class_name)
            time_element = div.find_element(By.TAG_NAME, "time")
            return time_element.text.strip()
        except NoSuchElementException:
            return ""
        except Exception as e:
            self.logger.error(f"Error extracting time from {class_name}: {e}")
            return ""
    
    def _extract_scheduled_datetime(self, row: WebElement) -> datetime | None:
        try:
            # Find the scheduled time div
            scheduled_div = row.find_element(By.CLASS_NAME, "td-scheduledTime")
            
            # Find the time element
            time_element = scheduled_div.find_element(By.TAG_NAME, "time")
            
            # Extract the time
            time_str = ""
            try:
                strong = time_element.find_element(By.TAG_NAME, "strong")
                time_str = strong.text.strip()
            except NoSuchElementException:
                time_str = time_element.text.strip()
            
            # Extract the date
            date_str = ""
            try:
                date_div = time_element.find_element(By.TAG_NAME, "div")
                date_str = date_div.text.strip()
            except NoSuchElementException:
                # If no date div, use current date
                date_str = datetime.now().strftime('%d/%m')
            
            # Parse date and time
            if time_str and date_str:
                day, month = map(int, date_str.split('/'))
                year = datetime.now().year
                hour, minute = map(int, time_str.split(':'))
                
                return datetime(year, month, day, hour, minute)
            return None
        except Exception as e:
            self.logger.error(f"Error extracting scheduled datetime: {e}")
            return None
    
    def _extract_status(self, row: WebElement) -> str:
        try:
            status_cell = row.find_element(By.CLASS_NAME, "row-status")
            status_div = status_cell.find_element(By.CSS_SELECTOR, "div[data-status]")
            return status_div.text.strip()
        except NoSuchElementException:
            pass
            
        return ""
      
    
    def _map_status(self, status_text: str) -> FlightStatus:
        status_mapping = {
            'מבוטלת': FlightStatus.CANCELED,
            'נחתה': FlightStatus.LANDED,
            'בנחיתה': FlightStatus.LANDING,
            'המריאה': FlightStatus.DEPARTED,
            'סופי': FlightStatus.FINAL,
            'עיכוב': FlightStatus.DELAYED 
        }
        
        # Default to FINAL if no mapping found
        return status_mapping.get(status_text, FlightStatus.FINAL)