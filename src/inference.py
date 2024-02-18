import argparse
import boto3
import json
from botocore.config import Config
from cd_writer import CDWriter
from s3_client import S3Client
from prompt_builder import PromptBuilder

def handler(event):
    input = event["input"]
    content_metadata = input["content_metadata"] # This is a dataframe
    examid = input["exam_id"]
    startIndex = input["start_index"]
    endIndex = input["end_index"]
    modelId = input["model_id"]
    segmentIndex=input["segment_index"]

    prompt = PromptBuilder.build_prompt_string(startIndex, endIndex, content_metadata)
    request = {
        "prompt": prompt,
        "max_tokens_to_sample": 4000,
        "temperature": 1,
    }
    response = bedrock_client.invoke_model(
        modelId=modelId,
        body=json.dumps(request),
    )

    response_body = json.loads(response["body"].read().decode("utf-8"))[
        "completion"
    ].strip()

    cdWriter.parse_and_save(response_body, examid+"_"+modelId, "contain_violence", str(segmentIndex) + "_" + str(startIndex)+"_" + str(endIndex))
    return {
        "response": response_body
    }

def retryFunc(fun, fun_arg, retry_time):
    attempts = 0
    while attempts < retry_time:
        try:
            fun(fun_arg)
            break
        except Exception as e:
            attempts += 1
            print(f"failed at attempt {attempts}", e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='use bedrock language model to predict content descriptor')
    parser.add_argument("--model_id", type=str)
    parser.add_argument("--segment_start_index", type=int)
    parser.add_argument("--segment_end_index", type=int)
    args, _ = parser.parse_known_args()

    arguments = vars(args)

    model_id = arguments["model_id"]
    segment_start_index = arguments["segment_start_index"]
    segment_end_index = arguments["segment_end_index"]

    cdWriter = CDWriter()
    s3_client=S3Client()
    bedrock_client = boto3.client(
        "bedrock-runtime", config=Config(retries={"max_attempts": 6, "mode": "standard"})
    )

    event = {
        "input": {
            "exam_id": "raw_input",
            "model_id": model_id,
            "start_index": 0,
            "end_index": 0,
            "content_metadata": None,
            "segment_index": 0
        }
    }

    step = 30 # anthropic.claude-instant-v1
    # step = 40 # anthropic.claude-v2:1
    segment_index = segment_start_index
    while segment_index <  segment_end_index:
        start_index=0
        title_metadata_df = s3_client.s3_to_dataframe(bucket_name="content-descriptor-prediction-training",s3_key=f"iad_training_{segment_index}.parquet.gz")
        event["input"]["content_metadata"] = title_metadata_df
        event["input"]["segment_index"] = segment_index
        while start_index < len(title_metadata_df):
            end_index = min(start_index+step, len(title_metadata_df))
            event["input"]["start_index"] = start_index
            event["input"]["end_index"] = end_index
            retryFunc(handler, event, 3)
            start_index = end_index
        segment_index = segment_index + 1