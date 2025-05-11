Israel Airport Authority Flight Tracker
A Python application that scrapes and exports real-time flight information from the Israel Airport Authority (IAA) website.
Features

Track both arrivals and departures at Israeli airports
Filter flights by city, country, airline, and date range
Export flight data to CSV format for further analysis
Supports both headless and visible browser automation
Cross-platform support (Windows, macOS, Linux)

Requirements

Python 3.10+
Chrome or Firefox browser
Required Python packages (see requirements.txt)


Create a virtual environment and activate it:
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

Install the required packages:
pip install -r requirements.txt


Usage
Run the application with the following command:
python -m flights.run
Follow the interactive prompts to:

Choose between arrival or departure flights
Select "All" to get all available flights or "Filter" to apply filters(Filtering is still at work)
If filtering, provide optional details such as city, country, airline, and date range

The application will:

Launch a web browser (Chrome by default)
Navigate to the IAA website
Access the flight information page
Extract flight data based on your criteria
Export the data to a flights.csv file in the current directory

Customization
Browser Options
By default, the application uses Chrome in visible mode. You can modify browser_factory.py to:

Use Firefox instead of Chrome
Run in headless mode for background operation
Configure additional browser options

Filtering Logic
The current implementation includes a placeholder for filtering logic. To extend the application with additional filters:

Update the search_flight method in flight_schedule.py
Implement the filtering logic based on the SearchParameters values

Troubleshooting
Common Issues

WebDriver not found: Ensure you have the latest Chrome or Firefox installed. The WebDriver manager should automatically download the appropriate driver version.
Connection errors: Check your internet connection and verify the IAA website is accessible.
Parsing errors: If the website structure changes, the selectors in flight_parser.py may need to be updated.

Logging
The application creates a flights_automation.log file with detailed logging information. Check this file for troubleshooting when errors occur.
