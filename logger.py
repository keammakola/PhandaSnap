"""
logger.py
---------
Stateless logging utility that prints generation events to stdout.
Perfect for serverless environments like Vercel which capture logs.
"""

import datetime

def log_generation(store_name, language, scenario, audience, tone):
    """Prints a generation event to the console."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[LOG] {timestamp} | {store_name} | {language} | {scenario} | {audience} | {tone}")
