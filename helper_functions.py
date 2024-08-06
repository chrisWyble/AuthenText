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
    try:
        # Initialize a session using your AWS credentials
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('aws_access_key_id'),
            aws_secret_access_key=os.getenv('aws_secret_access_key')
        )

        s3_resource = boto3.resource(
                        's3',
                        aws_access_key_id=os.getenv('aws_access_key_id'),
                        aws_secret_access_key=os.getenv('aws_secret_access_key')
                    )
        
        bucket_name = 'authen-text-archive'
    
        # Listing out the objects in a bucket
        essay_trainning_bucket = s3_resource.Bucket(name = bucket_name)
        keys = [object.key for object in essay_trainning_bucket.objects.all()]

        series_lst = []

        for file_key in keys:
            # Download the file from S3 to a string buffer
            obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            data = obj['Body'].read().decode('utf-8')
            
            
            # Use StringIO to convert the string data to a pandas-readable buffer
            data_buffer = StringIO(data)
            
            # Read the data into a pandas DataFrame
            series = pd.read_json(data_buffer, typ='series')
            
            series['text'] = series['text'][:60] if len(series['text']) > 60 else series['text']
            series['mgt_status'] = 'Yes' if series['mgt_status'] else 'No'
            series['Document'] = file_key.split('.')[0].split('__')[1]
            series['Student ID'] = file_key.split('/')[0]

            series_lst.append(series)
        
        df = pd.DataFrame(series_lst)
        df = df[['Student ID', 'Document', 'text', 'mgt_status']]
        df.set_index('Student ID',inplace=True)
        df.rename(columns={'mgt_status':'Potential MGT Detected'}, inplace=True)
        st.dataframe(df)
    except Exception as e:
        print(e)
        


