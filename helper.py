from urlextract import URLExtract
from wordcloud import  WordCloud
import pandas as pd 
from collections import Counter
import nltk 
from nltk.corpus import stopwords 
nltk.download('stopwords') 
from string import punctuation
import emoji

extract= URLExtract()



def total_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    # total number of messages 
    num_message = df['message'].shape[0]
    # total number of words 
    words=[]
    for word in df['message']:
        words.extend(word.split())
    num_words=len(words)
    # total number of media 
    num_media=df[df['message']=='<Media omitted>'].shape[0]
    # total number of links 
    links=[]
    for msg in df['message']:
        links.extend(extract.find_urls(msg))
    num_links=len(links)
    return num_message,num_words,num_media,num_links


def  most_busy_user(df):
    x=df['user'].value_counts().head()
    df2=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index()
    df2.columns = ['user', 'percentage']
    return x,df2



def wordcld(selected_user,df):
    df=df[df['message']!='<Media omitted>']
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(height=500,width=600,background_color='white')
    x=wc.generate(df['message'].str.cat(sep=" "))
    return x

def most_common_words(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    with open("hinglish_stopwords.txt", "r", encoding="utf-8") as f:
        l1 = f.read().splitlines()
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>']
    words=[]
    stp=stopwords.words("english")
    x=stp+list(punctuation)+l1
    for word in temp['message']:
        words.extend(word.split())
    filtered=[]
    for i in words:
        if i not in x:
            filtered.append(i)
        
    cnt=Counter(filtered)
    x=pd.DataFrame((cnt.most_common(20)))
    x= x.sort_values(by=1, ascending=True)
    return x



def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['message']:
        if isinstance(message, str):
            emojis.extend([c for c in message if emoji.is_emoji(c)])
    
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(), columns=['emoji', 'count'])
    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
      time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    new_df=df.groupby(['only_date']).count()['message'].reset_index()
    return new_df

def daily_activity_map(selected_user,df):
    if selected_user !='Overall':
         df=df[df['user']==selected_user]
    x=df['day_name'].value_counts()
    return x

def monthly_activity_map(selected_user,df):
    if selected_user !='Overall':
         df=df[df['user']==selected_user]
    x=df['month'].value_counts()
    return x

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap
    



