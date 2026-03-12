import streamlit as st
import requests

API_KEY = "AIzaSyAK89AZdFqWG3NJmR1TnUbM1QUdrQWD6AM"

st.title("YouTube Video Search")

query = st.text_input("Search video")

if query:
    url = "https://www.googleapis.com/youtube/v3/search"

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,
        "key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    for item in data["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]

        st.write(title)
        st.video(f"https://youtube.com/watch?v={video_id}")
