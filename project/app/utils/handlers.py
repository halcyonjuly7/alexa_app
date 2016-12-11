import requests
import json
import abc
from flask_ask import session
import logging
logging.basicConfig(level=logging.DEBUG)

class NoMovieError(Exception):
    pass


class BaseApiCaller(metaclass=abc.ABCMeta):
    def __init__(self, target):
        self._target = target

    @abc.abstractmethod
    def get_data(self, **kwargs):
        pass


class MoviesApiCaller(BaseApiCaller):
    def get_data(self, **kwargs):
        data = {
            "t": self._target,
            "r": "json"
        }
        data.update(**kwargs)
        response = json.loads(requests.get("http://www.omdbapi.com", params=data).text)
        if "Error" in response:
            raise NoMovieError("Cannot find data for {0} ".format(self._target))
        new_data = {key.lower():value for key, value in response.items()}
        return new_data


class BaseHandler(metaclass=abc.ABCMeta):
    def __init__(self, target=None, data=None):
        self._target = target
        self._data = data
        self._source_mapper = None
        self._response_formatter = None

    @abc.abstractmethod
    def set_source_mapper(self, source_mapper):
        pass

    @abc.abstractmethod
    def set_response_formatter(self, data_formatter):
        pass

    @abc.abstractmethod
    def _get_default_response(self):
        pass

    @abc.abstractmethod
    def get_response(self, json_data, attribute):
        pass


class MovieHandler(BaseHandler):
    def __init__(self, target=None, data=None):
        self._target = target
        self._data = data
        self._source_mapper = None
        self._response_formatter = None

    def set_source_mapper(self, source_mapper):
        self._source_mapper = source_mapper

    def set_response_formatter(self, data_formatter):
        self._response_formatter = data_formatter

    def _get_default_response(self):
        if not self._target:
            response = "I don't think you mentioned what movie. Can you repeat that?"
        else:
            response = "I didn't get what you wanted me to look up for {0}. Can you repeat that?".format(self._target)
        return response

    def get_response(self, attribute):
        mapped_source = self._source_mapper.get_mapped_attribute()
        logging.debug("--------------------" + str(self._target))
        logging.debug("+++++++++++++++++++++++++" + str(self._source_mapper.get_mapped_attribute()))
        response = self._get_default_response()
        if self._target:
                data_format = self._response_formatter.format_data(self._target, self._data[mapped_source])
                misc_response = " is there anything else you'd like to know about {0} besides the {1}?".format(self._target,
                                                                                                               attribute)
                response=data_format + misc_response
        return response





class SessionHandler:
    @staticmethod
    def set_attribute(key, value):
        session.attributes[key] = value

    @staticmethod
    def get_attribute(key):
        return session.attributes.get(key)

    @staticmethod
    def pop_attributes(*attributes):
        for attribute in attributes:
            try:
                session.attributes.pop(attribute)
            except KeyError as exception:
                logging.debug(exception)


