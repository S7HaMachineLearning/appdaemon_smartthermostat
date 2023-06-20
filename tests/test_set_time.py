'''test for set_time'''
import unittest
import sys
sys.path.append('..')
from mock import MagicMock
from appdaemon_testing.pytest import automation_fixture
from apps.smart_thermostat.set_time import set_time


# class TestSetTemp(unittest.TestCase):
#     """setup test"""
#     def setUp(self):
#         print('setup')
#         self.set_time = set_time()
#         self.set_time.get_state = MagicMock(return_value='morning_on_weekend_entity')
#         self.set_time.args = {
#             'input_select': 'input_select.house_mode',
#             'morning_on_weekend': 'morning_on_weekend_entity',
#             'morning_on_week': 'morning_on_week_entity',
#             'sleep_on': 'sleep_on_entity',
#             'evening_on': 'evening_on_entity'
#         }

#     def test_get_housemode_morning_weekend(self):
#         '''testing housemode morning weekend sould be correct'''
#         expected_entity_id = 'morning_on_weekend_entity'
#         entity_id = self.set_time.get_housemode()
#         self.assertEqual(entity_id, expected_entity_id)

# if __name__ == '__main__':
#     unittest.main()

# def test():
#     pass

# @automation_fixture(
#     set_time,
#     args={
#             'input_select': 'input_select.house_mode',
#             'morning_on_weekend': 'morning_on_weekend_entity',
#             'morning_on_week': 'morning_on_week_entity',
#             'sleep_on': 'sleep_on_entity',
#             'evening_on': 'evening_on_entity',
#     },
# )
# def set_time() -> set_time:
#     pass
