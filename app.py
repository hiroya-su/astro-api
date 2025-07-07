from flask import Flask, request, jsonify
from flask_cors import CORS
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import datetime
import traceback
from flask_cors import CORS

# CORS設定を厳密に記述
CORS(app, resources={r"/get_zodiac": {"origins": "https://hiroya-su.github.io"}}, supports_credentials=True)



@app.route('/get_zodiac', methods=['POST'])
def get_zodiac():
    try:
        data = request.get_json()
        print("📥 受け取ったデータ：", data)

        raw_date = data['date']
        time = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])

        # name や worry は使わないが、エラー防止で受け取る
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
        print("❌ エラー内容（str）:", str(e))
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
