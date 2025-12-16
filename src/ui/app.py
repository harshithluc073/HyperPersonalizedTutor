import streamlit as st
import requests
from io import BytesIO

# Configuration
API_URL = "http://localhost:8000"

# 1. Page Configuration
st.set_page_config(
    page_title="Hyper-Personalized Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for a "Best Looking" Modern UI
st.markdown("""
    <style>
    /* Main Background & Fonts */
    .main {
        background-color: #f8f9fa;
    }
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Custom Card Style for Results */
    .stCard {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar UI
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=80)
    st.title("Study Companion")
    st.markdown("---")
    st.markdown("**System Status**")
    st.caption("✅ Vision Engine: **Online**")
    st.caption("✅ Tutor Intelligence: **Active**")
    st.caption("✅ Database: **Connected**")
    st.markdown("---")
    st.info("Upload your messy handwritten notes, and let the AI build a curriculum for you.")

# 4. Main Title Area
st.title("🎓 Hyper-Personalized Tutor")
st.markdown("### Transform your handwritten notes into an interactive tutor.")
st.markdown("---")

# 5. Main Tabs
tab_upload, tab_quiz = st.tabs(["📂 Digitizer Studio", "🧠 Interactive Quiz"])

# --- TAB 1: UPLOAD & PROCESS ---
with tab_upload:
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader("1. Upload Notes")
        uploaded_file = st.file_uploader("Select an image file (JPG/PNG)", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Preview", use_container_width=True)
    
    with col2:
        st.subheader("2. Digital Extraction")
        if uploaded_file:
            if st.button("✨ Analyze & Digitize Content", type="primary"):
                with st.spinner("Vision Engine is analyzing handwriting and diagrams..."):
                    try:
                        # Prepare file for API
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{API_URL}/ingest", files=files)
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Success Message
                            st.success("Analysis Complete!")
                            
                            # Display Results in a Clean Layout
                            st.markdown("#### 📝 Extracted Content")
                            with st.container():
                                st.markdown(f"<div class='stCard'>{data.get('raw_text', '')}</div>", unsafe_allow_html=True)
                            
                            st.markdown("#### 🔑 Key Concepts Detected")
                            st.write(data.get("key_concepts", []))
                            
                        else:
                            st.error(f"Processing Error: {response.text}")
                            
                    except requests.exceptions.ConnectionError:
                        st.error("❌ Cannot connect to the Brain. Ensure the Backend is running.")
        else:
            st.info("Waiting for upload...")

# --- TAB 2: QUIZ MODE ---
with tab_quiz:
    st.subheader("🧠 Adaptive Knowledge Check")
    
    # Context Banner
    st.info("Topic: **Linear Algebra - Eigenvectors** (Derived from your notes)")
    
    # Question Card
    question_text = "Explain the geometric interpretation of an eigenvalue in the context of a transformation matrix."
    st.markdown(f"""
    <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; border-left: 5px solid #00a8cc;">
        <h3 style="margin:0;">Question:</h3>
        <p style="font-size: 1.1em;">{question_text}</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    # Answer Input
    student_answer = st.text_area("Write your answer here:", height=150, placeholder="Type your explanation...")
    
    col_submit, col_clear = st.columns([1, 4])
    with col_submit:
        submit_btn = st.button("Submit Answer", type="primary")

    if submit_btn:
        if not student_answer:
            st.warning("Please provide an answer to receive feedback.")
        else:
            with st.spinner("AI Tutor is grading your response..."):
                try:
                    payload = {
                        "question": question_text,
                        "student_answer": student_answer,
                        "correct_answer": "Eigenvectors are vectors that do not change direction during transformation, only magnitude. The eigenvalue is the scaling factor."
                    }
                    response = requests.post(f"{API_URL}/grade", json=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        grade = result['grade']
                        
                        # Dynamic Color based on grade
                        color = "green" if grade >= 7 else "orange" if grade >= 5 else "red"
                        
                        st.markdown("---")
                        st.subheader("Result")
                        
                        # Metric Row
                        c1, c2 = st.columns(2)
                        with c1:
                            st.metric(label="Score", value=f"{grade}/10")
                        
                        st.markdown(f"**Feedback:**")
                        st.markdown(f"""
                        <div style="border: 1px solid {color}; padding: 15px; border-radius: 5px; background-color: rgba(255,255,255,0.5);">
                            {result['feedback']}
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:
                        st.error("Grading Engine Error")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to the Brain.")