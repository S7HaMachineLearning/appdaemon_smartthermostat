import hassapi as hass
from datetime import datetime, timedelta
import adbase as ad
import json as json



class set_time(hass.Hass):
    def initialize(self):

        # Subscribe to thermostat preset changes
        self.listen_state(self.set_sleep_time, self.args["thermostat"], attribute="preset_mode")

        self.listen_state(self.set_new_daytime, self.args["thermostat"], attribute="temperature")

    def set_sleep_time(self, entity, attribute, old, new, kwargs):   
        if new == 'sleep':
            self.log("detected manual sleep mode activated")
            new_time = self.get_new_time(self.args['sleep_on'])
            self.sleep = self.get_entity(self.args['sleep_on'])
            self.sleep.call_service(
                service = "set_datetime",
                time=new_time,
            )
            self.log("new time set to {}".format(new_time))

    def set_new_daytime(self, entity, attribute, old, new, kwargs):
        if new != old:
            time = datetime.now()
            time = time.strftime('%H:%M:%S')
            self.log("detected manual daytime mode activated")
            temp = self.get_state(self.args['thermostat'], attribute='temperature')
            entity_id = self.get_housemode()
            new_time = self.get_new_time(entity_id)
            self.entity_id = self.get_entity(entity_id)
            self.entity_id.call_service(
                service = "set_datetime",
                time=new_time,
            )
            self.log("new time set to {}".format(new_time))


    def get_housemode(self):
        mode = self.get_state(self.args['input_select'])

        if mode == "morning_weekend":
            return self.args['morning_on_weekend']
        elif mode == "morning_week":
            return self.args['morning_on_week']
        elif mode == "sleep":
            return self.args['sleep_on']
        elif mode == "evening":
            return self.args['evening_on']
        else:
            self.log("housemode not found")

        

    def get_new_time (self, entity): 
        timestamp = []
        history = self.get_history(entity_id = entity, days = 14)

        for item in history[0]:
            state = item['state']
            if state != '00:00:00':
                timestamp.append(state)

        times = [datetime.strptime(dt, '%H:%M:%S') for dt in timestamp if dt]
        hours = sum(time.hour for time in times) // len(times)
        minutes = sum(time.minute for time in times) // len(times)
        seconds = sum(time.second for time in times) // len(times)

        average_time = f'{hours:02d}:{minutes:02d}:{seconds:02d}'
        return average_time
