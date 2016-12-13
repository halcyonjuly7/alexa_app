from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.automap import automap_base
#
# base = automap_base()
# engine = create_engine("mysql+pymysql://odroid:Jiujitsu123@192.168.1.211/movies")
# base.prepare(engine, reflect=True)
# Session = sessionmaker(bind=engine)
# session = scoped_session(Session)
# movie_info = base.classes["movie_info"]



class BaseModelHandler:

    def __init__(self, uri):
        self.base = automap_base()
        self._engine = create_engine(uri)




class ModelHandler:
    def __init__(self, uri):
        self._engine = create_engine(uri)
        self._base = automap_base()
        self._base.prepare(self._engine, reflect=True)
        self.scoped_session = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.scoped_session.remove()

    def get_session(self):
        session_factory = sessionmaker(bind=self._engine)
        self.scoped_session = scoped_session(session_factory)
        return self.scoped_session()

    def get_model(self, model_name):
        return self._base.classes.get(model_name)

