import abc
from flask_ask import session
import logging

logging.basicConfig(level=logging.DEBUG)


class BaseHandler(metaclass=abc.ABCMeta):
    def __init__(self, data):
        self._data = data
        self._source_mapper = None
        self._response_formatter = None

    def set_source_mapper(self, source_mapper):
        self._source_mapper = source_mapper

    def set_response_formatter(self, data_formatter):
        self._response_formatter = data_formatter

    @abc.abstractmethod
    def get_response(self, attribute):
        pass


class JsonHandler(BaseHandler, metaclass=abc.ABCMeta):
    def __init__(self, target=None, data=None):
        super().__init__(data)
        self._target = target

    def get_response(self, attribute):
        return self._get_attribute_data(attribute)

    @abc.abstractmethod
    def _get_attribute_data(self, attribute):
        pass


class OmdbSourceHandler(JsonHandler):

    def _get_default_response(self):
        if not self._target:
            response = "I don't think you mentioned what movie. Can you repeat that?"
        else:
            response = "I didn't get what you wanted me to look up for {0}. Can you repeat that?".format(self._target)
        return response

    def _get_attribute_data(self, attribute):
        mapped_source = self._source_mapper.get_mapped_attribute()
        logging.debug("--------------------" + str(self._target))
        logging.debug("+++++++++++++++++++++++++" + str(self._source_mapper.get_mapped_attribute()))
        response = self._get_default_response()
        if self._target:
                data_format = self._response_formatter.format_data(self._target, self._data[mapped_source])
                misc_response = " is there anything else you'd like to know about {0} besides the {1}?".format(self._target,
                                                                                                               attribute)
                response = data_format + misc_response
        return response


class SQLHandler(BaseHandler, metaclass=abc.ABCMeta):
    def get_response(self, attribute):
        return self._get_model_data(attribute)

    @abc.abstractmethod
    def _get_model_data(self, attribute):
        pass


class MovieInfoSourceHandler(SQLHandler):

    def _get_default_response(self):
        pass

    def get_response(self, attribute):
        self.data


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


