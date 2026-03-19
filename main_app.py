import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("A/B Testing Data App")

# ---- LOAD DATA ----
uploaded_file = st.file_uploader("Upload your dataset (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("weather.csv")  # default dataset

st.subheader("Dataset preview")
st.dataframe(df.head())

# ---- COLUMN SELECTION ----
st.subheader("Select variables")

columns = df.columns.tolist()

x_var = st.selectbox("Select X variable (categorical)", columns)
y_var = st.selectbox("Select Y variable (numeric)", columns)

# ---- CHARTS ----
st.header("Compare two charts")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Chart A: Distribution")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=df, x=x_var, ax=ax1)
    plt.xticks(rotation=20)
    st.pyplot(fig1)

with col2:
    st.subheader("Chart B: Average comparison")
    try:
        avg_data = df.groupby(x_var)[y_var].mean().reset_index()
        fig2, ax2 = plt.subplots()
        sns.barplot(data=avg_data, x=x_var, y=y_var, ax=ax2)
        plt.xticks(rotation=20)
        st.pyplot(fig2)
    except:
        st.write("Please select a valid numeric Y variable.")

# ---- VOTING ----
st.subheader("Vote")
vote = st.radio("Which chart is better?", ["Chart A", "Chart B"])

if "votes_a" not in st.session_state:
    st.session_state.votes_a = 0
if "votes_b" not in st.session_state:
    st.session_state.votes_b = 0

if st.button("Submit vote"):
    if vote == "Chart A":
        st.session_state.votes_a += 1
    else:
        st.session_state.votes_b += 1

# ---- RESULTS ----
st.subheader("Results")
results = pd.DataFrame({
    "Chart": ["Chart A", "Chart B"],
    "Votes": [st.session_state.votes_a, st.session_state.votes_b]
})

st.dataframe(results)
