
import requests
import json
import xml.etree.ElementTree as ET
from requests.exceptions import RequestException
import os
from dotenv import load_dotenv
load_dotenv()

class CDIAuthentication:
    def __init__(self):
        self.url = "https://cdtpt.ltweb.net.nz/CDTPT/WebServices/Security/AccessControl.asmx"
        self.headers = {
            'Host': 'cdtpt.ltweb.net.nz',
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': '"http://schemas.cdi.ltsa.govt.nz/Security/AccessControl/AuthenticateClient"'
        }
        self.payload = f'''<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Header>
                    <Security
                        xmlns="http://www.docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                        <UserNameToken>
                            <UserName>{os.getenv('CDI_USERNAME')}</UserName>
                            <Password>{os.getenv('CDI_PASSWORD')}</Password>
                        </UserNameToken>
                    </Security>
                </soap:Header>
                <soap:Body>
                    <AuthenticateClient xmlns="http://schemas.cdi.ltsa.govt.nz/Security/AccessControl/">
                        <AuthenticateClientRequest xmlns="http://localhost/Schema/SecurityService">
                            <RequestBody />
                        </AuthenticateClientRequest>
                    </AuthenticateClient>
                </soap:Body>
            </soap:Envelope>
        '''
    def authenticate(self):
        try:
            response = requests.post(self.url, headers=self.headers, data=self.payload)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            namespace = {"soap": "http://schemas.xmlsoap.org/soap/envelope/"}
            result = root.find(".//soap:Body", namespaces=namespace)

            response_data = {
                "response": ET.tostring(result, encoding="unicode", method="xml")
            }
            json_response = json.dumps(response_data)
            return True, json_response

        except RequestException as e:
            return False, "Request failed: " + str(e)

        except ET.ParseError as e:
            return False, "XML parsing error: " + str(e)

        except Exception as e:
            return False, "An error occurred: " + str(e)


class CDIVehicleFetcher:
    def __init__(self, cdi_auth: CDIAuthentication):
        self.cdi_auth = cdi_auth

    def fetch_vehicle_by_plate_number(self, plate_number):
        try:
            if plate_number is None:
                return {'success': False, 'message': 'Please provide a valid Plate number in the request.'}

            cdi_user_authentication_details = self.cdi_auth.authenticate()

            if cdi_user_authentication_details[0]:
                authentication_details = cdi_user_authentication_details[1]
                
                cdi_token_id = authentication_details.CDIToken.Id
                cdi_token_value = authentication_details.CDIToken.TokenValue
                cdi_session_token = authentication_details.CDISessionToken
                cdi_function_name = ""

                url = "https://cdtpt.ltweb.net.nz/CDTPT/WebServices/Vehicle.asmx"
                headers = {
                    'Host': 'cdtpt.ltweb.net.nz',
                    'Content-Type': 'text/xml; charset=utf-8',
                    'SOAPAction': '"http://schemas.cdi.ltsa.govt.nz/Vehicle/InquireVehicleDetails"'
                }

                xml_payload = f'''
                <?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
                                xmlns:xsd="http://www.w3.org/2001/XMLSchema" 
                                xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Header>
                        <UserNameToken>
                                <UserName>{os.getenv('CDI_USERNAME')}</UserName>
                                <GroupName>{os.getenv('CDI_GROUP_NAME')}</GroupName>
                                <Password>{os.getenv('CDI_PASSWORD')}</Password>
                                <LocationID xmlns="http://schemas.cdi.ltsa.govt.nz/SecurityService.xsd">{os.getenv('CDI_LOCATION_ID')}</LocationID>
                                <EndPointID xmlns="http://schemas.cdi.ltsa.govt.nz/SecurityService.xsd">{os.getenv('CDI_ENDPOINT_ID')}</EndPointID>
                        </UserNameToken>
                        <CDIToken Id={cdi_token_id} xmlns="http://schemas.cdi.ltsa.govt.nz/SecurityService">
                                <TokenValue>{cdi_token_value}</TokenValue>
                                <GroupName>{os.getenv('CDI_GROUP_NAME')}</GroupName>
                                <FunctionName>{cdi_function_name}</FunctionName>
                                <UserName>{os.getenv('CDI_USERNAME')}</UserName>
                        </CDIToken>
                        <CDISessionToken xmlns="http://schemas.cdi.ltsa.govt.nz/SecurityService">{cdi_session_token}</CDISessionToken>
                        <SecurityTokenReference=""/>
                        <ClientIdentifiers xmlns="http://schemas.cdi.ltsa.govt.nz/SecurityService">
                                <UserName>{os.getenv('CDI_USERNAME')}</UserName>
                                <AccountId AccountType="MotoCheck">{os.getenv('CDI_ACCOUNT_ID')}</AccountId>
                                <IPAddress>{os.getenv('CDI_IP_ADDRESS')}</IPAddress>
                        </ClientIdentifiers>
                    </soap:Header>
                    <soap:Body>
                        <InquireVehicleDetails xmlns="http://schemas.cdi.ltsa.govt.nz/Vehicle/InquireVehicleDetails/">
                            <InquireVehicleDetailsRequest xmlns="https://localhost/Schema/VehicleService/">
                                <RequestBody>
                                    <Vehicle>
                                        <PlateNumber>{plate_number}</PlateNumber>
                                    </Vehicle>
                                </RequestBody>
                            </InquireVehicleDetailsRequest>
                        </InquireVehicleDetails>
                    </soap:Body>
                </soap:Envelope>
                </xml>
                '''
                
                response = requests.post(
                url, headers=headers, data=xml_payload)
                response.raise_for_status()
                root = ET.fromstring(response.content)
                namespace = {
                    "soap": "http://schemas.xmlsoap.org/soap/envelope/"}
                result = root.find(".//soap:Body", namespaces=namespace)

                response_data = {
                    "response": ET.tostring(result, encoding="unicode", method="xml")
                }
                json_response = json.dumps(response_data)
                return {'success': True, 'data': json_response}
            else:
                return {'success': False, 'message': cdi_user_authentication_details[1]}

        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': 'Request failed: ' + str(e)}

        except ET.ParseError as e:
            return {'success': False, 'error': 'XML parsing error: ' + str(e)}

        except Exception as e:
            return {'success': False, 'error': 'An error occurred: ' + str(e)}


if __name__ == "__main__":
    cdi_auth = CDIAuthentication()
    cdi_vehicle_fetcher = CDIVehicleFetcher(cdi_auth)

    plate_number = "YOUR_PLATE_NUMBER"
    result = cdi_vehicle_fetcher.fetch_vehicle_by_plate_number(plate_number)

    print(result)