import argparse
from s3_client import S3Client
from pandas import DataFrame
from prediction_result import PredictionResult

def summary(segment: int, prediction_dfs: [DataFrame], label_df: DataFrame, canonical_label = "contain_violence", raw_label = "vcc_cd_violence_contain"):
    result = PredictionResult([segment], canonical_label = canonical_label, raw_label = raw_label)

    for segment in range(len(prediction_dfs)):
        for i in range(len(prediction_dfs[segment])):
            asin = prediction_dfs[segment].asin[i]
            prediction_index = (prediction_dfs[segment].asin == asin).argmax()
            label_index= (label_df.asin ==asin).argmax()
            prediction = prediction_dfs[segment].contain_violence[prediction_index]
            label_boo = raw_label in label_df.cd_labels[label_index]
            updatePredictionResult(prediction, label_boo, result)
    return result

def updatePredictionResult(prediction: str, label: bool, result: PredictionResult):
    if prediction == 'True':
        if label == True:
            result.true_positive += 1
        else:
            result.false_positive += 1
    else:
        if label == True:
            result.false_negative += 1
        else:
            result.true_negative += 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='validate model prediction accuracy')
    parser.add_argument("--model_id", type=str)
    parser.add_argument("--segment_start_index", type=int)
    parser.add_argument("--segment_end_index", type=int)
    args, _ = parser.parse_known_args()

    arguments = vars(args)

    model_id = arguments["model_id"]
    segment_start_index = arguments["segment_start_index"]
    segment_end_index = arguments["segment_end_index"]

    s3_client=S3Client()
    bucket_name="linziye-content-descriptor-bedrock-prediction"
    canonical_label="contain_violence"
    raw_label = "vcc_cd_violence_contain"
    result = PredictionResult([], canonical_label = canonical_label, raw_label = raw_label)
    for segment in range(segment_start_index, segment_end_index):
        prefix=f"raw_input_{model_id}/{canonical_label}/{segment}_*"
        prediction_dfs = s3_client.get_s3_objects_as_df(bucket_name, prefix)
        label_df= s3_client.s3_to_dataframe(bucket_name="content-descriptor-prediction-training",s3_key=f"iad_training_{segment}.parquet.gz")
        result.accumulate(summary(segment, prediction_dfs, label_df))
    print(result)