#!/usr/bin/python
# -*- coding: utf-8 -*-

from beautifulhue.api import Bridge


class LightControl:

    def __init__(self, deviceIP, username, _id, data,\
                 *args, **kwargs):

        self.deviceIP = deviceIP
        self.username = username
        self.data = data
        self.ligth_id = _id

        #print(self.deviceIP, self.username, self.data, self.ligth_id)

        self.bridge = Bridge(device={'ip': self.deviceIP}, \
                             user={'name': self.username}
        )


    def get_light_id(self):
        return self.ligth_id

    def which_data(self):
        resource = {
            'which':self.ligth_id,
            'data': self.data
        }
        self.bridge.light.update(resource)



#some testing
json_params = {'state':{'on':True, 'ct':245}}
test = LightControl("10.10.30.49", "newdeveloper", 1, json_params)
print(test.which_data())


