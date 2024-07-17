import string
import random as r
from datetime import datetime
 
 
def generating_secret_key():
    random_ascii = [r.choice(string.ascii_letters) for i in range(10)] + [r.choice(string.digits) for i in
                                                                          range(10)]
    new_random_ascii = ''.join(random_ascii)
    return new_random_ascii
 
 
def copyright_year():
    year = datetime.now().strftime('%Y')
    return year