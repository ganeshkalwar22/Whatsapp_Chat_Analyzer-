import re
import pandas as pd 

def preprocess(data):

    pattern = r'(?:\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s)'
    message = re.split(pattern, data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':message,'dates':dates})

    df['dates'] = (df['dates'].str.replace('\u202f', ' ', regex=False).str.replace('-', '', regex=False) .str.strip())
    df['dates'] = pd.to_datetime(df['dates'],format='%d/%m/%y, %I:%M %p')
    users = []
    messages = []

    for message in df['user_message']:
    
            match = re.match(r'^([\+\w\s\(\)\-]+):\s*(.*)', message, re.DOTALL)
            
            if match:
                users.append(match.group(1).strip())
                messages.append(match.group(2).strip())
            else:
            
                users.append('group_notification')
                messages.append(message.strip())

    df['user']=users
    df['message']=messages
    df.drop(['user_message'],axis=1,inplace=True)
    df['year']=df['dates'].dt.year
    df['month']=df['dates'].dt.month_name()
    df['month_num'] = df['dates'].dt.month
    df['day']=df['dates'].dt.day
    df['hour']=df['dates'].dt.hour
    df['minutes']=df['dates'].dt.minute
    df['message'] = df['message'].replace('', '<Media omitted>')
    df['only_date']=df['dates'].dt.date
    df['day_name']=df['dates'].dt.day_name()

    
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
     if hour == 23:
      period.append(str(hour) + "-" + str('00'))
     elif hour == 0:
      period.append(str('00') + "-" + str(hour + 1))
     else:
      period.append(str(hour) + "-" + str(hour + 1))   

    df['period'] = period




    return df

    