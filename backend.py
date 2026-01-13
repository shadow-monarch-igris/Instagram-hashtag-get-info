"""
Instagram Hashtag Analyzer - Backend
Handles all API calls and data fetching
"""

import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIG =================
GRAPH_URL = "https://graph.facebook.com/v19.0"
IG_USER_ID = os.getenv("IG_USER_ID", "")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")

# ================= VALIDATION =================
def validate_token():
    """Check if token is valid"""
    if not ACCESS_TOKEN:
        return False
    return True


# ================= HASHTAG FUNCTIONS =================
def get_hashtag_id(hashtag):
    """
    Search for hashtag and get its ID
    
    Args:
        hashtag (str): Hashtag name (with or without #)
    
    Returns:
        str: Hashtag ID or None if not found
    """
    hashtag = hashtag.replace("#", "").replace(" ", "")
    
    if not hashtag:
        raise ValueError("Please enter a hashtag")
    
    try:
        url = f"{GRAPH_URL}/ig_hashtag_search"
        params = {
            "user_id": IG_USER_ID,
            "q": hashtag,
            "access_token": ACCESS_TOKEN
        }
        
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        
        data = r.json().get("data", [])
        
        if not data:
            raise ValueError(f"Hashtag '#{hashtag}' not found on Instagram")
        
        return data[0]["id"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error searching hashtag: {str(e)}")


def get_hashtag_posts(hashtag_id, limit=50):
    """
    Fetch recent posts for hashtag
    
    Args:
        hashtag_id (str): Instagram hashtag ID
        limit (int): Number of posts to fetch (10-100)
    
    Returns:
        list: List of post dictionaries with media data
    """
    url = f"{GRAPH_URL}/{hashtag_id}/recent_media"
    params = {
        "user_id": IG_USER_ID,
        "fields": "id,caption,media_type,media_url,permalink,like_count,comments_count,timestamp",
        "limit": 25,
        "access_token": ACCESS_TOKEN
    }

    posts = []
    page_count = 0
    
    while url and len(posts) < limit:
        page_count += 1
        
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            
            res = r.json()
            posts.extend(res.get("data", []))
            url = res.get("paging", {}).get("next")
            params = {}
            time.sleep(0.3)
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching posts (page {page_count}): {str(e)}")

    return posts[:limit]


# ================= SEARCH FUNCTION =================
def search_hashtag_and_fetch_posts(hashtag, limit=50):
    """
    Complete flow: Search hashtag and fetch posts
    
    Args:
        hashtag (str): Hashtag name
        limit (int): Number of posts to fetch
    
    Returns:
        list: List of post dictionaries
    """
    # Get hashtag ID
    hid = get_hashtag_id(hashtag)
    
    # Fetch posts
    posts = get_hashtag_posts(hid, limit)
    
    return posts
