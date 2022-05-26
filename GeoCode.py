import sys  # 入出力
import urllib.request # URLアクセス
import urllib.parse # URL生成
import json    # JSON（APIの受け取り形式）


def latlng(json_result):
    return json_result["Feature"][0]["Geometry"]["Coordinates"].split(",")

def site(json_result):
    return json_result["Feature"][0]["Name"]

def count(json_result):
    return json_result["ResultInfo"]["Count"]


def get_position(query):
    url = "https://map.yahooapis.jp/geocode/cont/V1/contentsGeoCoder?{}".format(
        urllib.parse.urlencode(
            {"appid"   : "Your appid",
             "query"   : "{}".format(query),
             "category": "landmark",
             "output"  : "json"                                    # レスポンス型式をJSONに指定
            }))
    print("URL:",url)
    f_url = urllib.request.urlopen(url).read()
    json_result = json.loads(f_url.decode("utf-8"))
    num_result = count(json_result)
    if num_result == 0:
        lat, lng = 140.88201194091562,38.2603041503113
        name = "仙台駅"
    else:
        lat, lng = latlng(json_result)
        name = site(json_result)
    
    return lat, lng, name, num_result

if __name__ == "__main__":
    lat, lng = get_position("仙台")
    # 出力
    print("lat={}, lng={}".format(lat, lng))
