"""
レストラン検索サンプルプログラム
# python search_gourmet_json.py 仙台 ラーメン ・・・
"""

import sys  # 入出力
import urllib.request # URLアクセス
import urllib.parse # URL生成
import json    # JSON（APIの受け取り形式）


def create_gourmet_info(index, shop):
#Webサービスからの出力を解析
    info =  """No. {}: 
【店名】 {}
【キャッチ】 {}
【営業時間】 {}""".format(index, # No.
                    shop["name"], # 店名
                    shop["catch"], 
                    shop["open"]# 営業時間
                    )
    photo_url = shop["photo"]["pc"]["l"]
    shop_url = shop["urls"]["pc"]

    return info, photo_url, shop_url


def create_result_info(json_result):
#Webサービスからの出力を解析
    return "-------- 付近に{}件のレストランが見つかりました。最初の{}件を表示します。 --------".format(
            json_result["results"]["results_available"], # ~件のレストランが・・・
            json_result["results"]["results_returned"]   # 最初の~件を・・・
            )


def search_gourmet(lat, lng):
    # APIを通して、Webサービスを実行
    url = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/?{}".format(
        urllib.parse.urlencode(
            {"key"     : "Your API key",                         # APIキー(このキーはダミー．自分で取得したものを記入。db*3+9)
             "lat"     : "{}".format(lat),
             "lng"     : "{}".format(lng),
             "range"   : "5",
             "count"   : "30",
             "format"  : "json"                                    # レスポンス型式をJSONに指定
            }))
    print("URL:",url)
    f_url = urllib.request.urlopen(url).read()
    json_result = json.loads(f_url.decode("utf-8"))   # JSON形式の実行結果を格納
    gourmet = []

    for index, shop in enumerate(json_result["results"]["shop"]): #enumerate → 何ループ目かがindexに格納される
        gourmet.append(create_gourmet_info(index+1,shop))

    return gourmet, create_result_info(json_result)

if __name__ == "__main__":
    gourmet = search_gourmet(35.669220,139.761457)
    for i in range(3):
        print(gourmet[i])
