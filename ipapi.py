import sys  # 入出力
import urllib.request # URLアクセス
import urllib.parse # URL生成
import json    # JSON（APIの受け取り形式）


def create_result_info(json_result):
    return json_result["latitude"], json_result["longitude"]


def get_position():
    url = "https://ipapi.co/json/"
    f_url = urllib.request.urlopen(url).read()
    json_result = json.loads(f_url.decode("utf-8"))
    lat, lng = create_result_info(json_result)
    
    return lat, lng

if __name__ == "__main__":
    lat, lng = get_position()
    # 出力
    print("lat={}, lng={}".format(lat, lng))