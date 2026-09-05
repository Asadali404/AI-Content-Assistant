import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ AI Content Assistant")
st.caption("Create platform-ready social content with Groq.")

# Read the API key from Streamlit Cloud Secrets or a local .streamlit/secrets.toml file.
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not api_key:
    st.error("GROQ_API_KEY is not configured. Add it to Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

with st.form("content_form"):
    content_type = st.selectbox(
        "Content type",
        ["Social media post", "LinkedIn post", "Instagram caption",
         "Facebook post", "X/Twitter post", "Product promotion", "Educational post"],
    )

    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "Instagram", "Facebook", "X/Twitter", "TikTok"],
    )

    topic = st.text_input(
        "Topic",
        placeholder="e.g. Benefits of learning Python",
    )

    target_audience = st.text_input(
        "Target audience",
        placeholder="e.g. University students and beginners",
    )

    tone = st.selectbox(
        "Tone",
        ["Professional", "Friendly", "Casual", "Educational",
         "Inspirational", "Persuasive", "Humorous"],
    )

    submitted = st.form_submit_button("🚀 Generate Content")

if submitted:
    if not topic.strip():
        st.warning("Please enter a topic.")
        st.stop()

    if not target_audience.strip():
        st.warning("Please enter a target audience.")
        st.stop()

    prompt = f"""
You are an expert social media content writer.

Create a complete, ready-to-publish piece of content using these requirements:

Content type: {content_type}
Platform: {platform}
Topic: {topic}
Target audience: {target_audience}
Tone: {tone}

Return the result in exactly this structure:

TITLE:
[short title]

POST:
[complete post/caption]

HASHTAGS:
[8-12 relevant hashtags]

Rules:
- Make the content original, useful, and engaging.
- Match the selected platform and tone.
- Do not explain your process.
- Do not add quotation marks around the post.
- Do not use fake statistics or unsupported claims.
"""

    try:
        with st.spinner("Generating your content..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You write concise, high-quality social media content.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1000,
            )

        result = response.choices[0].message.content

        st.success("Content generated!")
        st.text_area("Generated content", result, height=450)

        st.download_button(
            "⬇️ Download as TXT",
            data=result,
            file_name="ai_content.txt",
            mime="text/plain",
        )

    except Exception as e:
        st.error(f"Generation failed: {e}")
