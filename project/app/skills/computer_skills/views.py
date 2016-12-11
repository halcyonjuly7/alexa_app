from project import ask
from .fabfile import shut_down

@ask.intent("comp_off")
def comp_off():
    shut_down()
