import re
import pandas as pd

def process(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    pattern1 = r'\[\d{1,2}\/\d{1,2}\/\d{1,2}\,\s\d{1,2}\:\d{1,2}\:\d{1,2}\]\s'
    date_pattern = r'\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(date_pattern,data)
    if len(messages)==0:
        messages = re.split(pattern1, data)[1:]

    df = pd.DataFrame({"date": dates, "message": messages})
    df['date'] = pd.to_datetime(df['date'])

    users = []
    msg = []

    for i in df['message']:
        entry = re.split(r'([\w\W]+?):\s', i)
        if entry[1:]:
            users.append(entry[1])
            msg.append(entry[2])
        else:
            users.append('group notification')
            msg.append(entry[0])
    df['user_name'] = users
    df['user_msg'] = msg
    df.drop(columns=['message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['month_name'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df.drop(columns=['date'], inplace=True)

    return df