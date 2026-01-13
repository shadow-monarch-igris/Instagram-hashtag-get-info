# 🚀 Quick Start Guide - Instagram Hashtag Analyzer

## Installation & Setup

### 1. Install Dependencies
```bash
pip install streamlit requests pandas
```

### 2. Get Your Credentials
1. Go to https://developers.facebook.com/
2. Create an app (or use existing one)
3. Get your **App ID** and **App Secret**
4. Set redirect URI to `http://localhost:8501`

### 3. Update Configuration
Edit [temp.py](temp.py) with your credentials:

```python
APP_ID = "YOUR_APP_ID"                    # From Facebook Developer Console
APP_SECRET = "YOUR_APP_SECRET"            # Keep this SECRET!
REDIRECT_URI = "http://localhost:8501"    # Streamlit default
IG_USER_ID = "YOUR_IG_BUSINESS_USER_ID"   # Your Instagram Business Account ID
```

### 4. Run the App
```bash
streamlit run temp.py
```

The app will open at `http://localhost:8501`

---

## 🎯 How the Token System Works

### The Problem (Before)
- Instagram tokens expire
- Manual re-login needed every 2 hours
- Bad user experience

### The Solution (Now) ✅
```
Login → Short Token (2h) → Long Token (60d) → AUTO REFRESH before expiry
```

**Result:** Users can work for 60 days without re-login!

---

## 📊 Token Lifecycle Visualization

```
                    LOGIN
                     │
                     ↓
            ┌────────────────┐
            │ Authorization  │
            │  Code Exchange │  (User grants permission)
            └────────────────┘
                     │
                     ↓
            ┌────────────────┐
            │ Short Token    │────── Valid for 2 hours only ⏰
            │ (2 hours)      │
            └────────────────┘
                     │
                     ↓ (Automatic Conversion)
            ┌────────────────┐
            │ Long Token     │────── Valid for 60 days 📅
            │ (60 days)      │
            └────────────────┘
                     │
        ┌────────────┴─────────────┐
        │                          │
        ↓                          ↓
    Auto-Refresh            Manual Refresh
    (< 30 min left)     (User clicks button)
        │                          │
        └────────────┬─────────────┘
                     ↓
            Token Extended
            (Another 60 days)
```

---

## 🔐 Security Features

✅ **Token Refresh Before Expiry**
- No sudden logout
- Seamless user experience

✅ **Session State Management**
- Token stored in memory (not hardcoded)
- Cleared on logout

✅ **Error Handling**
- 401/400 errors trigger re-login
- Network errors caught gracefully

✅ **Secure Practices**
- Never expose APP_SECRET in frontend
- Use environment variables for secrets
- HTTPS recommended for production

---

## 🎮 User Interface Guide

### Login Screen
```
🔓 Please login to continue
🔐 Login with Instagram
```

### After Login
```
Sidebar:
├─ 🔐 Token Status
│  ├─ ✅ Active for 59d 23h 45m
│  ├─ 🔄 Refresh Now (button)
│  └─ 🚪 Logout (button)
│
├─ 🔍 Search Hashtag
│  ├─ Hashtag (text input)
│  ├─ Posts (slider, 10-100)
│  └─ 🔍 Fetch Posts (button)
```

### Results View
```
Title: Instagram Hashtag Analyzer

Cards:
├─ ✅ Fetched X posts for #hashtag
├─ 📊 Posts Table
│  └─ Table with: media_type, likes, comments, timestamp
│
├─ 📸 Post Details
│  ├─ Post 1
│  │  ├─ Caption
│  │  ├─ Image/Video
│  │  ├─ ❤️ Likes metric
│  │  ├─ 💬 Comments metric
│  │  └─ Timestamp
│  │
│  ├─ Post 2
│  └─ Post 3 ...
```

---

## 🛠️ Configuration Options

### Change Refresh Threshold
```python
# Default: 30 minutes
REFRESH_THRESHOLD = 30 * 60  

# Change to 1 hour
REFRESH_THRESHOLD = 60 * 60
```

### Change Long Token Validity
```python
# Default: 60 days
LONG_TOKEN_EXPIRY = 60 * 24 * 60 * 60

# Change to 30 days
LONG_TOKEN_EXPIRY = 30 * 24 * 60 * 60
```

---

## ❌ Common Issues & Solutions

### "Hashtag not found"
- ✅ Check spelling
- ✅ Hashtag must exist on Instagram
- ✅ Account must be Instagram Business account

### "Access token expired"
- ✅ Click "🔄 Refresh Now" button
- ✅ Or logout and login again
- ✅ Auto-refresh should prevent this

### "Redirect URI mismatch"
- ✅ Set correct redirect URI: `http://localhost:8501`
- ✅ Update in Facebook Developer Console
- ✅ Must match REDIRECT_URI in code

### "No posts returned"
- ✅ Hashtag exists but has no recent media
- ✅ Try popular hashtags like "travel", "photography"
- ✅ Account must have business permissions

### "Connection timeout"
- ✅ Check internet connection
- ✅ Instagram API might be down
- ✅ Try again after few seconds

---

## 📈 Features Summary

| Feature | Implemented | Details |
|---------|-------------|---------|
| OAuth Login | ✅ | Full OAuth flow |
| Token Conversion | ✅ | Short → Long |
| Auto Refresh | ✅ | Before expiry |
| Token Status | ✅ | Countdown display |
| Hashtag Search | ✅ | Find any hashtag |
| Post Fetching | ✅ | Up to 100 posts |
| Post Display | ✅ | Images, videos, captions |
| Pagination | ✅ | Automatic |
| Error Handling | ✅ | Comprehensive |
| Session Management | ✅ | Persistent |

---

## 🚀 Deployment (Production)

### Environment Variables
Create `.env` file:
```dotenv
APP_ID=your_app_id
APP_SECRET=your_app_secret
IG_USER_ID=your_ig_user_id
REDIRECT_URI=https://yourdomain.com
```

### Load in Code
```python
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
IG_USER_ID = os.getenv("IG_USER_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
```

### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Connect to https://share.streamlit.io
3. Set environment variables in secrets
4. Deploy!

---

## 📚 Additional Resources

- **[Complete Token Refresh Guide](TOKEN_REFRESH_GUIDE.md)** - Deep dive into token system
- **Instagram Graph API Docs:** https://developers.facebook.com/docs/instagram-api/
- **Facebook Developer Console:** https://developers.facebook.com/
- **Streamlit Docs:** https://docs.streamlit.io/

---

## 💡 Tips & Tricks

### Test Token Refresh
1. Set `REFRESH_THRESHOLD = 5 * 60` (5 minutes instead of 30)
2. Fetch posts multiple times
3. Watch auto-refresh in action!

### Debug Token Status
```python
# Add to sidebar to see token details
st.write(st.session_state.access_token[:20] + "...")
st.write(f"Expires: {st.session_state.token_expires_at}")
```

### Monitor API Calls
```python
# Add logging to api_get()
print(f"API Call: {url}")
print(f"Token: {params['access_token'][:20]}...")
```

---

## 📞 Support

For issues:
1. Check [Common Issues](#-common-issues--solutions) section
2. Review [TOKEN_REFRESH_GUIDE.md](TOKEN_REFRESH_GUIDE.md)
3. Check Instagram API status
4. Review Streamlit documentation

---

**Enjoy your Instagram Hashtag Analyzer! 🎉**

**All features working. No tokens to worry about. Happy coding! 🚀**
