import time
import pandas as pd
import streamlit as st
from src.pipeline.predict_pipeline import predict_output
from src.utils import replace_num, get_metrics

st.set_page_config(page_title="SkimLit", layout="wide")

def p_title(title):
    st.markdown(f'<h3 style="text-align: left;w-screen; color:white; font-size:28px;">{title}</h3>', unsafe_allow_html=True)

def stream_data(text):
    for word in text.split(' '):
        yield word + ' '
        time.sleep(0.1)

st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown("<h1 style='text-align: center; color:yellow;'>SkimLit</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:white;'>SkimLit is tool to summarize biomedical research abstracts. It is trained on a dataset comprising of research abstracts from 20,000 research papers published on PubMed. The main of the model is to classify all information into 5 functional classes: BACKGROUND, OBJECTIVE, METHOD, RESULT, CONCLUSION for better readability.</p>", unsafe_allow_html=True)
st.text('A few things to keep in mind:')
st.text('1. This model has been trained on 20k abstracts from PubMed. Kindly use PubMed research abstracts only for increased accuracy.')
st.text('2. The model will replace numeric values with @ sign. This was done to increase the model accuracy.')
st.text('3. The model is not perfect and may not always provide accurate results.')
st.text('4. The model is not a substitute for professional medical advice.')
st.text('You can choose the abstracts from PubMed to test the model. Click on the button below to get the abstracts.')
col1, col2, col3, col4 = st.columns([1,1,1,1])
with col1:
    st.link_button(label='Get abstracts to test from PubMed', url='https://pubmed.ncbi.nlm.nih.gov/', use_container_width=True)
with col2:
    metrics = st.button('Get Model Metrics', use_container_width=True)
with col3:
    get_pred = st.button('Get Predictions', use_container_width=True)
with col4:
    st.link_button(label='Back to Website', url='https://portfolio-5aa32iczs-adityas-projects-d6de9cbc.vercel.app/projects/planetfall', use_container_width=True)


st.text('')
p_title("Choose an option below")
st.text('')

source = st.radio("How would you like to start? Choose an option below",
                          ("I want to use demo text","I want to input some text"))
st.text('')
    
s_example = 'To evaluate the performance ( efficacy , safety and acceptability ) of a new micro-adherent absorbent dressing ( UrgoClean ) compared with a hydrofiber dressing ( Aquacel ) in the local management of venous leg ulcers , in the debridement stage .	A non-inferiority European randomised controlled clinical trial ( RCT ) was conducted in @ centres , on patients presenting with venous or predominantly venous , mixed aetiology leg ulcers at their sloughy stage ( with more than @ \%\ of the wound bed covered with slough at baseline ) .	Patients were followed over a @-week period and assessed weekly .	The primary judgement criteria was the relative regression of the wound surface area after the @-week treatment period .	Secondary endpoints were the relative reduction of sloughy tissue and the percentage of patients presenting with a debrided wound .	Altogether , @ patients were randomised to either UrgoClean ( test group ; n = @ ) or Aquacel ( control group ; n = @ ) dressings .	Regarding the wound healing process predictive factors ( wound area , duration , ABPI value , recurrence ) , at baseline , the two groups were well balanced , for both wound and patient characteristics .	Compression therapy was administered to both groups and after a median @-day treatment period , the percentage of relative reduction of the wound surface area was very similar ( -@ % vs -@ \%\ in the UrgoClean and control groups , respectively ) .	When considering the secondary criteria at week @ , the relative reduction of sloughy tissue was significantly higher in the UrgoClean group than in the control group ( -@ % vs -@,@ % ; p = @ ) .	The percentage of debrided wounds was also significantly higher in the test group ( @ % vs @ % ; p = @ ) .	This ` EARTH ` RCT confirmed that the UrgoClean dressing has similar efficacy and safety compared to Aquacel .	However , UrgoClean also showed better autolytic properties than the control group in the management of venous leg ulcers at the sloughy stage .	The new UrgoClean dressing therefore represents a promising therapeutic option within the current range of autolytic dressings available .	This study was sponsored by a grant from the pharmaceutical company Laboratoires Urgo .	S. Bohbot and O. Tacca are employees of Laboratoires Urgo .	S. Meaume , J. Dissemond and G. Perceau have received monetary compensation as presenters for Laboratoires Urgo .Data management and statistical analyses were conducted independently by Vertical ( Paris , France ) .'
# https://pubmed.ncbi.nlm.nih.gov/39181133/

if metrics:
    model_metrics, baseline_metrics, image = get_metrics()
    st.markdown('___')
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("<h3 style='text-align: center; color:white;'>Model Metrics</h3>", unsafe_allow_html=True)
        st.dataframe(model_metrics, use_container_width=True)
    with col2:
        st.markdown("<h3 style='text-align: center; color:white;'>Baseline Metrics</h3>", unsafe_allow_html=True)
        st.dataframe(baseline_metrics, use_container_width=True)
    st.image(image, use_column_width=True)

if not metrics or get_pred:
    if source == 'I want to input some text':
        input_su = st.text_area("Enter Data", max_chars=10000, height=200)
        if st.button('Submit', use_container_width=True):
            with st.spinner('Processing...'):
                input_su = replace_num(input_su)
                abstract_lines, abstract_pred_classes = predict_output(input_su)
                st.markdown('___')
                st.success('Output')
                my_string = ''
                nl = '  \n  \n' #2 spaces + Line feed
                for i , line in enumerate(abstract_lines):
                    my_string += f"{nl}{abstract_pred_classes[i]}:  {line}"
                st.write_stream(stream_data(my_string))

    if source == 'I want to use demo text':
        input_su = st.text_area("Enter Data", value=s_example, max_chars=10000, height=200)
        if st.button('Submit', use_container_width=True):
            with st.spinner('Processing...'):
                abstract_lines, abstract_pred_classes = predict_output(input_su)
                st.markdown('___')
                st.success('Output')
                my_string = ''
                nl = '  \n  \n' #2 spaces + Line feed
                for i , line in enumerate(abstract_lines):
                    my_string += f"{nl}{abstract_pred_classes[i]}:  {line}"
                st.write_stream(stream_data(my_string))


