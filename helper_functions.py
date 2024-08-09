from imports import st, PdfReader,\
    requests, boto3, pd, os, StringIO

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


def extract_contents(files):
    lst = []
    for f in files:
        file_content = ''
        for p in PdfReader(f).pages:
            file_content += p.extract_text()
        lst.append(file_content)
    return lst

def run_binoculars(files, verbose=True):
    # Get the LLM server IP dynamically
    llm_server_ip = get_ec2_public_ip()
    LLM_SERVER_URL = f'http://{llm_server_ip}:5000/predict'
    
    text_lst = extract_contents(files)
    
    try:
        response = requests.post(LLM_SERVER_URL, json={'text': text_lst}) 
        response_data = response.json()
        return response_data['response']
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def archive(creds, files, mgt_status):
    # Get the LLM server IP dynamically
    llm_server_ip = get_ec2_public_ip()
    LLM_SERVER_URL = f'http://{llm_server_ip}:5000/archive'
    
    filenames = [f'{creds[0]}/{creds[1]}_{creds[2]}__{f.name[:-4]}' for f in files]
    text_lst = extract_contents(files)
    
    try:
        response = requests.put(LLM_SERVER_URL, json={'text': text_lst,
                                                    'filenames': filenames,
                                                    'mgt_status':mgt_status}) 
        response_data = response.json()
        return response_data['response']
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def view_archive():
    
    llm_server_ip = get_ec2_public_ip()
    LLM_SERVER_URL = f'http://{llm_server_ip}:5000/view_archive'
    
    try:
        response = requests.get(LLM_SERVER_URL) 
        response_data = response.json()
        res = response_data['response']
        
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
    df = pd.DataFrame(res)
    df.set_index('Student ID', inplace=True)
    st.dataframe(df)
    
        


