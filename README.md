# 🛫 Israel Airport Authority Flight Tracker

A Python application that scrapes and exports real-time flight information from the Israel Airport Authority (IAA) website.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python" alt="Python 3.10+"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"/>
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge" alt="Platform: Windows | macOS | Linux"/>
</p>

## ✨ Features

- 🛬 Track both arrivals and departures at Israeli airports
- 🔍 Filter flights by city, country, airline, and date range
- 📊 Export flight data to CSV format for further analysis
- 🌐 Supports both headless and visible browser automation
- 💻 Cross-platform support (Windows, macOS, Linux)

## 📋 Requirements

- Python 3.10+
- Chrome or Firefox browser
- Required Python packages (see `requirements.txt`)

## 🚀 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/israel-flight-tracker.git
cd israel-flight-tracker
```

2. **Create and activate a virtual environment**

```bash
# Create virtual environment
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install the required packages**

```bash
pip install -r requirements.txt
```

## 📝 Usage

Run the application with the following command:

```bash
python -m flights.run
```

### 🔄 Interactive Workflow

1. Choose between arrival or departure flights
2. Select "All" to get all available flights or "Filter" to apply filters
3. If filtering, provide optional details such as:
   - City
   - Country
   - Airline
   - Date range

### 🔍 What the Application Does

- Launches a web browser (Chrome by default)
- Navigates to the IAA website
- Accesses the flight information page
- Extracts flight data based on your criteria
- Exports the data to a `flights.csv` file in the current directory

## ⚙️ Customization

### 🌐 Browser Options

By default, the application uses Chrome in visible mode. You can modify `browser_factory.py` to:

- Use Firefox instead of Chrome
- Run in headless mode for background operation
- Configure additional browser options

### 🔍 Filtering Logic

The current implementation includes a placeholder for filtering logic. To extend the application with additional filters:

- Update the `search_flight` method in `flight_schedule.py`
- Implement the filtering logic based on the `SearchParameters` values

## 🔧 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| WebDriver not found | Ensure you have the latest Chrome or Firefox installed. The WebDriver manager should automatically download the appropriate driver version. |
| Connection errors | Check your internet connection and verify the IAA website is accessible. |
| Parsing errors | If the website structure changes, the selectors in `flight_parser.py` may need to be updated. |

### 📝 Logging

The application creates a `flights_automation.log` file with detailed logging information. Check this file for troubleshooting when errors occur.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

<p align="center">Made with ❤️ for travelers and data enthusiasts</p>
