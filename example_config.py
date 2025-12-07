"""
Example configuration file for the uptime monitor.
Copy this to your main script or use it as a reference.
"""

# Example 1: Basic monitoring with default settings
def basic_config():
    from uptime_monitor import UptimeMonitor
    
    urls = [
        'https://www.google.com',
        'https://www.github.com',
    ]
    
    monitor = UptimeMonitor(urls=urls)
    monitor.start_monitoring(continuous=True)


# Example 2: Fast monitoring with short intervals
def fast_monitoring():
    from uptime_monitor import UptimeMonitor
    
    urls = [
        'https://api.example.com/health',
        'https://app.example.com',
    ]
    
    monitor = UptimeMonitor(
        urls=urls,
        timeout=5,           # 5 second timeout
        check_interval=30    # Check every 30 seconds
    )
    monitor.start_monitoring(continuous=True)


# Example 3: Single check (no continuous monitoring)
def single_check():
    from uptime_monitor import UptimeMonitor
    
    urls = [
        'https://www.example.com',
    ]
    
    monitor = UptimeMonitor(urls=urls)
    monitor.start_monitoring(continuous=False)


# Example 4: Production monitoring with multiple sites
def production_monitoring():
    from uptime_monitor import UptimeMonitor
    
    urls = [
        'https://www.mycompany.com',
        'https://api.mycompany.com',
        'https://blog.mycompany.com',
        'https://shop.mycompany.com',
        'https://admin.mycompany.com',
    ]
    
    monitor = UptimeMonitor(
        urls=urls,
        timeout=15,          # 15 second timeout for slower sites
        check_interval=120   # Check every 2 minutes
    )
    monitor.start_monitoring(continuous=True)


if __name__ == '__main__':
    # Choose which configuration to run
    basic_config()
    # fast_monitoring()
    # single_check()
    # production_monitoring()
