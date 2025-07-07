from flask import Flask, request, jsonify
from flask_cors import CORS
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import datetime  # ← 追加

app = Flask(__name__)
CORS(app)

@app.route('/get_zodiac', methods=['POST'])
def get_zodiac():
    try:
        data = request.get_json()

        # 📌 日付フォーマットを修正： '1989-10-11' → '1989/10/11'
        raw_date = data['date']
        date_obj = datetime.strptime(raw_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%Y/%m/%d')

        time = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])

        dt = Datetime(formatted_date, time, '+09:00')
        pos = GeoPos(str(lat), str(lon))
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
