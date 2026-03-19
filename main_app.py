import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Weather Data A/B Testing App")
st.write("Business question: Which chart better helps compare weather patterns across locations?")
df1 = pd.read_csv("weather.csv")
uploaded_file = st.file_uploader("Upload a second dataset (same columns, different values)", type=["csv"])
if uploaded_file is not None:
    df2 = pd.read_csv(uploaded_file)
    dataset_choice = st.selectbox("Choose dataset to analyze", ["Dataset 1", "Dataset 2"])
    if dataset_choice == "Dataset 1":
        df = df1
    else:
        df = df2
else:
    df = df1
st.subheader("Dataset preview")
st.dataframe(df.head())
st.subheader("Dataset summary")
st.write("Rows:", df.shape[0])
st.write("Columns:", df.shape[1])
columns = df.columns.tolist()
numeric_columns = df.select_dtypes(include="number").columns.tolist()
st.subheader("Choose variables for each chart")
chartA_x = st.selectbox("Chart A: choose X variable", columns, index=columns.index("location") if "location" in columns else 0)
chartA_hue = st.selectbox("Chart A: choose category variable", columns, index=columns.index("weather") if "weather" in columns else 0)
chartB_x = st.selectbox("Chart B: choose X variable", columns, index=columns.index("location") if "location" in columns else 0)
chartB_y = st.selectbox("Chart B: choose numeric variable", numeric_columns, index=numeric_columns.index("temp_max") if "temp_max" in numeric_columns else 0)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Chart A")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df, x=chartA_x, hue=chartA_hue, ax=ax1)
    plt.xticks(rotation=20)
    st.pyplot(fig1)
with col2:
    st.subheader("Chart B")
    avg_data = df.groupby(chartB_x)[chartB_y].mean().reset_index()
    fig2, ax2 = plt.subplots()
    sns.countplot(data=avg_data, x=chartB_x, y=chartB_y, ax=ax2)
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
