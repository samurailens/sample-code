import java.util.Iterator;
import java.util.Map;

import javax.xml.namespace.QName;
import javax.xml.soap.*;

public class SOAPClientNZTA {
	
	
	/**
	 * Kept all the strings and variables outside the code, 
	 * so it's easier to refactor for your own application.
	 * 
	 * Please note that this code may fail if you have a 
	 * corporate proxy in place, how to pass requests through 
	 * a proxy is outside the scope of this example.
	 * 
	 * You must also change the usernameValue and passwordValue 
	 * fields to be those given to you by NZTA after registration
	 */
	public final static String APIns 			= "cam";
	public final static String APInsURI			= "https://infoconnect.highwayinfo.govt.nz/schemas/camera2";
	public final static String soapEndpointUrl 	= "https://infoconnect1.highwayinfo.govt.nz:443/ic/jbi/TrafficCameras2/SOAP/FeedService/";
	public final static String soapAction 		= "getCamerasRequest";
	
	public final static String contentTypeValue = "Content-Type";
	public final static String contentTypeKey 	= "text/xml";
	
	public final static String usernameKey 		= "Username";
	public final static String usernameValue 	= "YOUR USERNAME";
	
	public final static String passwordKey 		= "Password";
	public final static String passwordValue 	= "YOUR PASSWORD";
	
	public final static String securitySchema 	= "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd";
	public final static String securityPrefix 	= "wsse";
	
	public final static String passwordType		= "Type";
	public final static String passwordURI		= "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText";

	public final static String usernameToken 	= "UsernameToken";
	public final static String security 		= "Security";
	
	public final static String cameraPrefix		= "tns:"; 
	public final static String[] myAttributes	= {"imageUrl", "id", "region"};
	
	
    public static void main(String[] args) {    	
    	callSoapWebService(soapEndpointUrl, soapAction);
    }
    
    private static void callSoapWebService(String soapEndpointUrl, String soapAction) {
        try {
            // Create SOAP Connection
            SOAPConnectionFactory 	soapConnectionFactory 	= SOAPConnectionFactory.newInstance();
            SOAPConnection 			soapConnection			= soapConnectionFactory.createConnection();
            SOAPMessage 			message 				= createSOAPRequest();
            SOAPMessage 			soapResponse 			= soapConnection.call(message, soapEndpointUrl);
            
            getMyData(soapResponse);
            soapConnection.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    
    /**
     * sample method for how to get individual camera 
     * data and filter out stuff you may not want
     * 
     * @param soapResponse what we got back from NZTA
     * @throws SOAPException
     */
    private static void getMyData(SOAPMessage soapResponse) throws SOAPException {
    	
    	SOAPBody body					 = soapResponse.getSOAPBody();
    	Iterator bodyElementsIterator 	 = body.getChildElements();
    	SOAPElement cameraResponse 		 = (SOAPElement) bodyElementsIterator.next();
    	Iterator cameraIterator 		 = cameraResponse.getChildElements();
    	SOAPElement cameraElement 		 = null;
    	
    	System.err.println(cameraResponse);
    	
    	//iterate through every camera in the response
    	while(cameraIterator.hasNext()){
    		cameraElement = (SOAPElement) cameraIterator.next();
    		
    		//iterate through all the fields of a camera
    		Iterator cameraFieldsIterator	= cameraElement.getChildElements();
    		while(cameraFieldsIterator.hasNext()){
    			SOAPElement cameraField = (SOAPElement) cameraFieldsIterator.next();
    			
    			//iterate through all the fields we care about in this example
    			for (int i = 0; i < myAttributes.length; i++) {
					String myField = myAttributes[i];
					
					//is the current field I'm looking at one of the ones I want
					if((cameraPrefix + myField).equals(cameraField.getNodeName())){
						System.out.println(cameraField.getValue());
					}
				}
    		}
    	}
	}

	private static SOAPMessage createSOAPRequest() throws Exception {
        MessageFactory 	messageFactory 	= MessageFactory.newInstance();
        SOAPMessage 	soapMessage 	= messageFactory.createMessage();

        createSoapEnvelope(soapMessage);

        
        MimeHeaders headers = soapMessage.getMimeHeaders();
        headers.addHeader(contentTypeKey, 	contentTypeValue);
        
        /*if you are using the REST API you just send HTTP
         *  and don't need to worry about the body of the request,
         *  so you can just put the credentials into the header */ 
        
        //headers.addHeader(usernameKey, 		usernameValue);
        //headers.addHeader(passwordKey, 		passwordValue);

        
        soapMessage.saveChanges();

        System.out.println("Request SOAP Message:");
        soapMessage.writeTo(System.out);
        System.out.println("\n");

        return soapMessage;
    }

    private static void createSoapEnvelope(SOAPMessage soapMessage) throws SOAPException {
    	//Header
    	SOAPHeader header 				= soapMessage.getSOAPHeader();    	 
    	SOAPHeaderElement securityEle 	= header.addHeaderElement(new QName(securitySchema, security, securityPrefix));
    	SOAPElement usernameTokenEle 	= securityEle.addChildElement(usernameToken, securityPrefix);
    	SOAPElement usernameElement 	= usernameTokenEle.addChildElement(usernameKey, securityPrefix);
    	SOAPElement passwordElement 	= usernameTokenEle.addChildElement(passwordKey, securityPrefix);
    	
    	passwordElement.addAttribute(new QName("", passwordType, ""), passwordURI);
    	usernameElement.setTextContent(usernameValue);
    	passwordElement.setTextContent(passwordValue);
    	  	
        //Envelope
    	SOAPPart soapPart 		= soapMessage.getSOAPPart();
        SOAPEnvelope envelope 	= soapPart.getEnvelope();
        envelope.addNamespaceDeclaration(APIns, APInsURI);        
        
        //Body
        SOAPBody soapBody = envelope.getBody();
        soapBody.addChildElement(soapAction, APIns);

    }
    
}