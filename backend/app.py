#!/usr/bin/env python3
import os
import sys
import time
import threading
import logging
import helper.constants as const
from flask import Flask, Response, json, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from requests.exceptions import ConnectionError
from downloader import downloadAV, getAVurl, combineAV

# Setting logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Flask setup
logging.info('Init Flask')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = const.tmp_path[:-1]
cors = CORS(app)
logging.info('Adding limiter')
limiter = Limiter(app,
                  key_func=get_remote_address,
                  default_limits=["10 per hour"]
                  )
cache_dict = dict()

@app.route('/', methods = ['GET','POST'])
def generateVideoURL():
    url = ''
    try:
        url = request.form['url']
        # Cache check
        if (url in cache_dict):
            logging.info('Found {} in cache'.format(url))
            return Response(json.dumps({"download": cache_dict[url]}), mimetype='application/json', status=200)
    except (TypeError, KeyError):
        return Response(
            "No URL fiel in request body",
            status=400,
        )
    try:
        av_path = combineAV(*downloadAV(*getAVurl(url)))

        # Save for caching
        cache_dict[url] = av_path
        return Response(json.dumps({"download": av_path}), mimetype='application/json', status=200)
    except (AttributeError, KeyError, ConnectionRefusedError, ConnectionError):
        return Response(
            "No resources found at the provided URL",
            status=404,
        )
    except Exception as err:
        logging.error(err, url)
        return Response(
            "Internal Server Error. Please Inform Support",
            status=503,
        )


@app.route('/' + const.tmp_path + '<video_id>')
def page(video_id):
    logging.info('Download reqest for ' + video_id)
    vids = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(vids, video_id)


@app.route('/health')
def health():
    res = {"status": 'ok',
           "commit_sha": os.getenv('COMMIT_HASH', 'none'),
           "commit_tag": os.getenv('COMMIT_TAG', 'none')
           }
    return jsonify(res)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        appenv = os.environ.get('FLASK_ENV', 'development')
        print("Appenv", appenv)
        if appenv == 'development':
            app.testing = True
            app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

    except KeyboardInterrupt:
        print('Interrupt received! Closing...')
