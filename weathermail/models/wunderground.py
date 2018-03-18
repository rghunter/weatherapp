import requests

class WundergroundAPIException(Exception):
    pass

class InvalidLocationException(WundergroundAPIException):
    """
    raised when a given location fails validation
    """
    pass

class WundergroundAPI(object):

    def __init__(self, api_key):
        self.api_key = api_key


    @staticmethod
    def join_features(data_features):
        """
        take a list of datafeatures and return a list the API will accept
        i.e. ['a', 'b'] becomes a/b
        """
        if not isinstance(data_features, list):
            raise WundergroundAPIException("data_features must be a list of features")
        return "/".join(data_features)

    def api_call_datafeature(self, data_features, city, state):
        resp = requests.get("http://api.wunderground.com/api/{api_key}/{data_feature_string}/q/{state}/{city}.json".format(
            api_key=self.api_key, data_feature_string=self.join_features(data_features), city=city, state=state))

        # Check that we get a 200 status code
        if not resp.status_code == 200:
            raise WundergroundAPIException("API returned: {} Mesasge: {}".format(resp.status_code, resp.text))
        parsed_response = resp.json()['response']

        # Wunderground API validation always returns a 200 status code, but will include an errors key if errors are present in the request
        if "error" in parsed_response.keys():
            raise WundergroundAPIException("API returned an error: {}".format(parsed_response['error']['type']))

        # Check if the location is valid. If geolookup fails, we will get a results key in the response object
        if "results" in parsed_response.keys():
            raise InvalidLocationException("The location you provided failed geolookup: city: {} state: {}".format(city, state))

        return resp.json()

    def __avg_temp(self, almanac):
        def temp(t):
            return t['normal']['F']
        high = float(temp(almanac['temp_high']))
        low = float(temp(almanac['temp_low']))
        return (high+low)/2.0

    def fetch_data(self, city, state):
        """ Wunderground API conditions and Almanac data
        for a given city and state, return the current weather conditions and historical temps
        API Docs: https://www.wunderground.com/weather/api/d/docs?d=data/conditions
        API Docs: https://www.wunderground.com/weather/api/d/docs?d=data/almanac

        :param city: string (the city)
        :param state: string (the state shortcode i.e MA for massachusetts)
        :return current temp, average temp, conditions, condition icon
        {
            "temperature": <temp in farenhieght>
            "condition": <condition string>
            "condition_icon": <condition icon>
            "average_temp": <float mean temperature> 
        }
        """
        resp = self.api_call_datafeature(["almanac","conditions"], city, state)
        conditions = resp['current_observation']

        return dict(
                temperature=conditions['temp_f'],
                condition=str(conditions['weather']),
                condition_icon=str(conditions['icon_url']),
                average_temp=self.__avg_temp(resp["almanac"])
                )


