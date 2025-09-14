from flask import Flask, jsonify, request, render_template
import datetime
import socket
import os


app = Flask(__name__)


@app.before_request
def log_request_info():
    print(f"Request: {request.method} {request.path} from {request.remote_addr}")


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/api/v1/info')
def info():
    return jsonify({
    	'time': datetime.datetime.now().strftime("%I:%M:%S%p  on %B %d, %Y"),
    	'hostname': socket.gethostname(),
        'message': 'You are doing great, big human!',
        'deployed_on': 'kubernetes'
    })


@app.route('/api/v1/healthz')
def health():
    return jsonify({'status': 'up'}), 200


@app.route('/api/v1/readyz')
def ready():
    # Aquí podrías chequear conexión a DB, etc.
    return jsonify({'ready': True}), 200


@app.route('/api/v1/version')
def version():
    return jsonify({'version': '1.0.0'})


@app.route('/api/v1/env')
def env():
    return jsonify({'env': os.environ.get('ENVIRONMENT', 'not set')})


if __name__ == '__main__':
    app.run(host="0.0.0.0")

