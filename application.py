import time
import pandas as pd
import streamlit as st
from src.pipeline.predict_pipeline import predict_output
from src.utils import replace_num, get_metrics

# -----------------------
# Streamlit page config
# -----------------------
st.set_page_config(page_title="PaperPulse", layout="wide")

# -----------------------
# Helpers
# -----------------------
def p_title(title: str):
    st.markdown(
        f"<h3 style='text-align: left; color:white; font-size:28px;'>{title}</h3>",
        unsafe_allow_html=True,
    )

def stream_data(text: str, delay: float = 0.05):
    """Stream output word by word."""
    placeholder = st.empty()
    out = ""
    for word in text.split(" "):
        out += word + " "
        placeholder.markdown(f"<p style='color:white'>{out}</p>", unsafe_allow_html=True)
        time.sleep(delay)

# -----------------------
# Custom CSS
# -----------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #121212; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton, #stDecoration {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Header
# -----------------------
st.markdown("<h1 style='text-align: center; color:yellow;'>SkimLit</h1>", unsafe_allow_html=True)
st.markdown(
    """
    <p style='text-align: center; color:white;'>
    SkimLit is a tool to summarize biomedical research abstracts.  
    It is trained on 20,000 PubMed abstracts and classifies text into 5 categories:  
    <b>BACKGROUND, OBJECTIVE, METHOD, RESULT, CONCLUSION</b>.
    </p>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Notes
# -----------------------
st.info(
    "⚠️ A few things to keep in mind:\n"
    "1. Best results with PubMed abstracts.\n"
    "2. Numbers are replaced with '@' for accuracy.\n"
    "3. Model is not perfect, may misclassify.\n"
    "4. Not a substitute for medical advice."
)

# -----------------------
# Buttons
# -----------------------
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    st.link_button("Get abstracts from PubMed", "https://pubmed.ncbi.nlm.nih.gov/", use_container_width=True)
with col2:
    metrics = st.button("Get Model Metrics", use_container_width=True)
with col3:
    get_pred = st.button("Get Predictions", use_container_width=True)
with col4:
    st.link_button(
        "Back to Website",
        "https://portfolio-5aa32iczs-adityas-projects-d6de9cbc.vercel.app/projects/planetfall",
        use_container_width=True,
    )

# -----------------------
# Options
# -----------------------
p_title("Choose an option below")
source = st.radio(
    "How would you like to start?",
    ("I want to use demo text", "I want to input some text"),
)

# -----------------------
# Demo text
# -----------------------
s_example = (
    "To evaluate the performance (efficacy, safety and acceptability) of a new "
    "micro-adherent absorbent dressing (UrgoClean) compared with a hydrofiber "
    "dressing (Aquacel) in the local management of venous leg ulcers..."
)

# -----------------------
# Metrics
# -----------------------
if metrics:
    model_metrics, baseline_metrics, image = get_metrics()
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Model Metrics")
        st.dataframe(model_metrics, use_container_width=True)
    with col2:
        st.subheader("Baseline Metrics")
        st.dataframe(baseline_metrics, use_container_width=True)
    st.image(image, use_column_width=True)

# -----------------------
# Predictions
# -----------------------
if not metrics or get_pred:
    if source == "I want to input some text":
        input_su = st.text_area("Enter abstract", max_chars=10000, height=200)
        if st.button("Submit", use_container_width=True):
            with st.spinner("Processing..."):
                input_su = replace_num(input_su)
                abstract_lines, abstract_pred_classes = predict_output(input_su)
                st.success("Output")
                my_string = "\n\n".join(
                    f"{abstract_pred_classes[i]}: {line}" for i, line in enumerate(abstract_lines)
                )
                stream_data(my_string)

    if source == "I want to use demo text":
        input_su = st.text_area("Demo Abstract", value=s_example, max_chars=10000, height=200)
        if st.button("Submit Demo", use_container_width=True):
            with st.spinner("Processing..."):
                abstract_lines, abstract_pred_classes = predict_output(input_su)
                st.success("Output")
                my_string = "\n\n".join(
                    f"{abstract_pred_classes[i]}: {line}" for i, line in enumerate(abstract_lines)
                )
                stream_data(my_string)
