
import sys  # 入出力
import urllib.request # URLアクセス
import urllib.parse # URL生成
import json    # JSON（APIの受け取り形式）
from urllib.error import URLError


def create_hotel_info(index, hotel):

#Webサービスからの出力を解析
    if (hotel["hotelBasicInfo"]["hotelMinCharge"] == None):
        info =  """No. {}: 
【店名】 {}
【施設特色】 {}
【最安料金】 施設情報ページから確認してください。""".format(index, # No.
                    hotel["hotelBasicInfo"]["hotelName"], # 店名
                    hotel["hotelBasicInfo"]["hotelSpecial"]
                    )
    else:
        info =  """No. {}: 
    【店名】 {}
    【施設特色】 {}
    【最安料金】 {}円""".format(index, # No.
                        hotel["hotelBasicInfo"]["hotelName"], # 店名
                        hotel["hotelBasicInfo"]["hotelSpecial"], 
                        hotel["hotelBasicInfo"]["hotelMinCharge"]
                        )
    hotel_image_url = hotel["hotelBasicInfo"]["hotelImageUrl"]
    hotel_room_url = hotel["hotelBasicInfo"]["roomImageUrl"]
    hotel_url = hotel["hotelBasicInfo"]["hotelInformationUrl"]
    return info, hotel_image_url, hotel_room_url, hotel_url



def create_result_info(json_result):
#Webサービスからの出力を解析
    return "-------- 付近に{}件のホテルが見つかりました。最初の{}件を表示します。 --------".format(
            json_result["pagingInfo"]["recordCount"], # ~件のレストランが・・・
            json_result["pagingInfo"]["last"]   # 最初の~件を・・・
            )


def search_hotel(lat, lng):
    # APIを通して、Webサービスを実行
    url = "https://app.rakuten.co.jp/services/api/Travel/SimpleHotelSearch/20170426?{}".format(
        urllib.parse.urlencode(
            {"applicationId"   : "1010432289426825145",
             "format"          : "json",
             "latitude"        : "{}".format(lat),
             "longitude"       : "{}".format(lng),
             "searchRadius"    : "3",
             "datumType"       : "1"
            }))
    print("URL:",url)
    try:
        f_url = urllib.request.urlopen(url).read()
    except URLError as e:
        if hasattr(e, 'reason'):
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        elif hasattr(e, 'code'):
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        hotel_list = []

        result_info = "-------- 付近に0件のホテルが見つかりました。最初の0件を表示します。 --------"


    else:
        json_result = json.loads(f_url.decode("utf-8"))   # JSON形式の実行結果を格納
        hotel_list = []

        for index, hotel in enumerate(json_result["hotels"]): #enumerate → 何ループ目かがindexに格納される
            hotel_list.append(create_hotel_info(index+1,hotel["hotel"][0]))
        
        result_info = create_result_info(json_result)
    
    return hotel_list, result_info

if __name__ == "__main__":
    h_list, result_info = search_hotel(42.7909779,140.2289796)
    for i, p, rp, u in h_list:
        print("{}:{}".format(i,rp))