import sys  # 入出力
import urllib.request # URLアクセス
import urllib.parse # URL生成
import json    # JSON（APIの受け取り形式）


def create_current_info(json_result):
#Webサービスからの出力を解析
    info =  """現在の気象情報: 
【気温】 {}℃
【湿度】 {}%
【天気】 {}""".format(
                    json_result["current"]["temp"],
                    json_result["current"]["humidity"],
                    json_result["current"]["weather"][0]["description"]
                    )
    
    icon = json_result["current"]["weather"][0]["icon"]

    hourly_weather = []
    for hour, weather in enumerate(json_result["hourly"]):
        if (0 <= hour and hour < 24):
            if (hour+1) % 3 == 0:
                hourly_weather.append("http://openweathermap.org/img/wn/{}@2x.png".format(weather["weather"][0]["icon"]))

    return info, "http://openweathermap.org/img/wn/{}@2x.png".format(icon), hourly_weather

def create_weekly_info(index, json_result_daily, json_result):
    info = """{}日後の気象情報: 
【最高気温】 {}℃　【最低気温】 {}℃
【湿度】 {}%
【天気】 {}""".format(
                    index,
                    json_result_daily["temp"]["max"],
                    json_result_daily["temp"]["min"],
                    json_result_daily["humidity"],
                    json_result_daily["weather"][0]["description"]
                    )
    icon = json_result_daily["weather"][0]["icon"]

    hourly_weather = []
    for hour, weather in enumerate(json_result["hourly"]):
        if (index * 24 <= hour and hour < (index+1) * 24):
            if (hour+1) % 3 == 0:
                hourly_weather.append("http://openweathermap.org/img/wn/{}@2x.png".format(weather["weather"][0]["icon"]))

    return info, "http://openweathermap.org/img/wn/{}@2x.png".format(icon), hourly_weather


def create_result_info(json_result):
#Webサービスからの出力を解析
    return "lat = {}, lon = {}".format(
            json_result["lat"],
            json_result["lon"]
            )


def get_weather(lat, lon):
    # APIを通して、Webサービスを実行
    url = "https://api.openweathermap.org/data/2.5/onecall?{}".format(
        urllib.parse.urlencode(
            {
             "lat" : "{}".format(lat), 
             "lon" : "{}".format(lon),
             "units"     : "metric",
             "lang"      : "ja",
             "appid"     : "dedfc953bd7d1a40042d9d001862118a"
            }))
    print("URL:",url)
    f_url = urllib.request.urlopen(url).read()
    json_result = json.loads(f_url.decode("utf-8"))   # JSON形式の実行結果を格納
    weeklyWeather = []
    weeklyWeather.append(create_current_info(json_result))
    for day, weather in enumerate(json_result["daily"]): #enumerate → 何ループ目かがindexに格納される
        weeklyWeather.append(create_weekly_info(day+1,weather,json_result))
        if day+1 == 5:
            break

    return weeklyWeather

if __name__ == "__main__":
    weekly_weather = get_weather(35.669220,139.761457)
    for i,p,w_list in enumerate(weekly_weather):
        print(i)
        print()