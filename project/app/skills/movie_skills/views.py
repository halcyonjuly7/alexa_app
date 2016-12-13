import logging

from flask_ask import question, statement

from project import ask
from project.app.utils.formatters import OmdbDataFormatter
from project.app.utils.handlers import OmdbSourceHandler, SessionHandler
from project.app.utils.mappers import OmdbSourceMapper
from project.app.utils.source_callers import NoMovieError, OmdbSourceCaller, MovieInfoSourceCaller


@ask.launch
def launch():
    greeting = "what would you like today?"
    return question(greeting)


@ask.intent("movie_list")
def get_movies():
    """
    :return:
    """
    source_caller = MovieInfoSourceCaller(uri="mysql+pymysql://odroid:Jiujitsu123@192.168.1.211/movies")

    movie_list = source_caller.get_data(model_name="movie_info", query_type="movie_list")
    movie_names = [movie["movie"] for movie in movie_list]
    answer = ";".join(["the movies are ", *movie_names])
    SessionHandler.set_attribute("movie_list", movie_list)
    logging.debug(movie_list)
    return statement(answer)






@ask.intent("movie_choice")
def movie_choice():
    response = "What movie would you like me to look up?"
    return question(response)


@ask.intent("movie_lookup")
def lookup_movie(movie):
    SessionHandler.set_attribute("has_session", True)
    SessionHandler.set_attribute("movie_context", movie)
    movie_handler = OmdbSourceCaller()
    try:
        SessionHandler.set_attribute("movie_data", movie_handler.get_data(t=movie, plot="short"))
        response = "I've found {movie} what would you like to know about {movie}?".format(movie=movie)
    except NoMovieError as error:
        logging.debug("---------------- Here in No Movie Error")
        logging.debug(error)
        SessionHandler.pop_attributes("has_session", "movie", "movie_data")
        response = "It seems that I could not find anything for {0}. could you say that again?".format(movie)
    return question(response)


@ask.intent("movie_info")
def get_movie_info(target):
    movie_context = SessionHandler.get_attribute("movie_context")
    movie_handler = OmdbSourceHandler(target=movie_context, data=SessionHandler.get_attribute("movie_data"))
    movie_handler.set_response_formatter(OmdbDataFormatter(target))
    movie_handler.set_source_mapper(OmdbSourceMapper(target))
    try:
        response = movie_handler.get_response(target)
    except KeyError as exception:
        logging.debug("---------------- Here in type Key error")
        logging.debug(exception)
        response = "I could not find {0} for {1}. could you say that again?".format(target,
                                                                                    movie_context)
    return question(response)


@ask.intent("movie_lookup_another")
def get_lookup_another_movie():
    return question("What other movie do you want me to look up?")



@ask.intent("no_more_info")
def no_more_info():
    has_session = SessionHandler.get_attribute("has_session")
    if has_session:
        SessionHandler.pop_attributes("has_session", "movie", "movie_data")
        return question("Is there anything else you'd like to do today?")
    else:
        return statement("Ok Bye")


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Goodbye")


@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement("Goodbye")


@ask.session_ended
def session_ended():
    return "", 200

