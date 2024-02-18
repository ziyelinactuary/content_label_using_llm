import boto3
import pandas as pd
import io
import awswrangler as wr
from urllib.parse import urlparse


class S3Client:

    def __init__(self):
        self.session = boto3.session.Session()
        self.s3_client = self.session.client(service_name='s3', region_name="us-east-1")

    def dataframe_to_s3(self, dataframe, bucket_name, s3_key):
        final_file_path = "/tmp/training.parquet.gz"
        dataframe.to_parquet(final_file_path,compression="gzip")
        self.s3_client.put_object(Bucket=bucket_name, Key=s3_key+".parquet.gz", Body=open(final_file_path, "rb"))

    def s3_to_dataframe(self, bucket_name, s3_key):
        s3_response_object = self.s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        gzipped_parquet = s3_response_object['Body'].read()
        df=pd.read_parquet(io.BytesIO(gzipped_parquet))
        return df

    def dataframe_to_s3(self, dataframe, examid, bucket_name, s3_key):
        final_file_path = "bedrocklabel.parquet.gz"
        dataframe.to_parquet(final_file_path,compression="gzip")
        self.s3_client.put_object(Bucket=bucket_name, Key=examid+"/"+s3_key+".parquet.gz", Body=open(final_file_path, "rb"))

    def list_objects(self, bucket_name, s3_key_pattern):
        return wr.s3.list_objects(f's3://{bucket_name}/{s3_key_pattern}', boto3_session=self.session)

    def get_s3_objects_as_df(self, bucket_name, s3_key_pattern):
        s3_items = self.list_objects(bucket_name, s3_key_pattern)
        s3_bucket = [self.parse_s3_url(url) for url in s3_items]
        dfs = [self.s3_to_dataframe(x["bucket_name"], x["key"]) for x in s3_bucket]
        return dfs

    def parse_s3_url(self, url):
        parsed_url=urlparse(url, allow_fragments=False)
        key = parsed_url.path.lstrip("/")
        if parsed_url.query:
            key = parsed_url.path.lstrip("/") + "?" + parsed_url.query
        return {"bucket_name": parsed_url.netloc, "key": key}
