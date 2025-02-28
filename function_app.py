import logging
import json
import requests
import os
from dotenv import load_dotenv
import azure.functions as func
from azure.iot.device import IoTHubDeviceClient, Message

# Load environment variables
load_dotenv()

# Azure and API credentials
API_KEY = os.getenv("IQAIR_API_KEY")
IOT_HUB_DEVICE_CONNECTION_STRING = os.getenv("IOT_HUB_DEVICE_CONNECTION_STRING")


# Verify required environment variables (for local development/testing)
if not API_KEY or not IOT_HUB_DEVICE_CONNECTION_STRING:
    raise ValueError("Missing environment variables. Check .env file")

app = func.FunctionApp()

@app.timer_trigger(schedule="0 */5 * * * *", 
                   arg_name="myTimer", 
                   run_on_startup=False,
                   use_monitor=False) 

def fetch_data(myTimer: func.TimerRequest) -> None:

    """Fetch AQ data and send to IoT Hub every 5 minutes."""
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function executed.')
    try:
        iqair_url = f"http://api.airvisual.com/v2/nearest_city?key={API_KEY}"
        response = requests.get(iqair_url)
        data = response.json()

        if response.status_code == 200:
            # Extract relevant data
            telemetry_data = {
                "city": data["data"]["city"],
                "state": data["data"]["state"],
                "country": data["data"]["country"],
                "coordinates": data["data"]["location"]["coordinates"],
                "timestamp": data["data"]["current"]["weather"]["ts"],
                "aqi_us": data["data"]["current"]["pollution"]["aqius"],
                "main_pollutant": data["data"]["current"]["pollution"]["mainus"],
                "temperature": data["data"]["current"]["weather"]["tp"],
                "humidity": data["data"]["current"]["weather"]["hu"],
            }
            
            message = Message(json.dumps(telemetry_data, indent=2))
            message.content_encoding = "utf-8"
            message.content_type = "application/json"

            client = IoTHubDeviceClient.create_from_connection_string(IOT_HUB_DEVICE_CONNECTION_STRING)
            print("Sending telemetry data to Azure IoT Hub...")
            client.send_message(message)

            logging.info("Telemetry data successfully sent to IoT Hub.")
            client.shutdown()
        else:
            logging.error(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
