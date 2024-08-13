import os
import requests
import boto3
import pandas as pd

from PyPDF2 import PdfReader
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError


load_dotenv('./.env')

INSTANCE_ID = os.getenv('instance_id')
REGION_NAME = os.getenv('region_name')


# Function to get the public IP of the second EC2 instance
def get_ec2_public_ip(instance_id, region_name):
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

def run_binoculars(files):
    # Get the LLM server IP dynamically
    try:
        llm_server_ip = get_ec2_public_ip(INSTANCE_ID, REGION_NAME)
        LLM_SERVER_URL = f'http://{llm_server_ip}:5000/predict'
        
        text_lst = extract_contents(files)
        

        response = requests.post(LLM_SERVER_URL, json={'text': text_lst}) 
        response_data = response.json()
        return response_data['response']
    except requests.exceptions.RequestException as e:
        return None
    except NoCredentialsError as e:
        return None
    except Exception as e:
        raise e


def archive(creds, files, mgt_status):
    # Get the LLM server IP dynamically
    llm_server_ip = get_ec2_public_ip(INSTANCE_ID, REGION_NAME)
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
        llm_server_ip = get_ec2_public_ip(INSTANCE_ID, REGION_NAME)
        LLM_SERVER_URL = f'http://{llm_server_ip}:5000/view_archive'
        
    
        response = requests.get(LLM_SERVER_URL) 
        response_data = response.json()
        res = response_data['response']
        
    except requests.exceptions.RequestException as e:
        return None
    except NoCredentialsError as e:
        return None
    else:

        df = pd.DataFrame(res)
        df.set_index('Student ID', inplace=True)
        
        return df
        
        


