from fabric.api import sudo
from fabric.api import env

env.use_ssh_config = True
env.host_string = "halcyonjuly@192.168.1.174"
env.passwords = {"halcyonjuly@192.168.1.174": "Jiujitsu123"}

def shut_down():
    sudo("shutdown -r now")