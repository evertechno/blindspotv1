import requests
import json

# Configuration: Replace these with your actual API credentials and URLs
CONTENT_API_URL = "https://your-content-api.com/generate"
CONTENT_API_KEY = "your-content-api-key"
GHOST_API_URL = "https://your-ghost-site.com/ghost/api/v3/content/posts/"
GHOST_API_KEY = "your-ghost-api-key"
GHOST_ADMIN_API_URL = "https://your-ghost-site.com/ghost/api/v3/admin/posts/"

# Generate Content
def generate_content():
    headers = {
        'Authorization': f"Bearer {CONTENT_API_KEY}",
        'Content-Type': 'application/json'
    }
    payload = {
        "prompt": "Write a blog post about AI in 2025",  # Example prompt, adjust as needed
        "language": "en",
        "max_tokens": 500  # Adjust based on your API limits
    }

    response = requests.post(CONTENT_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        generated_content = response.json()
        return generated_content['text']
    else:
        print("Error generating content:", response.text)
        return None

# Post Content to Ghost
def post_to_ghost(title, content):
    headers = {
        'Authorization': f"Ghost {GHOST_API_KEY}",
        'Content-Type': 'application/json'
    }
    data = {
        "posts": [
            {
                "title": title,
                "html": content,
                "status": "draft",  # Use 'published' for immediate publishing
            }
        ]
    }

    response = requests.post(GHOST_ADMIN_API_URL, headers=headers, json=data)

    if response.status_code == 201:
        print("Content posted successfully.")
    else:
        print("Error posting to Ghost:", response.text)

# Main AutoPilot Logic
def autopilot():
    print("Starting autopilot...")

    # Generate Content
    content = generate_content()
    if content:
        title = "AI in 2025"  # Customize title if needed
        # Post the generated content to Ghost
        post_to_ghost(title, content)
    else:
        print("No content generated, aborting autopilot.")

if __name__ == "__main__":
    autopilot()
