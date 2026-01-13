"""
Instagram Hashtag Analyzer - Frontend
Streamlit UI for hashtag search and post display
"""

import streamlit as st
import pandas as pd
from backend import validate_token, search_hashtag_and_fetch_posts

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Instagram Hashtag Analyzer", layout="wide")
st.title("📊 Instagram Hashtag Analyzer")
st.caption("Official Instagram Graph API • Recent posts only • Production safe")

# ================= TOKEN CHECK =================
if not validate_token():
    st.error("❌ No access token found in .env file")
    st.stop()

# ================= SIDEBAR =================
with st.sidebar:
    hashtag = st.text_input("Hashtag", placeholder="travel")
    post_limit = st.slider("Number of posts to fetch", 10, 100, 50)
    fetch_btn = st.button("🔍 Fetch Data")

# ================= MAIN LOGIC =================
if fetch_btn:
    if not hashtag:
        st.error("Please enter a hashtag")
        st.stop()

    try:
        posts = search_hashtag_and_fetch_posts(hashtag, post_limit)
        if not posts:
            st.warning("No posts returned by Instagram API")
            st.stop()

        df = pd.DataFrame(posts)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        df["caption"] = df["caption"].fillna("").str.slice(0, 150)
        
        # Handle NaN values
        df["like_count"] = df["like_count"].fillna(0).astype(int)
        df["comments_count"] = df["comments_count"].fillna(0).astype(int)

        st.info(f"🔢 Posts fetched: {len(df)}")

        # ================= TABLE =================
        st.subheader("📋 Recent Hashtag Posts")
        st.dataframe(
            df[
                [
                    "media_type",
                    "like_count",
                    "comments_count",
                    "timestamp",
                    "permalink",
                    "caption",
                ]
            ],
            use_container_width=True,
            hide_index=True,
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
        for idx, (_, post) in enumerate(df.iterrows(), 1):
            with st.expander(
                f"Post {idx} | ❤️ {post.like_count} | 💬 {post.comments_count} | {post.timestamp}"
            ):
                # Caption
                if post.caption:
                    st.markdown(f"**Caption:**\n\n{post.caption}")
                    st.divider()
                
                # Media Type & Link
                st.write("**Media Type:**", post.media_type)
                st.markdown(f"**Link:** [View on Instagram]({post.permalink})")
                st.divider()
                
                # Media and Stats side by side
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # 🔥 DIRECT MEDIA RENDER
                    if post.media_type == "IMAGE":
                        st.image(post.media_url, use_container_width=True)

                    elif post.media_type == "VIDEO":
                        st.video(post.media_url)

                    elif post.media_type == "CAROUSEL_ALBUM":
                        st.info("Carousel post (preview media)")
                        st.image(post.media_url, use_container_width=True)
                
                with col2:
                    st.metric("❤️ Likes", int(post.like_count))
                    st.metric("💬 Comments", int(post.comments_count))
                    st.caption(f"📅 {post.timestamp.strftime('%Y-%m-%d %H:%M')}")

    except Exception as e:
        st.error(f"❌ Error: {e}")

st.markdown("---")
st.caption("Powered by Instagram Graph API • Permanent Token • Production Ready ✅")
