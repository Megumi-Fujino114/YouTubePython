from apiclient.errors import HttpError

# API情報
DEVELOPER_KEY = 'AIzaSyBNzumwkqIsXCZ2jtXpEudvcrHi_MX40vE'
# YouTubeのAOIキーを取得する
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY
    )

#検索ワード：検索したいキーワードを入力
search_response = youtube.search().list(
  q='筋トレ',
  part='id,snippet'
).execute()
 
search_response

#入力
#['items']で検索結果をリストで取得（データ数多いので出力結果は割愛
search_response['items']

search_response['pageInfo']

# 最後に、データをpandasのDataFrame型に変換する方法を記します。
import pandas as pd
 
#youtubeデータをpandasに変換する関数
def get_video_info(part, q, order, type, num):
    dic_list = []
    search_response = youtube.search().list(part=part,q=q,order=order,type=type)
    output = youtube.search().list(part=part,q=q,order=order,type=type).execute()
 
    #デフォルトでは5件しか取得できないので、繰り返し取得
    for i in range(num):
        dic_list = dic_list + output['items']
        search_response = youtube.search().list_next(search_response, output)
        output = search_response.execute()
 
    df = pd.DataFrame(dic_list)
    #各動画毎に一意のvideoIdを取得
    df1 = pd.DataFrame(list(df['id']))['videoId']
    #各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
    df2 = pd.DataFrame(list(df['snippet']))[['channelTitle','publishedAt','channelId','title','description']]
    ddf = pd.concat([df1,df2], axis = 1)
 
    return ddf
 
#キーワード筋トレでデータを20回×5件取得
df_out = get_video_info(part='snippet',q='筋トレ',order='viewCount',type='video',num = 20)
df_out


#動画再生回数、高評価、低評価数などを取得する方法は下記の通りです。詳細は参考文献をどうぞ。
def get_statistics(id):
    statistics = youtube.videos().list(part = 'statistics', id = id).execute()['items'][0]['statistics']
    return statistics
 
df_static = pd.DataFrame(list(df_out['videoId'].apply(lambda x : get_statistics(x))))
 
df_output = pd.concat([df_out,df_static], axis = 1)
df_output
