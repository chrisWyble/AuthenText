import streamlit as st
from helper_functions import write_text

# Function to manage navigation
def navigate_to(section):
    st.session_state.section = section

# Set the title of the app
st.title("AuthenText")

# Initialize session state
if 'section' not in st.session_state:
    st.session_state.section = 'Home'

# Add a sidebar with a logo and navigation buttons
st.sidebar.image("logo.png", width=100)  # Adjust the path to your logo file
st.sidebar.title("Navigation")

# Navigation buttons
st.sidebar.button("Home", on_click=navigate_to, args=("Home",))
st.sidebar.button("About the Team", on_click=navigate_to, args=("About the Team",))
st.sidebar.button("Instructions", on_click=navigate_to, args=("Instructions",))
st.sidebar.button("Disclaimer", on_click=navigate_to, args=("Disclaimer",))
st.sidebar.button("Citations", on_click=navigate_to, args=("Citations",))

# Define content for each section
if st.session_state.section == "Home":
    st.write("Welcome to my AuthenText app!")
    st.write("This is a simple boilerplate to get you started.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.write("File uploaded!")
        # Process the uploaded file if needed
    
    # Student ID
    student_id = st.text_input("", placeholder="Student ID*").strip()
    if student_id:
        st.write(f"Student ID: {student_id}")
    
    # Student Last Name
    student_ln = st.text_input("",placeholder="Student's Last Name*").strip().title()
    if student_ln:
        st.write(f"Last Name: {student_ln}")

    # Student First Name
    student_fn = st.text_input("",placeholder="Student's First Name*").strip().title()
    if student_fn:
        st.write(f"First Name: {student_fn}")

    
    # Button for Student Name
    if st.button("Submit Student Credentials"):
        if student_ln and student_fn and student_id:
            st.write("Student credentials:")
            st.write(f"{student_id}: {student_ln}, {student_fn}")
    
    # Sample chart
    st.write("Here is a sample chart:")
    data = {
        'Category': ['A', 'B', 'C'],
        'Values': [10, 20, 30]
    }
    st.bar_chart(data)
    

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
