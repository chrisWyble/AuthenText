import streamlit as st
import requests
import boto3
import os
import pandas as pd

from io import StringIO
from PyPDF2 import PdfReader
from streamlit_pdf_viewer import pdf_viewer