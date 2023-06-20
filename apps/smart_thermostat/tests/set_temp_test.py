from schedule import schedule
import unittest
from unittest.mock import MagicMock

class TestEvening(unittest.TestCase):
    def test_evening_temperature(self):
        # Mocking required functions and attributes
        args = {
            "input_select": "test_input_select",
            "switch": "test_switch",
            "evening_temp": "test_evening_temp"
        }
        obj = schedule()  # Replace MyClass with the actual class name
        obj.log = MagicMock()
        obj.select_option = MagicMock()
        obj.get_state = MagicMock(side_effect=["on", "20"])  # Return values for get_state()

        # Call the method being tested
        obj.evening(kwargs=args)

        # Assertions
        obj.log.assert_called_with("Evening heat check")
        obj.select_option.assert_called_with("test_input_select", "evening")
        obj.get_state.assert_any_call("test_switch")  # Check if get_state() was called with "test_switch"
        obj.get_state.assert_any_call("test_evening_temp")  # Check if get_state() was called with "test_evening_temp"
        obj.set_thermostat.assert_called_with("20")  # Check if set_thermostat() was called with the expected temperature

if __name__ == '__main__':
    unittest.main()