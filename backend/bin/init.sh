pip3 install gunicorn
#Create and activate virtual environment
python3 -m venv .
# create gunicorn_start em run $ bin/gunicorn_start
# When you run your gunicorn_start script it will create one socket in the run/ directory. This socket you will use in nginx.
pip3 install setproctitle
