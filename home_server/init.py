from django.core.management.utils import get_random_secret_key
import os
import sys

with open('home_server/.env', 'a') as env:

    # Write new
    if not("SECRET_KEY" in os.environ):
        # os.environ.putenv("SECRET_KEY", get_random_secret_key())
        # os.environ['SECRET_KEY'] = get_random_secret_key()

        SECRET_KEY = get_random_secret_key()

        env.write("# Secret Key \n")
        env.write("SECRET_KEY=" + SECRET_KEY + "\n")

    try:
        mode = sys.argv[1]
        if mode == 'dev':
            os.environ['DEBUG'] = 'True'
            env.write("# Debug \n")
            env.write("DEBUG=" + 'True' + "\n")
        if mode == 'deploy':
            os.environ['DEBUG'] = 'False'
            env.write("# Debug \n")
            env.write("DEBUG=" + 'False' + "\n")
    except:
        pass
