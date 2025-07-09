import streamlit as st
import pandas as pd
import plotly.express as px
import os
from openai import OpenAI
from dotenv import load_dotenv
import re
from ydata_profiling import ProfileReport
import streamlit.components.v1 as components

# --- Load Gemini API key ---
load_dotenv()
gemini_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
if not gemini_key:
    st.error("❌ GEMINI_API_KEY not found.")
    st.stop()

client = OpenAI(
    api_key=gemini_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# --- Page Config ---
st.set_page_config(page_title="🧠 AI Data Analyst", layout="wide")
st.title("📊 AI Data Analyst")
st.caption("👨‍💻 Made by Arpit Mohankar")

# --- Sidebar ---
with st.sidebar:
    st.header("📂 Upload Dataset")
    uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])
    df = None

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"❌ Error reading file: {e}")
            st.stop()

        st.markdown("---")
        st.subheader("📊 Dataset Summary")
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        if st.checkbox("Show dtypes & memory"):
            st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={"index": "Column", 0: "Dtype"}))

        st.markdown("---")
        st.subheader("🧠 What is this dataset about?")
        with st.spinner("Analyzing..."):
            try:
                summary_prompt = [
                    {"role": "system", "content": "You are a professional data analyst. Describe what this dataset is about based on its columns and sample values, in simple terms."},
                    {"role": "user", "content": f"Here are the first few rows of the dataset:\n\n{df.head(5).to_csv(index=False)}"}
                ]
                summary_response = client.chat.completions.create(
                    model="gemini-2.5-flash",  # ✅ Valid Gemini model name
                    messages=summary_prompt
                )
                dataset_summary = summary_response.choices[0].message.content.strip()
                st.write(dataset_summary)
            except Exception as e:
                st.error(f"⚠️ Gemini API Error: {e}")

        st.markdown("---")
        with st.expander("📋 Generate Full Data Profile"):
            if st.button("🔎 Generate Profiling Report"):
                with st.spinner("Generating report..."):
                    try:
                        profile = ProfileReport(df, explorative=True, minimal=True)
                        profile_html = profile.to_html()
                        components.html(profile_html, height=1000, scrolling=True)
                        st.download_button("📥 Download HTML Report", profile_html, file_name="report.html")
                    except Exception as e:
                        st.error(f"❌ Failed to generate report: {e}")

# --- Main App ---
if df is not None:
    tab1, tab2 = st.tabs(["📁 Explore Data", "🤖 Ask AI"])

    with tab1:
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head(100), use_container_width=True)

        st.subheader("📈 Visualize Data")
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        all_cols = df.columns.tolist()

        if len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox("X-axis", numeric_cols)
            with col2:
                y_axis = st.selectbox("Y-axis", numeric_cols)

            color_col = st.selectbox("Color By", [None] + all_cols)
            chart_type = st.radio("Chart Type", ["Scatter", "Bar", "Line"], horizontal=True)

            dark_colors = ['#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1']
            layout_config = dict(
                margin=dict(t=40),
                title_x=0.5,
                plot_bgcolor="#1e1e1e",
                paper_bgcolor="#1e1e1e",
                font=dict(color="white")
            )

            if chart_type == "Scatter":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col or None,
                                 template="plotly_dark", color_discrete_sequence=dark_colors)
            elif chart_type == "Bar":
                fig = px.bar(df, x=x_axis, y=y_axis, color=color_col or None,
                             template="plotly_dark", color_discrete_sequence=dark_colors)
            else:
                fig = px.line(df, x=x_axis, y=y_axis, color=color_col or None,
                              template="plotly_dark", color_discrete_sequence=dark_colors)

            fig.update_layout(**layout_config)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough numeric columns to plot.")

    with tab2:
        st.subheader("💬 Chat with Data Analyst")

        if "chat_context" not in st.session_state:
            st.session_state.chat_context = [
                {"role": "system", "content": (
                    "You're a professional data analyst AI. Explain uploaded data clearly, "
                    "suggest useful insights, and use charts when helpful. Answer in simple language."
                )},
                {"role": "system", "content": f"Preview of data:\n{df.head(100).to_csv(index=False)}"}
            ]

        for msg in st.session_state.chat_context[2:]:
            with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
                st.markdown(msg["content"])

        query = st.chat_input("Ask a question about the data...")
        if query:
            st.session_state.chat_context.append({"role": "user", "content": query})
            with st.chat_message("user", avatar="🧑"):
                st.markdown(query)

            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("Thinking..."):
                    try:
                        response = client.chat.completions.create(
                            model="gemini-2.5-flash",
                            messages=st.session_state.chat_context
                        )
                        answer = response.choices[0].message.content.strip()
                        st.session_state.chat_context.append({"role": "assistant", "content": answer})
                        st.markdown(answer)

                        code_blocks = re.findall(r"```python(.*?)```", answer, re.DOTALL)
                        for code in code_blocks:
                            with st.expander("📊 AI Chart Output"):
                                try:
                                    exec(code, {"df": df, "px": px, "st": st})
                                except Exception as e:
                                    st.error(f"⚠️ Chart error: {e}")
                    except Exception as e:
                        st.error(f"❌ Gemini API Error: {e}")

        if st.button("🧹 Clear Chat"):
            del st.session_state.chat_context
            st.rerun()
else:
    st.info("👈 Upload a dataset from the sidebar to begin.")
