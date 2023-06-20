# pylint: disable=E1101
"""smart thermostat app for HACS."""
from datetime import datetime
import hassapi as hass

class set_time(hass.Hass): # pylint: disable=invalid-name
    """this app will make a schedule for the thermostat based on the user's behavior"""
    def initialize(self):
        """ 
        this function will initialize the app
        start listening to changes in the thermostat preset mode
        start listening to changes in the thermostat temperature

        """
        # Subscribe to thermostat preset changes
        self.listen_state(self.set_sleep_time, self.args["thermostat"], attribute="preset_mode")

        self.listen_state(self.set_new_daytime, self.args["thermostat"], attribute="temperature")

    def set_sleep_time(self, entity, attribute, old, new, kwargs): # pylint: disable=too-many-arguments, unused-argument
        """this function will set the new time"""	
        if new == 'sleep':
            self.log("detected manual sleep mode activated")
            new_time = self.get_new_time(self.args['sleep_on'])
            self.sleep = self.get_entity(self.args['sleep_on']) # pylint: disable=attribute-defined-outside-init
            self.sleep.call_service(
                service = "set_datetime",
                time=new_time,
            )
            self.log(f"new time set to {new_time}")

    def set_new_daytime(self, entity, attribute, old, new, kwargs): # pylint: disable=too-many-arguments, unused-argument
        """this function will set the new time"""
        if new != old:
            time = datetime.now()
            time = time.strftime('%H:%M:%S')
            self.log("detected manual daytime mode activated")
            entity_id = self.get_housemode()
            new_time = self.get_new_time(entity_id)
            self.entity_id = self.get_entity(entity_id) # pylint: disable=attribute-defined-outside-init
            self.entity_id.call_service(
                service = "set_datetime",
                time=new_time,
            )
            self.log(f"new time set to {new_time}")


    def get_housemode(self):
        """this function will get the housemode"""
        mode = self.get_state(self.args['input_select'])

        if mode == "morning_weekend":
            entity_id = self.args['morning_on_weekend']
        if mode == "morning_week":
            entity_id = self.args['morning_on_week']
        if mode == "sleep":
            entity_id = self.args['sleep_on']
        if mode == "evening":
            entity_id = self.args['evening_on']
        return entity_id

    def get_new_time (self, entity):
        """this function will get the new time"""
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
