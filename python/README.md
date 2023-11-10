### NZTA MotoCheck Python Project

## Overview

This Python project provides a simple interface to interact with MotoCheck services, allowing you to authenticate a client and fetch vehicle details using the provided plate number.

## Requirements

Python 3.x
Dependencies listed in requirements.txt

# Setup

1. Clone the repository:
   https://github.com/Alamance-IT-Solution/sample-code.git
2. Navigate to the project directory:
   cd python
3. Install dependencies:
   pip install -r requirements.txt
4. Create a .env file in the project root and add the following environment variables:
   CDI_USERNAME=your_username
   CDI_PASSWORD=your_password
   CDI_GROUP_NAME=your_group_name
   CDI_LOCATION_ID=your_location_id
   CDI_ENDPOINT_ID=your_endpoint_id
   CDI_ACCOUNT_ID=your_account_id
   CDI_IP_ADDRESS=your_ip_address

   Replace your_username, your_password, etc., with your actual NZTA MotoCheck account details.

# Running the Project

1. Open a terminal and navigate to the project directory.

2. Run the authentication script:
   python authenticate_cdi_admin.py

   This script authenticates the client and displays the authentication response.

3. Run the script to fetch vehicle details using a plate number:
   python fetch_vehicle_by_platenumber.py YOUR_PLATE_NUMBER

   Replace YOUR_PLATE_NUMBER with the actual plate number you want to query.
