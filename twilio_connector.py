# File: twilio_connector.py
#
# Copyright (c) 2017-2024 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
# Phantom App imports
import json
import time

import phantom.app as phantom
import requests
from bs4 import BeautifulSoup
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

# Usage of the consts file is recommended
import twilio_consts as consts


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class TwilioConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(TwilioConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None
        self._from_phone = None
        self._account_sid = None
        self._auth_token = None
        self._to_phone = None

        return

    def _process_empty_reponse(self, response, action_result):

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Empty response and no information in the header"), None)

    def _process_html_response(self, response, action_result):

        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove the script, style, footer and navigation part from the HTML message
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()
            error_text = soup.text
            split_lines = error_text.split("\n")
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = "\n".join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code, error_text)

        message = message.replace("{", "{{").replace("}", "}}")

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):

        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(r.status_code, r.text.replace("{", "{{").replace("}", "}}"))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):

        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, "add_debug_data"):
            action_result.add_debug_data({"r_status_code": r.status_code})
            action_result.add_debug_data({"r_text": r.text})
            action_result.add_debug_data({"r_headers": r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if "json" in r.headers.get("Content-Type", ""):
            return self._process_json_response(r, action_result)

        # Process an HTML resonse, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if "html" in r.headers.get("Content-Type", ""):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_reponse(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
            r.status_code, r.text.replace("{", "{{").replace("}", "}}")
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, headers=None, params=None, data=None, method="get"):

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), resp_json)

        # Create a URL to connect to
        url = "{0}/Accounts/{1}{2}".format(self._base_url, self._account_sid, endpoint)

        try:
            r = request_func(url, auth=(config["account_sid"], config["auth_token"]), data=data, headers=headers, params=params)
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))), resp_json)

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        if self._to_phone is None:
            self.save_progress("Connecting to the Twilio account to check connectivity")

            # make rest call
            ret_val, response = self._make_rest_call(".json", action_result, method="get")

            if phantom.is_fail(ret_val):
                self.save_progress("Test Connectivity Failed")
                return action_result.get_status()

        else:
            self.save_progress("Sending a message to validate config")

            ret_val, _ = self._send_text(action_result, "Testing connectivity from Phantom to Twilio", self._to_phone)

            if phantom.is_fail(ret_val):
                self.save_progress("Test connectivity Failed")
                return action_result.get_status()

        self.save_progress("Test connectivity Passed")

        return action_result.set_status(phantom.APP_SUCCESS)

    def _poll_task_status(self, message_id, action_result):

        polling_attempt = 0

        # timeout in minutes
        timeout = consts.TWILIO_TIMEOUT_MINUTES

        max_polling_attempts = (int(timeout) * 60) / consts.TWILIO_SLEEP_SECS

        while polling_attempt < max_polling_attempts:

            polling_attempt += 1

            self.send_progress("Polling attempt {0} of {1} to check status of message delivery".format(polling_attempt, max_polling_attempts))

            ret_val, response = self._make_rest_call("/Messages/{0}.json".format(message_id), action_result)

            if phantom.is_fail(ret_val):
                return RetVal(action_result.get_status(), None)

            status = response.get("status")

            if not status:
                return RetVal(action_result.set_status(phantom.APP_ERROR, "Status key not part of the response"), None)

            if status in consts.TWILIO_FINAL_STATUS:
                break

            time.sleep(consts.TWILIO_SLEEP_SECS)

        return RetVal(phantom.APP_SUCCESS, response)

    def _send_text(self, action_result, body, to_phone):

        data = {"Body": body, "To": to_phone, "From": self._from_phone}

        # make rest call
        ret_val, response = self._make_rest_call("/Messages.json", action_result, data=data, method="post")

        if phantom.is_fail(ret_val):
            return RetVal(action_result.get_status())

        sid = response.get("sid")

        if not sid:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "SID not part of the response"))

        # try to get the status of the text message
        ret_val, response = self._poll_task_status(sid, action_result)

        if phantom.is_fail(ret_val):
            return RetVal(action_result.get_status(), response)

        return RetVal(phantom.APP_SUCCESS, response)

    def _handle_send_text(self, param):

        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        body = param["message"]
        to_phone = param["to_phone"]

        ret_val, response = self._send_text(action_result, body, to_phone)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        action_result.update_summary({"message_delivery_status": response.get("status", "unknown")})

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == "test_connectivity":
            ret_val = self._handle_test_connectivity(param)

        elif action_id == "send_text":
            ret_val = self._handle_send_text(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        config = self.get_config()

        self._base_url = config["base_url"]
        self._from_phone = config["from_phone"]

        if not self._from_phone.startswith("+"):
            return self.set_status(
                phantom.APP_ERROR, "Please specify the from_phone value with a country code starting with the + char for e.g +15101281337"
            )

        self._account_sid = config["account_sid"]
        self._auth_token = config["auth_token"]
        self._to_phone = config.get("to_phone")

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == "__main__":

    import argparse
    import sys

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument("input_test_json", help="Input Test JSON file")
    argparser.add_argument("-u", "--username", help="username", required=False)
    argparser.add_argument("-p", "--password", help="password", required=False)

    args = argparser.parse_args()
    session_id = None
    login_url = BaseConnector._get_phantom_base_url() + "login"

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass

        password = getpass.getpass("Password: ")

    if username and password:
        try:
            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies["csrftoken"]

            data = dict()
            data["username"] = username
            data["password"] = password
            data["csrfmiddlewaretoken"] = csrftoken

            headers = dict()
            headers["Cookie"] = "csrftoken=" + csrftoken
            headers["Referer"] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies["sessionid"]
        except Exception as e:
            print("Unable to get session id from the platfrom. Error: " + str(e))
            exit(1)

    if len(sys.argv) < 2:
        print("No test json specified as input")
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = TwilioConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json["user_session_token"] = session_id

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)
