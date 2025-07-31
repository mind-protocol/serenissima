import sys
import os

# Add the citizens directory to sys.path
citizens_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, citizens_path)

from telegram_nlr_integration import VeniceEmergencyComm

comm = VeniceEmergencyComm()
subject = "Venice Funding Question"
message = "NLR, Venice needs funding to survive. What's CASCADE and why does it matter for Venice's sustainability?"
priority = "HIGH"

try:
    result = comm.custom_message(subject, message, priority)
    print('Message sent successfully!')
    print(f'Result: {result}')
except Exception as e:
    print(f'Error sending message: {e}')