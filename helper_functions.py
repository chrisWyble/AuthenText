from imports import st, PdfReader, requests, boto3

def write_text(page):
    if page == 'team':
        return 'Team Info'
    if page == 'instructions':
        return 'instructions'
    if page == 'disclaimer':
        return 'disclaimer'
    if page == 'citations':
        return 'citations'

def view_pdf(files):
    # Read PDF
    pdf_reader = PdfReader(files[0])

    # Display PDF content (first page for example)
    first_page = pdf_reader.pages[0].extract_text()
    st.markdown(f"First page of {files[0].name}:")
    st.text_area("", first_page, height=250)


# Function to get the public IP of the second EC2 instance
def get_ec2_public_ip(instance_id='i-0800501d08d7bdc6f', region_name='us-east-1'):
    ec2 = boto3.client('ec2', region_name=region_name)
    response = ec2.describe_instances(InstanceIds=[instance_id])
    status = response['Reservations'][0]['Instances'][0]['State']['Name']
    if status in ['running','stopping']:
        return response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    return response['Reservations'][0]['Instances'][0]#['PrivateIpAddress']



def run_binoculars(text, verbose=True):
    # Get the LLM server IP dynamically
    llm_server_ip = get_ec2_public_ip()
    LLM_SERVER_URL = f'http://{llm_server_ip}:5000/predict'
    text = 'from client to server and back again :D'
    try:
        response = requests.post(LLM_SERVER_URL, json={'text': text}) 
        response_data = response.json()
        st.markdown(str(response_data))
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}



