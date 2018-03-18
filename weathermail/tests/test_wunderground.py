from django.test import TestCase

import requests_mock

from weathermail.models.wunderground import WundergrounAPI

class WundergroundAPITestCase(TestCase):

    almanac_query = "http://api.wunderground.com/api/API_KEY/almanac/q/ma/boston.json"
    almanac_response = """
        {
            "response": {
                "version": "0.1",
                "termsofService": "http://www.wunderground.com/weather/api/d/terms.html",
                "features": {
                    "almanac": 1
                }
            },
            "almanac": {
                "airport_code": "KBOS",
                "temp_high": {
                    "normal": {
                        "F": "46",
                        "C": "8"
                    },
                    "record": {
                        "F": "70",
                        "C": "21"
                    },
                    "recordyear": "1990"
                },
                "temp_low": {
                    "normal": {
                        "F": "31",
                        "C": "-1"
                    },
                    "record": {
                        "F": "10",
                        "C": "-12"
                    },
                    "recordyear": "1916"
                }
            }
        }
        """


    conditions_query = "http://api.wunderground.com/api/API_KEY/conditions/q/ma/boston.json"
    conditions_response = """
        {
           "response": {
               "version": "0.1",
               "termsofService": "http://www.wunderground.com/weather/api/d/terms.html",
               "features": {
                   "conditions": 1
               }
           },
           "current_observation": {
               "image": {
                   "url": "http://icons.wxug.com/graphics/wu2/logo_130x80.png",
                   "title": "Weather Underground",
                   "link": "http://www.wunderground.com"
               },
               "display_location": {
                   "full": "Boston, MA",
                   "city": "Boston",
                   "state": "MA",
                   "state_name": "Massachusetts",
                   "country": "US",
                   "country_iso3166": "US",
                   "zip": "02108",
                   "magic": "1",
                   "wmo": "99999",
                   "latitude": "42.36000061",
                   "longitude": "-71.06999969",
                   "elevation": "21.9"
               },
               "observation_location": {
                   "full": "North End, Boston, Boston, Massachusetts",
                   "city": "North End, Boston, Boston",
                   "state": "Massachusetts",
                   "country": "US",
                   "country_iso3166": "US",
                   "latitude": "42.366951",
                   "longitude": "-71.056152",
                   "elevation": "69 ft"
               },
               "estimated": {},
               "station_id": "KMABOSTO132",
               "observation_time": "Last Updated on March 17, 7:40 PM EDT",
               "observation_time_rfc822": "Sat, 17 Mar 2018 19:40:18 -0400",
               "observation_epoch": "1521330018",
               "local_time_rfc822": "Sat, 17 Mar 2018 19:40:41 -0400",
               "local_epoch": "1521330041",
               "local_tz_short": "EDT",
               "local_tz_long": "America/New_York",
               "local_tz_offset": "-0400",
               "weather": "Clear",
               "temperature_string": "28.0 F (-2.2 C)",
               "temp_f": 28,
               "temp_c": -2.2,
               "relative_humidity": "22%",
               "wind_string": "From the WNW at 26.2 MPH Gusting to 32.4 MPH",
               "wind_dir": "WNW",
               "wind_degrees": 286,
               "wind_mph": 26.2,
               "wind_gust_mph": "32.4",
               "wind_kph": 42.2,
               "wind_gust_kph": "52.1",
               "pressure_mb": "1006",
               "pressure_in": "29.72",
               "pressure_trend": "+",
               "dewpoint_string": "-6 F (-21 C)",
               "dewpoint_f": -6,
               "dewpoint_c": -21,
               "heat_index_string": "NA",
               "heat_index_f": "NA",
               "heat_index_c": "NA",
               "windchill_string": "13 F (-11 C)",
               "windchill_f": "13",
               "windchill_c": "-11",
               "feelslike_string": "13 F (-11 C)",
               "feelslike_f": "13",
               "feelslike_c": "-11",
               "visibility_mi": "10.0",
               "visibility_km": "16.1",
               "solarradiation": "0",
               "UV": "0.0",
               "precip_1hr_string": "0.00 in ( 0 mm)",
               "precip_1hr_in": "0.00",
               "precip_1hr_metric": " 0",
               "precip_today_string": "0.00 in (0 mm)",
               "precip_today_in": "0.00",
               "precip_today_metric": "0",
               "icon": "clear",
               "icon_url": "http://icons.wxug.com/i/c/k/nt_clear.gif",
               "forecast_url": "http://www.wunderground.com/US/MA/Boston.html",
               "history_url": "http://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID=KMABOSTO132",
               "ob_url": "http://www.wunderground.com/cgi-bin/findweather/getForecast?query=42.366951,-71.056152",
               "nowcast": ""
           }
        }
        """

    def setUp(self):
        self.api_client = WundergrounAPI("API_KEY")  ## instantiate the client with a fake api key

    @requests_mock.mock()
    def test_almanac(self, m):
        m.get(self.almanac_query, text=self.almanac_response)
        resp = self.api_client.historical("boston", "ma")
        self.assertEqual(resp, dict(average_temp=28))

    @requests_mock.mock()
    def test_conditions(self, m):
        m.get(self.conditions_query, text=self.conditions_response)
        resp = self.api_client.conditions("boston", "ma")
