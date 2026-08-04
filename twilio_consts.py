# File: twilio_consts.py
#
# Copyright (c) 2017-2026 Splunk Inc.
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
TWILIO_FINAL_STATUS = ["failed", "delivered", "undelivered"]
TWILIO_TIMEOUT_MINUTES = 1
TWILIO_SLEEP_SECS = 5
TWILIO_DEFAULT_REQUEST_TIMEOUT = 30
TWILIO_ALLOWED_API_BASE_URLS = (
    "https://api.twilio.com/2010-04-01",
    "https://api.us1.twilio.com/2010-04-01",
    "https://api.dublin.ie1.twilio.com/2010-04-01",
    "https://api.sydney.au1.twilio.com/2010-04-01",
)
