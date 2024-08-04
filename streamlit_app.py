import helper_functions 
from imports import st, requests

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
    st.session_state.section = 'Instructions'
    st.session_state.student_id = ""
    st.session_state.student_ln = ""
    st.session_state.student_fn = ""


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
            helper_functions.view_pdf(uploaded_files)
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
    col1, col2 = st.columns(spec=[0.89,0.11])
    with col1:
        scan_disabled = not (student_id and student_ln and student_fn and uploaded_files)
        
        if st.button("Scan Essay", disabled=scan_disabled):
            helper_functions.run_binoculars(uploaded_files)
    with col2:
        if st.button("Clear"):
            clear_credentials()
    
    # Output for Student Creds
    if student_ln and student_fn and student_id:
        st.write("Student credentials:")
        st.write(f"{student_id}: {student_ln}, {student_fn}")

elif st.session_state.section == "About the Team":
    st.header("About the Team")
    st.write(helper_functions.write_text('team'))
    col1, col2, col3=st.columns([1,1,1])
    with col1:
        st.image("Brendan Ho.png", width=195)
        st.markdown("""
            <h2 style='font-size: 24px; text-align: center;'>Brendan Ho</h2>""", unsafe_allow_html=True)
    with col2:
        st.image("Chris Wyble.png", width=195)
        st.markdown("""
            <h2 style='font-size: 24px; text-align: center;'>Chris Wyble</h2>""", unsafe_allow_html=True)
    with col3:
        st.image("Terence Pak.png", width=195)
        st.markdown("""
            <h2 style='font-size: 24px; text-align: center;'>Terence Pak</h2>""", unsafe_allow_html=True)

elif st.session_state.section == "Instructions":
    st.header("Instructions")
    st.write(helper_functions.write_text('instructions'))
    st.markdown("**Please follow the instructions listed below.**")
    st.markdown("- Refer to the 'Choose a file' prompt and click 'Browse files.'")
    st.markdown("- Locate and select the PDF file that you would like to evaluate and click 'Open'")
    st.markdown("- Fill out student information including Student ID, First Name, and Last Name")
    st.markdown("- Select the 'Scan Essay' button. The MGT determination will appear below")

elif st.session_state.section == "Disclaimer":
    st.header("Disclaimer")
    st.write(helper_functions.write_text('disclaimer'))
    # Add more disclaimer information

elif st.session_state.section == "Citations":
    st.header("Citations")
    st.write(helper_functions.write_text('citations'))

    # Add more citations and references
