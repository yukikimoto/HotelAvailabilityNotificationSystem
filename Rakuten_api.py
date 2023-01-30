import requests
from time import sleep
import json
import config


RAKUTEN_URL = "https://app.rakuten.co.jp/services/api/Travel/VacantHotelSearch/20170426"
RAKUTEN_API_ID = config.RAKUTEN_API_ID

WETHER_URL = 'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&lang=ja&units=metric'
WETHER_API_KEY = config.OPENWETHER_API_KEY

def rakuten_api():
    params = {
        "formatVersion":2,
        "checkinDate":"2023-02-22",
        "checkoutDate":"2023-02-23",
        "largeClassCode":"japan",
        "middleClassCode":"tiba",
        "smallClassCode":"keiyo",
        "adultNum":2,
        "sort":"standard",
        "hits":3,
        "applicationId":RAKUTEN_API_ID
    }

    res = requests.get(RAKUTEN_URL, params=params)
    result = res.json()
    
    
    URL = WETHER_URL.format(city='Kyoto,JP', key=WETHER_API_KEY)
    jsonData = requests.get(URL).json()
    temp = jsonData["main"]["temp"]
    temp_maX = jsonData["main"]["temp_max"]
    temp_min = jsonData["main"]["temp_min"]

    
    msg = "\nおはようございます。" "\n今日の京都市の気温は、 \n最高" + str(temp_maX) + "℃,最低" + str(temp_min) + "℃です。" + "\n現在の気温は" + str(temp) + "℃です。" + "\n\n今日のホテル状況を通知します。\n\n" 

    for hotel in result["hotels"]:
        hotel_name = hotel[0]["hotelBasicInfo"]["hotelName"]
        hotel_url = hotel[0]["hotelBasicInfo"]["hotelInformationUrl"]
        hotel_review = hotel[0]["hotelBasicInfo"]["reviewAverage"]
        hotel_total = hotel[1]["roomInfo"][1]["dailyCharge"]["total"]
        hotel_total2 = f'{hotel_total:,}'

        
        msg += "ホテル名：" + hotel_name + ",\n URL：" + hotel_url + ",\n レビュー評価：" + str(hotel_review) + ",\n 部屋の金額：" + str(hotel_total2) + "円" + "\n\n\n"
    msg = msg.rstrip()
    return msg
    



message = rakuten_api()

LINE_URL = 'https://notify-api.line.me/api/notify'
LINE_API_TOKEN = config.LINE_NOTIFY_KEY

headers = {'Authorization': f'Bearer {LINE_API_TOKEN}'}
data = {'message': f'{message}'}
requests.post(LINE_URL, headers=headers, data=data)