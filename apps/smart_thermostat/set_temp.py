# pylint: disable=E1101
"""smart thermostat app for HACS."""
import hassapi as hass

class set_temp(hass.Hass): # pylint: disable=invalid-name
    """this app will set the temperature of the thermostat based on the user's behavior"""

    def initialize(self):
        """
        this function will initialize the app
        
        It wil run evry 5 minutes to check if the temperature has changed manualy

        If the temperature has changed manualy it will set the new temperature

        """
        self.run_every(self.check_change, "now+5", 5 * 60) # pylint: disable=E1101

    def check_change(self, kwargs): # pylint: disable=unused-argument
        """this function will check if the temperature has changed manualy"""
        entity = self.get_housemode()
        pref = float(self.get_state(entity))
        temp = float(self.get_state(self.args['thermostat'], attribute='temperature')) # pylint: disable=E1123
        # minimum temperature is 10 degrees
        if temp != pref and temp >= 10:
            self.log("change detected")
            self.set_new_temp(entity= self.args["thermostat"], attribute = temp )

    def set_new_temp(self, entity, attribute):
        """this function will set the new temperature"""
        entity = self.get_housemode()
        self.log(entity) # pylint: disable=E1101
        new_temp = self.get_new_temp(entity, attribute = attribute)
        self.set_state(entity, state=new_temp)
        self.log(f"new temperature set to {new_temp}")

    def get_new_temp(self, entity, attribute):
        """this function will calculate the new temperature based on the last 14 days"""
        temps = []
        history = self.get_history(entity_id = entity, days = 14)

        for item in history[0]:
            state = item['state']
            # minimum temperature is 10 degrees
            if state >= '10.0':
                temps.append(state)

        if len(temps) < 14:
            self.log("not enough data to calculate new temperature") # pylint: disable=E1101
            # round to nearest .5 or .0
            new_temp = round(attribute * 2) / 2
        else:
            self.log("Calculating new temperature...") # pylint: disable=E1101
            numbers = [float(number) for number in attribute]
            average = sum(numbers) / len(numbers)
            # round to nearest .5 or .0
            new_temp = round(average * 2) / 2
        return new_temp

    def get_housemode(self):
        """this function will get the temperature entity based on the housemode"""
        mode = self.get_state(self.args['input_select'])
        if mode == "morning_weekend":
            entity = self.args['morning_temp'] # pylint: disable=E1101
        if mode == "morning_week":
            entity = self.args['morning_temp'] # pylint: disable=E1101
        if mode == "sleep":
            entity = self.args['sleep_temp'] # pylint: disable=E1101
        if mode == "evening":
            entity = self.args['evening_temp'] # pylint: disable=E1101
        return entity
