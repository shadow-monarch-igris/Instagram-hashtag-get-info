# 📊 Visual Reference & Flowcharts

## 🔄 Complete Token Refresh Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      USER STARTS APPLICATION                            │
└─────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │  Check: Has access_token?    │
                    └──────────────────────────────┘
                        YES ↓            ↓ NO
                           │            │
                    ┌──────▼─────────┐  │
                    │ Authenticated  │  │
                    │   State        │  │
                    └────────────────┘  │
                           │            │
                           │       ┌────▼──────────────────┐
                           │       │ Show Login Button     │
                           │       │ "🔐 Login with IG"    │
                           │       └────┬─────────────────┘
                           │            │
                           │      USER CLICKS LOGIN
                           │            │
                           │       ┌────▼──────────────────┐
                           │       │ Redirect to OAuth     │
                           │       │ (Facebook Login)      │
                           │       └────┬─────────────────┘
                           │            │
                           │      USER GRANTS PERMISSION
                           │            │
                           │       ┌────▼──────────────────┐
                           │       │ Redirect back with    │
                           │       │ authorization code    │
                           │       └────┬─────────────────┘
                           │            │
                           │       ┌────▼──────────────────┐
                           │       │ Exchange code for     │
                           │       │ short-lived token     │
                           │       │ (2 hours validity)    │
                           │       └────┬─────────────────┘
                           │            │
                           │       ┌────▼──────────────────┐
                           │       │ Convert to           │
                           │       │ long-lived token      │
                           │       │ (60 days validity)    │
                           │       └────┬─────────────────┘
                           │            │
                    ┌──────┴────────────▼──────────┐
                    │  Store in session_state      │
                    │  - access_token              │
                    │  - token_created_at          │
                    │  - token_expires_at          │
                    │  - token_type = "long"       │
                    └──────────┬───────────────────┘
                               │
                    ┌──────────▼────────────┐
                    │  SHOW MAIN APP        │
                    │  - Token Status       │
                    │  - Search Bar         │
                    │  - Fetch Button       │
                    └──────────┬────────────┘
                               │
                           MAIN LOOP
                               │
                    ┌──────────▼────────────┐
                    │ User searches for     │
                    │ hashtag or scrolls    │
                    └──────────┬────────────┘
                               │
                    ┌──────────▼────────────┐
                    │ Check: Token valid?   │
                    │ (ensure_token_valid)  │
                    └────────┬──────┬───────┘
                         YES │      │ EXPIRING SOON?
                             │      │ (< 30 minutes)
                             │      │
                    ┌────────▼──┐   ▼─────────────────────┐
                    │ Continue   │   ┌──────────────────┐  │
                    │ to API     │   │ Refresh Token    │  │
                    │ call       │   │ (Auto-refresh!)  │  │
                    └────────┬───┘   └────────┬─────────┘  │
                             │                │             │
                    ┌────────▼────────────────▼──────────┐
                    │ Make API Call                      │
                    │ - Search hashtag / Fetch posts     │
                    │ (Token automatically added)        │
                    └──────────┬───────────────────────┘
                               │
                    ┌──────────▼────────────┐
                    │ Display Results       │
                    │ - Posts Table         │
                    │ - Individual Cards    │
                    └──────────┬────────────┘
                               │
                           CONTINUE
                           (Loop back)
```

---

## 🔐 Token Lifecycle Timeline

```
Day 1                          Day 30                         Day 60
├─ 00:00 ─ Login ───────────────┤ Auto-refresh triggered ───────┤ Token Expires
│  SHORT TOKEN (2h)             │ (when 30 min left)            │
│  └─ Valid for 2 hours         │ └─ Extended 60 days           │
│                               │                                │
├─ CONVERT TO LONG TOKEN        ├─ NEW LONG TOKEN (60 days)     │
│  Valid for 60 days            │                                │
│  ├─ Days 1-30: No refresh     │ Days 30-60: One auto-refresh  │
│  └─ Day 30: Auto-refresh      │                                │
│                               │ Can refresh multiple times!    │
│
Timeline without limit:
Day 1 ─ Login
  └─ Day 1-30: Token valid
  └─ Day 30: Auto-refresh #1 → Valid until Day 90
  └─ Day 60: Auto-refresh #2 → Valid until Day 120
  └─ Day 90: Auto-refresh #3 → Valid until Day 150
  ...and so on!

User can work indefinitely! 🎉
```

---

## 🔍 API Call Flow (With Auto-Refresh)

```
┌──────────────────┐
│ User Action      │
│ (Fetch Posts)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ call api_get(url, params)            │
│ "Make an API call"                   │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ call ensure_token_valid()            │
│ "Is token ready?"                    │
└────────┬─────────────────────────────┘
         │
         ▼
    ┌────────────────┐
    │ Token exists?  │
    └───┬──────────┬─┘
        │ YES      │ NO
        │          │
        │     ┌────▼──────────────┐
        │     │ ERROR: No token   │
        │     │ Show "Re-login"   │
        │     │ st.stop()         │
        │     └───────────────────┘
        │
        ▼
    ┌────────────────────────┐
    │ Check expiry time      │
    │ is_token_expiring_     │
    │  soon()                │
    └───┬────────────────┬───┘
        │ NOT SOON       │ EXPIRING SOON!
        │ (> 30 min)     │ (< 30 min left)
        │                │
        ▼                ▼
    ┌─────┐      ┌────────────────┐
    │PASS │      │ Refresh Token  │
    └──┬──┘      │ (Auto!)        │
       │         └────────┬───────┘
       │                  │
       │         ┌────────▼──────────┐
       │         │ Call fb_exchange_ │
       │         │ token API         │
       │         │ (Convert to new)  │
       │         └────────┬──────────┘
       │                  │
       │         ┌────────▼──────────┐
       │         │ Update session:   │
       │         │ - new token       │
       │         │ - new expiry      │
       │         │ Show toast!       │
       │         └────────┬──────────┘
       │                  │
       └──────────┬───────┘
                  │
         ┌────────▼──────────┐
         │ Add token to      │
         │ API params        │
         │ params["access_   │
         │  token"] = token  │
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │ Make HTTP GET     │
         │ request to API    │
         └────────┬──────────┘
                  │
         ┌────────▼──────────┐
         │ Check response    │
         │ status code       │
         └────────┬──────────┘
                  │
        ┌─────────┴──────────┬───────────┐
        │                    │           │
    200 ▼ OK           400/401 ▼      Other ▼
        │             (Auth Error)      │
   ┌────────┐      ┌──────────────┐  ┌────────┐
   │ Return │      │ ERROR        │  │ Raise  │
   │ result │      │ Re-login     │  │ Error  │
   └────────┘      │ st.stop()    │  └────────┘
                   └──────────────┘
```

---

## 🎯 Token Refresh Decision Tree

```
                    API Call Made?
                         │
                    ┌────┴────┐
                    │          │
                    ▼          ▼
                  YES          NO
                    │          │
            ┌───────┘          └─────────────┐
            │                                 │
            ▼                                 ▼
    Has Token?                         No API Call
        │                              (Skip checks)
        ├─ NO → Re-login
        │       Error & Stop
        │
        ├─ YES → Continue
        │        │
        │        ▼
        │    Token Expires At?
        │        │
        │        ├─ NULL → Continue
        │        │         (No expiry info)
        │        │
        │        ├─ YES → Calculate
        │        │        Time Left
        │        │        │
        │        │        ▼
        │        │    < 30 minutes?
        │        │        │
        │        │   ┌────┴───┐
        │        │   │        │
        │        │ YES      NO
        │        │   │        │
        │    ┌───▼─┐ │    ┌───▼──┐
        │    │REFRESH    │CONTINUE
        │    └───┬─┘     └────┬──┘
        │        │            │
        │    Update       Proceed
        │    session      to API
        │    Show toast
        │        │
        └────────┴────────┐
                         │
                    Proceed
                    to API
```

---

## 📱 Session State Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  st.session_state                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ access_token (String)                          │   │
│  │ ────────────────────────                        │   │
│  │ Value: "EAAWum2I4bRkBQ..."                     │   │
│  │ Type: Long-lived OAuth token                   │   │
│  │ Used: Every API call                           │   │
│  │ Updated: On login & auto-refresh               │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ token_type (String)                            │   │
│  │ ──────────────────                             │   │
│  │ Value: "short" or "long"                       │   │
│  │ Purpose: Track token type                      │   │
│  │ Updated: During conversion & refresh           │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ token_created_at (DateTime)                    │   │
│  │ ──────────────────────────                     │   │
│  │ Value: 2024-01-15 10:30:45 UTC                 │   │
│  │ Purpose: Track creation time                   │   │
│  │ Updated: On login & auto-refresh               │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
│  ┌────────────────────────────────────────────────┐   │
│  │ token_expires_at (DateTime)                    │   │
│  │ ────────────────────────────                   │   │
│  │ Value: 2024-03-14 10:30:45 UTC (60 days later) │   │
│  │ Purpose: Track expiry time                     │   │
│  │ Used: For countdown & refresh check            │   │
│  │ Updated: On login & auto-refresh               │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘

Data flows:
┌─ Set on Login ──────────────┐
│                             │
├─ Updated on Auto-Refresh ──┤
│                             │
├─ Cleared on Logout ────────┤
│                             │
└─ Persists across Reloads ──┘
  (Streamlit Session = Browser Tab)
```

---

## 🔔 User Notifications

```
Scenario 1: Initial Login
┌────────────────────────┐
│ 🔐 Login with Instagram│
│ (Click to authorize)   │
└────────────────────────┘
        ↓ (User clicks)
┌────────────────────────┐
│ ⏳ Logging in...       │
│ (Spinner)              │
└────────────────────────┘
        ↓ (After OAuth)
┌────────────────────────┐
│ ✅ Login successful    │
│ (60-day token)         │
└────────────────────────┘
        ↓
   Show Main App
   + Token Status
   + Search Bar

─────────────────────────────────

Scenario 2: Auto-Refresh (30-min before expiry)
During normal usage...
        │
   User makes API call
        │
   Token < 30 min left
        │
   ┌────▼────┐
   │ Auto-   │
   │Refresh  │
   │in bg    │
   └────┬────┘
        │
   ┌────▼─────────────────────┐
   │ 🔄 Access token          │
   │ auto-refreshed! ✅       │
   │ (Toast notification)     │
   └──────────────────────────┘
        │
   User continues working
   Token extended 60 more days

─────────────────────────────────

Scenario 3: Failed Refresh
Rare case (network error)
        │
   Auto-refresh triggered
        │
   Network error occurs
        │
   ┌──────────────────────────┐
   │ ⚠️ Token refresh failed  │
   │ (Error message)          │
   └──────────────────────────┘
        │
   ┌──────────────────────────┐
   │ ❌ Token Expired         │
   │ Please re-login          │
   │ (User message)           │
   └──────────────────────────┘

─────────────────────────────────

Scenario 4: Manual Refresh
User clicks button
        │
   ┌────▼───────────┐
   │ 🔄 Refresh Now │
   │ (Button)       │
   └────┬───────────┘
        │
   Refresh triggered
        │
   ┌────▼─────────────────────┐
   │ 🔄 Access token          │
   │ auto-refreshed! ✅       │
   │ (Toast notification)     │
   └──────────────────────────┘
        │
   App reloads
   Countdown resets to 60 days
```

---

## 🎯 Function Call Stack (Hashtag Search)

```
User clicks "🔍 Fetch Posts"
        │
        ▼
if fetch:
        │
        ▼
get_hashtag_id(hashtag)
    │
    └─▶ api_get(url, params)
        │
        ├─▶ ensure_token_valid()
        │   │
        │   ├─▶ is_token_expiring_soon()
        │   │   └─▶ Return Boolean
        │   │
        │   ├─▶ refresh_long_lived_token()
        │   │   │
        │   │   └─▶ exchange_long_lived(token)
        │   │       └─▶ requests.get() [API]
        │   │
        │   └─▶ Return Boolean
        │
        ├─▶ requests.get() [API]
        │
        └─▶ Return Response
    │
    └─▶ Return Hashtag ID
        │
        ▼
get_hashtag_posts(hashtag_id, limit)
    │
    └─▶ Loop: while url and len(posts) < limit
        │
        ├─▶ api_get(url, params)
        │   ├─▶ ensure_token_valid()
        │   ├─▶ requests.get() [API]
        │   └─▶ Return Response
        │
        ├─▶ Extract posts from response
        │
        ├─▶ Get next page URL
        │
        ├─▶ time.sleep(0.3)
        │
        └─▶ Repeat
    │
    └─▶ Return Posts List
        │
        ▼
Display Results
    │
    ├─▶ Create DataFrame
    │
    ├─▶ Show Table
    │
    └─▶ Show Expanders
        (Each post card)
```

---

## 📊 Data Structure

```
API Response (Hashtag ID)
{
  "data": [
    {
      "id": "hashtag_id_12345",
      "name": "travel"
    }
  ]
}

API Response (Recent Posts)
{
  "data": [
    {
      "id": "post_123",
      "caption": "Beautiful sunset...",
      "media_type": "IMAGE",
      "media_url": "https://...",
      "like_count": 1250,
      "comments_count": 45,
      "timestamp": "2024-01-15T10:30:00+0000"
    },
    ...
  ],
  "paging": {
    "next": "https://graph.facebook.com/..."
  }
}

Session State
{
  "access_token": "EAAWum2I4bRkBQ...",
  "token_type": "long",
  "token_created_at": DateTime(2024-01-15 10:30:45),
  "token_expires_at": DateTime(2024-03-14 10:30:45)
}

DataFrame
  id    | media_type | like_count | comments_count | timestamp
────────┼────────────┼────────────┼────────────────┼──────────────
post_1  | IMAGE      | 1250       | 45             | 2024-01-15
post_2  | VIDEO      | 2100       | 78             | 2024-01-14
post_3  | IMAGE      | 890        | 32             | 2024-01-13
```

---

## ✅ Validation Checklist

```
DURING LOGIN:
☑️ Authorization code captured from URL
☑️ Code exchanged for short token
☑️ Short token converted to long token
☑️ Long token stored in session
☑️ Expiry time calculated (now + 60 days)
☑️ Success message shown
☑️ App reloaded with auth state

BEFORE EACH API CALL:
☑️ Token exists in session
☑️ Expiry time checked
☑️ If < 30 min left → auto-refresh
☑️ Token added to API request
☑️ Request made successfully

AFTER API RESPONSE:
☑️ Status code checked (200, 400, 401)
☑️ Error handling applied
☑️ Response parsed
☑️ Data returned to caller

ON LOGOUT:
☑️ access_token cleared
☑️ token_type cleared
☑️ token_created_at cleared
☑️ token_expires_at cleared
☑️ App reloaded
☑️ Login screen shown
```

---

**All visualizations are ready! The system is fully documented.** 🎉
