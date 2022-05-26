from flask import Flask, render_template, request
from GeoCode import get_position
from weather import get_weather
from gourmet import search_gourmet
from hotel import search_hotel
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get():
    return render_template('index.html', \
        title = '旅info', \
        message = '旅行先の観光名所などの場所を入力してください。', \
        image_url = "https://thumb.ac-illust.com/ea/ea09aa9543f600c2f3cd7a78b4e2cb52_t.jpeg")

@app.route('/', methods=['POST'])
def post():
    #time.sleep(2)
    place = request.form['place']
    lng, lat, name, count = get_position(place)
    w_list = get_weather(lat, lng)
    g, g_result = search_gourmet(lat, lng)
    h, h_result = search_hotel(lat, lng)

    return render_template('index.html', \
        title = '旅info', \
        geo_count = count, \
        message = '{}（{}）付近の情報を表示します。'.format(place, name), \
        weather_message = '{}（{}）の天気'.format(place, name), \
        weekly_weather = w_list, \
        gourmet_result = '{}'.format(g_result), \
        gourmet_message = '画像をクリックすると店舗情報ページを開きます。', \
        gourmet = g, \
        hotel_result = '{}'.format(h_result), \
        hotel_message = '画像をクリックすると施設情報ページを開きます。', \
        hotel = h)
            

if __name__ == '__main__':
    app.run()