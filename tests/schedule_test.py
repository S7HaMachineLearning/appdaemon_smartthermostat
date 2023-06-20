import sys
sys.path.append('..')
import unittest
from appdaemon_testing.pytest import automation_fixture
from apps.smart_thermostat.schedule import schedule
from unittest import mock
from unittest.mock import MagicMock

def test_test():
    pass

def test_callbacks_are_registered(hass_driver, schedule: schedule):
    listen_state = hass_driver.get_mock("listen_state")
    listen_state.assert_called_once_with(
        schedule.presence_change, "device_tracker"
    )

@automation_fixture(
    schedule,
    args={
        'evening_on': 'input_datetime.smart_thermosat_evening',
        'sleep_on': 'input_datetime.smart_thermosat_sleep',
        'morning_on_week': 'input_datetime.smart_thermosat_morning_on_week', 
        'morning_on_weekend': 'input_datetime.smart_thermosat_morning_on_weekend',
        'input_select': 'input_select.smart_thermostat_house_mode',
        'morning_temp': 'input_number.smart_thermostat_morning_temp',
        'sleep_temp': 'input_number.smart_thermostat_sleep_temp',
        'evening_temp': 'input_number.smart_thermostat_evening_temp',
        'thermostat': 'climate.toon_thermostat',
        'switch': 'input_boolean.smartthermostat_switch',
    },
)
def schedule() -> schedule:
    pass