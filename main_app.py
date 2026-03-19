import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Weather Chart A/B Test", layout="wide")

st.title("Weather Data A/B Testing App")
st.write("Business question: Which chart better helps compare weather patterns across locations?")

# Load dataset
FILE_PATH = "weather.csv"

if os.path.exists(FILE_PATH):
    df = pd.read_csv(FILE_PATH)
else:
    uploaded_file = st.file_uploader("Upload weather.csv", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.warning("Please place weather.csv in the same folder as main.py or upload it here.")
        st.stop()

# Basic cleaning
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna()

st.subheader("Dataset preview")
st.dataframe(df.head())

st.subheader("Dataset summary")
st.write(f"Rows: {df.shape[0]}")
st.write(f"Columns: {df.shape[1]}")
st.write("Locations in dataset:", ", ".join(df["location"].unique()))

# A/B testing section
st.header("A/B Test: Which chart is better?")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Chart A: Weather condition distribution by location")
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.countplot(data=df, x="location", hue="weather", ax=ax1)
    ax1.set_title("Weather Types by Location")
    ax1.set_xlabel("Location")
    ax1.set_ylabel("Count")
    plt.xticks(rotation=20)
    st.pyplot(fig1)

with col2:
    st.subheader("Chart B: Average max temperature by location")
    avg_temp = df.groupby("location", as_index=False)["temp_max"].mean()
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=avg_temp, x="location", y="temp_max", ax=ax2)
    ax2.set_title("Average Maximum Temperature by Location")
    ax2.set_xlabel("Location")
    ax2.set_ylabel("Average Max Temperature")
    plt.xticks(rotation=20)
    st.pyplot(fig2)

st.subheader("Vote")
vote = st.radio("Which chart better answers the business question?", ["Chart A", "Chart B"])

if "votes_a" not in st.session_state:
    st.session_state.votes_a = 0
if "votes_b" not in st.session_state:
    st.session_state.votes_b = 0
if "has_voted" not in st.session_state:
    st.session_state.has_voted = False

if st.button("Submit vote"):
    if not st.session_state.has_voted:
        if vote == "Chart A":
            st.session_state.votes_a += 1
        else:
            st.session_state.votes_b += 1
        st.session_state.has_voted = True
        st.success("Your vote has been recorded.")
    else:
        st.info("You already voted in this session.")

st.subheader("Current A/B Test Results")
results = pd.DataFrame({
    "Chart": ["Chart A", "Chart B"],
    "Votes": [st.session_state.votes_a, st.session_state.votes_b]
})
st.dataframe(results)

fig3, ax3 = plt.subplots(figsize=(6, 4))
sns.barplot(data=results, x="Chart", y="Votes", ax=ax3)
ax3.set_title("A/B Test Vote Results")
st.pyplot(fig3)

st.markdown("### Conclusion")
st.write(
    "This app compares two visualizations of the same dataset and collects votes to evaluate "
    "which chart users think better answers the business question."
)
