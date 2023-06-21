'''test for set_time'''
from unittest.mock import MagicMock
import unittest
import sys
sys.path.append('..')
from apps.smart_thermostat.set_time import set_time


class TestSetTime(unittest.TestCase):
    """setup test"""
    def setUp(self):
        self.set_time = set_time()
        # self.set_time.get_entity_state = MagicMock(return_value='morning_weekend')
        # self.set_time.get_entity_history = MagicMock(return_value= [[{'entity_id': 'input_datetime.smart_thermosat_sleep', 'state': '00:00:00', 'attributes': {'hour': 0, 'minute': 0, 'second': 0, 'timestamp': 0, 'friendly_name': 'smart_thermosat_sleep'}, 'last_changed': '2023-06-11T15:11:27.490231+00:00', 'last_updated': '2023-06-11T15:11:27.490231+00:00'}, {'entity_id': 'input_datetime.smart_thermosat_sleep', 'state': '21:00:00', 'attributes': {'hour': 0, 'minute': 0, 'second': 0, 'timestamp': 0, 'friendly_name': 'smart_thermosat_sleep'}, 'last_changed': '2023-06-11T15:30:27.937523+00:00', 'last_updated': '2023-06-11T15:30:27.937523+00:00'}, {'entity_id': 'input_datetime.smart_thermosat_sleep', 'state': '22:00:00', 'attributes': {'hour': 0, 'minute': 0, 'second': 0, 'timestamp': 0, 'friendly_name': 'smart_thermosat_sleep'}, 'last_changed': '2023-06-11T15:30:39.803266+00:00', 'last_updated': '2023-06-11T15:30:39.803266+00:00'}]])
        self.set_time.args = {
            'input_select': 'input_select.house_mode',
            'morning_on_weekend': 'input_datetime.smart_thermosat_morning_on_weekend',
            'morning_on_week': 'input_datetime.smart_thermosat_morning_on_week',
            'sleep_on': 'input_datetime.smart_thermosat_sleep',
            'evening_on': 'input_datetime.smart_thermosat_evening'
        }

    def test_get_housemode_morning_weekend(self):
        '''testing housemode morning weekend sould be correct'''
        self.set_time.get_entity_state = MagicMock(return_value='morning_weekend')

        expected_entity_id = 'input_datetime.smart_thermosat_morning_on_weekend'
        entity_id = self.set_time.get_housemode()
        self.assertEqual(entity_id, expected_entity_id)

    def test_geting_new_time_based_on_hystory(self):
        '''testing geting new time based on hystory'''
        self.set_time.get_entity_history = MagicMock(return_value= [[{'entity_id': 'input_datetime.smart_thermosat_sleep', 'state': '00:00:00', 'attributes': {'hour': 0, 'minute': 0, 'second': 0, 'timestamp': 0, 'friendly_name': 'smart_thermosat_sleep'}, 'last_changed': '2023-06-11T15:11:27.490231+00:00', 'last_updated': '2023-06-11T15:11:27.490231+00:00'}, {'entity_id': 'input_datetime.smart_thermosat_sleep', 'state': '21:00:00', 'attributes': {'hour': 0, 'minute': 0, 'second': 0, 'timestamp': 0, 'friendly_name': 'smart_thermosat_sleep'}, 'last_changed': '2023-06-11T15:30:27.937523+00:00', 'last_updated': '2023-06-11T15:30:27.937523+00:00'}, {'entity_id': 'input_datetime.smart_thermosat_sleep', 'state': '22:00:00', 'attributes': {'hour': 0, 'minute': 0, 'second': 0, 'timestamp': 0, 'friendly_name': 'smart_thermosat_sleep'}, 'last_changed': '2023-06-11T15:30:39.803266+00:00', 'last_updated': '2023-06-11T15:30:39.803266+00:00'}]])
        expected_new_time = '21:00:00'
        new_time = self.set_time.get_new_time('morning_on_weekend')
        self.assertEqual(new_time, expected_new_time)

    def test_compare_temp(self):
        # Mock de externe afhankelijkheden
        self.set_time.get_entity_state = MagicMock(side_effect=[
            '10',
            '10',
            '19',
            '20',
        ])
        self.set_time.log = MagicMock()

        # Roep de functie aan die je wilt testen
        result = self.set_time.compaire_temp('input_datetime.smart_thermosat_morning_on_weekend')

        # Asserts om de verwachte resultaten te controleren
        self.assertEqual(result, self.set_time.args['morning_on_week'])


if __name__ == '__main__':
    unittest.main()
    