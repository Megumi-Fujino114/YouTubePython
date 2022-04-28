from googleapiclient.discovery import build

YOUTUBE_API_KEY = '<API KEY>'


def youtube_channel_detail(channel_id, api_key):
    api_service_name = 'youtube'
    api_version = 'v3'
    youtube = build(api_service_name, api_version, developerKey=api_key)
    search_response = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id,
    ).execute()

    return search_response['items'][0]

def main():

    d = youtube_channel_detail('UCHVXbQzkl3rDfsXWo8xi2qw', YOUTUBE_API_KEY)
    print(d['snippet']['title'])
    print(d['statistics']['subscriberCount'])

# ＫＥＹの方で取得したＩＤを使用し、
# ここでYouTubeのチャンネル登録者数を取得する

# 上段のコード
 # 特定のユーチューバーの Channel ID を取得
channelID = response['items'][0]['snippet']['channelId']
print(channelID)
# 下段のコード
request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=channelID
)
response = request.execute()
response

# 添付のプログラム見てました。
# ここの環境だとライブラリが足りず、検証不可なので持ち帰り、、、
# ライブラリのインポートが足りない気もする、、、
# ちなみに、➀②は昨日動いたコードがあるのですが、自宅PCに、、、
# ↓のソースがベースで少々カスタマイズしてます。
## ➀キーワードでチャンネルを検索（とりあえず50件） ##
api_key = "API Key"
from apiclient.discovery import build
youtube = build("youtube","v3",developerKey=api_key)
request = youtube.search().list(
    part="snippet",
    type="channel",
    regionCode="JP",
    q="プログラミング",
    publishedBefore="2022-04-01T00:00:00Z",  #from  after  to  before
    publishedAfter="2022-04-27T00:00:00Z",
    maxResults=50)
response = request.execute()
response
# →maxResults の値を変えることで、キーワード（変数：q）を含むチャンネルが検索数を変更できます。
## ②検索結果から必要な要素のみリストに抽出 ##
# 検索結果から、チャンネルのタイトルと、チャンネルIDのみをリストに抽出するには下記。
i = 0
channel_Title_list = []
channel_ID_list = []
while i < 5:
    channel_Title = response['items'][i]['snippet']['channelTitle']
    channel_ID = response['items'][i]['snippet']['channelId']
    channel_Title_list.append(channel_Title)
    channel_ID_list.append(channel_ID)
    i += 1
print(channel_Title_list)
print(channel_ID_list)
# ➀の結果、②の結果は、整形する前の状態でそれぞれcsvに保存かな。
# ②のchannelIDを使って、個別のチャンネルにAPIでアクセスして登録者数を取得ができると思うけど、まだ手付かず。。。