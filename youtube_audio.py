import streamlit as st
import yt_dlp

'Youtube Song Player'

url = st.text_input('youtube','https://www.youtube.com/watch?v=9Zj0JOHJR-s')

ydl_opts = {
        'format': 'bestaudio/best', # Select the best audio str
        
        # Tell yt-dlp to write the output to our in-memory buffer
        'quiet': True,
        'noprogress': True,
        'nocheckcertificate': True
    }
info = yt_dlp.YoutubeDL(ydl_opts).extract_info(url, download=False)

info['fulltitle'] , info['duration_string']
st.image(info['thumbnail'])

st.audio(info['url'])
