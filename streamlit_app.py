import streamlit as st
import pandas as pd

from streamlit_pdf_viewer import pdf_viewer

from helper import utils


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
    st.session_state.mgt_status = ""
    st.session_state.file_uploader_key = 0
    st.session_state.uploaded_files = []
    st.session_state.binary_data = None

# Function to clear the student credentials and uploaded files
def clear_credentials():
    st.session_state.student_id = ""
    st.session_state.student_ln = ""
    st.session_state.student_fn = ""

# Add a sidebar with a logo and navigation buttons
st.sidebar.image("static/logo.png", width=100) 
st.sidebar.title("Navigation")

# Navigation buttons
st.sidebar.button("Home", on_click=navigate_to, args=("Home",))
st.sidebar.button("Instructions", on_click=navigate_to, args=("Instructions",))
st.sidebar.button("Archive", on_click=navigate_to, args=("Archive",))
st.sidebar.button("Disclaimer", on_click=navigate_to, args=("Disclaimer",))
st.sidebar.button("About the Team", on_click=navigate_to, args=("About the Team",))
st.sidebar.button("Citations", on_click=navigate_to, args=("Citations",))

# Define content for each section
if st.session_state.section == "Home":

    # File uploader
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, type=('pdf'), key=st.session_state["file_uploader_key"])

    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files
        binary_data = uploaded_files[0].getvalue()
        st.session_state.binary_data = binary_data
        st.write("PDF preview:")
        with st.container(border=True, height=300):
            pdf_viewer(
                input=binary_data,
                width=700,
            )

    # Student ID
    student_id = st.text_input("Student ID", value=st.session_state.student_id, placeholder="Student ID*").strip()
    st.session_state.student_id = student_id
    
    # Student First Name
    student_fn = st.text_input("First Name", value=st.session_state.student_fn, placeholder="Student's First Name*").strip().title()
    st.session_state.student_fn = student_fn

    # Student Last Name
    student_ln = st.text_input("Last Name", value=st.session_state.student_ln, placeholder="Student's Last Name*").strip().title()
    st.session_state.student_ln = student_ln
    
    # Layout for buttons
    col1, col2, col3 = st.columns(spec=[0.68,0.21,0.11])
        
    scan_successful, archive_successful = None, None
    scan_disabled = not (student_id and student_ln and student_fn and uploaded_files)  
    
    with col1:  
        if st.button("Scan for MGT", disabled=scan_disabled):
            st.session_state.mgt_status = utils.run_binoculars(uploaded_files)
            if st.session_state.mgt_status:
                scan_successful = True
            else:
                st.error('Unable to run model. Please try again later.', icon="🚨")
    with col2:
        archive_disabled = not scan_successful
        if st.button("Archive Essay(s)", disabled=archive_disabled):
            mgt_status = [1 if 'Potential' in scan else 0 for scan in st.session_state.mgt_status]
            utils.archive([student_id,student_ln,student_fn], uploaded_files, mgt_status)
            archive_successful = True
            
    with col3:
        if st.button("Clear"):
            clear_credentials()
            st.session_state["file_uploader_key"] += 1
            st.rerun()
    
    # Output for Student Creds
    if scan_successful:
        st.success("✅ Done!")
        
        st.markdown('## Results')
        
        filename_list = [upload.name for upload in uploaded_files]

        df = pd.DataFrame({'Filename': filename_list, 'MGT Detected': st.session_state.mgt_status})
        df = df.set_index('Filename')
        st.write(df)

    # Output for Archive Status
    if archive_successful:
        st.success("✅ Archived!")
        filename_list = [upload.name for upload in uploaded_files]
        st.markdown('The following files were archived:')
        for file in filename_list:
            st.markdown(f"- {file}")

elif st.session_state.section == "About the Team":
    st.text("")
    st.text("")
    st.markdown(f"""
            <h1 style='font-size: 32px; text-align: left;'>
            About the Team</h1>""", unsafe_allow_html=True)
        
    st.text("")        
    
    col1, col2=st.columns([11,20],vertical_alignment="center", gap='medium')
    with col1:
        st.image("static/Brendan Ho.png", width=195)
        st.markdown(f"""
            <h2 style='font-size: 24px; text-align: left;'>{'&nbsp;'*8}Brendan Ho</h2>""", unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.text("")
    with col2:
        st.markdown("""I thoroughly enjoyed the program because it allowed me to meet and work with many brilliant individuals, further fostering my passion for data science.
                    During the project, I played a key role in overseeing the development of machine learning models as well as assisting dataset generation and creating visualizations.
                    My goal is to leverage my skills in data science to make a meaningful impact in the food or music industry.
                    In my free time, I enjoy cooking, music, anime/manga, and video games.""", unsafe_allow_html=True)


    col1, col2=st.columns([11,20],vertical_alignment="center", gap='medium')
    
    with col1:
        st.image("static/Chris Wyble.png", width=195)
        st.markdown(f"""
                <h2 style='font-size: 24px; text-align: left;'>{'&nbsp;'*8}Chris Wyble""", unsafe_allow_html=True)
    st.text("")
    st.text("")
    st.text("")
    with col2:
        st.markdown("""MIDS had amazing coverage of topics for in-demand skills along side the opportunity to work with talented peers.
                    For our capstone project, I lead the data and cloud engineer tasks such as AWS architecture design, developer operations, streamlit development, and assisted in model evaluation.
                    Going forward, I desire to apply data science to a variety of practical industries, specifically medical, to help others. 
                    For fun I enjoy participating in pickleball, playing super smash brothers, and watching anime.""", unsafe_allow_html=True)

    col1, col2=st.columns([11,20],vertical_alignment="center", gap='medium')

    with col1:
        st.image("static/Terence Pak.png", width=195)   
        st.markdown(f"""
            <h2 style='font-size: 24px; text-align: left;'>{'&nbsp;'*8}Terence Pak</h2>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""This program was an amazing experience with great people, allowing me to build valuable connections and build up a stronger data science foundation.
                    As the project manager, I managed the project and defined our scope. 
                    Some of additional tasks I took on included evaluating the model and the datasets, building our presentations, and create visuals for our presentation.
                    Moving forward, I intend to build a data science career and pursue my passion in the videogame industry.
                    In my free time, I enjoy baking, watching anime and photography.""", unsafe_allow_html=True)

elif st.session_state.section == "Instructions":
    st.header("Instructions")
    st.markdown("**Please follow the instructions listed below.**")
    st.markdown("- Refer to the 'Choose a file' prompt and click 'Browse files.'")
    st.markdown("- Locate and select the PDF file(s) that you would like to evaluate and click 'Open'")
    st.markdown("- Fill out student information including Student ID, First Name, and Last Name")
    st.markdown("- Select the 'Scan Essay' button. The MGT determination will appear below")
    st.markdown("- If you desire, you may select the 'Archive' button to store and later view the checked essay(s)")

elif st.session_state.section == "Disclaimer":
    st.header("Disclaimer")
    # Add more disclaimer information
    st.markdown("**Please refer to the following disclaimers below.**")
    st.markdown("- This MGT detection tool was optimized for a false positive rate of 1%.")
    st.markdown("- This is an MGT detection tool. It is not meant to capture plagiarism.")
    st.markdown("- Educators should always cross-check positive results.")
    st.markdown("- Educators need to be cognizant of incorrect results, use social context, and must be the one to make the final decision.")
    st.markdown("- Students should be informed about the existence of this tool and that their data will only be used for MGT evaluation.")

elif st.session_state.section == "Citations":
    st.header("Citations")
    st.markdown("**References can be seen below.**")
    st.write("[1] Spotting LLMs With Binoculars [link](https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
    st.write("[2] DAIGT Dataset [link](https://www.kaggle.com/datasets/xiranhu/daigt-proper-train-dataset)")
    st.write("[3] MGT Student Usage [link](https://www.forbes.com/sites/chriswestfall/2023/01/28/educators-battle-plagiarism-as-89-of-students-admit-to-using-open-ais-chatgpt-for-homework/?sh=64ffc7ec750d)")
    st.write("[4] MGT Identified by Educators [link](https://medium.com/@ajaykrishna.m1237890/teachers-struggle-to-identify-ai-written-texts-6488ed83bc13)")
    st.write("[5] Available MGT detection tools are unreliable [link](https://edintegrity.biomedcentral.com/articles/10.1007/s40979-023-00146-z#Sec18)")

    # Add more citations and references

elif st.session_state.section == "Archive":
    st.header("Archive")
    archive_df = utils.view_archive()
    if archive_df is not None:
        st.dataframe(archive_df)
    else:
        st.error('Could not access archive. Please try again later.', icon="🚨")
    # Add more archive and references
