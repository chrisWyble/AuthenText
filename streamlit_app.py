from imports import st, pickle
from helper_functions import write_text, run_binoculars, view_pdf

# Function to manage navigation
def navigate_to(section):
    st.session_state.section = section

# Set the title of the app
st.markdown("""
    <h1 style='font-size: 56px; text-align: center; opacity: 0.7;'>
        <span style='color: #2030DF;'>Authen</span><span style='color: black;'>Text</span>
    </h1>
    """, unsafe_allow_html=True)

# Initialize session state
if 'section' not in st.session_state:
    st.session_state.section = 'Home'
    st.session_state.student_id = ""
    st.session_state.student_ln = ""
    st.session_state.student_fn = ""

# # Load in Binoculars Model
# with open('model.pkl', 'rb') as file:
#     model = pickle.load(file)

# Function to clear the student credentials
def clear_credentials():
    st.session_state.student_id = ""
    st.session_state.student_ln = ""
    st.session_state.student_fn = ""

# Add a sidebar with a logo and navigation buttons
st.sidebar.image("logo.png", width=100) 
st.sidebar.title("Navigation")

# Navigation buttons
st.sidebar.button("Home", on_click=navigate_to, args=("Home",))
st.sidebar.button("About the Team", on_click=navigate_to, args=("About the Team",))
st.sidebar.button("Instructions", on_click=navigate_to, args=("Instructions",))
st.sidebar.button("Disclaimer", on_click=navigate_to, args=("Disclaimer",))
st.sidebar.button("Citations", on_click=navigate_to, args=("Citations",))

# Define content for each section
if st.session_state.section == "Home":
    st.write("Welcome to AuthenText app!")
    
    # File uploader
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
    if uploaded_files:
        if uploaded_files[0].name.endswith('pdf'): 
            view_pdf(uploaded_files)
        else:
            # Previews the first file uploaded
            file_content = uploaded_files[0].read().decode("utf-8")
            st.text_area("File Content", file_content, height=250)
    
    # Student ID
    student_id = st.text_input("", value=st.session_state.student_id, placeholder="Student ID*").strip()
    st.session_state.student_id = student_id
    
    # Student Last Name
    student_ln = st.text_input("", value=st.session_state.student_ln, placeholder="Student's Last Name*").strip().title()
    st.session_state.student_ln = student_ln
    
    # Student First Name
    student_fn = st.text_input("", value=st.session_state.student_fn, placeholder="Student's First Name*").strip().title()
    st.session_state.student_fn = student_fn
    
    # Layout for buttons
    col1, col2 = st.columns(spec=[0.85,0.15])
    with col1:
        if st.button("Clear"):
            clear_credentials()
    with col2:
        scan_disabled = not (student_id and student_ln and student_fn and uploaded_files)
        
        st.button("Scan Essay", disabled=scan_disabled, on_click=run_binoculars())

    
    # Output for Student Creds
    if student_ln and student_fn and student_id:
        st.write("Student credentials:")
        st.write(f"{student_id}: {student_ln}, {student_fn}")

elif st.session_state.section == "About the Team":
    st.header("About the Team")
    st.write(write_text('team'))
    # Add more content about the team

elif st.session_state.section == "Instructions":
    st.header("Instructions")
    st.write(write_text('instructions'))
    # Add more detailed instructions

elif st.session_state.section == "Disclaimer":
    st.header("Disclaimer")
    st.write(write_text('disclaimer'))
    # Add more disclaimer information

elif st.session_state.section == "Citations":
    st.header("Citations")
    st.write(write_text('citations'))
    # Add more citations and references
