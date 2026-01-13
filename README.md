# 📊 Instagram Hashtag Analyzer

A powerful and simple tool to search Instagram hashtags and fetch recent posts using the Instagram Graph API.

## ✨ Features

- 🔍 **Hashtag Search** - Search any Instagram hashtag
- 📸 **Post Fetching** - Get 10-100 recent posts
- 💾 **CSV Export** - Download posts as CSV
- 🔗 **Direct Links** - View posts on Instagram
- ❤️ **Engagement Metrics** - Likes and comments count
- 📱 **Media Display** - Images, videos, and carousel support
- 🔐 **Permanent Token** - No login needed, works forever!
- ♾️ **No Refresh Required** - System user token never expires

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- conda or venv
- Instagram Business Account
- Facebook App with Instagram Graph API access

### Installation

1. **Clone the repository**
```bash
git clone <repo-url>
cd insta_hashtag
```

2. **Create virtual environment**
```bash
conda create -n insta_env python=3.10
conda activate insta_env
```

3. **Install dependencies**
```bash
pip install streamlit requests pandas python-dotenv
```

4. **Add credentials to `.env`**
```env
ACCESS_TOKEN = "your_permanent_system_user_token_here"
IG_USER_ID = "your_ig_user_id"
APP_ID = "your_app_id"
APP_SECRET = "your_app_secret"
```

5. **Run the app**
```bash
streamlit run frontend.py
```

6. **Open in browser**
```
http://localhost:8501
```

## 📋 File Structure

```
insta_hashtag/
├── frontend.py           # Streamlit UI
├── backend.py            # API logic
├── .env                  # Credentials (keep secret!)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔧 How It Works

### Backend (`backend.py`)
- `validate_token()` - Check if token is valid
- `get_hashtag_id(hashtag)` - Search for hashtag
- `get_hashtag_posts(hashtag_id, limit)` - Fetch recent posts
- `search_hashtag_and_fetch_posts(hashtag, limit)` - Complete flow

### Frontend (`frontend.py`)
- Clean Streamlit UI
- Sidebar controls (search, limit slider)
- Posts table with all metrics
- CSV download option
- Detailed post view with media

## 🔐 Security Notes

- ⚠️ **Keep `.env` file secret** - Never commit it to git
- ✅ `.gitignore` is configured to exclude `.env`
- 🔑 Use permanent system user tokens (never share!)
- 📝 Check `.gitignore` for other excluded files

## 📊 API Details

Uses **Instagram Graph API v19.0** with fields:
- `id` - Post ID
- `caption` - Post caption
- `media_type` - IMAGE, VIDEO, or CAROUSEL_ALBUM
- `media_url` - Direct media URL
- `permalink` - Link to Instagram post
- `like_count` - Number of likes
- `comments_count` - Number of comments
- `timestamp` - Post date/time

## 🛠️ Troubleshooting

### Token Invalid Error
```
❌ No access token found in .env file
```
**Solution:** Check `.env` file exists and `ACCESS_TOKEN` is set correctly

### Hashtag Not Found
```
❌ Hashtag '#{hashtag}' not found on Instagram
```
**Solution:** Hashtag must be searchable on Instagram, try popular hashtags like "travel"

### No Posts Returned
```
⚠️ No posts returned by Instagram API
```
**Solution:** Instagram API only returns posts visible to the authenticated account

## 📈 Token Management

**Type:** Permanent System User Token
- **Expiry:** Never expires ♾️
- **Refresh:** Not needed
- **Login:** Not required

## 🤝 Contributing

Feel free to improve this project!

## 📝 License

Open source - use freely!

---

**Made by shivam "AI/ML engineer"** ✨
