import xml.etree.ElementTree as ET
import pandas as pd
import boto3
from src.s3_client import S3Client

class CDWriter:

    def __init__(self):
        self.session = boto3.session.Session()
        self.s3_client = S3Client()

    def parse_and_save(self, xml, examid, exam_label, record_index):

        root = ET.fromstring(xml)

        data = []
        for li in root:
            asin = li.find('id').text
            contains_violence = li.find('cv').text

            data.append({
                'asin': asin,
                'contain_violence': contains_violence
            })

        df = pd.DataFrame(data)

        self.s3_client.dataframe_to_s3(df, examid, "linziye-content-descriptor-bedrock-prediction", exam_label +"/"+ str(record_index))