import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import random
import pandas as pd

# Set page config for the app
st.set_page_config(
    page_title="KPLC Dashboard",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Load the saved tokenizer and model
model = load_model('categorization_model.h5')
with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Title and Subheader
st.title("⚡ KPLC Customer Support ")
st.markdown(" 🤖 Ask me anything about Kenya Power services")
st.subheader("Get instant responses to your queries")

st.markdown("""
    *Key Features:*
    - 🧠 Intelligent Query Categorization
    - 📋 Custom Responses
    - 💬 Real-Time Interaction

    """)

# Sidebar
with st.sidebar:
    st.header("Navigation")
    st.write("For more information, visit [KPLC's website](https://www.kplc.co.ke/)")

    # Sidebar for county selection
    county = st.sidebar.selectbox("Select Your County:", [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Nyeri", "Machakos", "Meru", "Embu"
    ])

    # Local contact information based on county selection
    local_contacts = {
        "Nairobi": "Contact Nairobi office: +254 123 456789",
        "Mombasa": "Contact Mombasa office: +254 987 654321",
        "Kisumu": "Contact Kisumu office: +254 567 890123",
        "Nakuru": "Contact Nakuru office: +254 345 678901",
        "Eldoret": "Contact Eldoret office: +254 234 567890",
        "Thika": "Contact Thika office: +254 678 901234",
        "Nyeri": "Contact Nyeri office: +254 456 789012",
        "Machakos": "Contact Machakos office: +254 789 012345",
        "Meru": "Contact Meru office: +254 890 123456",
        "Embu": "Contact Embu office: +254 012 345678",
    }

    st.write(local_contacts[county])

# Load sentiment analysis data (outside any conditional blocks)
df = pd.read_csv("combined.csv")

# Function for sentiment analysis (reusable)
def filter_by_sentiment(sentiment):
    filtered_df = df[df['Vader_sentiment_label'] == sentiment]
    st.write(filtered_df)
    return f"Number of {sentiment} tweets: {filtered_df.shape[0]}"

# Tabs (using `st.tabs`)
tabs = st.tabs(["Main Dashboard", "About Us", "Contact Us", "Sentiment Analysis"])

with tabs[0]:  # Main Dashboard Tab

    # Meter or account number input
    meter_account_number = st.text_input("Please enter your meter or account number:")

    # Check if meter/account number provided
    if meter_account_number:

        # User input and submit button
        user_input = st.text_input("Enter your query here:")

        if st.button("Submit"):
            if user_input:

                # Query processing and response (can be improved)
                def preprocess_text(text):
                    seq = tokenizer.texts_to_sequences([text])
                    padded = pad_sequences(seq, maxlen=50)
                    return padded

                def predict_category(text):
                    processed_text = preprocess_text(text)
                    prediction = model.predict(processed_text)
                    category = np.argmax(prediction, axis=1)[0]
                    return category

                category = predict_category(user_input)

                # Generate a random waiting number
                waiting_number = random.randint(100, 999)

                # Define the responses with placeholders for the waiting number
                responses = {
                    2: f"Hello, apologies. Our team is working to restore power in your area. Your issue is queued and your waiting number is {waiting_number}.",
                    3: f"Hello, apologies for the delay. You can also check the last 3 token transactions you have made using *977#. Your issue is queued and your waiting number is {waiting_number}.",
                    4: f"Hi. Apologies for the inconvenience. It is a faulty transformer issue affecting the area. We are working to resolve the issue. Your issue is queued and your waiting number is {waiting_number}.",
                    0: f"Send an email to customercare@kplc.co.ke indicating your account details, exact location, and phone number, and request your bill statement. Your issue is queued and your waiting number is {waiting_number}.",
                    1: f"If you have a complaint, we're here to listen. Please provide more details so we can assist you better. Your issue is queued and your waiting number is {waiting_number}."
                }
                response = responses.get(category, "Sorry, I couldn't understand your request. Please try again.")

                st.write(response)
            else:
                st.write("Please enter a query.")
    else:
        st.write("Please enter your meter or account number to proceed.")

with tabs[1]:  # About Us Tab
    st.header("About Us")
    st.write("""
    Kenya Power and Lighting Company (KPLC) is committed to providing reliable and high-quality electricity services to all Kenyans.
    We understand the importance of electricity in your daily life, and we are here to support you with any issues you may encounter.
    Our mission is to deliver safe, affordable, and sustainable electricity to every home and business across Kenya.
    """)

with tabs[2]:  # Contact Us Tab
    st.header("Contact Us")
    st.write("""
    If you need to get in touch with us, please reach out via the following channels:
    - **Email:** customercare@kplc.co.ke
    - **Phone:** +254 20 3201000
    - **Website:** [KPLC Website](https://www.kplc.co.ke)
    - **Social Media:** Follow us on [Twitter](https://twitter.com/KenyaPower_Care), [Facebook](https://www.facebook.com/KenyaPowerLtd/)
    """)

with tabs[3]:  # Sentiment Analysis Tab
    st.header("Sentiment Analysis")
    sentiment = st.selectbox("Select Sentiment Category", options=["positive", "negative", "neutral"])
    result = filter_by_sentiment(sentiment)
    st.write(result)

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #000000;
        color: #2196f3;
        text-align: center;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Footer
st.markdown("""
    <div class="footer">
        <p>© 2024 KPLC | Powered by Streamlit</p>
    </div>
    """, unsafe_allow_html=True)