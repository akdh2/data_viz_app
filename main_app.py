import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Weather Data A/B Testing App")
st.write("Business question: Which chart better helps compare weather patterns across locations?")

df = pd.read_csv("weather.csv")

st.subheader("Dataset preview")
st.dataframe(df.head())

st.subheader("Dataset summary")
st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])

col1, col2 = st.columns(2)

with col1:
    st.subheader("Chart A: Weather types by location")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df, x="location", hue="weather", ax=ax1)
    plt.xticks(rotation=20)
    st.pyplot(fig1)

with col2:
    st.subheader("Chart B: Average max temperature by location")
    avg_temp = df.groupby("location")["temp_max"].mean().reset_index()
    fig2, ax2 = plt.subplots()
    sns.barplot(data=avg_temp, x="location", y="temp_max", ax=ax2)
    plt.xticks(rotation=20)
    st.pyplot(fig2)

st.subheader("Vote for the better chart")
vote = st.radio("Choose one:", ["Chart A", "Chart B"])

if "votes_a" not in st.session_state:
    st.session_state.votes_a = 0
if "votes_b" not in st.session_state:
    st.session_state.votes_b = 0

if st.button("Submit vote"):
    if vote == "Chart A":
        st.session_state.votes_a += 1
    else:
        st.session_state.votes_b += 1

st.subheader("Current results")
results = pd.DataFrame({
    "Chart": ["Chart A", "Chart B"],
    "Votes": [st.session_state.votes_a, st.session_state.votes_b]
})
st.dataframe(results)
