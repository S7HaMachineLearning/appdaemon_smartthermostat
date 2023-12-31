# pylint: disable=E1101
"""smart thermostat app for HACS."""
from datetime import datetime
import hassapi as hass

class set_time(hass.Hass): # pylint: disable=invalid-name
    """
    this app will make a schedule for the thermostat based on the user's behavior
    
    args:

    evening_on: input_datetime.smart_thermosat_evening
    sleep_on: input_datetime.smart_thermosat_sleep
    morning_on_week: input_datetime.smart_thermosat_morning_on_week
    morning_on_weekend: input_datetime.smart_thermosat_morning_on_weekend
    thermostat: climate.toon_thermostat
    input_select: input_select.smart_thermostat_house_mode
    smart_time_switch: input_boolean.smart_thermostat_time_switch
    morning_temp: input_number.smart_thermostat_morning_temp
    sleep_temp: input_number.smart_thermostat_sleep_temp
    evening_temp: input_number.smart_thermostat_evening_temp 
    """

    def initialize(self):
        """ 
        this function will initialize the app
        start listening to changes in the thermostat preset mode
        start listening to changes in the thermostat temperature

        """
        # Subscribe to thermostat preset changes for sleep mode
        self.listen_state(self.set_sleep_time, self.args["thermostat"], attribute="preset_mode")

        # Subscribe to thermostat temperature changes for new daytime
        self.listen_state(self.set_new_daytime, self.args["thermostat"], attribute="temperature")

    def set_sleep_time(self, entity, attribute, old, new, kwargs): # pylint: disable=too-many-arguments, unused-argument
        """this function will set the new time"""	
        if new == 'sleep' and self.get_state(self.args["smart_time_switch"]) == "on":
            self.log("detected manual sleepmode override")
            new_time = self.get_new_time(self.args['sleep_on'])
            self.sleep = self.get_entity(self.args['sleep_on']) # pylint: disable=attribute-defined-outside-init
            self.sleep.call_service(
                service = "set_datetime",
                time=new_time,
            )
            self.log(f"new time set to {new_time}")

    def set_new_daytime(self, entity, attribute, old, new, kwargs): # pylint: disable=too-many-arguments, unused-argument
        """this function will set the new time"""
        if new != old and self.get_state(self.args["smart_time_switch"]) == "on":
            time = datetime.now()
            time = time.strftime('%H:%M:%S')
            entity_id = self.get_housemode()
            entity = self.compaire_temp(housemode= entity_id)
            if entity != "":
                self.log("detected manual housemode override")
                new_time = self.get_new_time(entity_id)
                self.entity_id = self.get_entity(entity_id) # pylint: disable=attribute-defined-outside-init
                self.entity_id.call_service(
                    service = "set_datetime",
                    time=new_time,
                )
                self.log(f"new time set to {new_time}")

    def compaire_temp(self, housemode):
        """this function will compaire the temperature with the housemode temperature"""
        temperature = float(self.get_entity_state(entity='thermostat',attribute='temperature'))
        morning_temp = float(self.get_entity_state(entity='morning_temp'))
        sleep_temp = float(self.get_entity_state(entity='sleep_temp'))
        evening_temp = float(self.get_entity_state(entity='evening_temp'))
        entity = ""

        if temperature == morning_temp and housemode != self.args['morning_on_week']:
            entity = self.args['morning_on_week']
        if temperature == morning_temp and housemode != self.args['morning_on_weekend']:
            entity = self.args['morning_on_weekend']
        if temperature == sleep_temp and housemode != self.args['sleep_on']:
            entity = self.args['sleep_on']
        if temperature == evening_temp and housemode != self.args['evening_on']:
            entity = self.args['evening_on']
        return entity

    def get_housemode(self):
        """this function will get the housemode"""
        mode = self.get_entity_state(entity='input_select')

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
        history = self.get_entity_history(entity = entity, days = 14)

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

    def get_entity_state(self, entity, attribute = " "):
        """this function will get the entity state"""
        if attribute == " ":
            return self.get_state(self.args[entity])
        return self.get_state(self.args[entity], attribute=attribute) # pylint: disable=unexpected-keyword-arg

    def get_entity_history(self, entity, days):
        """this function will get the entity history"""
        return self.get_history(entity_id = entity, days = days)
