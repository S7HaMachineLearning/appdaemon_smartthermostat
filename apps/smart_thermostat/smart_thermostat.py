"""smart thermostat app for HACS."""

import hassapi as hass


# App to manage heating:
# - Turn on at different times in morning for weekdays and weekend, only if someone present
# - Stay on all day as long someone present
# - Turn off if everyone leaves
# - Turn off at night when input_select changes state
#
# Smart Heat doesn't actually turn the heat on and off, it merely sets it to a lower temperature for off so the house does not get too cold
#
# Args:
#
# morning_on_week = Weekday on time
# morning_on_weekend = Weekend on time
# evening_on = Evening on time of noone around
# sleep_on = sleep on time
# switch = Input boolean to activate and deactivate smartThermostat
# thermostat = The termostat to manage
# off_temp = Temperature to set thermostat to "off"
# on_temp = Temperature to set thermostat to "on"
# conf_temp = Temperature to set thermostat to comfort
# input_select = Name of input_select to monitor followed by comma separated list of values for which heating should be ON


class smart_thermostat(hass.Hass):
    def initialize(self):
        # Test

        # Subscribe to presence changes
        self.presence = self.listen_state(self.presence_change, "device_tracker")

        # Set current state according to switch
        self.state = self.get_state(self.args["switch"])
        self.log("Current state = {}".format(self.state))

        # set schedule
        self.evening_time = self.get_state(self.args["evening_on"])
        evening = self.parse_time(self.evening_time)
        self.run_daily(self.evening, evening)

        self.sleep_time = self.get_state(self.args["sleep_on"])
        sleep = self.parse_time(self.sleep_time)
        self.run_daily(self.sleep, sleep)

        self.morning_on_weekend_time = self.get_state(self.args["morning_on_weekend"])
        morning_weekend = self.parse_time(self.morning_on_weekend_time)
        self.run_daily(self.morning, morning_weekend, constrain_days="sat,sun", kwargs = "morning_weekend")

        self.morning_on_week_time = self.get_state(self.args["morning_on_week"])
        morning_week = self.parse_time(self.morning_on_week_time)
        self.run_daily(self.morning, morning_week, constrain_days="mon,tue,wed,thu,fri", kwargs = "morning_week")

    def evening(self, kwargs):
        # If noone home in the evening turn heat on in preparation (if someone is home heat is already on)
        self.log("Evening heat check")
        # set state to input select
        self.select_option(self.args["input_select"], "evening")
        self.log(self.get_state(self.args["switch"]))
        if self.anyone_home() and self.get_state(self.args["switch"]) == "on":
            self.set_thermostat('comfort')

    def sleep(self, kwargs):
        # If noone home in the evening turn heat on in preparation (if someone is home heat is already on)
        self.log("Evening heat check")
        # set state to input select
        self.select_option(self.args["input_select"], "sleep")
        if self.noone_home() and self.get_state(self.args["switch"]) == "on":
            self.set_thermostat('sleep')


    def morning(self, kwargs):
        # Setup tomorrows callback
        self.log("Morning heat check")
        self.select_option(self.args["input_select"], kwargs)
        if self.anyone_home() and self.get_state(self.args["switch"]) == "on":
            self.set_thermostat()

    def presence_change(self, entity, attribute, old, new, kwargs):
        if old != new and self.get_state(self.args["switch"]) == "on":
            if self.anyone_home():
                self.set_thermostat('home')
            else:
                self.set_thermostat('away')
    
    def set_thermostat(self, attibute):
        self.log("Turning heat on")
        self.log(attibute)
        self.entity = self.get_entity(self.args["thermostat"])
        self.entity.call_service(
            service = "set_preset_mode",
            preset_mode= attibute,
        )
