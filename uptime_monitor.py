#!/usr/bin/env python3
"""
Website Uptime and Performance Monitor
A simple yet production-useful tool to monitor website availability and performance.
"""

import requests
import csv
import smtplib
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


class UptimeMonitor:
    """Monitor website uptime and performance."""
    
    def __init__(self, urls, timeout=10, check_interval=60):
        """
        Initialize the uptime monitor.
        
        Args:
            urls (list): List of URLs to monitor
            timeout (int): Request timeout in seconds (default: 10)
            check_interval (int): Time between checks in seconds (default: 60)
        """
        self.urls = urls
        self.timeout = timeout
        self.check_interval = check_interval
        self.csv_file = 'uptime_log.csv'
        self.down_sites = {}  # Track which sites are down to avoid spam
        
        # Email configuration (set these via environment variables or modify directly)
        self.email_enabled = False
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', '')
        
        # Enable email if credentials are provided
        if self.sender_email and self.sender_password and self.recipient_email:
            self.email_enabled = True
        
        self._initialize_csv()
    
    def _initialize_csv(self):
        """Create CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'URL', 'Status', 'Response Time (ms)', 'Status Code'])
            print(f"✓ Created log file: {self.csv_file}")

    def check_website(self, url):
        """
        Check a single website's uptime and performance.
        
        Args:
            url (str): The URL to check
            
        Returns:
            dict: Status information including response time and status code
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=self.timeout)
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            status = 'UP' if response.status_code == 200 else 'DOWN'
            status_code = response.status_code
            
            return {
                'timestamp': timestamp,
                'url': url,
                'status': status,
                'response_time': round(response_time, 2),
                'status_code': status_code
            }
            
        except requests.exceptions.Timeout:
            return {
                'timestamp': timestamp,
                'url': url,
                'status': 'DOWN',
                'response_time': self.timeout * 1000,
                'status_code': 'TIMEOUT'
            }
        except requests.exceptions.RequestException as e:
            return {
                'timestamp': timestamp,
                'url': url,
                'status': 'DOWN',
                'response_time': 0,
                'status_code': f'ERROR: {str(e)[:50]}'
            }
    
    def log_to_console(self, result):
        """Print status to console with color coding."""
        status_symbol = '✓' if result['status'] == 'UP' else '✗'
        status_color = '\033[92m' if result['status'] == 'UP' else '\033[91m'
        reset_color = '\033[0m'
        
        print(f"{status_color}{status_symbol}{reset_color} [{result['timestamp']}] "
              f"{result['url']} - {result['status']} - "
              f"{result['response_time']}ms - Code: {result['status_code']}")
    
    def log_to_csv(self, result):
        """Append result to CSV log file."""
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                result['timestamp'],
                result['url'],
                result['status'],
                result['response_time'],
                result['status_code']
            ])

    def send_email_alert(self, result):
        """
        Send email alert when a website is down.
        
        Args:
            result (dict): The check result containing status information
        """
        if not self.email_enabled:
            return
        
        # Only send alert if site just went down (not already down)
        if result['url'] not in self.down_sites:
            try:
                msg = MIMEMultipart()
                msg['From'] = self.sender_email
                msg['To'] = self.recipient_email
                msg['Subject'] = f"🚨 ALERT: {result['url']} is DOWN"
                
                body = f"""
Website Downtime Alert

URL: {result['url']}
Status: {result['status']}
Status Code: {result['status_code']}
Response Time: {result['response_time']}ms
Timestamp: {result['timestamp']}

This is an automated alert from your uptime monitor.
                """
                
                msg.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
                
                print(f"  📧 Email alert sent for {result['url']}")
                self.down_sites[result['url']] = True
                
            except Exception as e:
                print(f"  ⚠ Failed to send email: {str(e)}")
        
        # Remove from down_sites if it's back up
        if result['status'] == 'UP' and result['url'] in self.down_sites:
            del self.down_sites[result['url']]
            print(f"  ✓ {result['url']} is back UP!")
    
    def run_check(self):
        """Run a single check cycle for all URLs."""
        print(f"\n{'='*70}")
        print(f"Starting check cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")
        
        for url in self.urls:
            result = self.check_website(url)
            self.log_to_console(result)
            self.log_to_csv(result)
            
            if result['status'] == 'DOWN':
                self.send_email_alert(result)
            elif result['status'] == 'UP' and result['url'] in self.down_sites:
                # Site recovered
                self.send_email_alert(result)
    
    def start_monitoring(self, continuous=True):
        """
        Start the monitoring process.
        
        Args:
            continuous (bool): If True, run continuously. If False, run once.
        """
        print("\n" + "="*70)
        print("Website Uptime Monitor Started")
        print("="*70)
        print(f"Monitoring {len(self.urls)} URL(s)")
        print(f"Check interval: {self.check_interval} seconds")
        print(f"Timeout: {self.timeout} seconds")
        print(f"Email alerts: {'Enabled' if self.email_enabled else 'Disabled'}")
        print(f"Log file: {self.csv_file}")
        print("="*70)
        
        if not continuous:
            self.run_check()
            print("\n✓ Single check completed")
            return
        
        try:
            while True:
                self.run_check()
                print(f"\n⏳ Next check in {self.check_interval} seconds... (Press Ctrl+C to stop)")
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("Monitor stopped by user")
            print("="*70)



def main():
    """Main function to configure and run the monitor."""
    
    # Configuration: Add your URLs here
    urls_to_monitor = [
        'https://www.google.com',
        'https://www.github.com',
        'https://www.python.org',
        'https://www.pyth8n.com'
        # Add more URLs as needed
    ]
    
    # Create monitor instance
    monitor = UptimeMonitor(
        urls=urls_to_monitor,
        timeout=10,           # Request timeout in seconds
        check_interval=60     # Check every 60 seconds
    )
    
    # Start monitoring
    # Set continuous=False for a single check, True for continuous monitoring
    monitor.start_monitoring(continuous=True)


if __name__ == '__main__':
    main()
