from unittest.mock import MagicMock
import unittest
import sys
sys.path.append('..')
from apps.smart_thermostat.set_temp import set_temp


class TestSetTemp(unittest.TestCase):
    """setup test"""
    def setUp(self):
        print('setup')
        self.set_temp = set_temp()
        self.set_temp.get_entity_state = MagicMock(return_value='morning_weekend')
        # 3 states in history 10.0, 15.0, 16.0. 
        self.set_temp.get_entity_history = MagicMock(return_value= [[{'entity_id': 'input_number.smart_thermostat_sleep_temp', 'state': '10.0', 'attributes': {'initial': None, 'unit_of_measurement': '��C', 'friendly_name': 'smart_thermostat_sleep_temp'}, 'last_changed': '2023-06-15T15:16:47.220532+00:00', 'last_updated': '2023-06-15T15:16:47.220532+00:00'}, {'entity_id': 'input_number.smart_thermostat_sleep_temp', 'state': '15.0', 'attributes': {'initial': None, 'unit_of_measurement': '��C', 'friendly_name': 'smart_thermostat_sleep_temp'}, 'last_changed': '2023-06-15T15:52:38.411697+00:00', 'last_updated': '2023-06-15T15:52:38.411697+00:00'}, {'entity_id': 'input_number.smart_thermostat_sleep_temp', 'state': '16.0', 'attributes': {'initial': None, 'unit_of_measurement': '��C', 'friendly_name': 'smart_thermostat_sleep_temp'}, 'last_changed': '2023-06-16T06:39:31.923175+00:00', 'last_updated': '2023-06-16T06:39:31.923175+00:00'}]])
        self.set_temp.args = {
            'input_select': 'input_select.house_mode',
            'morning_temp': 'input_number.smart_thermostat_morning_temp',
            'sleep_temp': 'input_number.smart_thermostat_sleep_temp',
            'evening_temp': 'input_number.smart_thermostat_evening_temp',
        }

    def test_get_housemode_morning_weekend(self):
        '''testing housemode morning weekend sould be correct'''
        expected_entity_id = 'input_number.smart_thermostat_morning_temp'
        entity_id = self.set_temp.get_housemode()
        self.assertEqual(entity_id, expected_entity_id)

    def test_geting_new_time_based_on_hystory(self):
        '''testing geting new time based on hystory'''
        # this temperture sould come out as a result after calculation and rounding
        expected_new_temp = 17.0
        # this is the temperture that is set in the thermnostat
        new_temp = self.set_temp.get_new_temp('input_number.smart_thermostat_sleep_temp', 17.1)
        self.assertEqual(new_temp, expected_new_temp)


if __name__ == '__main__':
    unittest.main()
    