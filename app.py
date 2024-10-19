from calendar import month

import streamlit as st
import pandas as pd
from matplotlib.pyplot import ylabel, subplots
from streamlit import columns

import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title('WhatsApp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a whatsApp chat", type="txt")

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode('utf-8')
    df=preprocessor.process(data)

    user_list = df['user_name'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,'OverAll')

    user = st.sidebar.selectbox("Select Contact",user_list)
    st.title("Chat Statistics")

    col1,col2,col3,col4 = st.columns(4)

    if st.sidebar.button("Show Analysis"):
        num_msg,num_words,num_media,num_urls= helper.get_details(user, df)
        with col1:
            st.text('Total Messages')
            st.text(num_msg)
        with col2:
            st.text('Total Words')
            st.text(num_words)
        with col3:
            st.text('Total Media')
            st.text(num_media)
        with col4:
            st.text('Total Links')
            st.text(num_urls)


        if user=='OverAll':
            st.title('Top Users in messages')
            col1,col2 = st.columns(2)
            x=helper.top_users(df)
            fig,ax = plt.subplots()
            with col1:
                st.text('Graphical Representation')
                ax.bar(x.index, x.values, color='violet')
                plt.ylabel('Word Count')
                plt.xlabel('User Name')
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                st.text('Top Users in Group')
                top = round((df['user_name'].value_counts()/df.shape[0])*100,2)
                st.dataframe(top)

        st.title('WordCloud')
        df_wc = helper.word_cloud(user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title('Most Common Words')
        most_cw = helper.most_common_words(user,df)
        most_cw_df = pd.DataFrame(most_cw)
        most_cw_df.rename(columns={0:'words',1:'counts'},inplace =True)
        fig,ax = plt.subplots()
        ax.barh(most_cw_df['words'],most_cw_df['counts'], color='violet')
        plt.ylabel('Words')
        plt.xlabel('Counts')
        st.pyplot(fig)

        #Monthly Timeline
        st.title('Per Monthly Timeline')
        monthly = helper.monthly_timeline(user,df)
        fig, ax = plt.subplots()
        ax.bar(monthly['monthly'], monthly['user_msg'], color='violet')
        plt.xticks(rotation=90)
        plt.xlabel('Month Name')
        plt.ylabel('Messages')
        st.pyplot(fig)

        #Daily Timeline
        st.title('Daily Timeline')
        daily = helper.daily_timeline(user, df)
        fig, ax = plt.subplots()
        ax.plot(daily['only_date'], daily['user_msg'], color='violet')
        plt.xticks(rotation=90)
        plt.xlabel('Day')
        plt.ylabel('Messages')
        st.pyplot(fig)

        st.title('WeekDay & Monthly Timeline')
        col1,col2 = st.columns(2)

        with col1:
            st.text('Weekday Timeline')
            wtl = helper.week_days(user,df)
            fig, ax = plt.subplots()
            ax.bar(wtl['day_name'],wtl['count'],color='violet')
            plt.xticks(rotation=90)
            plt.xlabel('Day Name')
            plt.ylabel('No. Of Messages')
            st.pyplot(fig)
        with col2:
            st.text('All Month Timeline')
            mtl = helper.all_month(user,df)
            fig, ax = plt.subplots()
            ax.bar(mtl['month_name'],mtl['count'],color='violet')
            plt.xticks(rotation=90)
            plt.xlabel('Month Name')
            plt.ylabel('No. Of Messages')
            st.pyplot(fig)

        #Emojis Details
        st.title("Most Common Emojis")
        col1,col2 = st.columns(2)
        em_df = helper.get_emojis_det(user, df)
        with col1:
            st.text("Emojis Dataframe")
            st.dataframe(em_df)

        with col2:
            st.text("Emoji Distribution")
            fig,ax = plt.subplots()
            ax.pie(em_df['Count'].head(),labels=em_df['Emoji'].head(),autopct='%1.1f%%')
            st.pyplot(fig)
