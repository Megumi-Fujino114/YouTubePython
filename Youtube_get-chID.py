##### ユーザ指定範囲 ↓ここから↓ #####
# APIキーを設定
api_key = "<API-Key>"

# 最大50まで（50以上を指定しても取得できる件数は50件まで）
search_num = 50

# チャンネル開設日の期間指定
# 期間開始日(yyyy-mm-dd の形式で指定)
range_start = "2022-01-01"

# 期間終了日(yyyy-mm-dd の形式で指定)
range_end = "2022-04-01"

##### ユーザ指定範囲 ↑ここまで↑ #####

# ライブラリをインポート
import datetime
import re
import json
import csv
import os
#from apiclient.discovery import build
from googleapiclient.discovery import build


# 本日日付を取得
now = datetime.datetime.now()
today = now.strftime('%Y-%m-%d')

# 検索ワード入力（プログラム実行後、入力プロンプトを表示）
search_word = input("検索ワードを入力してください > ")

# 保存ファイル名（yyyy-mm-dd_検索ワード.ファイル拡張子）
if search_word == "":
    jfile = today+"_NoKeyword.json"
    cfile = today+"_NoKeyword.csv"
else:
    jfile = today+"_"+search_word+".json"
    cfile = today+"_"+search_word+".csv"


# 関数：URL形式の文字列のみ抽出してリターン
def FindURL(string): 
    # findall() URL形式の合致する文字列を抽出する
    url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+.+', string)
    return url

### Youtubeからの情報取得　###
youtube = build("youtube","v3",developerKey=api_key)

# search()リクエスト送信　#
request_s = youtube.search().list(
    part = "snippet",
    type = "channel",
    regionCode = "JP",
    q = search_word,
    publishedBefore = range_end+"T00:00:00Z",  # 指定日時より前に登録されたchを検索
    publishedAfter = range_start+"T00:00:00Z", # 指定日時より後に登録されたchを検索
    maxResults = search_num)

# search()リクエストの結果を取得
response_s = request_s.execute()

# search()リクエストの結果から channelId を抽出　→ リストに代入
channel_ID_list = []
for i in range(len(response_s['items'])):
    channel_ID = response_s['items'][i]['snippet']['channelId']
    channel_ID_list.append(channel_ID)

# csvファイルのヘッダと、検索結果格納用リスト
csv_header = [["channelId", "subscriberCount", "viewCount", "publishedAt", "Twitter", "Instagram", "Facebook", "TikTok", "LINE"]]
search_result = []

### 取得した channelId を使って、1件ずつ channels() リクエストを送信 ###
for channelID in channel_ID_list:
    request_c = youtube.channels().list(
        part = "snippet, contentDetails, statistics",
        id = channelID
    )

    # channels()リクエストの結果を取得
    response_c = request_c.execute()

    # channels()リクエストの結果をjson形式で保存
    with open(jfile, 'a', encoding="utf-8") as f:
        json.dump(response_c, f, ensure_ascii=False, indent=2)

    # csvファイルに保存する情報をリストに格納
    tmp = ["-", "-", "-", "-", "-", "-", "-", "-", "-"]
    tmp[0] = response_c["items"][0]["id"]
    if response_c["items"][0]["statistics"]["hiddenSubscriberCount"] == False:
        tmp[1] = response_c["items"][0]["statistics"]["subscriberCount"]
    else:
        tmp[1] = "-"
    tmp[2] = response_c["items"][0]["statistics"]["viewCount"]
    tmp[3] = response_c["items"][0]["snippet"]["publishedAt"][:10]

    # FindURL()関数で、descriptionから、URLのみ抽出（抽出したURLがリストでリターンされる）
    desc = response_c["items"][0]["snippet"]["description"]
    sns = FindURL(desc)

    # 抽出したURLのリストから、SNSアカウントのみリスト格納
    for url in sns:
        if "twitter" in url:
            tmp[4] = url
        elif "instagram" in url:
            tmp[5] = url
        elif "facebook" in url:
            tmp[6] = url
        elif "tiktok" in url:
            tmp[7] = url
        elif "line" in url:
            tmp[8] = url

    # チャンネルIDの検索結果から抽出した値をリストに格納
    search_result.append(tmp)


# 保存するファイルがあるかチェック
is_file = os.path.isfile(cfile)

# 抽出した結果をcsvファイルに保存
with open(cfile, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f)

    # ヘッダ行を記入するか判定
    if is_file:
        pass
    else:
        w.writerows(csv_header)

    # csvファイルに検索結果を追記
    w.writerows(search_result)