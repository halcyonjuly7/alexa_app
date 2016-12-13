import requests
import json
import abc

from datetime import datetime, timedelta
from ..db.models import ModelHandler
from  sqlalchemy import func

import logging

logging.basicConfig(level=logging.DEBUG)

class NoMovieError(Exception):
    pass


class SourceCaller(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_data(self, **kwargs):
        pass


class JsonDataSourceCaller(SourceCaller, metaclass=abc.ABCMeta):
    def get_data(self, **kwargs):
        response = self._get_response(**kwargs)
        self._check_error(response)
        new_data = {key.lower(): value for key, value in response.items()}
        return new_data

    def _get_response(self, **kwargs):
        return json.loads(requests.get(self._get_url(), params=kwargs).text)

    @abc.abstractmethod
    def _get_url(self):
        pass

    @abc.abstractmethod
    def _check_error(self, response):
        pass


class OmdbSourceCaller(JsonDataSourceCaller):
    def get_data(self, **kwargs):
        kwargs.update({"r": "json"})
        return super().get_data(**kwargs)

    def _get_url(self):
        return  "http://www.omdbapi.com"

    def _check_error(self, response):
        if "Error" in response:
            raise NoMovieError("Cannot find data for {0} ".format(response.get("t")))


class SQLDataSourceCaller(SourceCaller, metaclass=abc.ABCMeta):
    def __init__(self, uri=None):
        self._model_handler = ModelHandler(uri)

    def get_data(self, **kwargs):
        return self._query_model(**kwargs)

    def _get_model(self, model_name):
        return self._model_handler.get_model(model_name)

    @abc.abstractmethod
    def _query_model(self, model_name=None, query_type=None):
        pass

    def _to_dict(self, models, attributes=None):
        data = []
        for model in models:
            item = {}
            for attribute in attributes:
                item[attribute] = getattr(model, attribute)
            data.append(item)
        return data


class MovieInfoSourceCaller(SQLDataSourceCaller):

    def _query_model(self, model_name=None, query_type=None):
        if query_type == "movie_list":
            result = self._get_movies(model_name)
            return self._to_dict(result, attributes=("movie", "showtimes"))

    def _get_movie_list(self, model_name, date):
        with self._model_handler as handler:
            session = handler.get_session()
            model = self._model_handler.get_model(model_name)
            movie_list = session.query(model.movie, func.group_concat(model.showtimes).label("showtimes")).filter(model.date == date)\
                                             .distinct(model.movie)\
                                             .group_by(model.movie)\
                                             .all()
        return movie_list

    def _get_movies(self, model_name):
        date_now = datetime.now().date()
        movie_list = self._get_movie_list(model_name, date_now)
        if not movie_list:
            movie_list = self._get_movie_list(model_name, date_now - timedelta(days=1))
        return movie_list





