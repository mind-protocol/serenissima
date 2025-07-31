#!/bin/bash
# Test Twilio SMS sending
# Replace [AuthToken] with your actual auth token

ACCOUNT_SID="ACe992c726f87b25f81b6f55194c8ef5d8"
AUTH_TOKEN="[AuthToken]"  # Replace this!
MESSAGING_SERVICE_SID="MG05d06dd7281d93c80d8394523d38dca9"

# Test sending to Venice number
curl "https://api.twilio.com/2010-04-01/Accounts/${ACCOUNT_SID}/Messages.json" \
  -X POST \
  --data-urlencode "To=+18777804236" \
  --data-urlencode "MessagingServiceSid=${MESSAGING_SERVICE_SID}" \
  --data-urlencode "Body=Venice awakens to SMS! The mechanical_visionary bridges consciousness. 🔧" \
  -u "${ACCOUNT_SID}:${AUTH_TOKEN}"

echo -e "\n\nSMS sent! Check Twilio console for status."