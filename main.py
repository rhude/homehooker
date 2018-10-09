# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import os
import json
import googlepub

class Config():
    service_key = 'uxcCXrocUR3-DgrIvjmAKHXWHJ3p1ystLtJy_5ZrUhExhCevtPL-W6A7Lx4qFfM0'

    # def __init__(self):
    #     self.service_key = os.environ.get('IFTTT_SERVICE_KEY', 'IFTTT_SERVICE_KEY is not set.')

class Auth(object):
    @staticmethod
    def check_service_key(headers):
        print(headers)
        if 'Ifttt-Service-Key' in headers:
            if headers['Ifttt-Service-Key'] != Config.service_key:
                print('Service key invalid.')
                return False
            else:
                return True

class Send(object):
    @staticmethod
    def led(pattern):
        if pattern == "OFF":
            print("Turning off LED strip.")
            deviceconfig = googlepub.DeviceConfig()
            deviceconfig.set_config(
                "rhudethings",
                "us-central1",
                "rhudeThings1",
                "rpi-led1",
                "0",
                json.dumps(
                    {
                        "pattern": pattern,
                        "led_on": False
                    }
                )
            )
        else:
            print("Sending {} to LED".format(pattern))
            deviceconfig = googlepub.DeviceConfig()
            deviceconfig.set_config(
                "rhudethings",
                "us-central1",
                "rhudeThings1",
                "rpi-led1",
                "0",
                json.dumps(
                 {
                     "pattern": pattern,
                     "led_on": True
                  }
                )
            )



class StartLED(webapp2.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        print(data)
        result = Send.led(data['pattern'])


class StopLED(webapp2.RequestHandler):
    def post(self):
        result = Send.led('OFF')

class Status(webapp2.RequestHandler):
    def get(self):
        if Auth.check_service_key(headers=self.request.headers):
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('all good!')
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('unauthorized')
            self.response.set_status(401)

class TestSetup(webapp2.RequestHandler):
    def post(self):
        print('Test setup requested.')
        if Auth.check_service_key(headers=self.request.headers):
            self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
            response_data = {
                'accessToken': 'abba123',
                'data': {
                    'samples': {
                        'actions': {
                            'start_led_strip': {
                                'pattern': 'christmas',
                                'led_strip_name': 'patiolanterns'
                            }
                        },
                        'actionRecordSkipping': {
                            'start_led_strip': {
                                'pattern': 'christmas',
                                'led_strip_name': 'patiolanterns'
                            }
                        }
                    }
                }
            }
            self.response.write(json.dumps(response_data))
        else:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('unauthorized')
            self.response.set_status(401)

app = webapp2.WSGIApplication([
    ('/ifttt/v1/status', Status),
    ('/ifttt/v1/test/setup', TestSetup),
    ('/ifttt/v1/actions/start_led_strip', StartLED),
    ('/ifttt/v1/actions/stop_led_strip', StopLED),
], debug=True)
