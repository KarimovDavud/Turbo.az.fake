# paypal_config.py
import paypalrestsdk
import logging

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET"
})

logging.basicConfig(level=logging.INFO)
