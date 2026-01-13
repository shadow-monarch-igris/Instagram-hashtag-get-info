import streamlit as st
import requests
import pandas as pd
import time

# ================= CONFIG =================
ACCESS_TOKEN = "acces token"
IG_USER_ID = "your user id "
GRAPH_URL = "https://graph.facebook.com/v24.0"

# ================= API FUNCTIONS =================

def get_hashtag_id(hashtag):
    hashtag = hashtag.replace("#","").replace(" ", "")
    url = f"{GRAPH_URL}/ig_hashtag_search"
    params = {
        "user_id": IG_USER_ID,
        "q": hashtag,
        "access_token": ACCESS_TOKEN
    }
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json().get("data", [])
    return data[0]["id"] if data else None


def get_hashtag_posts(hashtag_id, limit=50):
    url = f"{GRAPH_URL}/{hashtag_id}/recent_media"
    params = {
        "user_id": IG_USER_ID,
        "fields": (
            "id,caption,media_type,media_url,"
            "permalink,like_count,comments_count,timestamp"
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
        time.sleep(0)    ## change to 0.3

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
        hashtag_id = get_hashtag_id(hashtag)
        if not hashtag_id:
            st.error("Hashtag not found")
            st.stop()

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

        # ================= DOWNLOAD CSV =================
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

                # 🔥 DIRECT MEDIA RENDER (NO LINK)
                if post.media_type == "IMAGE":
                    st.image(post.media_url, use_container_width=True)

                elif post.media_type == "VIDEO":
                    st.video(post.media_url)

                elif post.media_type == "CAROUSEL_ALBUM":
                    st.info("Carousel post (preview media)")
                    st.image(post.media_url, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")


st.markdown("---")
st.caption("Powered by MRT • RAJ • Suraj • shiv • Production Ready")
