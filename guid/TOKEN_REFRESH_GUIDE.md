# Instagram Hashtag Analyzer - Token Refresh System Guide

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│         Instagram OAuth Flow with Auto Token Refresh        │
└─────────────────────────────────────────────────────────────┘

1. USER LOGIN
   └─> Clicks "Login with Instagram" button
   └─> Redirected to Facebook OAuth dialog
   └─> User grants permissions

2. AUTHORIZATION CODE
   └─> Facebook redirects to http://localhost:8501?code=XXX
   └─> App captures authorization code

3. SHORT-LIVED TOKEN (2 hours)
   └─> POST /oauth/access_token
   └─> Exchange authorization code for short-lived token
   └─> Valid for only 2 hours

4. LONG-LIVED TOKEN (60 days)  ⭐ KEY FEATURE
   └─> GET /oauth/access_token?grant_type=fb_exchange_token
   └─> Convert short-lived token to long-lived token
   └─> Valid for 60 days
   └─> Stored in st.session_state

5. AUTO REFRESH (Before Expiry)  ⭐ KEY FEATURE
   └─> Every API call checks: is_token_expiring_soon()?
   └─> If token expires in < 30 minutes → Refresh automatically
   └─> refresh_long_lived_token() extends token life by 60 days
   └─> User doesn't need to re-login!

6. TOKEN STATUS DISPLAY  ⭐ NEW FEATURE
   └─> Shows remaining time (days, hours, minutes)
   └─> Manual refresh button available
   └─> Logout button to clear session
```

---

## 🔐 Token Types & Lifecycle

### Short-Lived Token (2 hours)
```python
SHORT_TOKEN_EXPIRY = 2 * 60 * 60  # 7,200 seconds
```
- **Validity:** 2 hours from creation
- **Use:** Temporary access right after OAuth login
- **Action:** Immediately convert to long-lived token

### Long-Lived Token (60 days)
```python
LONG_TOKEN_EXPIRY = 60 * 24 * 60 * 60  # 5,184,000 seconds
```
- **Validity:** 60 days from last refresh
- **Use:** Primary token for API calls
- **Action:** Auto-refresh before expiry

---

## 🔄 Auto-Refresh Logic

### 1. Check Before Every API Call
```python
def ensure_token_valid():
    """Ensure token is valid before API calls"""
    if not st.session_state.access_token:
        return False
    
    # Auto-refresh if expiring soon
    if is_token_expiring_soon():
        return refresh_long_lived_token()
    
    return True
```

### 2. Expiry Detection (30-min threshold)
```python
REFRESH_THRESHOLD = 30 * 60  # 30 minutes

def is_token_expiring_soon():
    """Check if token is expiring soon (within refresh threshold)"""
    if not st.session_state.token_expires_at:
        return False
    
    time_until_expiry = st.session_state.token_expires_at - datetime.now()
    return time_until_expiry.total_seconds() < REFRESH_THRESHOLD
```

**When does refresh happen?**
- When token has < 30 minutes remaining
- Before ANY API call
- NO USER INTERACTION NEEDED ✅

### 3. Token Refresh Function
```python
def refresh_long_lived_token():
    """Refresh long-lived token before it expires"""
    try:
        new_token = exchange_long_lived(st.session_state.access_token)
        st.session_state.access_token = new_token
        st.session_state.token_type = "long"
        st.session_state.token_created_at = datetime.now()
        st.session_state.token_expires_at = datetime.now() + timedelta(seconds=LONG_TOKEN_EXPIRY)
        st.toast("🔄 Access token auto-refreshed!", icon="✅")
        return True
    except Exception as e:
        st.error(f"⚠️ Token refresh failed: {e}")
        return False
```

---

## 📊 Session State Tracking

```python
if "access_token" not in st.session_state:
    st.session_state.access_token = None           # Token string
    st.session_state.token_type = None             # "short" or "long"
    st.session_state.token_created_at = None       # When created
    st.session_state.token_expires_at = None       # When expires
```

**Stored Information:**
1. `access_token` - The actual OAuth token
2. `token_type` - Track if it's "short" or "long" lived
3. `token_created_at` - Timestamp of creation
4. `token_expires_at` - Exact expiry datetime

---

## 🎯 Complete OAuth Flow Step-by-Step

### Step 1: User Initiates Login
```python
def login_button():
    auth_url = (
        f"{OAUTH_URL}"
        f"?client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=instagram_basic,pages_show_list"
        f"&response_type=code"
    )
    st.markdown(f"### 🔐 [Login with Instagram]({auth_url})")
```

### Step 2: Exchange Code for Short Token
```python
def exchange_code_for_token(code):
    url = "https://graph.facebook.com/v19.0/oauth/access_token"
    params = {
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    r = requests.get(url, params=params, timeout=30)
    return r.json()["access_token"]
```

### Step 3: Convert to Long-Lived Token
```python
def exchange_long_lived(short_token):
    r = requests.get(
        f"{GRAPH_URL}/oauth/access_token",
        params={
            "grant_type": "fb_exchange_token",      # ⭐ Magic!
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "fb_exchange_token": short_token,       # Convert short → long
        },
        timeout=30,
    )
    return r.json()["access_token"]
```

### Step 4: Handle Redirect & Store Token
```python
query = st.query_params
if "code" in query and not st.session_state.access_token:
    with st.spinner("Logging in…"):
        short_token = exchange_code_for_token(query["code"])
        long_token = exchange_long_lived(short_token)
        st.session_state.access_token = long_token
        st.session_state.token_type = "long"
        st.session_state.token_created_at = datetime.now()
        st.session_state.token_expires_at = datetime.now() + timedelta(seconds=LONG_TOKEN_EXPIRY)
        st.success("✅ Login successful (60-day token)")
        st.rerun()
```

---

## 🛡️ Error Handling

### During API Calls
```python
def api_get(url, params):
    """Safe API call with token validation"""
    if not ensure_token_valid():
        st.error("❌ Access token expired or invalid. Please re-login.")
        st.stop()
    
    params["access_token"] = st.session_state.access_token
    r = requests.get(url, params=params, timeout=30)
    
    if r.status_code in (400, 401):
        st.error("⚠️ Access token expired. Please re-login.")
        st.stop()
    
    r.raise_for_status()
    return r
```

**Handles:**
- ✅ No token (requires login)
- ✅ Token expiring soon (auto-refresh)
- ✅ Token invalid/expired (show error)
- ✅ HTTP 400/401 errors (re-login)

---

## 📱 User Interface Features

### Token Status Display
```
🔐 Token Status
────────────────
✅ Active for 59d 12h 45m
┌─────────┬────────┐
│ Refresh │ Logout │
└─────────┴────────┘
```

### Features:
1. **Live Countdown** - Shows remaining token validity
2. **Manual Refresh Button** - User can refresh anytime
3. **Logout Button** - Clear session & require re-login
4. **Auto Toast Notifications** - Feedback on auto-refresh

---

## 🚀 How to Use (For End Users)

1. **First Time:**
   - Click "🔐 Login with Instagram" button
   - Grant permissions
   - Redirected back automatically

2. **Long Session:**
   - Token auto-refreshes every time it's about to expire
   - No action needed from user
   - See countdown in sidebar

3. **Manual Refresh (Optional):**
   - Click "🔄 Refresh Now" button anytime
   - Token validity resets to 60 days

4. **Logout:**
   - Click "🚪 Logout" button
   - All session data cleared
   - Must login again to use app

---

## 🔧 Configuration

Edit these values in the code:

```python
# How long until token expires before refresh?
REFRESH_THRESHOLD = 30 * 60  # 30 minutes

# Short-lived token validity
SHORT_TOKEN_EXPIRY = 2 * 60 * 60  # 2 hours

# Long-lived token validity
LONG_TOKEN_EXPIRY = 60 * 24 * 60 * 60  # 60 days
```

---

## 📚 Instagram API References

- **Official Docs:** https://developers.facebook.com/docs/instagram-api/guides/access-tokens
- **Token Exchange:** https://developers.facebook.com/docs/facebook-login/access-tokens/refreshing
- **Graph API v19.0:** https://graph.facebook.com/v19.0

---

## ⚠️ Important Notes

1. **Never hardcode tokens** in production
2. **Store APP_SECRET securely** (use environment variables)
3. **REDIRECT_URI must match** registered URL in app
4. **Scopes must be approved** by Instagram review team
5. **Token refresh happens automatically** - no user action needed

---

## 🎯 Summary

| Feature | Status | Details |
|---------|--------|---------|
| OAuth Login | ✅ | Full flow implemented |
| Short Token | ✅ | 2-hour temporary token |
| Long Token | ✅ | 60-day persistent token |
| Auto Refresh | ✅ | Before 30-min expiry |
| Token Status UI | ✅ | Countdown display |
| Manual Refresh | ✅ | User can refresh anytime |
| Logout | ✅ | Clear all session data |
| Error Handling | ✅ | Comprehensive checks |

**Result:** Users can work for hours without re-login! 🎉
