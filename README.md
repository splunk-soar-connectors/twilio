[comment]: # "Auto-generated SOAR connector documentation"
# Twilio

Publisher: Splunk  
Connector Version: 2.0.3  
Product Vendor: Twilio  
Product Name: Twilio  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 4.9.39220  

This app integrates with Twilio for sending messages

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Twilio asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base_url** |  required  | string | Twilio Base URL (e.g. https://api.twilio.com/2010-04-01)
**account_sid** |  required  | string | Account SID
**auth_token** |  required  | password | Auth Token
**from_phone** |  required  | string | From Phone Number (Twilio Assigned, e.g. +15101281337)
**to_phone** |  optional  | string | To Phone Number (Used only for test connectivity)

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[send message](#action-send-message) - Send an SMS Text  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'send message'
Send an SMS Text

Type: **generic**  
Read only: **False**

Sends an SMS text to the specified Phone number.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**to_phone** |  required  | To Phone Number. If country code not specified will default to +1 | string |  `phone number`  `phone` 
**message** |  required  | Message to send | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.parameter.to_phone | string |  `phone number`  `phone`  |   5101112345 
action_result.parameter.message | string |  |   Happy Halloween to GV 
action_result.status | string |  |   success  failed 
action_result.message | string |  |   Error from server. Status Code: 404 Data from server: {"code": 20404, "message": "The requested resource /2010-04-01/Accounts/ABCDEF48541a12345fef18219497c47101/Messages.json was not found", "more_info": "https://www.twilio.com/docs/errors/20404", "status": 404}  Message delivery status: delivered 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1  0 
action_result.data.\*.body | string |  |   Sent from your Twilio trial account - Happy Halloween to GV 
action_result.data.\*.status | string |  |   queued  delivered 
action_result.data.\*.direction | string |  |   outbound-api 
action_result.data.\*.from | string |  |   +15123456789 
action_result.data.\*.num_segments | string |  |   1 
action_result.data.\*.date_updated | string |  |   Wed, 01 Nov 2017 20:56:57 +0000  Wed, 01 Nov 2017 22:31:18 +0000 
action_result.data.\*.uri | string |  |   /2010-04-01/Accounts/ABCDEF48541a49795fef18219497c47101/Messages/SM0123b6decd8146398c975ae9c3111111.json  /2010-04-01/Accounts/ABCDEF48541a49795fef18219497c47101/Messages/SAZ123AB33c7764e599999970933d6d68f.json 
action_result.data.\*.account_sid | string |  |   ABCDEF48541a49795fef18219497c47101 
action_result.data.\*.num_media | string |  |   0 
action_result.data.\*.to | string |  |   +15101112222 
action_result.data.\*.sid | string |  |   SM0123b6decd8146398c975ae9c3123456  SAZ123AB33c7764e599123456789d6d68f 
action_result.data.\*.date_created | string |  |   Wed, 01 Nov 2017 20:56:57 +0000  Wed, 01 Nov 2017 22:31:16 +0000 
action_result.data.\*.subresource_uris.media | string |  |   /2010-04-01/Accounts/ABCDEF48541a49795fef18219497c47101/Messages/SM0123b6decd8146398c975ae9c3111111/Media.json  /2010-04-01/Accounts/ABCDEF48541a49795fef18219497c47101/Messages/SAZ123AB33c7764e599999970933d6d68f/Media.json 
action_result.data.\*.price_unit | string |  |   USD 
action_result.data.\*.api_version | string |  |   2010-04-01 
action_result.data.\*.date_sent | string |  |   Wed, 01 Nov 2017 22:31:16 +0000 
action_result.data.price | string |  |  
action_result.data.error_message | string |  |  
action_result.data.messaging_service_sid | string |  |  
action_result.data.error_code | string |  |  
action_result.summary.message_delivery_status | string |  |   delivered 
action_result.data.\*.price | string |  |  
action_result.data.\*.error_code | string |  |  
action_result.data.\*.error_message | string |  |  
action_result.data.\*.subresource_uris.feedback | string |  |  
action_result.data.\*.messaging_service_sid | string |  |  