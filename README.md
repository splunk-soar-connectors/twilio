[comment]: # "Auto-generated SOAR connector documentation"
# Twilio

Publisher: Splunk  
Connector Version: 2\.0\.1  
Product Vendor: Twilio  
Product Name: Twilio  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app integrates with Twilio for sending messages

### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Twilio asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base\_url** |  required  | string | Twilio Base URL \(e\.g\. https\://api\.twilio\.com/2010\-04\-01\)
**account\_sid** |  required  | string | Account SID
**auth\_token** |  required  | password | Auth Token
**from\_phone** |  required  | string | From Phone Number \(Twilio Assigned, e\.g\. \+15101281337\)
**to\_phone** |  optional  | string | To Phone Number \(Used only for test connectivity\)

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

Sends an SMS text to the specified Phone number\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**to\_phone** |  required  | To Phone Number\. If country code not specified will default to \+1 | string |  `phone number`  `phone` 
**message** |  required  | Message to send | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.to\_phone | string |  `phone number`  `phone` 
action\_result\.parameter\.message | string | 
action\_result\.status | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 
action\_result\.data\.\*\.body | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.direction | string | 
action\_result\.data\.\*\.from | string | 
action\_result\.data\.\*\.num\_segments | string | 
action\_result\.data\.\*\.date\_updated | string | 
action\_result\.data\.\*\.uri | string | 
action\_result\.data\.\*\.account\_sid | string | 
action\_result\.data\.\*\.num\_media | string | 
action\_result\.data\.\*\.to | string | 
action\_result\.data\.\*\.sid | string | 
action\_result\.data\.\*\.date\_created | string | 
action\_result\.data\.\*\.subresource\_uris\.media | string | 
action\_result\.data\.\*\.price\_unit | string | 
action\_result\.data\.\*\.api\_version | string | 
action\_result\.data\.\*\.date\_sent | string | 
action\_result\.data\.price | string | 
action\_result\.data\.error\_message | string | 
action\_result\.data\.messaging\_service\_sid | string | 
action\_result\.data\.error\_code | string | 
action\_result\.summary\.message\_delivery\_status | string | 
action\_result\.data\.\*\.price | string | 
action\_result\.data\.\*\.error\_code | string | 
action\_result\.data\.\*\.error\_message | string | 
action\_result\.data\.\*\.subresource\_uris\.feedback | string | 
action\_result\.data\.\*\.messaging\_service\_sid | string | 