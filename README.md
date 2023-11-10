# sample-code

## NZTA MotoCheck Java Project

This Java project provides a simple interface to interact with NZTA MotoCheck services, allowing you to authenticate a client and fetch vehicle details using Java.

## Prerequisites

1. Java 1.8 installed in system , with environment path set
2. External JAR files: saaj-api-1.3.5.jar and saaj-impl-1.3.8.jar (already included in the project)

# Installation

1. Clone the repository:
   https://github.com/Alamance-IT-Solution/sample-code.git
2. Navigate to the project directory:
   cd java

# Compiling the Code

1. Before compiling, remove the existing .class files:
   rm \*.class
2. Compile the Java file:
   javac -cp .:saaj-api-1.3.5.jar:saaj-impl-1.3.8.jar -source 1.8 -target 1.8 SOAPClientNZTA.java

# Running the Code

1. Execute the compiled Java file:
   java -cp .:saaj-api-1.3.5.jar:saaj-impl-1.3.8.jar SOAPClientNZTA

##############################################################################################################################################################

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
