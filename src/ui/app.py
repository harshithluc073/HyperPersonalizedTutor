import streamlit as st
import requests

# --- CONFIGURATION ---
API_URL = "http://localhost:8000"
PAGE_TITLE = "Hyper-Personalized Tutor"

st.set_page_config(
    page_title=PAGE_TITLE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED CSS STYLING ---
st.markdown("""
    <style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Global Reset */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1e293b;
    }

    /* Backgrounds */
    .stApp {
        background-color: #f8fafc;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a; /* Slate 900 */
        border-right: 1px solid #1e293b;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] p {
        color: #94a3b8 !important;
    }

    /* Custom Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
        letter-spacing: -0.025em;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748b;
        margin-bottom: 2rem;
    }

    /* Card Component */
    .custom-card {
        background: white;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
    }
    .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #334155;
        margin-bottom: 16px;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 8px;
    }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .status-active {
        background-color: #dcfce7;
        color: #166534;
    }
    .status-offline {
        background-color: #fee2e2;
        color: #991b1b;
    }
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: currentColor;
        border-radius: 50%;
        margin-right: 8px;
    }

    /* Button Overrides */
    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    div.stButton > button:active {
        background-color: #1e40af;
    }

    /* Input Fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        background-color: white;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
    }

    /* Tag Styling */
    .concept-tag {
        display: inline-block;
        background-color: #f1f5f9;
        color: #475569;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid #e2e8f0;
    }

    /* Hide standard Streamlit decorations */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        color: #64748b;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb;
        border-bottom: 2px solid #2563eb;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR DASHBOARD ---
with st.sidebar:
    st.markdown("<div style='margin-bottom: 20px; font-weight: 700; color: white; font-size: 1.2rem;'>SYSTEM CONTROL</div>", unsafe_allow_html=True)
    
    # Status Indicators
    st.markdown("""
    <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px;'>
        <div style='margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 0.85rem;'>Vision Engine</span>
            <span class='status-badge status-active'><span class='status-dot'></span>ONLINE</span>
        </div>
        <div style='margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 0.85rem;'>Grading Logic</span>
            <span class='status-badge status-active'><span class='status-dot'></span>READY</span>
        </div>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <span style='font-size: 0.85rem;'>API Latency</span>
            <span style='color: #94a3b8; font-size: 0.85rem; font-family: monospace;'>24ms</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.75rem; color: #475569;'>SESSION ID: 8F-2910-X2</div>", unsafe_allow_html=True)

# --- MAIN LAYOUT ---

# Header
st.markdown("<div class='main-header'>Hyper-Personalized Tutor</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Advanced Multi-Modal Curriculum Generation Platform</div>", unsafe_allow_html=True)

# Navigation
tab_ingest, tab_quiz = st.tabs(["DATA INGESTION", "ADAPTIVE ASSESSMENT"])

# --- TAB 1: INGESTION ---
with tab_ingest:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Use columns for a grid layout
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.markdown("""
        <div class="custom-card">
            <div class="card-title">Upload Source Material</div>
            <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 20px;">
                Upload raw images of handwritten notes, whiteboard diagrams, or scanned documents.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # File Uploader (Streamlit's native widget is hard to style completely, but we wrap it)
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

        if uploaded_file:
            st.image(uploaded_file, caption="Preview", use_container_width=True)
            if st.button("INITIATE DIGITIZATION"):
                with st.spinner("Processing semantics..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{API_URL}/ingest", files=files)
                        if response.status_code == 200:
                            st.session_state['ingestion_result'] = response.json()
                        else:
                            st.error(f"System Error: {response.text}")
                    except:
                        st.error("Connection Refused: Backend API is offline.")

    with col_right:
        if 'ingestion_result' in st.session_state:
            data = st.session_state['ingestion_result']
            
            # Result Card
            st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Digitized Output</div>
                <div style="font-family: 'Courier New', monospace; font-size: 0.9rem; color: #334155; white-space: pre-wrap; line-height: 1.6;">
{data.get('raw_text', 'No text extracted.')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Concepts Card
            concepts_html = "".join([f"<span class='concept-tag'>{c}</span>" for c in data.get("key_concepts", [])])
            st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Identified Concepts</div>
                <div>{concepts_html}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Empty State
            st.markdown("""
            <div class="custom-card" style="text-align: center; padding: 60px;">
                <div style="color: #cbd5e1; font-size: 4rem; margin-bottom: 20px;">⟲</div>
                <div style="color: #94a3b8; font-weight: 600;">Waiting for Input</div>
                <div style="color: #cbd5e1; font-size: 0.9rem;">Upload a file to begin the digitization pipeline.</div>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: QUIZ ---
with tab_quiz:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # We simulate a "Context" state
    topic = "Linear Algebra: Eigenvalues & Vectors"
    
    col_q, col_fb = st.columns([2, 1], gap="large")
    
    with col_q:
        question_text = "Explain the geometric interpretation of an eigenvalue in the context of a transformation matrix."
        
        st.markdown(f"""
        <div class="custom-card" style="border-left: 4px solid #2563eb;">
            <div style="font-size: 0.85rem; color: #64748b; text-transform: uppercase; margin-bottom: 8px;">Current Topic: {topic}</div>
            <div style="font-size: 1.2rem; font-weight: 600; color: #1e293b;">{question_text}</div>
        </div>
        """, unsafe_allow_html=True)
        
        student_answer = st.text_area("Your Answer", height=200, placeholder="Type your response here...")
        
        submit = st.button("SUBMIT FOR EVALUATION")
        
        if submit and student_answer:
            with st.spinner("Analyzing logic..."):
                try:
                    payload = {
                        "question": question_text,
                        "student_answer": student_answer,
                        "correct_answer": "Eigenvectors are vectors that do not change direction during transformation. The eigenvalue is the scaling factor."
                    }
                    response = requests.post(f"{API_URL}/grade", json=payload)
                    if response.status_code == 200:
                        st.session_state['grade_result'] = response.json()
                    else:
                        st.error("Grading Engine Failed")
                except:
                    st.error("Connection Refused")

    with col_fb:
        if 'grade_result' in st.session_state:
            res = st.session_state['grade_result']
            score = res['grade']
            
            # Color logic for score
            score_color = "#166534" if score >= 7 else "#ca8a04" if score >= 4 else "#991b1b"
            bg_color = "#dcfce7" if score >= 7 else "#fef9c3" if score >= 4 else "#fee2e2"
            
            st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">Assessment Report</div>
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 3rem; font-weight: 700; color: {score_color};">{score}/10</div>
                    <div style="font-size: 0.85rem; color: #64748b; text-transform: uppercase;">Confidence Score</div>
                </div>
                <div style="background-color: {bg_color}; padding: 15px; border-radius: 8px; color: {score_color}; font-size: 0.95rem; line-height: 1.5;">
                    {res['feedback']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
             st.markdown("""
            <div class="custom-card" style="height: 100%;">
                <div style="color: #94a3b8; text-align: center; margin-top: 40px;">
                    Assessment pending...
                </div>
            </div>
            """, unsafe_allow_html=True)