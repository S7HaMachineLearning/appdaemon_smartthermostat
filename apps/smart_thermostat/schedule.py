# pylint: disable=E1101
"""smart thermostat app for HACS."""
import hassapi as hass

class schedule(hass.Hass): # pylint: disable=invalid-name
    """
    Args:
    morning_on_week: Time schedule for weekdays
    morning_on_weekend: Time schedule for weekends
    evening_on: Time schedule for evenings
    sleep_on: Time schedule for sleep
    switch: Input boolean to activate and deactivate smartThermostat
    thermostat: The termostat to manage
    off_temp: Temperature to set thermostat to "off"
    on_temp: Temperature to set thermostat to "on"
    conf_temp: Temperature to set thermostat to comfort
    input_select: entity whit home modes

    App to manage heating:
    Turn on at different times in morning for weekdays and weekend, only if someone present
    Stay on all day as long someone present
    Turn off if everyone leaves
    Turn off at night
    """

    def initialize(self):
        """ Subscribe to presence changes """
        self.presence = self.listen_state(self.presence_change, "device_tracker") # pylint: disable=attribute-defined-outside-init

        # Set current state according to switch
        self.state = self.get_state(self.args["switch"]) # pylint: disable=attribute-defined-outside-init
        self.log(f"Current state = {self.state}")

        # start set smart schedule
        self.evening_time = self.get_state(self.args["evening_on"]) # pylint: disable=attribute-defined-outside-init
        evening = self.parse_time(self.evening_time)
        self.run_daily(
            self.evening,
            evening
            )

        self.sleep_time = self.get_state(self.args["sleep_on"]) # pylint: disable=attribute-defined-outside-init
        sleep = self.parse_time(self.sleep_time)
        self.run_daily(
            self.sleep,
            sleep
            )

        self.morning_on_weekend_time = self.get_state(self.args["morning_on_weekend"]) # pylint: disable=attribute-defined-outside-init
        morning_weekend = self.parse_time(self.morning_on_weekend_time)
        self.run_daily(
            self.morning,
            morning_weekend,
            constrain_days="sat,sun",
            kwargs = "morning_weekend"
            )

        self.morning_on_week_time = self.get_state(self.args["morning_on_week"]) # pylint: disable=attribute-defined-outside-init
        morning_week = self.parse_time(self.morning_on_week_time)
        self.run_daily(
            self.morning,
            morning_week,
            constrain_days="mon,tue,wed,thu,fri",
            kwargs = "morning_week"
            )
        # end set smart schedule

    def evening(self, kwargs): # pylint: disable=unused-argument
        """set evening temperature based on smart schedule"""
        self.log("Evening heat check")
        self.select_option(self.args["input_select"], "evening")
        if self.anyone_home() and self.get_state(self.args["switch"]) == "on":
            self.set_thermostat(self.get_state(self.args["evening_temp"]))

    def sleep(self, kwargs): # pylint: disable=unused-argument
        """set sleep temperature based on smart schedule"""
        self.log("Sleep heat check")
        # set state to input select
        self.select_option(self.args["input_select"], "sleep")
        if self.anyone_home() and self.get_state(self.args["switch"]) == "on":
            self.set_thermostat(self.get_state(self.args["sleep_temp"]))


    def morning(self, kwargs):
        """set morning temperature based on smart schedule"""	
        # Setup tomorrows callback
        self.log("Morning heat check")
        self.select_option(self.args["input_select"], kwargs)
        if self.anyone_home() and self.get_state(self.args["switch"]) == "on":
            self.set_thermostat(self.get_state(self.args["morning_temp"]))

    def presence_change(self, entity, attribute, old, new, kwargs): # pylint: disable=unused-argument, too-many-arguments
        """ If noone home turn heat off, if someone home turn heat on """
        if old != new and self.get_state(self.args["switch"]) == "on":
            if self.anyone_home():
                self.set_thermostat(self.get_state(self.args["morning_temp"]))
            else:
                self.set_thermostat(self.get_state(self.args["sleep_temp"]))

    def set_thermostat(self, attibute):
        """ Call temperature service to set thermostat to desired temperature"""	
        self.log(f"Setting temperature to {attibute}")
        self.entity = self.get_entity(self.args["thermostat"]) # pylint: disable=attribute-defined-outside-init
        self.entity.call_service(
            service = "set_temperature",
            temperature= attibute,
        )
