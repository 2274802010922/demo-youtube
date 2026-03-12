import streamlit as st
import requests
import pandas as pd

API_KEY = "AIzaSyAK89AZdFqWG3NJmR1TnUbM1QUdrQWD6AM"

st.title("YouTube Comment Extractor")

video_url = st.text_input("Enter YouTube Video URL")

if video_url:

    video_id = video_url.split("v=")[-1]

    url = "https://www.googleapis.com/youtube/v3/commentThreads"

    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": 100,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    comments = []

    for item in data["items"]:
        snippet = item["snippet"]["topLevelComment"]["snippet"]

        comments.append({
            "author": snippet["authorDisplayName"],
            "comment": snippet["textDisplay"],
            "likes": snippet["likeCount"]
        })

    df = pd.DataFrame(comments)

    st.write("Comments")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "Download CSV",
        csv,
        "youtube_comments.csv",
        "text/csv"
    )
