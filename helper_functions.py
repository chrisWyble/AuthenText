from imports import st, PdfReader

def write_text(page):
    if page == 'team':
        return 'Team Info'
    if page == 'instructions':
        return 'instructions'
    if page == 'disclaimer':
        return 'disclaimer'
    if page == 'citations':
        return 'citations'

def run_binoculars(verbose=True):
    pass

def view_pdf(files):
    # Read PDF
    pdf_reader = PdfReader(files[0])

    # Display PDF content (first page for example)
    first_page = pdf_reader.pages[0].extract_text()
    st.markdown(f"First page of {files[0].name}:")
    st.text_area("", first_page, height=250)
