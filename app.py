import streamlit as st
import requests
import pandas as pd

API_KEY = "AIzaSyAK89AZdFqWG3NJmR1TnUbM1QUdrQWD6AM"

st.title("YouTube Video & Comment Extractor")

# search video
query = st.text_input("Search video")

if query:

    search_url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "key": API_KEY
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    videos = []

    for item in data["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]

        videos.append({
            "title": title,
            "video_id": video_id
        })

    video_titles = [v["title"] for v in videos]

    selected_title = st.selectbox("Choose video", video_titles)

    selected_video = next(v for v in videos if v["title"] == selected_title)

    video_id = selected_video["video_id"]

    st.video(f"https://youtube.com/watch?v={video_id}")

    if st.button("Load Comments"):

        comment_url = "https://www.googleapis.com/youtube/v3/commentThreads"

        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "key": API_KEY
        }

        response = requests.get(comment_url, params=params)
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

        st.subheader("Comments")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "Download CSV",
            csv,
            "youtube_comments.csv",
            "text/csv"
        )
