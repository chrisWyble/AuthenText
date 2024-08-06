import helper_functions
import style

from imports import st

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
    st.session_state.mgt_status = ""


# Function to clear the student credentials
def clear_credentials():
    st.session_state.student_id = ""
    st.session_state.student_ln = ""
    st.session_state.student_fn = ""
    st.session_state.pdf_view = ""

# Add a sidebar with a logo and navigation buttons
st.sidebar.image("logo.png", width=100) 
st.sidebar.title("Navigation")

# Navigation buttons
st.sidebar.button("Home", on_click=navigate_to, args=("Home",))
st.sidebar.button("About the Team", on_click=navigate_to, args=("About the Team",))
st.sidebar.button("Instructions", on_click=navigate_to, args=("Instructions",))
st.sidebar.button("Disclaimer", on_click=navigate_to, args=("Disclaimer",))
st.sidebar.button("Archive", on_click=navigate_to, args=("Archive",))
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
    col1, col2, col3 = st.columns(spec=[0.68,0.21,0.11])
        
    scan_disabled = not (student_id and student_ln and student_fn and uploaded_files)  
    with col1:  
        if st.button("Scan for MGT", disabled=scan_disabled):
            st.session_state.mgt_status = helper_functions.run_binoculars(uploaded_files)
            
    with col2:
        archive_cond = st.session_state.mgt_status and not scan_disabled
        archive_disabled = not bool(archive_cond)
        if st.button("Archive Essay(s)", disabled=archive_disabled):
            mgt_status = [1 if 'Potential' in scan else 0 for scan in st.session_state.mgt_status]
            helper_functions.archive([student_id,student_ln,student_fn], uploaded_files, mgt_status)
            
    with col3:
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
    st.markdown("**Please refeer to the following disclaimers below.**")
    st.markdown("- This MGT detection tool was optimized for a false positive rate of 1%.")
    st.markdown("- This is an MGT detection tool. It is not meant to capture plagiarism.")
    st.markdown("- Educators should always cross-check positive results.")
    st.markdown("- Educators need to be cognizant of incorrect results, use social context, and must be the one to make the final decision.")
    st.markdown("- Students should be informed about the existence of this tool and that their data will only be used for MGT evaluation.")

elif st.session_state.section == "Citations":
    st.header("Citations")
    st.write(helper_functions.write_text('citations'))
    st.markdown("**References can be seen below.**")
    st.write("[1] Spotting LLMs With Binoculars [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
    st.write("[2] DAIGT Dataset [link](https://www.kaggle.com/datasets/xiranhu/daigt-proper-train-dataset)")
    st.write("[3] MGT Student Usage [link](https://www.forbes.com/sites/chriswestfall/2023/01/28/educators-battle-plagiarism-as-89-of-students-admit-to-using-open-ais-chatgpt-for-homework/?sh=64ffc7ec750d)")
    st.write("[4] MGT Identified by Educators [link](https://medium.com/@ajaykrishna.m1237890/teachers-struggle-to-identify-ai-written-texts-6488ed83bc13)")
    st.write("[5] Available MGT detection tools are unreliable [link](https://edintegrity.biomedcentral.com/articles/10.1007/s40979-023-00146-z#Sec18)")

    # Add more citations and references

elif st.session_state.section == "Archive":
    st.header("Archive")
    st.write(helper_functions.write_text('archive'))
    helper_functions.view_archive()
    # Add more archive and references
