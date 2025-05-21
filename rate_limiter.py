from flask import Flask, request, jsonify
from datetime import datetime, timedelta

rate_limit = {
    "default" : {
        "count" : 2,
        "time_interval" : 5,
        "clients": {}
    },
    "endpoint1" : {
        "count" : 1,
        "time_interval" : 5,
        "clients": {}
    },
}


def is_limit_exceeded(requests_list, client, present_time_stamp):
    min_timestamp_allowed = present_time_stamp - requests_list["time_interval"]
    count =0
    for item in reversed(requests_list["clients"][client]):
        count += 1
        if item > min_timestamp_allowed:
            if count - 1>= requests_list["count"]:
                return True
            continue
        else:
            return False
    return False
    
class Middleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        with app.request_context(environ):
            # Code to be executed before the request is processed
            endpoint = request.endpoint
            if endpoint in rate_limit:
                rate_limit_config = endpoint
            else:
                rate_limit_config = "default"
            present_time_stamp = datetime.now().timestamp()
            # Client will be picked from X-Api-Key in header if present else ip of the request
            client = request.headers.get('X-Api-Key', request.remote_addr)
            if client not in rate_limit[rate_limit_config]["clients"]:
                rate_limit[rate_limit_config]["clients"][client] = []
            rate_limit[rate_limit_config]["clients"][client].append(present_time_stamp)
            if is_limit_exceeded(rate_limit[rate_limit_config], client, present_time_stamp):
                res = jsonify({"error": "Rate limit exceeded"})
                start_response('429 TOO MANY REQUESTS', [('Content-Type', 'application/json')])
                return [res.get_data()]
        # Process the request and get the response
        response = self.app(environ, start_response)
        # Code to be executed after the request is processed
        return response


app = Flask(__name__)
app.wsgi_app = Middleware(app.wsgi_app)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/endpoint1')
def endpoint1():
    return jsonify({"message": "This is endpoint1", "request" : rate_limit}), 200

@app.route('/endpoint2')
def endpoint2():
    return jsonify({"message": "This is endpoint2", "request" : rate_limit}), 200

if __name__ == '__main__':
    app.run(debug=True)