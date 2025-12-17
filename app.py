import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt 
import seaborn as sns 

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show analysis"):
        num_message,num_words,num_media,num_links=helper.total_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total message")
            st.title(num_message)
        with col2:
            st.header("Total words")
            st.title(num_words)
        with col3:
            st.header("Total media")
            st.title(num_media)
        with col4:
            st.header("Total links")
            st.title(num_links)
        
        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['only_date'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #  Activity map 

        # Daily Activity map
        
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            x=helper.daily_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        # Monthly Activity Map
        
        with col2:
            st.header("Most busy month")
            x=helper.monthly_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(x.index,x.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        # Heat map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        

        #finding the  most busy user 
        if selected_user=='Overall':
            st.title("Most busy User")
            x,df2=helper.most_busy_user(df)
            col1,col2=st.columns(2)
            with col1:
                fig,ax=plt.subplots()
                ax.bar(x.index,x.values,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(df2)
        # Wordcloud
        st.title("Word Cloud")
        x=helper.wordcld(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(x)
        st.pyplot(fig)

        # most common  words 
        st.title("most common words")
        x=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(x[0],x[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji analysis 
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2 = st.columns(2)

        with col1:
         st.dataframe(emoji_df)
        with col2:
         fig,ax = plt.subplots()
        ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct="%0.2f%%")
        st.pyplot(fig)


    


