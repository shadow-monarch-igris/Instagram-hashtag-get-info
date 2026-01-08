import streamlit as st
import requests
import os


CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8501"

AUTH_URL = "https://api.instagram.com/oauth/authorize"
TOKEN_URL = "https://api.instagram.com/oauth/access_token"
GRAPH_URL = "https://graph.instagram.com/me"

st.set_page_config(page_title="Instagram OAuth Login")
st.title(" Instagram Login using OAuth (Streamlit)")

auth_link = (
    f"{AUTH_URL}"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&scope=user_profile"
    f"&response_type=code"
)

st.markdown("### Step 1: Login with Instagram")
st.markdown(f"[🔐 Login with Instagram]({auth_link})")


query_params = st.query_params
auth_code = query_params.get("code")

if auth_code:
    st.success("✅ Authorization code received!")

    token_payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": auth_code
    }

    token_response = requests.post(TOKEN_URL, data=token_payload)
    token_data = token_response.json()

    if "access_token" in token_data:
        access_token = token_data["access_token"]
        st.success("✅ Access Token generated!")


        user_response = requests.get(
            GRAPH_URL,
            params={
                "fields": "id,username",
                "access_token": access_token
            }
        )

        user_data = user_response.json()

        if "username" in user_data:
            st.subheader("🎉 Login Successful")
            st.write("👤 Instagram Username:")
            st.code(user_data["username"])

            print("Logged-in Instagram Username:", user_data["username"])
        else:
            st.error("❌ Failed to fetch user profile")
    else:
        st.error("❌ Failed to get access token")
