---
inclusion: always
---

# Uptime Monitor Project Guidelines

## Project Overview
This is a Python-based website uptime and performance monitoring tool designed to be beginner-friendly yet production-useful.

## Code Standards

### Python Style
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Keep functions focused and single-purpose
- Add docstrings to all classes and methods
- Use meaningful variable names

### Error Handling
- Always handle network exceptions gracefully
- Provide clear error messages in logs
- Never let the monitor crash - catch and log errors

### Performance
- Keep timeout values reasonable (5-15 seconds)
- Don't check too frequently (minimum 30 seconds recommended)
- Be mindful of rate limiting on monitored sites

## Project Structure
```
.
├── uptime_monitor.py      # Main monitoring script
├── example_config.py      # Configuration examples
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── uptime_log.csv        # Generated log file (gitignored)
└── .kiro/                # Kiro configuration
```

## Dependencies
- Only use `requests` as external dependency
- Keep standard library usage for everything else
- Avoid adding unnecessary dependencies

## Testing Approach
When testing changes:
1. Test with a single URL first
2. Use `continuous=False` for quick tests
3. Verify CSV logging works correctly
4. Test email alerts in a safe environment
5. Check error handling with invalid URLs

## Common Tasks

### Adding New Features
- Keep backward compatibility
- Update README.md with new features
- Add examples to example_config.py
- Test thoroughly before committing

### Modifying Email Alerts
- Always test with real SMTP settings
- Handle authentication errors gracefully
- Avoid sending duplicate alerts

### Performance Improvements
- Profile before optimizing
- Consider async requests for multiple URLs
- Keep logging efficient
