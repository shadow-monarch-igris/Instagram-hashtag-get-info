import streamlit as st
import requests
import pandas as pd
import time

# ================= CONFIG =================
ACCESS_TOKEN = "EAAWum2I4bRkBQQCPiPnMwL6Sp8ctVoTXyZAOVKZCceiWfWGJQ97RazEGo1XV9EauRGZBvvN7GgpNPhZAkfv7YowNKZBsuzu4amJChMh90z4oIKy8PH8cY3hZBUUvg9NZCZCTJQkuwtjxLyHAdfCYdjjWwFANukJDHRmghO6WM9zmSwmu5NxBKvoKnT0tuYX4ziQssJ711ATUCQDkLpHw3qf3O1CBW8gjZALqSTMJkvXZC09JPH99ZCvnMMcyaMHa7nnuzwZCRoYy3tOIfPUZD"
IG_USER_ID = "17841480245320197"
GRAPH_URL = "https://graph.facebook.com/v24.0"

# ================= API FUNCTIONS =================

def get_hashtag_id(hashtag):
    hashtag = hashtag.replace("#", "").replace(" ", "")

    url = f"{GRAPH_URL}/ig_hashtag_search"
    params = {
        "user_id": IG_USER_ID,
        "q": hashtag,
        "access_token": ACCESS_TOKEN
    }

    try:
        r = requests.get(url, params=params, timeout=30)

        # 🔥 INVALID / BAD HASHTAG HANDLING
        if r.status_code == 400:
            return None

        r.raise_for_status()

        data = r.json().get("data", [])
        return data[0]["id"] if data else None

    except requests.exceptions.RequestException:
        return None


def get_hashtag_posts(hashtag_id, limit=50):
    url = f"{GRAPH_URL}/{hashtag_id}/recent_media"
    params = {
        "user_id": IG_USER_ID,
        "fields": (
            "id,caption,media_type,media_url,"
            "Post_link,like_count,comments_count,timestamp"
        ),
        "access_token": ACCESS_TOKEN,
        "limit": 25
    }

    posts = []
    while url and len(posts) < limit:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        res = r.json()

        data = res.get("data", [])
        remaining = limit - len(posts)
        posts.extend(data[:remaining])

        if len(posts) >= limit:
            break

        url = res.get("paging", {}).get("next")
        params = None
        time.sleep(0.3)

    return posts


# ================= STREAMLIT UI =================

st.set_page_config(page_title="Instagram Hashtag Analyzer", layout="wide")
st.title("📊 Instagram Hashtag Analyzer")
st.caption("Official Instagram Graph API • Recent posts only • Production safe")

with st.sidebar:
    hashtag = st.text_input("Hashtag ", placeholder="travel")
    post_limit = st.slider("Number of posts to fetch", 10, 100, 50)
    fetch_btn = st.button("🔍 Fetch Data")


if fetch_btn:
    if not hashtag:
        st.error("Please enter a hashtag")
        st.stop()

    try:
        with st.spinner("Fetching hashtag ID..."):
            hashtag_id = get_hashtag_id(hashtag)

        # ✅ CLEAN INVALID TAG MESSAGE
        if not hashtag_id:
            st.error("❌ Invalid or unavailable hashtag. Please try another one.")
            st.stop()

        st.success(f"Hashtag ID: {hashtag_id}")

        with st.spinner("Fetching posts..."):
            posts = get_hashtag_posts(hashtag_id, post_limit)

        if not posts:
            st.warning("No posts returned by Instagram API")
            st.stop()

        df = pd.DataFrame(posts)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df["caption"] = df["caption"].fillna("").str.slice(0, 150)

        st.info(f"🔢 Posts fetched: {len(df)}")

        # ================= TABLE =================
        st.subheader("📋 Recent Hashtag Posts")
        st.dataframe(
            df[
                [
                    "id",
                    "media_type",
                    "like_count",
                    "comments_count",
                    "timestamp",
                    "permalink",
                    "caption",
                ]
            ],
            use_container_width=True,
        )

        # ================= DOWNLOAD =================
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download CSV",
            csv,
            file_name=f"{hashtag}_recent_posts.csv",
            mime="text/csv",
        )

        # ================= DETAILS =================
        st.subheader("🧾 Post Details")
        for _, post in df.iterrows():
            with st.expander(
                f"❤️ {post.like_count} | 💬 {post.comments_count} | {post.timestamp}"
            ):
                st.write("**Caption:**", post.caption)
                st.write("**Media Type:**", post.media_type)
                st.markdown(f"[Open Post]({post.permalink})")

    except Exception as e:
        st.error(f"❌ Error: {e}")


st.markdown("---")
st.caption("Powered by MRT • RAJ • Suraj • shiv • Production Ready")
