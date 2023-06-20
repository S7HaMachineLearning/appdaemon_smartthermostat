import unittest
from unittest.mock import MagicMock
from appdaemon_smartthermostat.apps.smart_thermostatset_temp.set_temp import set_temp

class TestSetTemp(unittest.TestCase):

    def setUp(self):
        self.app = set_temp()

    def test_check_change(self):
        self.app.get_housemode = MagicMock(return_value='morning_weekend')
        self.app.get_state = MagicMock(side_effect=['15.0', '15.0'])
        self.app.set_new_temp = MagicMock()

        self.app.check_change({})
        
        self.assertEqual(self.app.get_housemode.call_count, 1)
        self.assertEqual(self.app.get_state.call_count, 2)
        self.assertEqual(self.app.set_new_temp.call_count, 0)

        self.app.get_state = MagicMock(side_effect=['15.0', '16.0'])
        self.app.check_change({})
        
        self.assertEqual(self.app.set_new_temp.call_count, 1)

    def test_get_new_temp(self):
        self.app.get_history = MagicMock(return_value=[[{'state': '10.0'}, {'state': '11.0'}, {'state': '12.0'}]])
        self.assertEqual(self.app.get_new_temp('thermostat', 14.5), 11.0)

    def test_get_housemode(self):
        self.app.get_state = MagicMock(return_value='morning_weekend')
        self.assertEqual(self.app.get_housemode(), self.app.args['morning_temp'])

        self.app.get_state = MagicMock(return_value='sleep')
        self.assertEqual(self.app.get_housemode(), self.app.args['sleep_temp'])

        self.app.get_state = MagicMock(return_value='evening')
        self.assertEqual(self.app.get_housemode(), self.app.args['evening_temp'])

if __name__ == '__main__':
    unittest.main()