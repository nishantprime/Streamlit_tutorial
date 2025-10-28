import streamlit as st
import yt_dlp
from youtubesearchpython import SearchVideos
import json

'Youtube Song Player'

query = st.text_input('enter song name', 'extreme ways')

search = SearchVideos(query, offset=1, mode="json", max_results=1)
results = search.result()



if results:
    results_data = json.loads()
    if results_data and results_data['search_result']:
        url = results_data['search_result'][0]['link']
        ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'noprogress': True,
                'nocheckcertificate': True
            }
        info = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)
        
        info['fulltitle'] , info['duration_string']
        st.image(info['thumbnail'])
        
        st.audio(info['url'])
    else:
        "No results found for the query."
else:
    "No results found for the query."




