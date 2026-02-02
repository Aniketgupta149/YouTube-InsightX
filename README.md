
# 🎥 YouTube Analytics Pro
![YouTube Analytics Pro Banner](Assets/Youtube_logo3.png)
**YouTube Analytics Pro** is a powerful, modern web application designed to extract, analyze, and visualize data from any YouTube channel. Built with **Streamlit** and the **YouTube Data API v3**, it provides deep insights into channel performance, video engagement, and growth trends through an intuitive and stunning dark-mode UI.

---

## ✨ Key Features

### 📊 Advanced Analytics Dashboard
- **Channel Overview:** View total subscribers, views, video count, and average engagement rates.
- **Interactive Charts:** 
  - 📈 **Views Over Time:** Track channel growth and viral spikes.
  - 📊 **Engagement Distribution:** Analyze how your audience interacts with content.
  - ⏱️ **Duration Analysis:** Find the optimal video length for your channel.
  - 💡 **Correlation Plots:** Explore relationships between views, likes, and comments.
- **Posting Frequency:** Visualize upload consistency over time.

### 🔍 Smart Search & Filtering
- **Real-time Search:** Instantly find videos by title or keyword.
- **Date Range Filter:** Analyze performance within specific timeframes.
- **View Count Filter:** Focus on high-performing or niche content.
- **Sorting:** Sort videos by Views, Likes, Comments, Engagement, Date, or Duration.

### 🏆 Top Performers
- Automatically identify your **Top 10** videos by:
  - 👁️ Views
  - 🔥 Engagement Rate
  - 👍 Likes
  - 💬 Comments

### 🖼️ Interactive Gallery
- Browse video thumbnails in a beautiful grid layout.
- View key metrics (Views, Likes, Date) for each video.
- Direct links to watch videos on YouTube.

### 💾 Data Export
- Download your complete channel dataset in multiple formats:
  - **CSV**
  - **JSON**
  - **Excel**

---

## 🎨 Modern UI/UX
- **Premium Dark Mode:** Sleek, eye-friendly design inspired by YouTube's aesthetic.
- **Glassmorphism:** Modern translucent cards and containers.
- **Responsive Design:** Works seamlessly on desktops and tablets.
- **Animated Backgrounds:** Dynamic, floating elements for an immersive experience.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Data Processing:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualization:** [Plotly Express](https://plotly.com/python/)
- **API:** [Google YouTube Data API v3](https://developers.google.com/youtube/v3)
- **Styling:** Custom CSS, HTML5

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- A Google Cloud Project with YouTube Data API v3 enabled (API Key)

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Aniketgupta149/YouTube_Info_Extractor.git
   cd YouTube_Info_Extractor
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Launch**
   - The app will open in your default browser at `http://localhost:8501`.
   - Enter a YouTube Channel URL (e.g., `https://www.youtube.com/@ChannelName`) to start analysing!

---

## 📂 Project Structure

```
YouTube_Info_Extractor/
├── Assets/                 # Images and icons for the UI
│   ├── Youtube_logo3.png
│   ├── work-from-home.svg
│   ├── visual-collaboration.svg
│   └── ...
├── app.py                  # Main application code
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
└── LICENSE                 # License file
```

---

## 🔑 API Configuration

The application comes with a default API key for testing. For production use or higher rate limits, replace it with your own key:

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable **YouTube Data API v3**.
3. Generate an **API Key**.
4. Enter your key in the app or update `st.session_state.api_key` in `app.py`.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <b>Made with by Aniket</b>
</div>


