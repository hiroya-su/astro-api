from flask import Flask, request, jsonify
from flask_cors import CORS
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

app = Flask(__name__)
CORS(app)

@app.route('/get_zodiac', methods=['POST'])
def get_zodiac():
    try:
        data = request.get_json()
        date = data['date']
        time = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])

        dt = Datetime(date, time, '+09:00')
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)

        result = {
            "太陽": chart.get("SUN").sign,
            "月": chart.get("MOON").sign,
            "水星": chart.get("MERCURY").sign,
            "金星": chart.get("VENUS").sign,
            "火星": chart.get("MARS").sign,
            "木星": chart.get("JUPITER").sign,
            "土星": chart.get("SATURN").sign,
            "アドバイス": "自分の太陽星座の個性を信じてください✨"
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
