import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import numpy as np
import isodate
import re
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import base64
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Page Configuration
st.set_page_config(
    page_title="YouTube Analytics", 
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern YouTube-Inspired Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&family=Inter:wght@300;400;500;600&family=Roboto+Mono:wght@400;500;700&display=swap');
    
    :root {
        --yt-red: #FF0000;
        --yt-black: #0F0F0F;
        --yt-white: #FFFFFF;
        --yt-gray-dark: #282828;
        --yt-gray-light: #CCCCCC;
        --yt-blue: #3EA6FF;
        --yt-green: #00FF84;
        --yt-yellow: #F4D03F;
    }

    * {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        color: var(--yt-white) !important;
    }

    .stApp {
        background-color: var(--yt-black);
        background-image: radial-gradient(circle at 50% 0%, #1a0000 0%, var(--yt-black) 70%);
    }
    
    /* Typography Overrides */
    .main-title {
        font-family: 'Poppins', sans-serif;
        font-size: 64px;
        font-weight: 700;
        background: linear-gradient(135deg, var(--yt-white) 0%, var(--yt-gray-light) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        text-align: center;
        font-size: 20px;
        color: var(--yt-gray-light) !important;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    /* Modern Cards */
    .glass-card, .stDataFrame, .stMetric {
        background: var(--yt-gray-dark);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 255, 255, 0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background-color: var(--yt-red);
        color: var(--yt-white);
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 16px;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(255, 0, 0, 0.2);
        width: 100%;
        text-transform: uppercase;
    }
    
    .stButton > button:hover {
        background-color: #cc0000;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(255, 0, 0, 0.3);
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background-color: var(--yt-gray-dark);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: var(--yt-white);
        padding: 12px 16px;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--yt-blue);
        box-shadow: 0 0 0 2px rgba(62, 166, 255, 0.2);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'Roboto Mono', monospace;
        font-size: 32px;
        font-weight: 700;
        color: var(--yt-white) !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 500;
        color: var(--yt-gray-light) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--yt-black);
        border-right: 1px solid var(--yt-gray-dark);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding: 0;
        border-bottom: 1px solid var(--yt-gray-dark);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: var(--yt-gray-light);
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        padding: 12px 24px;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--yt-white);
        border-bottom-color: var(--yt-red);
    }
    
    /* DataFrames */
    .stDataFrame {
        background-color: var(--yt-gray-dark);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Logo Container */
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
        padding: 20px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: var(--yt-red);
    }
    
    /* Selectbox & Date Input */
    .stSelectbox > div > div, .stDateInput > div > div > input {
        background-color: var(--yt-gray-dark);
        border-radius: 8px;
        color: var(--yt-white);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background-color: var(--yt-gray-light);
    }
    
    .stSlider > div > div > div > div {
        background-color: var(--yt-red);
    }
    
    </style>
""", unsafe_allow_html=True)

# Session State Initialization
if "start_dashboard" not in st.session_state:
    st.session_state.start_dashboard = False

if "api_key" not in st.session_state:
    st.session_state.api_key = "AIzaSyDl_pvtmwWypY8RuhywsIB_DlxxSAzLZvg"

if "channel_url" not in st.session_state:
    st.session_state.channel_url = ""

if "df" not in st.session_state:
    st.session_state.df = None

if "channel_info" not in st.session_state:
    st.session_state.channel_info = {}

# Helper Functions
def extract_channel_id(url, youtube=None):
    """Extract channel ID from various URL formats"""
    try:
        url = url.strip()
        
        if "/channel/" in url:
            return url.split("/channel/")[-1].split("?")[0]
        
        if "/@" in url and youtube:
            username = re.findall(r"/@([A-Za-z0-9_-]+)", url)
            if username:
                res = youtube.search().list(
                    part="snippet", q=username[0], type="channel", maxResults=1
                ).execute()
                if res.get("items"):
                    return res["items"][0]["snippet"]["channelId"]
        
        if re.match(r"^[A-Za-z0-9_-]{24}$", url):
            return url
        
        return None
    except Exception as e:
        st.error(f"Error extracting channel ID: {str(e)}")
        return None


def get_uploads_playlist_id(channel_id, youtube):
    """Get uploads playlist ID and channel information"""
    try:
        res = youtube.channels().list(
            part="contentDetails,snippet,statistics",
            id=channel_id
        ).execute()
        
        if not res.get("items"):
            return None, None, None, None
        
        info = res["items"][0]
        
        playlist_id = info["contentDetails"]["relatedPlaylists"]["uploads"]
        channel_name = info["snippet"]["title"]
        stats = info["statistics"]
        
        thumbnail_info = info["snippet"]["thumbnails"]
        channel_logo = thumbnail_info.get("high", thumbnail_info.get("default"))["url"]
        
        return playlist_id, channel_name, stats, channel_logo
    except Exception as e:
        st.error(f"Error fetching channel info: {str(e)}")
        return None, None, None, None


def get_videos_from_playlist(playlist_id, youtube, max_results=200):
    """Get video IDs from uploads playlist"""
    videos = []
    next_page = None
    
    try:
        while len(videos) < max_results:
            res = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page
            ).execute()
            
            for item in res.get("items", []):
                videos.append(item["contentDetails"]["videoId"])
            
            next_page = res.get("nextPageToken")
            if not next_page:
                break
        
        return videos
    except Exception as e:
        st.error(f"Error fetching videos: {str(e)}")
        return []


def get_video_stats(video_ids, youtube):
    """Get detailed statistics for videos"""
    data = []
    
    try:
        for i in range(0, len(video_ids), 50):
            chunk = video_ids[i:i+50]
            
            res = youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=",".join(chunk)
            ).execute()
            
            for item in res["items"]:
                snippet = item.get("snippet", {})
                stats = item.get("statistics", {})
                
                view_count = int(stats.get("viewCount", 0))
                like_count = int(stats.get("likeCount", 0))
                comment_count = int(stats.get("commentCount", 0))
                
                engagement = round((like_count + comment_count) / view_count * 100, 3) if view_count > 0 else 0
                
                duration_iso = item["contentDetails"].get("duration", "PT0S")
                duration_td = isodate.parse_duration(duration_iso)
                duration_minutes = round(duration_td.total_seconds() / 60, 2)
                
                thumbnail_url = snippet["thumbnails"].get("high", snippet["thumbnails"].get("default"))["url"]
                
                data.append({
                    "VideoID": item["id"],
                    "Title": snippet.get("title", ""),
                    "Published": snippet.get("publishedAt", "").split("T")[0],
                    "Views": view_count,
                    "Likes": like_count,
                    "Comments": comment_count,
                    "Engagement (%)": engagement,
                    "Duration_minutes": duration_minutes,
                    "Thumbnail": thumbnail_url,
                    "URL": f"https://youtu.be/{item['id']}"
                })
        
        return data
    except Exception as e:
        st.error(f"Error fetching video stats: {str(e)}")
        return []


# Landing Page
if not st.session_state.start_dashboard:
    # Logo
    try:
        with open("Assets/Youtube_logo3.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
        
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom:0px;">
                <img src="data:image/png;base64,{data}" width="500">
            </div>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.error("Logo file not found in Assets folder.")
    
    # Decorative Background Elements
    try:
        def get_base64(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")

        poly_img = get_base64("Assets/Polygon 1.png")
        ellipse_img = get_base64("Assets/Ellipse 3.png")
        sub_img = get_base64("Assets/Subtract.png")
        
        st.markdown(
            f"""
            <style>
            .decoration {{
                position: fixed;
                z-index: 0;
                opacity: 0.4;
                pointer-events: none;
            }}
            </style>
            
            <!-- Top Left Cluster -->
            <img src="data:image/png;base64,{poly_img}" class="decoration" style="top: 5%; left: 2%; width: 80px; animation: float 6s ease-in-out infinite;">
            <img src="data:image/png;base64,{sub_img}" class="decoration" style="top: 15%; left: 8%; width: 60px; animation: float 8s ease-in-out infinite 1s;">
            
            <!-- Top Right Cluster -->
            <img src="data:image/png;base64,{sub_img}" class="decoration" style="top: 8%; right: 5%; width: 100px; opacity: 0.3;">
            <img src="data:image/png;base64,{ellipse_img}" class="decoration" style="top: 20%; right: 15%; width: 50px; animation: pulse 5s ease-in-out infinite;">
            
            <!-- Bottom Left Cluster -->
            <img src="data:image/png;base64,{ellipse_img}" class="decoration" style="bottom: 10%; left: 5%; width: 120px; animation: pulse 7s ease-in-out infinite;">
            <img src="data:image/png;base64,{poly_img}" class="decoration" style="bottom: 25%; left: 10%; width: 60px; animation: float 9s ease-in-out infinite 2s;">
            
            <!-- Bottom Right Cluster -->
            <img src="data:image/png;base64,{ellipse_img}" class="decoration" style="bottom: 5%; right: 5%; width: 150px; animation: pulse 4s ease-in-out infinite;">
            <img src="data:image/png;base64,{sub_img}" class="decoration" style="bottom: 30%; right: 8%; width: 80px; opacity: 0.2;">
            
            <!-- Center/Random -->
            <img src="data:image/png;base64,{poly_img}" class="decoration" style="top: 40%; left: 15%; width: 40px; opacity: 0.2; animation: float 10s ease-in-out infinite;">
            <img src="data:image/png;base64,{poly_img}" class="decoration" style="top: 60%; right: 20%; width: 50px; opacity: 0.2; animation: float 7s ease-in-out infinite 1s;">
            
            <style>
            @keyframes float {{
                0% {{ transform: translateY(0px) rotate(0deg); }}
                50% {{ transform: translateY(-20px) rotate(10deg); }}
                100% {{ transform: translateY(0px) rotate(0deg); }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except Exception:
        pass # Fail silently if decorations are missing

    st.markdown("<h1 class='main-title'>YouTube Analytics Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Unlock Deep Insights into Your YouTube Channel Performance</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("###  Channel Information")
        channel_url = st.text_input(
            "Channel URL or Channel ID",
            placeholder="https://www.youtube.com/@channelname or UC...",
            help="Enter the full channel URL or just the channel ID"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Launch Analytics Dashboard"):
            if not channel_url:
                st.error("⚠️ Please enter a Channel URL or ID.")
            else:
                # API key is already in session state
                st.session_state.channel_url = channel_url
                st.session_state.start_dashboard = True
                st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Feature Highlights
    st.markdown("### ✨ Features")
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("Assets/work-from-home.svg", use_container_width=True)
        st.markdown("""
        ### 📊 Advanced Analytics & Filtering
        * **Deep Insights:** Engagement metrics, performance trends, and growth predictions.
        * **Smart Search:** Filter videos by date, views, and keywords instantly.
        """)
    
    with col2:
        st.image("Assets/visual-collaboration.svg", use_container_width=True)
        st.markdown("""
        ### 📈 Visuals & Exports
        * **Interactive Charts:** Compare videos, analyze distributions, and spot trends.
        * **Easy Export:** Download your data in CSV, JSON, or Excel formats.
        """)

# Dashboard
else:
    api_key = st.session_state.api_key
    channel_url = st.session_state.channel_url
    
    # Fetch data if not already cached
    if st.session_state.df is None:
        with st.spinner("🔄 Fetching channel data..."):
            try:
                youtube = build("youtube", "v3", developerKey=api_key)
                
                channel_id = extract_channel_id(channel_url, youtube)
                if not channel_id:
                    st.error("❌ Invalid channel URL or ID. Please go back and try again.")
                    if st.button("← Go Back"):
                        st.session_state.start_dashboard = False
                        st.rerun()
                    st.stop()
                
                playlist_id, channel_name, stats, channel_logo = get_uploads_playlist_id(channel_id, youtube)
                
                if not playlist_id:
                    st.error("❌ Could not fetch channel information. Please check your API key and channel URL.")
                    if st.button("← Go Back"):
                        st.session_state.start_dashboard = False
                        st.rerun()
                    st.stop()
                
                st.session_state.channel_info = {
                    "name": channel_name,
                    "stats": stats,
                    "logo": channel_logo
                }
                
                video_ids = get_videos_from_playlist(playlist_id, youtube, 200)
                df = pd.DataFrame(get_video_stats(video_ids, youtube))
                df['Published'] = pd.to_datetime(df['Published'])
                st.session_state.df = df
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                if st.button("← Go Back"):
                    st.session_state.start_dashboard = False
                    st.rerun()
                st.stop()
    
    df = st.session_state.df
    channel_info = st.session_state.channel_info
    
    # Header
    # Header
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: center; gap: 25px; margin-bottom: 25px;">
        <img src="{channel_info['logo']}" style="width: 120px; height: 120px; border-radius: 50%; object-fit: cover; border: 3px solid #FF0000; box-shadow: 0 0 20px rgba(255, 0, 0, 0.3);">
        <h1 style="margin: 0; font-size: 50px; font-weight: 900; background: linear-gradient(135deg, #FF0000 0%, #FF6B6B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{channel_info['name']}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Home"):
            st.session_state.start_dashboard = False
            st.session_state.df = None
            st.rerun()
    
    st.markdown("---")
    # API KEy :AIzaSyAMZsRj_ZFqSd07UO8PVHjQDSV1isCPeAA
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📹 Total Videos", f"{int(channel_info['stats'].get('videoCount', 0)):,}")
    col2.metric("👁️ Total Views", f"{int(channel_info['stats'].get('viewCount', 0)):,}")
    col3.metric("👥 Subscribers", f"{int(channel_info['stats'].get('subscriberCount', 0)):,}" if channel_info['stats'].get('subscriberCount') else "Hidden")
    col4.metric("📊 Avg Engagement", f"{df['Engagement (%)'].mean():.2f}%")
    
    st.markdown("---")
    
    # Sidebar Filters
    with st.sidebar:
        st.header("🔍 Filters & Search")
        
        # Search
        search_query = st.text_input("🔎 Search Videos", placeholder="Enter keywords...")
        
        # Date Range
        st.subheader("📅 Date Range")
        min_date = df['Published'].min().date()
        max_date = df['Published'].max().date()
        
        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # View Count Filter
        st.subheader("👁️ View Count")
        min_views = int(df['Views'].min())
        max_views = int(df['Views'].max())
        
        view_range = st.slider(
            "Minimum Views",
            min_value=min_views,
            max_value=max_views,
            value=min_views
        )
        
        # Sort Options
        st.subheader("📊 Sort By")
        sort_by = st.selectbox(
            "Sort Videos By",
            ["Views", "Likes", "Comments", "Engagement (%)", "Published", "Duration_minutes"]
        )
        sort_order = st.radio("Order", ["Descending", "Ascending"])
    
    # Apply Filters
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[filtered_df['Title'].str.contains(search_query, case=False, na=False)]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['Published'].dt.date >= start_date) & 
            (filtered_df['Published'].dt.date <= end_date)
        ]
    
    filtered_df = filtered_df[filtered_df['Views'] >= view_range]
    
    # Sort
    ascending = sort_order == "Ascending"
    filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview", 
        "📄 Video Table", 
        "📈 Analytics", 
        "🏆 Top Performers",
        "🖼️ Gallery",
        "💾 Export"
    ])
    
    with tab1:
        st.header("📊 Channel Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Views Over Time
            st.subheader("📈 Views Over Time")
            views_over_time = filtered_df.groupby(filtered_df['Published'].dt.to_period('M'))['Views'].sum().reset_index()
            views_over_time['Published'] = views_over_time['Published'].astype(str)
            
            fig = px.line(
                views_over_time, 
                x='Published', 
                y='Views',
                title="Monthly Views Trend"
            )
            fig.update_traces(line_color='#FF0000', line_width=3)
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Engagement Distribution
            st.subheader("📊 Engagement Distribution")
            fig = px.histogram(
                filtered_df, 
                x='Engagement (%)',
                nbins=30,
                title="Engagement Rate Distribution"
            )
            fig.update_traces(marker_color='#FF0000')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Duration Distribution
            st.subheader("⏱️ Video Duration Distribution")
            fig = px.box(
                filtered_df, 
                y='Duration_minutes',
                title="Duration Analysis (Minutes)"
            )
            fig.update_traces(marker_color='#FF0000')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Engagement vs Views
            st.subheader("💡 Engagement vs Views")
            fig = px.scatter(
                filtered_df, 
                x='Views', 
                y='Engagement (%)',
                size='Likes',
                hover_data=['Title'],
                title="Performance Correlation"
            )
            fig.update_traces(marker_color='#FF0000')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("📄 All Videos")
        st.info(f"Showing {len(filtered_df)} of {len(df)} videos")
        
        # Display dataframe
        display_df = filtered_df[['Title', 'Published', 'Views', 'Likes', 'Comments', 'Engagement (%)', 'Duration_minutes', 'URL']].copy()
        display_df['Published'] = display_df['Published'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "URL": st.column_config.LinkColumn("Video Link"),
                "Views": st.column_config.NumberColumn(format="%d"),
                "Likes": st.column_config.NumberColumn(format="%d"),
                "Comments": st.column_config.NumberColumn(format="%d"),
            }
        )
    
    with tab3:
        st.header("📈 Advanced Analytics")
        
        # Posting Frequency
        st.subheader("📅 Posting Frequency Analysis")
        posting_freq = filtered_df.groupby(filtered_df['Published'].dt.to_period('M')).size().reset_index(name='Video Count')
        posting_freq['Published'] = posting_freq['Published'].astype(str)
        
        fig = px.bar(
            posting_freq,
            x='Published',
            y='Video Count',
            title="Videos Published Per Month"
        )
        fig.update_traces(marker_color='#FF0000')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance Metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Avg Views per Video", f"{filtered_df['Views'].mean():,.0f}")
            st.metric("👍 Avg Likes per Video", f"{filtered_df['Likes'].mean():,.0f}")
        
        with col2:
            st.metric("💬 Avg Comments per Video", f"{filtered_df['Comments'].mean():,.0f}")
            st.metric("⏱️ Avg Duration", f"{filtered_df['Duration_minutes'].mean():.1f} min")
        
        with col3:
            st.metric("🔥 Best Engagement", f"{filtered_df['Engagement (%)'].max():.2f}%")
            st.metric("📈 Total Engagement", f"{filtered_df['Engagement (%)'].sum():.0f}%")
        
        # Likes vs Comments
        st.subheader("💡 Likes vs Comments Correlation")
        fig = px.scatter(
            filtered_df,
            x='Likes',
            y='Comments',
            size='Views',
            hover_data=['Title'],
            title="Audience Interaction Patterns"
        )
        fig.update_traces(marker_color='#FF0000')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.header("🏆 Top Performing Videos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👁️ Most Viewed")
            top_views = filtered_df.nlargest(10, 'Views')[['Title', 'Views', 'Published', 'URL']]
            top_views['Published'] = top_views['Published'].dt.strftime('%Y-%m-%d')
            st.dataframe(
                top_views,
                use_container_width=True,
                hide_index=True,
                column_config={"URL": st.column_config.LinkColumn("Link")}
            )
        
        with col2:
            st.subheader("🔥 Highest Engagement")
            top_engagement = filtered_df.nlargest(10, 'Engagement (%)')[['Title', 'Engagement (%)', 'Published', 'URL']]
            top_engagement['Published'] = top_engagement['Published'].dt.strftime('%Y-%m-%d')
            st.dataframe(
                top_engagement,
                use_container_width=True,
                hide_index=True,
                column_config={"URL": st.column_config.LinkColumn("Link")}
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👍 Most Liked")
            top_likes = filtered_df.nlargest(10, 'Likes')[['Title', 'Likes', 'Published', 'URL']]
            top_likes['Published'] = top_likes['Published'].dt.strftime('%Y-%m-%d')
            st.dataframe(
                top_likes,
                use_container_width=True,
                hide_index=True,
                column_config={"URL": st.column_config.LinkColumn("Link")}
            )
        
        with col2:
            st.subheader("💬 Most Commented")
            top_comments = filtered_df.nlargest(10, 'Comments')[['Title', 'Comments', 'Published', 'URL']]
            top_comments['Published'] = top_comments['Published'].dt.strftime('%Y-%m-%d')
            st.dataframe(
                top_comments,
                use_container_width=True,
                hide_index=True,
                column_config={"URL": st.column_config.LinkColumn("Link")}
            )
    
    with tab5:
        st.header("🖼️ Thumbnail Gallery")
        st.info(f"Displaying {len(filtered_df)} thumbnails")
        
        # Gallery Grid
        cols = st.columns(4)
        for idx, row in filtered_df.iterrows():
            with cols[idx % 4]:
                st.image(row['Thumbnail'], use_container_width=True)
                st.caption(f"**{row['Title'][:50]}...**")
                st.caption(f"👁️ {row['Views']:,} | 👍 {row['Likes']:,} | 💬 {row['Comments']:,}")
                st.caption(f"📅 {row['Published'].strftime('%Y-%m-%d')}")
                st.markdown(f"[▶️ Watch]({row['URL']})")
                st.markdown("---")
    
    with tab6:
        st.header("💾 Export Data")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("📄 CSV Export")
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"{channel_info['name']}_analytics.csv",
                mime="text/csv"
            )
        
        with col2:
            st.subheader("📋 JSON Export")
            json_data = filtered_df.to_json(orient='records', indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"{channel_info['name']}_analytics.json",
                mime="application/json"
            )
        
        with col3:
            st.subheader("📊 Excel Export")
            # Note: Excel export requires openpyxl
            try:
                from io import BytesIO
                output = BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    filtered_df.to_excel(writer, index=False, sheet_name='Analytics')
                excel_data = output.getvalue()
                
                st.download_button(
                    label="📥 Download Excel",
                    data=excel_data,
                    file_name=f"{channel_info['name']}_analytics.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except ImportError:
                st.warning("Excel export requires 'openpyxl'. Install it with: pip install openpyxl")
        
        st.markdown("---")
        st.subheader("📊 Export Summary")
        st.write(f"**Total Videos:** {len(filtered_df)}")
        st.write(f"**Date Range:** {filtered_df['Published'].min().strftime('%Y-%m-%d')} to {filtered_df['Published'].max().strftime('%Y-%m-%d')}")
        st.write(f"**Total Views:** {filtered_df['Views'].sum():,}")
        st.write(f"**Total Likes:** {filtered_df['Likes'].sum():,}")
        st.write(f"**Total Comments:** {filtered_df['Comments'].sum():,}")
