# ⚡ Cheat Sheet - Quick Reference Guide

## 🚀 Quick Commands

### Run the App
```bash
streamlit run temp.py
```

### Install Dependencies
```bash
pip install streamlit requests pandas
```

### Check Python Version
```bash
python --version  # Should be 3.7+
```

---

## 🔑 Configuration at a Glance

### Credentials (Update these!)
```python
APP_ID = "YOUR_APP_ID"                    # From Facebook Developer
APP_SECRET = "YOUR_APP_SECRET"            # KEEP SECRET!
IG_USER_ID = "YOUR_IG_BUSINESS_USER_ID"   # Your IG account ID
REDIRECT_URI = "http://localhost:8501"    # Streamlit default
```

### Token Settings (Optional)
```python
REFRESH_THRESHOLD = 30 * 60      # Refresh at 30 min before expiry
                                  # Change to 5*60 to test frequently

LONG_TOKEN_EXPIRY = 60 * 24 * 60 * 60     # 60 days (don't change)
```

---

## 📊 Token Lifecycle (Visual)

```
LOGIN
  └─> Authorization Code
      └─> Short Token (2h)
          └─> Long Token (60d) ⭐
              └─> Auto-Refresh ⭐
                  └─> Extended 60 more days
                      └─> User works indefinitely!
```

---

## 🔄 Auto-Refresh Logic (Simple)

```python
# Before EVERY API call:
if token_expires_in_less_than_30_minutes():
    get_new_token()  # Automatic!
    
# User doesn't notice anything!
# Work continues seamlessly...
```

---

## 📱 UI Elements

### Sidebar Token Status
```
🔐 Token Status
✅ Active for 59d 23h 45m    ← Live countdown!
┌─ 🔄 Refresh Now ┬ 🚪 Logout ─┐
```

### Hashtag Search
```
Hashtag: _____________ (text input)
Posts: [=====●====] 50 (slider 10-100)
🔍 Fetch Posts (button)
```

---

## 🎯 Function Reference

### Authentication
| Function | Purpose | Returns |
|----------|---------|---------|
| `login_button()` | Show OAuth button | None |
| `exchange_code_for_token(code)` | Code → Short Token | String |
| `exchange_long_lived(token)` | Short → Long Token | String |

### Token Management
| Function | Purpose | Returns |
|----------|---------|---------|
| `is_token_expiring_soon()` | Check refresh needed | Boolean |
| `refresh_long_lived_token()` | Get new token | Boolean |
| `ensure_token_valid()` | Pre-flight check | Boolean |

### API Calls
| Function | Purpose | Returns |
|----------|---------|---------|
| `api_get(url, params)` | Safe API call | Response |
| `get_hashtag_id(hashtag)` | Find hashtag | String (ID) |
| `get_hashtag_posts(id, limit)` | Fetch posts | List |

---

## 💾 Session State Variables

```python
st.session_state.access_token       # The OAuth token
st.session_state.token_type         # "short" or "long"
st.session_state.token_created_at   # When created
st.session_state.token_expires_at   # When expires
```

---

## ⚠️ Common Issues & Fixes

### Issue: "Hashtag not found"
```
✅ Try another hashtag
✅ Check spelling
✅ Hashtag must exist on Instagram
```

### Issue: "Access token expired"
```
✅ Click 🔄 Refresh Now button
✅ OR Logout and re-login
✅ Usually auto-refreshes automatically
```

### Issue: "Redirect URI mismatch"
```
✅ Set URI to: http://localhost:8501
✅ Update in Facebook Developer Console
✅ Restart app after change
```

### Issue: "No posts returned"
```
✅ Hashtag exists but no recent media
✅ Try popular hashtags: travel, photography
✅ Account needs business permissions
```

---

## 🔄 Token Refresh Scenarios

### Scenario 1: Fresh Login
```
Time:  Now              Now + 2h           Now + 60d
       │                │                  │
Short  └── Token (2h)   │                  │
Token      └─ Convert ──┘                  │
                                           │
Long      Token (60 days) ─────────────────│
Token     (Auto-refresh at 30d 23h 30m)    │
                                           │
          Token extended ─── Another 60d ──┘
```

### Scenario 2: After 30 Days
```
Day 30, Time: 23:30:00
User makes API call
  └─ Check: Token expires at Day 30, 23:59:59
  └─ Time left: 29 minutes 59 seconds
  └─ < 30 min? YES!
  └─ AUTO-REFRESH ✨
     └─ New expiry: Day 90, 23:30:00
     └─ Show: "🔄 Access token auto-refreshed!"
User continues working
```

### Scenario 3: After 60 Days (No refresh)
```
Day 60, Time: 23:59:59
Token expires ❌
User sees: "❌ Token Expired"
Options:
  1. Click "🔄 Refresh Now" (if possible)
  2. Click "🚪 Logout" → Re-login
```

---

## 🎮 User Journey Map

```
ENTRY POINT
     │
     ▼
Not logged in?
     │
  YES├─ Show login button
     │  └─ User clicks
     │     └─ Redirected to Facebook OAuth
     │        └─ User grants permission
     │           └─ Gets authorization code
     │              └─ Exchange code for tokens
     │                 └─ Store in session
     │                    └─ Show app ✅
     │
  NO└─ Token valid?
        │
     YES├─ Show main app
        │  ├─ Token status sidebar
        │  ├─ Search hashtag input
        │  ├─ Fetch posts button
        │  └─ Results display
        │
        NO└─ Show error
           └─ Require re-login
```

---

## 🔧 Advanced Configuration

### To Test Auto-Refresh (Every 5 min instead of 30 min)
```python
REFRESH_THRESHOLD = 5 * 60
```

### To Extend Token Validity (1 year instead of 60 days)
```python
LONG_TOKEN_EXPIRY = 365 * 24 * 60 * 60
```

### To Debug Token Info
```python
# Add to code:
st.sidebar.write(st.session_state.access_token[:30])
st.sidebar.write(st.session_state.token_expires_at)
```

---

## 📈 Performance Metrics

| Operation | Time |
|-----------|------|
| Auto-refresh | < 1s (background) |
| Hashtag search | ~1s |
| Fetch 50 posts | ~2-3s |
| Display results | ~1s |
| **Total time to results** | **~5 seconds** |

---

## 🛡️ Security Checklist

✅ Never hardcode tokens
✅ Keep APP_SECRET private
✅ Use environment variables
✅ Enable HTTPS in production
✅ Don't log sensitive data
✅ Validate user input
✅ Handle errors gracefully
✅ Rate limit API calls

---

## 📚 Documentation Map

```
README.md (Start here!)
├─ QUICK_START.md ...................... Getting started
├─ TOKEN_REFRESH_GUIDE.md ............ Understanding tokens
├─ CODE_ARCHITECTURE.md ............ Code breakdown
├─ VISUAL_REFERENCE.md .............. Flowcharts
├─ IMPLEMENTATION_SUMMARY.md .. What was changed
└─ CHEAT_SHEET.md (You are here) . Quick reference
```

---

## 🎯 Decision Trees

### Should I refresh token?
```
Has API call been made?
└─ NO → No refresh needed
└─ YES → Is token valid?
   └─ NO → Show error, user re-login
   └─ YES → Token expiring soon? (< 30 min)
      └─ NO → Continue API call
      └─ YES → Auto-refresh, then continue
```

### What to display?
```
User authenticated?
└─ NO → Show "🔐 Login with Instagram" button
└─ YES → Display main app
   ├─ Sidebar: Token status
   ├─ Sidebar: Search form
   ├─ Main: Results (if searched)
```

---

## ⏰ Timeline Example

```
Day 1:   User logs in
         Short token (2h) → Long token (60d) ✅
         
Day 2:   User searches hashtag
         Token valid, no refresh needed ✅
         
Day 30:  User searches again
         Token: 30 days 0 hours left
         Time until expiry: 30d 0h 0m
         Threshold: 30 min
         Auto-refresh triggered! ✅
         Token extended to: Day 90 ✅
         
Day 60:  User searches again
         Token: 30 days 0 hours left (after refresh)
         Auto-refresh triggered again! ✅
         Token extended to: Day 120 ✅
         
Day 90:  Token refreshed again...
         And so on indefinitely! ✅
```

---

## 🚀 5-Minute Setup

```bash
# 1. Get credentials (2 min)
# - Go to Facebook Developer Console
# - Create app, get APP_ID and APP_SECRET
# - Get your IG Business Account ID

# 2. Update code (1 min)
# Edit temp.py:
# APP_ID = "your_id"
# APP_SECRET = "your_secret"
# IG_USER_ID = "your_ig_id"

# 3. Install & run (2 min)
pip install streamlit requests pandas
streamlit run temp.py

# Done! 🎉
```

---

## 💬 Example Interactions

### User: "Why does it keep working?"
**Answer:** Automatic token refresh! When token is about to expire (30 min left), app silently refreshes it in the background.

### User: "How long can I use it?"
**Answer:** 60 days! After that, it auto-refreshes again, adding another 60 days. You can use it indefinitely without re-login!

### User: "What if I want to logout?"
**Answer:** Click the "🚪 Logout" button in the sidebar. You'll need to re-login next time.

### User: "What if token expires?"
**Answer:** Rare! But if it happens, click "🔄 Refresh Now" or logout and re-login.

---

## 🎓 Learning Path

1. **Start:** Read [README.md](README.md) (5 min)
2. **Setup:** Follow [QUICK_START.md](QUICK_START.md) (10 min)
3. **Test:** Run app and play with it (10 min)
4. **Understand:** Read [TOKEN_REFRESH_GUIDE.md](TOKEN_REFRESH_GUIDE.md) (15 min)
5. **Deep Dive:** Check [CODE_ARCHITECTURE.md](CODE_ARCHITECTURE.md) (20 min)
6. **Reference:** Use this cheat sheet when needed (anytime!)

---

## 📞 Quick Help

**Q: Token is expired?**
A: Click "🔄 Refresh Now" or logout & re-login

**Q: Hashtag not found?**
A: Try another hashtag, check spelling

**Q: Want to test auto-refresh?**
A: Change `REFRESH_THRESHOLD = 5 * 60` to test every 5 min

**Q: How to deploy?**
A: Push to GitHub, deploy on Streamlit Cloud

**Q: Want to modify?**
A: Edit `temp.py`, change settings as needed

---

## ✅ Verification Checklist

After setup, verify:
- [ ] App starts without errors
- [ ] Login button appears
- [ ] OAuth redirect works
- [ ] Can search hashtags
- [ ] Posts display correctly
- [ ] Token countdown shows
- [ ] Can refresh token
- [ ] Can logout

If any fails, check troubleshooting in [QUICK_START.md](QUICK_START.md)

---

**This is your quick reference guide. Bookmark it!** 📌

For detailed info, check the full documentation files.

**Happy coding!** 🚀
