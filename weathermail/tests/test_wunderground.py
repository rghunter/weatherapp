from django.test import TestCase

import requests_mock
import mock, json

from weathermail.models.wunderground import WundergroundAPI, WundergroundAPIException, InvalidLocationException

class WundergroundAPITestCase(TestCase):

    error_query = "http://api.wunderground.com/api/API_KEY/alsdfmanac/q/ma/boston.json"
    error_response= """
    {
       "response": {
           "version": "0.1",
           "termsofService": "http://www.wunderground.com/weather/api/d/terms.html",
           "features": {},
           "error": {
               "type": "unknownfeature"
           }
       }
    }
    """

    bad_loc_query = "http://api.wunderground.com/api/API_KEY/almanac/q/ca/boston.json"
    bad_loc_response= """
    {
       "response": {
           "version": "0.1",
           "termsofService": "http://www.wunderground.com/weather/api/d/terms.html",
           "features": {},
           "results": []
       }
    }
    """


    fetch_query = "http://api.wunderground.com/api/API_KEY/almanac/conditions/q/ma/boston.json"
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

    fetch_data_response = json.loads("""
        {
            "response": {
                "version": "0.1",
                "termsofService": "http://www.wunderground.com/weather/api/d/terms.html",
                "features": {
                    "almanac": 1,
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
                "observation_time": "Last Updated on March 17, 9:19 PM EDT",
                "observation_time_rfc822": "Sat, 17 Mar 2018 21:19:34 -0400",
                "observation_epoch": "1521335974",
                "local_time_rfc822": "Sat, 17 Mar 2018 21:19:43 -0400",
                "local_epoch": "1521335983",
                "local_tz_short": "EDT",
                "local_tz_long": "America/New_York",
                "local_tz_offset": "-0400",
                "weather": "Clear",
                "temperature_string": "25.2 F (-3.8 C)",
                "temp_f": 25.2,
                "temp_c": -3.8,
                "relative_humidity": "24%",
                "wind_string": "From the NW at 18.6 MPH Gusting to 24.8 MPH",
                "wind_dir": "NW",
                "wind_degrees": 313,
                "wind_mph": 18.6,
                "wind_gust_mph": "24.8",
                "wind_kph": 29.9,
                "wind_gust_kph": "39.9",
                "pressure_mb": "1009",
                "pressure_in": "29.79",
                "pressure_trend": "+",
                "dewpoint_string": "-6 F (-21 C)",
                "dewpoint_f": -6,
                "dewpoint_c": -21,
                "heat_index_string": "NA",
                "heat_index_f": "NA",
                "heat_index_c": "NA",
                "windchill_string": "12 F (-11 C)",
                "windchill_f": "12",
                "windchill_c": "-11",
                "feelslike_string": "12 F (-11 C)",
                "feelslike_f": "12",
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
        """)

    def setUp(self):
        self.api_client = WundergroundAPI("API_KEY")  ## instantiate the client with a fake api key


    @requests_mock.mock()
    def test_api_error(self, m):
        m.get(self.error_query, text=self.error_response)
        self.assertRaises(WundergroundAPIException, self.api_client.api_call_datafeature, ["alsdfmanac"], "boston", "ma")


    @requests_mock.mock()
    def test_api_status_code_error(self, m):
        m.get(self.error_query, status_code=500) # Since we are testing for an actual status code return, the query URL is more or less irrelevant for this test.
        self.assertRaises(WundergroundAPIException, self.api_client.api_call_datafeature, ["alsdfmanac"], "boston", "ma")

    @requests_mock.mock()
    def test_bad_loc(self, m):
        m.get(self.bad_loc_query, text=self.bad_loc_response)
        self.assertRaises(InvalidLocationException, self.api_client.api_call_datafeature, ["almanac"], "boston", "ca")

    def test_join_features(self):
        resp = self.api_client.join_features(['a', 'b'])
        self.assertEqual('a/b', resp)

    @mock.patch.object(WundergroundAPI, 'api_call_datafeature') 
    def test_fetch_data(self, m):
        m.return_value = self.fetch_data_response
        resp = self.api_client.fetch_data("boston", "ma")
        self.assertEqual(resp, dict(
            temperature=25.2, 
            condition="Clear", 
            condition_icon="http://icons.wxug.com/i/c/k/nt_clear.gif", 
            average_temp=38.5,
            precipitating=False))
