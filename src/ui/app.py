import streamlit as st
import requests
from io import BytesIO

# Configuration
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Hyper-Personalized Tutor", page_icon="🎓", layout="wide")

st.title("🎓 Hyper-Personalized Tutor")
st.markdown("""
*An Advanced Multi-Modal Educational Platform powered by Vision-Language Models and Fine-Tuned SLMs.*
""")

# Sidebar for Architecture info
st.sidebar.header("System Architecture")
st.sidebar.info("**Ingestion:** GPT-4o / Llama-3-Vision")
st.sidebar.info("**Grading:** Fine-Tuned Phi-3 (QLoRA)")
st.sidebar.markdown("---")
st.sidebar.markdown("Status: **Prototype**")

# Main Tabs
tab1, tab2 = st.tabs(["📝 Ingestion (VLM)", "🧠 Study & Quiz (SLM)"])

# --- TAB 1: Ingestion ---
with tab1:
    st.header("Digitize Handwritten Notes")
    uploaded_file = st.file_uploader("Upload an image of your notes", type=["jpg", "png", "jpeg"])

    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(uploaded_file, caption="Original Handwriting", use_container_width=True)
        
        with col2:
            if st.button("Process with VLM Pipeline"):
                with st.spinner(" extracting semantics from chaos..."):
                    try:
                        # Prepare file for API
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{API_URL}/ingest", files=files)
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.success("Ingestion Complete!")
                            
                            with st.expander("Parsed Markdown", expanded=True):
                                st.markdown(data.get("raw_text", ""))
                            
                            st.subheader("Key Concepts Extracted")
                            st.write(data.get("key_concepts", []))
                        else:
                            st.error(f"Error {response.status_code}: {response.text}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Could not connect to Backend. Is 'main.py' running?")

# --- TAB 2: Grading ---
with tab2:
    st.header("Adaptive Quiz Mode")
    st.markdown("The system generates questions based on your specific notes and grades them using the **Fine-Tuned SLM**.")

    # Mock Data for demonstration until DB is connected
    st.info("Context: Linear Algebra - Eigenvalues (derived from upload)")
    
    question = "Explain the geometric interpretation of an eigenvalue in the context of a transformation matrix."
    st.markdown(f"**Question:** {question}")
    
    student_answer = st.text_area("Your Answer:", height=150)
    
    if st.button("Submit Answer"):
        if not student_answer:
            st.warning("Please write an answer first.")
        else:
            with st.spinner("Running inference on Fine-Tuned Model..."):
                try:
                    payload = {
                        "question": question,
                        "student_answer": student_answer,
                        "correct_answer": "Eigenvectors are vectors that do not change direction during transformation, only magnitude. The eigenvalue is the scaling factor."
                    }
                    response = requests.post(f"{API_URL}/grade", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.metric(label="AI Grade", value=f"{result['grade']}/10")
                        st.markdown("### Feedback")
                        st.write(result['feedback'])
                    else:
                        st.error("Grading Service Error")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Could not connect to Backend.")