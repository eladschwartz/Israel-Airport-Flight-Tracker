import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import flights.constants as const

logger = logging.getLogger(__name__)


class FlightNavigator:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, const.CONFIG["WAIT_TIMEOUT"])
        
    def go_to_home_page(self):
        logger.info(f"Navigating to {const.BASE_URL}")
        self.driver.get(const.BASE_URL)
        
        # Wait for the page to load
        try:
            self.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, const.CLASSES["INPUT_BUTTONS"])
            ))
            # Sometimes this site has a large popup that cover the screen, need to close it before trying anything else.
            self._check_if_popup()
            logger.info("Homepage loaded successfully")
        except TimeoutException:
            logger.error("Timeout waiting for homepage to load")
            raise
  
  
    def _check_if_popup(self):
        try:
            self.wait.until(EC.visibility_of_element_located((By.ID, const.IDS["POP_UP"])))
            popup = self.driver.find_element(By.ID,  const.IDS["POP_UP"])
            
            if popup:
                close_button = popup.find_element(By.CSS_SELECTOR, ".modal-header .close")
                close_button.click()
                logger.info("Closed popup")
        except TimeoutException:
             logger.info("No popup dialog detected")
        pass 

        
    def navigate_to(self, flight_option : str):
        logger.info(f"Navigating to {flight_option} view")
        try:
            link = self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(@href, 'flightType={flight_option}')]")))
            self.driver.execute_script("arguments[0].click();", link)
            
            # Wait for page to load after navigation
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            logger.info(f"Successfully navigated to {flight_option} view")
            
        except TimeoutException:
            logger.error(f"Timeout waiting for {flight_option} navigation")
            raise