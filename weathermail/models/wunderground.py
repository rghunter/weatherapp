import requests


class InvalidLocation(Exception):
    """
    raised when a given location fails validation
    """
    pass

class WundergrounAPI(object):

    def __init__(self, api_key):
        self.api_key = api_key


    def __api_call(self, data_feature, city, state):
        if len(state) > 2:  # Not a very smart validator, but this will catch scenarios where state name instead of state apprv is used
            raise InvalidLocation("Invalid State: {}. Make sure your useing the shortcode (ie. MA for Massachuesetts)".format(state))
        return requests.get("http://api.wunderground.com/api/{api_key}/{data_feature}/q/{state}/{city}.json".format(
                api_key=self.api_key, data_feature=data_feature, city=city, state=state)).json()

    def conditions(self, city, state):
        """ Wunderground API conditions
        for a given city and state, return the current weather conditions
        API Docs: https://www.wunderground.com/weather/api/d/docs?d=data/conditions
        :param city: string (the city)
        :param state: string (the state shortcode i.e MA for massachusetts)
        :return current temp, average temp, conditions, condition icon
        {
            "temperature": <temp in farenhieght>
            "conditions": <condition string>
            "condition_icon": <condition icon>
        }
        """
        pass


    def historical(self, city, state):
        """
        Get the historical average temperature for a given location

        I generate an average temperature by taking the mean of the average high and low

        :param city: string (the city)
        :param state: string (the state shortcode i.e MA for massachusetts)
        :return { "average_temp": <float mean temperature> }
        """
        resp = self.__api_call(data_feature="almanac", city=city, state=state)
        pass
