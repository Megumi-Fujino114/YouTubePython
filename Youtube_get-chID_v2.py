# APIキーを設定
api_key = "<API-Key>"

# 検索ワード入力
search_word = input("検索ワードを入力してください > ")

# 最大50まで（50以上を指定しても取得できる件数は50件まで）
search_num = 50

# 本日日付を取得
import datetime
dt_now = datetime.datetime.today()
day_now = dt_now.strftime('%Y-%m-%d')

### Youtubeへsearch()リクエスト送信　###
#from apiclient.discovery import build
from googleapiclient.discovery import build
youtube = build("youtube","v3",developerKey=api_key)

request_s = youtube.search().list(
    part="snippet",
    type="channel",
    regionCode="JP",
    q=search_word,
    publishedBefore="2022-03-01T00:00:00Z",  # 期間指定（終了日時）
    publishedAfter="2022-01-01T00:00:00Z",   # 期間指定（開始日時）
    maxResults=search_num)

# search()リクエストの結果を取得
response_s = request_s.execute()

# search()リクエストの結果から channelId を抽出　→ リストに代入
channel_ID_list = []
for i in range(len(response_s['items'])):
    channel_ID = response_s['items'][i]['snippet']['channelId']
    channel_ID_list.append(channel_ID)


import json
jfile = day_now+"_"+search_word+".json"

#search_result = [["channelId", "subscriberCount", "viewCount", "publishedAt", "description"]]
search_result = [["channelId", "subscriberCount", "viewCount", "publishedAt"]]

### 取得した channelId の分、channels() リクエストを送信 ###
for channelID in channel_ID_list:
    request_c = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channelID
    )
    response_c = request_c.execute()

    # APIで検索した結果を全て保存（json形式）
    with open(jfile, 'a', encoding="utf-8") as f:
        json.dump(response_c, f, ensure_ascii=False, indent=2)

    # 必要項目のみ抽出
    tmp = []
    tmp.append(response_c["items"][0]["id"])
    if response_c["items"][0]["statistics"]["hiddenSubscriberCount"] == False:
        tmp.append(response_c["items"][0]["statistics"]["subscriberCount"])
    else:
        tmp.append("-")
    tmp.append(response_c["items"][0]["statistics"]["viewCount"])
    tmp.append(response_c["items"][0]["snippet"]["publishedAt"][:10])
#    tmp.append(response_c["items"][0]["snippet"]["description"])

    search_result.append(tmp)


# 検索結果から、必要項目のみcsvに保存
import csv
cfile = day_now+"_"+search_word+".csv"
with open(cfile, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerows(search_result)
