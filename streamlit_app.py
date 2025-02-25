import streamlit as st
import google.generativeai as genai
import requests
import json

# Configure the Gemini AI API key securely
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Ghost API credentials from Streamlit secrets
GHOST_API_URL = st.secrets["GHOST_API_URL"]
GHOST_API_KEY = st.secrets["GHOST_API_KEY"]
GHOST_API_VERSION = "v5.0"  # Specify the Ghost API version you are using

# Streamlit App UI
st.title("Ever AI Autopilot")
st.write("Generate AI content and post it to your Ghost blog automatically.")

# Prompt input field
prompt = st.text_input("Enter your prompt:", "Best alternatives to javascript?")

# Button to generate and post content
if st.button("Generate and Post"):
    try:
        # Load and configure the Gemini model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Generate response from the model
        response = model.generate_content(prompt)
        
        # Display response in Streamlit
        st.write("Generated Response:")
        st.write(response.text)
        
        # Prepare post data for Ghost API
        post_data = {
            "posts": [
                {
                    "title": f"Generated Post: {prompt}",
                    "slug": prompt.replace(" ", "-").lower(),
                    "html": f"<p>{response.text}</p>",
                    "status": "published"  # Automatically publish
                }
            ]
        }
        
        # Make API call to Ghost to post the content
        headers = {
            "Authorization": f"Ghost {GHOST_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Send POST request to create a new post on Ghost
        api_url = f"{GHOST_API_URL}/ghost/api/{GHOST_API_VERSION}/posts/"
        response = requests.post(api_url, headers=headers, data=json.dumps(post_data))
        
        # Check for successful response
        if response.status_code == 201:
            st.success("Post successfully created on Ghost blog!")
        else:
            st.error(f"Failed to post content: {response.status_code} - {response.text}")
    
    except Exception as e:
        st.error(f"Error: {e}")
