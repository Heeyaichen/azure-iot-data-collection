# Air Quality Telemetry Ingestion with Azure Services
This solution ingests real-time air quality data from an external API, sends it to Azure IoT Hub using Azure Functions SDK for Python, process it with Azure Stream Analytics and store it in Cosmos DB—all while keeping things serverless and scalable.

---

![Image](https://github.com/user-attachments/assets/7cc60c9d-68d2-4fd6-a225-e9af069c20cf)
---

## Table of Contents

  - [Overview](#overview)
  - [Architecture](#architecture)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
    - [Function App Creation](#function-app-creation)
    - [Azure IoT Hub \& Device](#azure-iot-hub--device)
    - [Environment Variables](#environment-variables)
    - [Cosmos DB Configuration](#cosmos-db-configuration)
    - [Azure Stream Analytics Job](#azure-stream-analytics-job)
  - [Deployment](#deployment)
  - [Monitoring](#monitoring)
  - [Troubleshooting](#troubleshooting)
  - [Resources \& Links](#resources--links)
  - [Contributing](#contributing)
  - [Future Extensions](#future-extensions)
    - [Power BI for Data Visualization](#power-bi-for-data-visualization)
    - [Machine Learning for Predictive Analysis](#machine-learning-for-predictive-analysis)
  - [License](#license)

---

## Overview

This project demonstrates how to:
- **Fetch Air Quality Data:** Use a Python timer-triggered Azure Function to query the IQAir API for the nearest city’s air quality.
- **Ingest Telemetry:** Send the fetched JSON data to an Azure IoT Hub.
- **Process & Store Data:** Route IoT Hub messages through a custom route and process them with Azure Stream Analytics, then store the results in an Azure Cosmos DB container.

---

## Architecture

The solution is composed of the following Azure services:

- **Azure Functions:** Runs a Python timer-triggered function (`fetch_aq_data.py`) that periodically fetches data every five minutes from the IQAir API.
- **Azure IoT Hub:** Receives the telemetry data. Custom message routing is set up using built-in endpoints (events).
- **IoT Explorer:** Used for managing the IoT device and validating/testing the telemetry.
- **Azure Cosmos DB:** Stores processed telemetry data in a container with `/city` as the partition key.
- **Azure Stream Analytics:** Processes data from IoT Hub as input and routes the output to Cosmos DB.

---

## Prerequisites

- An [Azure Subscription](https://azure.microsoft.com/free/)
- [Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local) installed
- [Python 3.8+](https://www.python.org/downloads/)
- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
- An IQAir API Key (grab it from the [IQAir Air Pollution API](https://www.iqair.com/in-en/?srsltid=AfmBOop_db8XRZ0lni7_4f5THX6oSTEW9tMN-PDAxLW7mL5FF7074kbr))
- [Azure IoT Explorer](https://learn.microsoft.com/en-us/azure/iot/howto-use-iot-explorer#install-azure-iot-explorer)

---

## Setup

### Function App Creation

1. **Create a Function App:**
   - Head over to the [Azure Portal](https://portal.azure.com) and create a new Function App.
   - Choose Python as your runtime.
   - For more info, check out the [Azure Functions Documentation](https://docs.microsoft.com/azure/azure-functions/).

### Azure IoT Hub & Device

2. **Create an IoT Hub:**
   - In the Azure Portal, create a new IoT Hub.
   - Add an IoT device to your hub
   - Add a custom route in IoT Hub message routing of endpoint type "built-in-endpoints" with the endpoint name being "events" by default.
   - More details here: [Azure IoT Hub Documentation](https://docs.microsoft.com/azure/iot-hub/).

### Environment Variables

3. **Configure App Settings:**
   - In your Function App’s configuration, add the following environment variables:
     - `AIRVISUAL_API_KEY`: Your IQAir API key.
     - `IOT_HUB_DEVICE_CONNECTION_STRING`: The connection string for your IoT device.
   - Learn how to manage these settings [here](https://docs.microsoft.com/azure/azure-functions/functions-how-to-use-azure-function-app-settings).

### Cosmos DB Configuration

4. **Set Up Cosmos DB:**
   - Create a Cosmos DB account.
   - Add a new container with:
     - **Database ID:** `AirQualityDB`
     - **Container ID:** `TelemetryData`
     - **Partition Key:** `/city`
   - More details can be found in the [Cosmos DB Documentation](https://docs.microsoft.com/azure/cosmos-db/introduction).

### Azure Stream Analytics Job

5. **Configure Stream Analytics:**
   - Set up an Azure Stream Analytics job:
     - **Input:** IoT Hub
     - **Output:** Cosmos DB
   - Refer to the [Stream Analytics Documentation](https://docs.microsoft.com/azure/stream-analytics/) for step-by-step instructions.

---

## Deployment

1. **Deploy the Azure Function:**
   - Use the following command to deploy your function:
     ```bash
     func azure functionapp publish <function-app-name>
     ```
   - After deployment, your `fetch_aq_data.py` function should appear in the Function App blade in the Azure Portal.
   - More on deploying functions [here](https://docs.microsoft.com/azure/azure-functions/functions-deployment-technologies).

2. **Configure IoT Explorer for verification:**
   - Add a new IoT Hub connection using the `iothubowner` shared access policy primary connection string.
   - Start sending telemetry.
   - Confirm that JSON data is being retrieved successfully.
   - Check out [IoT Explorer Documentation](https://docs.microsoft.com/azure/iot-hub/iot-hub-device-explorer) for more info.

3. **Stream Analytics Job:**
   - Configure Query in Job Topology
   - Test Query and Start Job
   - For more information - [Create Stream Analytics Job](https://learn.microsoft.com/en-us/azure/stream-analytics/stream-analytics-quick-create-portal).

---

## Monitoring

- **Function App:**  
  - Execution logs, performance metrics, and failures.  
  - Use the Azure Portal’s built-in monitoring and [Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview) for detailed telemetry.

- **IoT Hub:**  
  - Device-to-cloud message traffic, connection statuses, and errors.  
  - Check IoT Hub metrics through the Azure Portal or via the [IoT Hub Metrics Dashboard](https://docs.microsoft.com/azure/iot-hub/iot-hub-metrics).

- **Stream Analytics:**  
  - Streaming Unit (SU) utilization and query performance.  
  - Monitor through the Azure Portal; configure alerts for high SU consumption to avoid query failures.

- **Cosmos DB:**  
  - Request Unit (RU) consumption, latency, and throughput.  
  - Use the Cosmos DB metrics in the Azure Portal to track RU usage and set alerts for spikes.

For a more comprehensive monitoring solution, consider integrating these services with [Azure Monitor](https://docs.microsoft.com/azure/azure-monitor/overview) and setting up custom alerts. This proactive approach helps you catch issues early and maintain optimal performance.

---

## Troubleshooting

- **No Telemetry Data?**
  - Verify your API key and IoT Hub device connection string in Function App Environment Variables App Settings.
  - Inspect Function App logs for errors.
- **Cosmos DB Issues?**
  - Ensure your container’s partition key is set to `/city`.
  - Review output configurations, job status & query in your Stream Analytics job.

---

## Resources & Links

- [Azure Functions Documentation](https://docs.microsoft.com/azure/azure-functions/)
- [Azure IoT Hub Documentation](https://docs.microsoft.com/azure/iot-hub/)
- [Azure Cosmos DB Documentation](https://docs.microsoft.com/azure/cosmos-db/introduction)
- [Azure Stream Analytics Documentation](https://docs.microsoft.com/azure/stream-analytics/)
- [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli)
- [IQAir API Documentation](https://api-docs.iqair.com/)

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

---

## Future Extensions

### Power BI for Data Visualization
Integrate [Power BI](https://docs.microsoft.com/power-bi/) to build interactive dashboards that visualize real-time air quality trends. This lets you monitor pollution levels, spot anomalies, and get actionable insights at a glance. Imagine tracking air quality like checking your Insta feed—only way more useful!

### Machine Learning for Predictive Analysis
Leverage [Azure Machine Learning](https://docs.microsoft.com/azure/machine-learning/) to train models on your historical telemetry data. With predictive analytics, you could forecast future air quality trends—think of it as your very own pollution weather channel. This not only adds a cool, futuristic twist but also paves the way for proactive interventions in urban planning or public health.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
