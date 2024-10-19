import urlextract
from numpy.ma.extras import column_stack
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

extract = urlextract.URLExtract()

def get_details(user,df):

    if user!="OverAll":
        df = df[df['user_name']==user]

    num_msg = df.shape[0]
    words=[]
    for i in df['user_msg']:
        words.extend(i.split())

    num_media = df[df['user_msg']=="<Media omitted>\n"].shape[0]
    urls = []
    for i in df['user_msg']:
        urls.extend(extract.find_urls(i))

    return num_msg,len(words),num_media,len(urls)

def top_users(df):
    x=df['user_name'].value_counts().head()
    return x

def word_cloud(user,df):
    if user!="OverAll":
        df = df[df['user_name']==user]


    temp_df = df[df['user_msg'] != "<Media omitted>\n"]
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    def asd(msg):
        words = []
        for i in msg.lower().split():
            if i not in stop_words:
                words.append(i)
        return " ".join(words)

    temp_df['user_msg'] = temp_df['user_msg'].apply(asd)
    wc = WordCloud(width=500,height=400,min_font_size=10,background_color='white')
    df_wc = wc.generate(temp_df['user_msg'].str.cat(sep=" "))
    return df_wc

def most_common_words(user,df):
    if user!="OverAll":
        df = df[df['user_name']==user]

    temp_df = df[df['user_name'] != 'group notification']
    temp_df = temp_df[temp_df['user_msg'] != "<Media omitted>\n"]
    temp_df = temp_df[temp_df['user_msg'] != "This message was deleted\n"]
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for i in temp_df['user_msg']:
        for word in i.split():
            if word not in stop_words:
                words.append(word)

    word_df = Counter(words).most_common(10)
    return word_df

def monthly_timeline(user,df):
    if user!="OverAll":
        df = df[df['user_name']==user]
    timeline = df.groupby(['year', 'month', 'month_name']).count()['user_msg'].reset_index()
    asd = []
    for i in range(timeline.shape[0]):
        asd.append(timeline['month_name'][i] + "-" + str(timeline['year'][i]))
    timeline['monthly'] = asd
    return timeline

def daily_timeline(user,df):
    if user!="OverAll":
        df = df[df['user_name']==user]

    daily_timeline = df.groupby('only_date').count()['user_msg'].reset_index()
    return daily_timeline

def week_days(user,df):
    if user!="OverAll":
        df = df[df['user_name']==user]

    weekly_tl = df['day_name'].value_counts().reset_index()
    return weekly_tl

def all_month(user,df):
    if user!="OverAll":
        df = df[df['user_name']==user]
    monthly_tl = df['month_name'].value_counts().reset_index()
    return monthly_tl

def get_emojis_det(user,df):
    if user!="OverAll":
        df = df[df['user_name']==user]
    emojis_list = []
    for msg in df['user_msg']:
        emojis = emoji.distinct_emoji_list(msg)
        emojis_list.extend([emoji.demojize(is_emoji) for is_emoji in emojis])

    emojis = []
    for i in emojis_list:
        ans = emoji.emojize(i)
        emojis.extend(ans)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(emojis)))
    emoji_df.rename(columns={0:'Emoji',1:'Count'}, inplace=True)
    return emoji_df