# Website Uptime and Performance Monitor

A simple yet production-useful Python script to monitor website availability and performance.

## Features

✅ **Uptime Checking** - Monitors if websites return 200 OK status  
✅ **Performance Metrics** - Measures response time in milliseconds  
✅ **Configurable Timeout** - Set custom timeout for HTTP requests  
✅ **Multiple URLs** - Monitor multiple websites simultaneously  
✅ **Console Logging** - Real-time status updates with color coding  
✅ **CSV Logging** - Automatic logging to CSV file for analysis  
✅ **Email Alerts** - Get notified when websites go down  
✅ **Beginner-Friendly** - Clean code with comments and documentation

## Requirements

- Python 3.6 or higher
- `requests` library (only external dependency)

## Installation

1. Install Python from [python.org](https://www.python.org/downloads/)

2. Install the required library:
```bash
pip install requests
```

## Quick Start

1. Edit `uptime_monitor.py` and add your URLs:
```python
urls_to_monitor = [
    'https://www.yourwebsite.com',
    'https://www.anothersite.com',
]
```

2. Run the script:
```bash
python uptime_monitor.py
```

3. The script will:
   - Check all URLs every 60 seconds
   - Display status in the console
   - Log results to `uptime_log.csv`
   - Send email alerts if configured (optional)

## Configuration

### Basic Settings

Edit the `main()` function in `uptime_monitor.py`:

```python
monitor = UptimeMonitor(
    urls=urls_to_monitor,
    timeout=10,           # Request timeout in seconds
    check_interval=60     # Time between checks in seconds
)
```

### Email Alerts (Optional)

Set environment variables for email notifications:

**Windows (Command Prompt):**
```cmd
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587
set SENDER_EMAIL=your-email@gmail.com
set SENDER_PASSWORD=your-app-password
set RECIPIENT_EMAIL=alert-recipient@gmail.com
```

**Windows (PowerShell):**
```powershell
$env:SMTP_SERVER="smtp.gmail.com"
$env:SMTP_PORT="587"
$env:SENDER_EMAIL="your-email@gmail.com"
$env:SENDER_PASSWORD="your-app-password"
$env:RECIPIENT_EMAIL="alert-recipient@gmail.com"
```

**Linux/Mac:**
```bash
export SMTP_SERVER=smtp.gmail.com
export SMTP_PORT=587
export SENDER_EMAIL=your-email@gmail.com
export SENDER_PASSWORD=your-app-password
export RECIPIENT_EMAIL=alert-recipient@gmail.com
```

**Gmail Users:** Use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

## Usage Examples

### Single Check (Run Once)

```python
monitor.start_monitoring(continuous=False)
```

### Continuous Monitoring

```python
monitor.start_monitoring(continuous=True)
```

### Custom Configuration

```python
monitor = UptimeMonitor(
    urls=['https://example.com', 'https://test.com'],
    timeout=5,            # 5 second timeout
    check_interval=30     # Check every 30 seconds
)
```

## Output

### Console Output
```
======================================================================
Website Uptime Monitor Started
======================================================================
Monitoring 3 URL(s)
Check interval: 60 seconds
Timeout: 10 seconds
Email alerts: Enabled
Log file: uptime_log.csv
======================================================================

======================================================================
Starting check cycle at 2025-12-07 14:30:00
======================================================================
✓ [2025-12-07 14:30:00] https://www.google.com - UP - 145.23ms - Code: 200
✓ [2025-12-07 14:30:01] https://www.github.com - UP - 234.56ms - Code: 200
✗ [2025-12-07 14:30:02] https://www.python.org - DOWN - 10000ms - Code: TIMEOUT
  📧 Email alert sent for https://www.python.org

⏳ Next check in 60 seconds... (Press Ctrl+C to stop)
```

### CSV Log File (`uptime_log.csv`)
```csv
Timestamp,URL,Status,Response Time (ms),Status Code
2025-12-07 14:30:00,https://www.google.com,UP,145.23,200
2025-12-07 14:30:01,https://www.github.com,UP,234.56,200
2025-12-07 14:30:02,https://www.python.org,DOWN,10000,TIMEOUT
```

## Status Codes

- **UP** - Website returned 200 OK
- **DOWN** - Website returned non-200 status, timeout, or error
- **200** - Success
- **TIMEOUT** - Request exceeded timeout limit
- **ERROR** - Connection error or other exception

## Tips

1. **Run in Background** - Use `nohup` (Linux/Mac) or Task Scheduler (Windows)
2. **Analyze Logs** - Import CSV into Excel/Google Sheets for analysis
3. **Adjust Intervals** - Balance between responsiveness and server load
4. **Test First** - Run with `continuous=False` to test configuration
5. **Monitor Logs** - Check `uptime_log.csv` regularly for patterns

## Troubleshooting

**Email not sending?**
- Verify SMTP settings and credentials
- Check if 2FA is enabled (use App Password for Gmail)
- Ensure firewall allows SMTP connections

**Timeout errors?**
- Increase timeout value
- Check your internet connection
- Verify the URL is correct

**Import errors?**
- Install requests: `pip install requests`
- Verify Python version: `python --version`

## License

Free to use and modify for personal and commercial projects.

## Contributing

Feel free to enhance this script and share improvements!
