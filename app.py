from flask import Flask, request, jsonify
from flask_cors import CORS
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import datetime
from flatlib import const
import traceback

app = Flask(__name__)

# 👇 GitHub Pagesだけを許可（ワイルドカードは使わない）
CORS(app, origins="*")

@app.route('/get_zodiac', methods=['POST'])
def get_zodiac():
    if request.method == 'OPTIONS':
        return '', 200  # Preflight用の応答

    try:
        data = request.get_json()
        print("📥 受け取ったデータ：", data)

        raw_date = data['date']
        time = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])

        name = data.get('name', '')
        worry = data.get('worry', '')

        date_obj = datetime.strptime(raw_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%Y/%m/%d')

        dt = Datetime(formatted_date, time, '+09:00')
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)

        result = {
            "太陽": chart.get(const.SUN).sign,
            "月": chart.get(const.MOON).sign,
            "水星": chart.get(const.MERCURY).sign,
            "金星": chart.get(const.VENUS).sign,
            "火星": chart.get(const.MARS).sign,
            "木星": chart.get(const.JUPITER).sign,
            "土星": chart.get(const.SATURN).sign,
            "アドバイス": "自分の太陽星座の個性を信じてください✨"
        }

        return jsonify(result)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
