import streamlit as st
import pandas as pd
import numpy as np
import base64
import sys
import os

# Add the utils directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Import with error handling
try:
    from utils.content_adaptor import ContentAdaptor
    from utils.assessment import AssessmentEngine
    from utils.accessibility import AccessibilityManager
    CONTENT_ADAPTOR_AVAILABLE = True
except ImportError as e:
    st.error(f"Content adaptor import error: {e}")
    CONTENT_ADAPTOR_AVAILABLE = False

try:
    from utils.tts_engine import TTSEngine, BrowserTTS
    TTS_AVAILABLE = True
except ImportError as e:
    st.error(f"TTS engine import error: {e}")
    TTS_AVAILABLE = False
    # Create dummy classes if import fails
    class TTSEngine:
        def text_to_speech(self, *args, **kwargs): 
            st.warning("TTS not available. Install gtts and pygame.")
            return None
        def create_audio_player(self, *args, **kwargs): 
            return None
    class BrowserTTS:
        def create_speech_controls(self, *args, **kwargs): 
            return "<div>TTS not available</div>"

import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="NeuroLearn - AI Learning Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize engines with error handling
@st.cache_resource
def load_engines():
    engines = {}
    
    try:
        from utils.content_adaptor import ContentAdaptor
        engines['content_adaptor'] = ContentAdaptor()
    except Exception as e:
        st.error(f"Error loading ContentAdaptor: {e}")
        # Create a dummy adaptor
        class DummyAdaptor:
            def adapt_content(self, content, profile, font_size=16):
                return content
            def generate_visual_content(self, *args, **kwargs):
                return None
        engines['content_adaptor'] = DummyAdaptor()
    
    try:
        from utils.assessment import AssessmentEngine
        engines['assessment'] = AssessmentEngine()
    except Exception as e:
        st.error(f"Error loading AssessmentEngine: {e}")
        engines['assessment'] = None
    
    try:
        from utils.accessibility import AccessibilityManager
        engines['accessibility'] = AccessibilityManager()
    except Exception as e:
        st.error(f"Error loading AccessibilityManager: {e}")
        engines['accessibility'] = None
    
    try:
        from utils.tts_engine import TTSEngine, BrowserTTS
        engines['tts'] = TTSEngine()
        engines['browser_tts'] = BrowserTTS()
    except Exception as e:
        st.error(f"Error loading TTS engines: {e}")
        # Create dummy TTS engines
        class DummyTTSEngine:
            def text_to_speech(self, *args, **kwargs): return None
            def create_audio_player(self, *args, **kwargs): return None
        class DummyBrowserTTS:
            def create_speech_controls(self, *args, **kwargs): 
                return "<div>TTS not available</div>"
        engines['tts'] = DummyTTSEngine()
        engines['browser_tts'] = DummyBrowserTTS()
    
    return engines

engines = load_engines()

def main():
    load_css()
    
    # Show warning if modules aren't available
    if not CONTENT_ADAPTOR_AVAILABLE or not TTS_AVAILABLE:
        st.warning("⚠️ Some features are unavailable. Please check that all files are in the correct location.")
    
    # Sidebar for user profile and preferences
    with st.sidebar:
        st.title("🧠 NeuroLearn Profile")
        
        # User profile
        st.subheader("Student Profile")
        learning_profile = st.selectbox(
            "Learning Preference",
            ["ADHD", "Dyslexia", "Autism Spectrum", "General"]
        )
        
        # Accessibility preferences
        st.subheader("Accessibility Settings")
        font_size = st.slider("Font Size", 14, 24, 16)
        contrast_mode = st.checkbox("High Contrast Mode")
        text_to_speech = st.checkbox("Enable Text-to-Speech")
        tts_method = st.selectbox("TTS Method", ["Browser Built-in", "Google TTS"])
        
        # Learning pace
        learning_pace = st.select_slider(
            "Learning Pace",
            options=["Very Slow", "Slow", "Medium", "Fast", "Very Fast"]
        )
    
    # Main content area
    st.markdown('<div class="main-header">NeuroLearn - AI-Powered Learning Assistant</div>', unsafe_allow_html=True)
    
    # Navigation
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Learning Hub", "🎯 Adaptive Content", "📊 Progress Tracking", "⚙️ Settings"])
    
    with tab1:
        show_learning_hub(learning_profile, font_size, contrast_mode, text_to_speech, tts_method)
    
    with tab2:
        show_adaptive_content(learning_profile, text_to_speech, tts_method)
    
    with tab3:
        show_progress_tracking()
    
    with tab4:
        show_settings()

def show_learning_hub(profile, font_size, contrast_mode, text_to_speech, tts_method):
    st.header("Personalized Learning Hub")
    
    # Content selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Available Learning Materials")
        
        # Sample subjects
        subjects = ["Mathematics", "Science", "Language Arts", "History", "Life Skills"]
        selected_subject = st.selectbox("Choose Subject", subjects)
        
        # Learning materials based on subject
        materials = {
            "Mathematics": ["Basic Arithmetic", "Geometry", "Algebra", "Word Problems"],
            "Science": ["Biology Basics", "Physics Fundamentals", "Chemistry Introduction"],
            "Language Arts": ["Reading Comprehension", "Writing Skills", "Grammar"],
            "History": ["Ancient Civilizations", "World History", "Local History"],
            "Life Skills": ["Time Management", "Social Skills", "Organization"]
        }
        
        if selected_subject in materials:
            selected_topic = st.selectbox("Choose Topic", materials[selected_subject])
            
            # Display adapted content
            display_adapted_content(selected_subject, selected_topic, profile, font_size, text_to_speech, tts_method)

def display_adapted_content(subject, topic, profile, font_size, text_to_speech, tts_method):
    st.markdown(f'<div class="adaptive-card">', unsafe_allow_html=True)
    st.subheader(f"{topic} - Adapted for {profile}")
    
    # Get and display content
    original_content = get_sample_content(subject, topic)
    
    if CONTENT_ADAPTOR_AVAILABLE:
        adapted_content = engines['content_adaptor'].adapt_content(original_content, profile, font_size)
    else:
        adapted_content = original_content  # Fallback to original content
    
    # Create a unique ID for this content section for TTS
    content_id = f"content-{subject}-{topic}".replace(" ", "-").lower()
    
    # Display content with TTS controls if enabled
    if text_to_speech and TTS_AVAILABLE:
        # Add TTS controls above content
        tts_controls = engines['browser_tts'].create_speech_controls(original_content, content_id)
        st.markdown(tts_controls, unsafe_allow_html=True)
    elif text_to_speech:
        st.info("🔊 Text-to-speech features require additional setup.")
    
    # Display the content in a div with the specific ID
    st.markdown(f'<div id="{content_id}">{adapted_content}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Visual explanation section
    st.subheader("🎨 Visual Explanation")
    
    # Generate and display visual content
    if CONTENT_ADAPTOR_AVAILABLE:
        with st.spinner("Creating visual explanation..."):
            try:
                img_str = engines['content_adaptor'].generate_visual_content(subject, topic, original_content)
                
                if img_str:
                    # Display the generated image
                    st.image(f"data:image/png;base64,{img_str}", 
                            use_column_width=True, 
                            caption=f"Visual explanation for {topic}")
                    
                    # Download button for the visual
                    st.download_button(
                        label="📥 Download Visual Aid",
                        data=base64.b64decode(img_str),
                        file_name=f"visual_aid_{topic.replace(' ', '_').lower()}.png",
                        mime="image/png"
                    )
            except Exception as e:
                st.error(f"Error generating visual: {e}")
                st.info("Visual content generation requires matplotlib and numpy.")
    else:
        st.info("Visual content generation is currently unavailable.")
    
    # Interactive elements
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎧 Listen to Content (Alternative)"):
            if tts_method == "Google TTS" and TTS_AVAILABLE:
                with st.spinner("Generating audio..."):
                    audio_file = engines['tts'].text_to_speech(original_content)
                    if audio_file:
                        audio_html = engines['tts'].create_audio_player(audio_file)
                        if audio_html:
                            st.markdown(audio_html, unsafe_allow_html=True)
            else:
                st.info("Use the speech controls above the content for browser-based TTS")
    
    with col2:
        if st.button("🔄 Generate New Visual"):
            st.rerun()

def show_adaptive_content(profile, text_to_speech, tts_method):
    st.header("Adaptive Learning Path")
    
    # Assessment section with visual feedback
    st.subheader("Interactive Learning Activity")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("### Math Practice: Addition")
        question = "What is 15 + 27?"
        
        # Visual math problem
        if CONTENT_ADAPTOR_AVAILABLE:
            try:
                img_str = engines['content_adaptor']._create_addition_visual("15 + 27")
                st.image(f"data:image/png;base64,{img_str}", use_column_width=True)
            except:
                st.info("Visual aids currently unavailable")
        
        answer = st.text_input("Your answer:")
        
        if st.button("Check Answer"):
            if answer == "42":
                st.success("Correct! 🎉")
                st.balloons()
            else:
                st.error("Let's try again. Look at the visual above for help.")
    
    with col2:
        st.subheader("Learning Tools")
        
        # Quick TTS for the question
        if text_to_speech and TTS_AVAILABLE:
            if st.button("🔊 Read Question Aloud"):
                if tts_method == "Google TTS":
                    audio_file = engines['tts'].text_to_speech(question)
                    if audio_file:
                        audio_html = engines['tts'].create_audio_player(audio_file)
                        st.markdown(audio_html, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Alternative Methods")
        st.write("• Break it down: 10 + 20 = 30, 5 + 7 = 12, 30 + 12 = 42")
        st.write("• Use a number line")
        st.write("• Draw pictures")

def show_progress_tracking():
    st.header("Learning Progress")
    
    # Sample progress data
    progress_data = pd.DataFrame({
        'Week': [1, 2, 3, 4, 5],
        'Mathematics': [60, 65, 70, 75, 80],
        'Science': [55, 60, 65, 70, 75],
        'Language Arts': [50, 55, 65, 70, 75]
    })
    
    # Progress chart
    fig = px.line(progress_data, x='Week', y=['Mathematics', 'Science', 'Language Arts'],
                 title='Learning Progress Over Time')
    st.plotly_chart(fig)
    
    # Strengths and areas for improvement
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Strengths")
        st.success("• Excellent problem-solving skills")
        st.success("• Great visual learning ability")
        st.success("• Strong memory retention")
    
    with col2:
        st.subheader("📈 Areas for Growth")
        st.info("• Focus on reading comprehension")
        st.info("• Practice time management")
        st.info("• Develop study strategies")

def show_settings():
    st.header("Personalization Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Learning Preferences")
        
        learning_style = st.selectbox(
            "Preferred Learning Style",
            ["Visual", "Auditory", "Kinesthetic", "Reading/Writing"]
        )
        
        break_frequency = st.slider("Break Frequency (minutes)", 15, 60, 25)
        
        reward_system = st.selectbox(
            "Motivation System",
            ["Points", "Badges", "Progress Bars", "Verbal Praise"]
        )
    
    with col2:
        st.subheader("Accessibility Features")
        
        st.checkbox("Dyslexia-friendly font")
        st.checkbox("Color-blind mode")
        st.checkbox("Reduce animations")
        st.checkbox("Extended time for activities")
        
        # Text simplification level
        simplification = st.slider("Content Simplification", 1, 5, 3)
        st.caption("1: Most detailed, 5: Most simplified")

def load_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .adaptive-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .highlight-box {
        background-color: #e6f3ff;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
    }
    /* High contrast mode */
    .high-contrast {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    .high-contrast .adaptive-card {
        background-color: #333333 !important;
        color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

def get_sample_content(subject, topic):
    # Enhanced sample content database
    content_db = {
        "Mathematics": {
            "Basic Arithmetic": """
            # Understanding Addition
            
            Addition is combining two or more numbers to find their total.
            
            **Example**: 2 + 3 = 5
            
            Think of it like having 2 apples and getting 3 more apples. Now you have 5 apples!
            
            ## Key Points:
            - The numbers you add are called "addends"
            - The answer is called the "sum"
            - Addition is commutative: 2 + 3 = 3 + 2
            
            ## Real-world Examples:
            - If you have 5 marbles and your friend gives you 3 more, you have 8 marbles total
            - Adding 15 minutes to 30 minutes gives you 45 minutes
            - Combining 20 students from class A and 25 from class B gives 45 students total
            """,
            "Geometry": """
            # Introduction to Geometry
            
            Geometry is the study of shapes, sizes, and properties of space.
            
            ## Basic Shapes:
            
            ### Square
            - 4 equal sides
            - 4 right angles (90 degrees)
            - Examples: chess board, window pane
            
            ### Circle
            - No corners or edges
            - All points are equidistant from center
            - Examples: wheel, clock face
            
            ### Triangle
            - 3 sides and 3 angles
            - Angles always add up to 180 degrees
            - Examples: pyramid, sandwich cut in half
            """
        },
        "Science": {
            "Biology Basics": """
            # Introduction to Biology
            
            Biology is the study of living organisms and their interactions.
            
            ## The Cell: Basic Unit of Life
            
            All living things are made of cells. There are two main types:
            
            ### Plant Cells
            - Have a rigid cell wall
            - Contain chloroplasts for photosynthesis
            - Usually have one large central vacuole
            
            ### Animal Cells
            - No cell wall (only cell membrane)
            - No chloroplasts
            - Have multiple small vacuoles
            
            ## Key Functions:
            - **Growth**: Cells divide and multiply
            - **Energy**: Cells convert food to energy
            - **Reproduction**: Cells create new organisms
            """
        }
    }
    
    return content_db.get(subject, {}).get(topic, "Content coming soon...")

if __name__ == "__main__":
    main()