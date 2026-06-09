import streamlit as st
from groq import Groq
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------
# Page Configuration
# -----------------------------------
st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="centered"
)

# -----------------------------------
# Sidebar
# -----------------------------------
with st.sidebar:

    st.header("🌱 Eco Tip of the Day")

    st.info(
        "Carry a reusable water bottle to reduce single-use plastic waste."
    )

    st.markdown("---")

    st.write("🎯 SDG 12")
    st.write("Responsible Consumption & Production")

# -----------------------------------
# Groq Configuration
# -----------------------------------

# Option 1 (Recommended):
# Set environment variable GROQ_API_KEY



client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# -----------------------------------
# AI Classification
# -----------------------------------

def classify_waste(item):

    prompt = f"""
Classify this waste item into ONE category:

- Recyclable
- Biodegradable
- E-Waste
- Hazardous

Item: {item}

Return ONLY the category name.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


def get_disposal_method(item, category):

    prompt = f"""
Waste Item: {item}
Category: {category}

Provide a safe disposal method in one sentence.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


def get_environmental_impact(item):

    prompt = f"""
Explain the environmental impact of improper disposal of:

{item}

Keep under 40 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()


def generate_ai_recommendation(
    item,
    category,
    disposal_method
):

    prompt = f"""
You are EcoSort AI, an expert in sustainability.

Waste Item: {item}
Category: {category}
Disposal Method: {disposal_method}

Return in markdown:

## ♻️ Environmental Impact
- One environmental risk
- One environmental benefit

## 💡 Recycling / Disposal Tip
- Three practical tips

## 🌱 Sustainability Recommendation
- Three eco-friendly recommendation

Keep under 200 words.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=250
    )

    return response.choices[0].message.content


# -----------------------------------
# Image Recognition
# -----------------------------------

def identify_waste_from_image(uploaded_file):

    image_bytes = uploaded_file.read()

    base64_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text":
                        """
Identify the waste item shown in the image.

Respond ONLY with the item name.

Examples:
plastic bottle
banana peel
battery
newspaper
old laptop
glass bottle
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":
                            f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content.strip()


# -----------------------------------
# Header
# -----------------------------------

st.title("♻️ EcoSort AI")
st.markdown(
    "### AI-Powered Waste Segregation & Recycling Assistant"
)

# -----------------------------------
# Statistics
# -----------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🤖 AI Classification", "Enabled")

with col2:
    st.metric("♻️ Categories", "4")

with col3:
    st.metric("🎯 SDG", "12")

st.write("---")

# -----------------------------------
# Text Classification
# -----------------------------------

waste_item = st.text_input(
    "Enter any waste item:",
    placeholder="Example: plastic bottle, old charger, banana peel"
)

if st.button("🔍 Classify Waste"):

    if waste_item.strip():

        try:

            with st.spinner(
                "Analyzing waste item..."
            ):

                category = classify_waste(
                    waste_item
                )

                disposal_method = get_disposal_method(
                    waste_item,
                    category
                )

                impact = get_environmental_impact(
                    waste_item
                )

            st.success(
                "✅ Item Classified Successfully"
            )

            st.subheader("📂 Category")
            st.success(category)

            st.subheader("🗑️ Disposal Method")
            st.write(disposal_method)

            st.subheader("🌍 Environmental Impact")
            st.info(impact)

            st.subheader(
                "🤖 AI Sustainability Insights"
            )

            ai_response = generate_ai_recommendation(
                waste_item,
                category,
                disposal_method
            )

            st.markdown(ai_response)

            st.subheader(
                "📊 Sustainability Score"
            )

            score_map = {
                "Recyclable": 8,
                "Biodegradable": 9,
                "E-Waste": 6,
                "Hazardous": 4
            }

            score = score_map.get(
                category,
                5
            )

            st.progress(score / 10)

            st.metric(
                "Score",
                f"{score}/10"
            )

            st.subheader(
                "🎯 SDG Alignment"
            )

            st.success(
                """
SDG 12: Responsible Consumption & Production

Proper waste segregation helps reduce landfill waste,
conserve resources, and encourage sustainable habits.
"""
            )

        except Exception as e:

            st.error(
                f"Error: {e}"
            )

# -----------------------------------
# Image Classification
# -----------------------------------

st.write("---")

st.subheader(
    "📸 Upload Waste Image"
)

uploaded_file = st.file_uploader(
    "Upload an image of waste",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    st.image(
        uploaded_file,
        caption="Uploaded Waste Image",
        width=350
    )

    if st.button(
        "🔍 Identify Waste From Image"
    ):

        try:

            with st.spinner(
                "Analyzing image..."
            ):

                detected_item = (
                    identify_waste_from_image(
                        uploaded_file
                    )
                )

            st.success(
                f"Detected Item: {detected_item}"
            )

            category = classify_waste(
                detected_item
            )

            st.success(
                f"Category: {category}"
            )

        except Exception as e:

            st.error(
                f"Image Recognition Error: {e}"
            )

# -----------------------------------
# Footer
# -----------------------------------

st.write("---")

st.caption(
    "♻️ EcoSort AI | AI-Powered Sustainability Assistant"
)

st.caption(
    "🎯 Supporting UN SDG 12: Responsible Consumption & Production"
)

