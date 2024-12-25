import streamlit as st
import pandas as pd

import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.sentiment_analysis import analyze_sentiment, SentimentResult

def load_sample_data() -> pd.DataFrame:
    """
    Load sample data for demonstration.
    Returns:
        pd.DataFrame: A DataFrame containing sample messages.
    """
    try:
        sample_data_path = "../data/sample_messages.csv"
        return pd.read_csv(sample_data_path)
    except FileNotFoundError:
        st.warning("Sample data not found. Please ensure `sample_messages.csv` exists in the `data/` folder.")
        return pd.DataFrame(columns=["Message"])

def display_results(messages: list[str], results: list[SentimentResult]) -> None:
    """
    Display the sentiment analysis results in a table.
    Args:
        messages (list[str]): List of messages.
        results (list[SentimentResult]): List of sentiment results corresponding to messages.
    """
    results_data = {
        "Message": messages,
        "Sentiment": [result.sentiment for result in results],
        "Score": [result.score for result in results],
    }
    df_results = pd.DataFrame(results_data)
    st.dataframe(df_results)

def main() -> None:
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(page_title="Santa's Sentiment Analyzer", page_icon="🎅", layout="wide")
    st.title("🎅 Santa's Sentiment Analyzer")
    st.subheader("Classify whether Christmas wishes are Naughty or Nice!")

    st.sidebar.header("Upload or Use Sample Data")
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file with messages", type=["csv"])
    use_sample_data = st.sidebar.checkbox("Use Sample Data")

    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"Failed to read uploaded file. Error: {e}")
            return
    elif use_sample_data:
        data = load_sample_data()
        if data.empty:
            return
    else:
        st.info("Upload a file or select 'Use Sample Data' to proceed.")
        return

    if "Message" not in data.columns:
        st.error("The uploaded CSV must contain a 'Message' column.")
        return

    messages = data["Message"].dropna().tolist()
    if not messages:
        st.warning("No messages found in the data.")
        return

    st.write("### Input Messages")
    st.write(data.head())

    st.write("### Sentiment Analysis Results")
    try:
        results = [analyze_sentiment(message) for message in messages]
        display_results(messages, results)
    except Exception as e:
        st.error(f"An error occurred while analyzing sentiment. Error: {e}")

if __name__ == "__main__":
    main()
