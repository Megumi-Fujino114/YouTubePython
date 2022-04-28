api_key = "AIzaSyBNzumwkqIsXCZ2jtXpEudvcrHi_MX40vE"
from apiclient.discovery import build
youtube = build("youtube","v3",developerKey=api_key)
request = youtube.search().list(
    part="snippet",
    type="channel",
    regionCode="JP",
    q="プログラミング",#ここは特に指定のキーワードがないのであれば空文字でOK
    publishedBefore="2022-04-01T00:00:00Z",  #from  after  to  before
    publishedAfter="2022-04-27T00:00:00Z",#大体直近一か月ほど
    maxResults=100)#100以上の動画を取得したい場合はここの数字を変更する
response = request.execute()
response

# まずは日付からここ一か月で投稿された動画を絞り込む