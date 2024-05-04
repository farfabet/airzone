from AirzoneCloud import AirzoneCloud
import logging, json
import time
from flask import Flask, request
import threading


def run(airzone:AirzoneCloud):
    while True:
        for dev in airzone.all_devices:
            dev.refresh()
            print(dev)
        time.sleep(60)

def mode_to_int(is_on:bool, mode:str):
    if not is_on:
        return 0
    elif mode == "heating":
        return 1
    elif mode == "cooling":
        return -1
    else:
        return 0

def create_app(airzone:AirzoneCloud):
    _az=airzone
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    @app.errorhandler(404)
    def page_not_found(e):
        return '404'

    @app.errorhandler(405)
    def invalid_method(e):
        return '405'

    @app.route('/stats',)
    def stats():
        if 'application/json' in request.headers.get('Accept', ''):
            return [ (lambda dev: {
                'name': dev.name, 
                'mode': mode_to_int(dev.is_on,dev.mode), 
                'current':dev.current_temperature, 
                'target':dev.target_temperature})(dev)
                  for dev in _az.all_devices ]
        elif 'text/lineprotocol' in request.headers.get('Accept', ''):
            return '\n'.join(f'{dev.name} mode={mode_to_int(dev.is_on,dev.mode)},current={dev.current_temperature},target:{dev.target_temperature}' for dev in _az.all_devices)
        else:
            return '\n'.join(f'{dev.name}({dev.is_on}):{dev.mode},{dev.current_temperature}->{dev.target_temperature}' for dev in _az.all_devices)
    return app

def web(az:AirzoneCloud):
    app=create_app(airzone=az)
    app.run(debug=True, use_reloader=False, host='127.0.0.1', port=8081)

if __name__ == "__main__":  # pragma: no cov
    config = json.load(open("config.json"))
    logging.basicConfig(level=config.get("log_level", "INFO"))
    az = AirzoneCloud(config.get("email"), config.get("password"))
    threading.Thread(target=run, daemon=True, kwargs={'airzone':az}).start()
    web(az)