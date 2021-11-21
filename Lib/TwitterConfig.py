
from twython import Twython

"""
Fungsi untuk setting twitter API
"""

#Twitter Configuration
CONSUMER_KEY    = 'consumer key anda disini'
CONSUMER_SECRET = 'consumer secret anda disini'

# Access Configuration:
ACCESS_TOKEN  = 'Akses token anda disini'
ACCESS_SECRET = 'Akses secret anda disini'


def login():

    key = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    return key 
    