from unittest.mock import MagicMock
from unittest import mock
from apps.smart_thermostat.set_temp import set_temp
from appdaemon_testing.pytest import automation_fixture
import sys
sys.path.append('..')


# def test_callbacks_are_registered(hass_driver, set_temp: set_temp):
#     run_every = hass_driver.get_mock("run_every")
#     run_every.assert_called_once_with(
#         set_temp.check_change, "now+5", 5 * 60)

# def test_set_temp(set_temp_instance):
#     """Test the set_temp app."""
#     set_temp_instance.initialize()

#     # set_temp_instance.args["thermostat"] = "climate.toon_thermostat"
#     # set_temp_instance.args["morning_temp"] = "input_number.smart_thermostat_morning_temp"
#     # set_temp_instance.args["sleep_temp"] = "input_number.smart_thermostat_sleep_temp"
#     # set_temp_instance.args["evening_temp"] = "input_number.smart_thermostat_evening_temp"
#     # set_temp_instance.args["input_select"] = "input_select.smart_thermostat_house_mode"

#     # Simuleer een verandering in temperatuur
#     set_temp_instance.set_new_temp(entity="thermostat", attribute=20)

#     # Controleer of de nieuwe temperatuur correct is ingesteld
#     new_temp = set_temp_instance.get_state("thermostat")
#     assert new_temp == 20

#     # Simuleer onvoldoende gegevens voor het berekenen van de nieuwe temperatuur
#     set_temp_instance.get_history = lambda entity_id, days: []
#     set_temp_instance.set_new_temp(entity="thermostat", attribute=25)

#     # Controleer of de nieuwe temperatuur correct is afgerond naar .5 of .0
#     new_temp = set_temp_instance.get_state("thermostat")
# #     assert new_temp == 25.0 or new_temp == 25.5


# @automation_fixture(
#     set_temp,
#     args={
#         "thermostat": "climate.toon_thermostat",
#         "morning_temp": "input_number.smart_thermostat_morning_temp",
#         "sleep_temp": "input_number.smart_thermostat_sleep_temp",
#         "evening_temp": "input_number.smart_thermostat_evening_temp",
#         "input_select": "input_select.smart_thermostat_house_mode"
#     },
# )
# def test_set_temp() -> set_temp:
#     pass
