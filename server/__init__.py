import os
from datetime import datetime

from flask import Flask, abort, session, request, redirect
from flask.json import jsonify
from flask_cors import CORS
# from flasgger import Swagger

app = Flask(__name__, template_folder="../public", static_folder="../public", static_url_path='')
credentials = {
    'username': 'apikey-v2-2ibs85wd6tef6n56oe5s8wugn9cog9r21akgg5515vdp',
    'password': '3a8350a3f76119441b1209359a576878',
    'custom_url': 'https://apikey-v2-2ibs85wd6tef6n56oe5s8wugn9cog9r21akgg5515vdp:3a8350a3f76119441b1209359a576878@c4583613-aaf0-4b6f-a936-8aaac98db589-bluemix.cloudantnosqldb.appdomain.cloud',
    'strain-list': '/chicken-strain/_design/strain/_view/list',
    'hist-list': '/historical/_design/hist/_view/list',
    'port': '50000',
    'chicken-strain': 'chicken-strain',
    'mortality': 'mortality',
    'strain': 'chicken-strain'
}
webapp = "https://app.omniofarm.com"
proxy = {'http': None, 'https': None}
auth = None

# Enable * for CORS
CORS(app, resources={r"*": {"origins": "*"}})

from server.routes import *
from server.services import *
from server.routes.index import connect_db


def log_error(status, typ):
    """Log errors to cloudant DB

    Args:
        status: message
        typ: which model type

    Returns:
        None
    """
    server_ = connect_db(url=credentials['custom_url'])
    temp = {
        "affects": typ,
        "status": status,
        "timestamp_name": datetime.utcnow().isoformat(),
        "timestamp": int(datetime.utcnow().timestamp() * 1000)
    }
    # if typ == "best-practice":
    date = datetime.utcnow().isoformat()
    if "error-logs" not in list(server_):
        server_.create("error-logs")
    db = server_['error-logs']

    if date in db:
        doc = db[date]
        doc.update(temp)
    db[date] = temp


initServices(app)
# app.config['SWAGGER'] = {
#     'title': 'OmnioFarm Local Insights APIs',
#     'uiversion': 3
# }
# swagger = Swagger(app)

if 'FLASK_LIVE_RELOAD' in os.environ and os.environ['FLASK_LIVE_RELOAD'] == 'true':
    import livereload

    app.debug = True
    server = livereload.Server(app.wsgi_app)
    server.serve(port=os.environ['port'], host=os.environ['host'])
