from flask import Flask, request, jsonify
from flask_cors import CORS
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/get_zodiac', methods=['POST'])
def get_zodiac():
    try:
        data = request.get_json()
        print("📥 受け取ったデータ：", data)

        raw_date = data['date']
        time = data['time']
        lat = float(data['lat'])
        lon = float(data['lon'])

        # 日付の変換
        date_obj = datetime.strptime(raw_date, '%Y-%m-%d')
        formatted_date = date_obj.strftime('%Y/%m/%d')

        print("📅 変換後の日付：", formatted_date)
        print("🕒 時間：", time)
        print("📍 緯度経度：", lat, lon)

        dt = Datetime(formatted_date, time, '+09:00')
        pos = GeoPos(lat, lon)
        chart = Chart(dt, pos)

        print("✅ チャート生成成功")

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
        print("❌ エラー内容：", e)
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
