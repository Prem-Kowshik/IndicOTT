import asyncio
from response_testing import return_video_data
from google import genai
from google.genai import types
from google.genai.types import (GenerateContentConfig,GoogleSearch,HttpOptions,Tool)
import json
import streamlit as st
from tenacity import retry, wait_random_exponential
GEMINI_API_KEY="AIzaSyC2bzsTTU5br0H-P-EQReLMHiOvLZLILW8"
async def fetch_video_url_title():
    video_data = await return_video_data()
    urls = []
    titles=[]
    for item in video_data:
            urls.append(item['url'])
            title=item['canonicaltitle'].lstrip('File:')
            title2=title.rstrip('.webm')
            title3=title2.rstrip('.ogv')
            titles.append(title3)
    return urls,titles    
def clean_response(response):
    response_text = response.text
    respr=response_text.rstrip("```")
    x=respr.find('json')
    x+=4
    resp=respr[x:len(respr)]
    print(respr)
    try:
        json_data = json.loads(resp)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    

@retry(wait=wait_random_exponential(multiplier=1, max=120))
async def fetch_genre(title, url):
    sem2=asyncio.Semaphore(10)  # Limit concurrent requests
    async with sem2:
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = await client.aio.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=f"""Find the genre of the movie with the title: {title}. The movie can be found at this URL: {url}
            Format the response as a JSON object with the following fields:
            {{
                "title": "{title}",
                "url": "{url}",
                "genre": "<estimated genre of the film>"
            }}""",
            config=GenerateContentConfig(
                tools=[Tool(google_search=GoogleSearch())],
            ),
        )
        if sem2.locked():
            print("concurrency limit reached")
            await asyncio.sleep(1)
    print("task done")
    return clean_response(response)

async def main():
    sem=asyncio.Semaphore(10)  # Limit concurrent requests
    urls, titles = await fetch_video_url_title()
    print("creating tasks")
    genre_tasks = [asyncio.create_task(fetch_genre(titles[i], urls[i])) for i in range(len(titles))]
    print("tasks created")
    print("gathering tasks")
    async with sem:
        lists=await asyncio.gather(*genre_tasks)
        if sem.locked():
            print("concurrency limit reached")
            await asyncio.sleep(1)
    print("tasks gathered")
    print("processing results")
    genre={}
    try:
        for i in lists:
            if i["genre"] not in genre.keys():
                genre[i["genre"]]=[]
            genre[i["genre"]].append({"title": i["title"], "url": i["url"]})
            print("here")
        print("done")
    except TypeError:
        print("object not readable")
    return genre    


def render_footer():
    st.markdown("""---""")
    st.markdown("### 🌐 Connect with Us")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="text-align: center;">
            <a href="mailto:reachus@swecha.net">
                <img src="https://moein.video/wp-content/uploads/2022/12/Gmail-Logo-GIF-Gmail-Icon-GIF-Royalty-Free-Animated-Icon-GIF-1080px-after-effects-project.gif" width="80" />
            </a>
            <br/>
            <a href="mailto:reachus@swecha.net" style="color: #ff4d4d;">Email</a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://instagram.com/swechafsmi" target="_blank">
                <img src="https://miro.medium.com/v2/resize:fit:1400/1*PPztoHHx7GPXCwTUHMmr4w.gif" width="150" />
            </a>
            <br/>
            <a href="https://instagram.com/swechafsmi" target="_blank" style="color: #e75480;">Instagram</a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="text-align: center;">
            <a href="https://twitter.com/SwechaFSMI" target="_blank">
                <img src="https://cdn.dribbble.com/userupload/9051959/file/original-006a32a7d1299ce2651e2835f852d90b.gif" width="80" />
            </a>
            <br/>
            <a href="https://twitter.com/SwechaFSMI" target="_blank" style="color: #66ccff;">Twitter</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""---""")

    with st.expander("👥 Team Members"):
        st.markdown("""
        - [*Prem Koushik*](mailto:)
        - [*Hemanth Kumar Putha*](mailto:putha.hemanth@gmail.com)  
        - [*Jyothishma Harivilam*](mailto:jyothishma.harivilam@gmail.com)  
        - [*Amar Kumar*](mailto:@gmail.com)  
        - [*Ankan Banerjee*](mailto:ankanb853@gmail.com)  
        - [*Lalithya *](mailto:lalithyamunigala330@gmail.com)  
        - [*Kotra Keshav Gupta*](mailto:@gmail.com)  
        - [*Harshit Royal*](mailto:@gmail.com) 
        - [*Soham Mutra*](mailto:sohanmutra28@gmail.com) 
        """, unsafe_allow_html=True)

    st.markdown("""
        <p style="text-align:center; font-size:0.8rem; color:gray; margin-top: 2rem;">
            © 2025 StreamFlix. Built with ❤ by the team. No copyright. Feel free to use with credit.
        </p>
    """, unsafe_allow_html=True)
