import logging
import os
import platform
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

logger = logging.getLogger(__name__)


class BrowserFactory:
    def prepare_browser(self, browser_type, detach=True, headless=False):
   
        browser_type = browser_type.lower()
        
        if browser_type == "chrome":
            return self._prepare_chrome_browser(detach, headless)
        elif browser_type == "firefox":
            return self._prepare_firefox_browser(detach)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
    
    
    def _prepare_chrome_browser(self, detach=True, headless=False):
        logger.info("Setting up Chrome browser")
        
        chrome_options = Options()
        is_apple_silicon = False
        if platform.system() == "Darwin" and platform.processor() == "arm":
            is_apple_silicon = True
            logger.info("Detected Apple Silicon (M1/M2) Mac")
            
        if detach:
            chrome_options.add_experimental_option("detach", True)
        
        
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        if headless:
        # For Apple Silicon, use a different approach for headless mode
            if is_apple_silicon:
                # Use the new headless mode that's more stable on Apple Silicon
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
                # These specific flags help with Apple Silicon compatibility
                chrome_options.add_argument("--use-gl=swiftshader")
                chrome_options.add_argument("--use-angle=swiftshader")
                # Disable sandbox for M1/M2
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
            else:
                # For non-Apple Silicon, use standard headless settings
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
            
      
            
        # Install and set up ChromeDriver
        try:
            driver_path = ChromeDriverManager().install()
            os.chmod(driver_path, 0o755) 
            chrome_service = ChromeService(driver_path)
            logger.info(f"ChromeDriver installed at: {driver_path}")
        except Exception as e:
            logger.error(f"Failed to set up ChromeDriver: {e}")
            raise
            
        logger.info("Chrome browser setup completed")
        return chrome_service, chrome_options
    
    
    def _prepare_firefox_browser(self, detach=True):
        logger.info("Setting up Firefox browser")
        
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--start-maximized")
        firefox_service = FirefoxService(GeckoDriverManager().install())
        
        logger.info("Firefox browser setup completed")
        return firefox_service, firefox_options