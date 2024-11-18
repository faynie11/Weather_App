import unittest
from unittest.mock import patch, MagicMock
from main import get_weather

class TestWeatherApp(unittest.TestCase):

    @patch('requests.get')
    def test_get_weather_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "name": "New York",
            "sys": {"country": "US"},
            "main": {"temp": 298.15, "humidity": 60, "pressure": 1012},
            "weather": [{"icon": "01d", "main": "Clear", "description": "clear sky"}],
            "clouds": {"all": 0},
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = get_weather("New York")

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "New York")
        self.assertEqual(result[1], "US")
        self.assertAlmostEqual(result[2], 25.0, places=1)  # Temp in Celsius
        self.assertEqual(result[5], "Clear")
        self.assertEqual(result[9], 0)

    @patch('requests.get')
    def test_get_weather_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"message": "city not found"}

        result = get_weather("InvalidCity")

        self.assertIsNone(result)


    @patch('tkinter.Label')
    def test_update_recent_city_label(self, mock_label):
        from main import update_recent_city_label
        from tkinter import Tk

        root = Tk()

        mock_city_label = MagicMock()
        mock_img_label = MagicMock()
        mock_temp_label = MagicMock()

        weather_data = ("New York", "US", 25.0, 298.15, "01d", "Clear", "clear sky", 60, 1012, 0)

        update_recent_city_label(mock_city_label, mock_img_label, mock_temp_label, weather_data)

        mock_city_label.config.assert_called_with(text="New York, US")
        mock_temp_label.config.assert_called_with(text="25°C")

        root.destroy()
