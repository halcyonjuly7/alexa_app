import logging
import abc


class SourceMapper(metaclass=abc.ABCMeta):

    def __init__(self, target_attribute):
        """

        :param target_attribute: the attribute to get from the json_source
        :type target_attribute: str
        """
        self.target_attribute = target_attribute

    @abc.abstractmethod
    def get_mapped_attribute(self):
        pass


class OmdbSourceMapper(SourceMapper):
    def get_mapped_attribute(self):
        logging.debug("**************************" + self.target_attribute)
        if self.target_attribute in ("duration", "runtime", "length", "run time"):
            return "runtime"
        elif self.target_attribute in ("actors", "actor", "actress", "actresses"):
            return "actors"
        elif self.target_attribute in ("story", "plot", "overview", "synopsis"):
            return "plot"

        elif self.target_attribute in ("rating", "score", "review"):
            return "imdbrating"

        elif self.target_attribute in ("genre",):
            return "genre"

        elif self.target_attribute in ("year",):
            return "year"

        elif self.target_attribute in ("awards", "nominations"):
            return "awards"

        elif self.target_attribute in ("country", "origin"):
            return "country"

        elif self.target_attribute in ("director", "directors"):
            return "director"

