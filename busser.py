import requests

from flask import jsonify
from flask import Flask
from flask_cors import CORS, cross_origin
from notify_thread import NotifyThread

app = Flask(__name__, static_url_path='')
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Notification Thread
notify_t = None

@app.route('/')
def index():
    print 'index'
    return app.send_static_file('index.html')

@app.route('/eta/<route_request>/<stop_request>')
@cross_origin()
def get_stop(route_request, stop_request):

    # Look through stops to find ID by given name
    try:
        stops = requests.get('http://citybus.doublemap.com/map/v2/stops').json()
        stop = next(stop['id'] for stop in stops if stop_request in stop['name'])
    except Exception:
        return "Error getting stop.", 404

    # Get etas if stop by stop ID
    try:
        etas = requests.get('http://citybus.doublemap.com/map/v2/eta?stop=%s' % stop).json()
    except Exception:
        return "Error getting ETAs.", 500

    # Actual ETAs for stop and given route is in [etas][stop_id][etas]
    real_etas = etas['etas'][str(stop)]['etas']

    # Turn into simple array of etas
    nice_etas = [e['avg'] for e in real_etas if route_request == str(e['route'])]

    return jsonify(results=nice_etas)

@app.route('/eta/<route_request>/<stop_request>/notify', methods=["POST"])
@cross_origin()
def post_notify_stop(route_request, stop_request):
    try:
        global notify_t

        # Stop other notification thread if it's running
        if notify_t is not None:
            notify_t.running = False
            notify_t.join()

        # Start new notifiy thread for current request
        notify_t = NotifyThread(route_request, stop_request)
        notify_t.start()
    except:
        return jsonify(success=False), 500

    return jsonify(success=True)

@app.route('/routes/')
@cross_origin()
def get_routes():
    try:
        routes_data = requests.get("http://citybus.doublemap.com/map/v2/routes").json()
    except Exception:
        return "Error getting routes.", 500

    # Map routes to relevant information
    routes = [{
               "name": r['name'],
               "short_name": r['short_name'],
               "id": r['id']
              } for r in routes_data]

    return jsonify(results=routes)

@app.route('/route/<route_request>/')
@cross_origin()
def get_route(route_request):
    try:
        routes_data = requests.get("http://citybus.doublemap.com/map/v2/routes").json()
    except Exception:
        return "Error getting routes.", 500

    # Filter Routes by Request, map to nicer info
    routes = [{
              "name": r['name'],
              "short_name": r['short_name'],
              "id": r['id']
              } for r in routes_data if r['short_name'].lower() == route_request.lower()]

    return jsonify(results=routes)


app.run(debug=False, host='0.0.0.0', port=4000, threaded=True)
