# Iris Classification on SageMaker

This is a little end-to-end project: train a scikit-learn model on the Iris dataset, upload it to S3, and spin up a real-time SageMaker endpoint that serves predictions.

The model is `DecisionTreeClassifier`. Feed it a flower's measurements (sepal length/width, petal length/width) and it tells you the species: 0 = setosa, 1 = versicolor, 2 = virginica.

## Contents

- `model_train.ipynb` — the notebook trains the model, saves `iris-model.pkl`, tars it up with the inference code, and uploads it all to S3
- `inference.py` — the SageMaker inference handlers (`model_fn`, `input_fn`, `predict_fn`, `output_fn`) that get packed into the tarball
- `deploy.py` — the script that actually deploys the endpoint using `ModelBuilder`
- `iris-model.pkl` / `model.tar.gz` — the trained model and the deployment package

## The flow

1. Train the model in the notebook and save it with joblib
2. Bundle `iris-model.pkl` + `inference.py` into `model.tar.gz` and upload to S3
3. Run `deploy.py` to stand up the endpoint

## Before you start

- Python 3.10+
- AWS creds set up (`aws configure`)
- A SageMaker execution role
- Install the dependencies:

```bash
pip install sagemaker boto3 joblib scikit-learn
```

## Modify the config

`deploy.py` contains few params that you want to change to your own setup:

- `region` — currently `ap-south-1`
- `s3_model_data_url` — where `model.tar.gz` is in S3
- `role_arn` — your SageMaker role
- `endpoint_name` — currently `vimal-sklearn-endpoint`
- `instance_type` — `ml.t2.medium`


## Deploy it

```bash
python deploy.py
```

That prints the image URI, registers the model, and creates the endpoint.

## Sample Endpoint call

```bash
aws sagemaker-runtime invoke-endpoint \
  --endpoint-name vimal-sklearn-endpoint \
  --content-type application/json \
  --body '{"instances": [[5.1, 3.5, 1.4, 0.2], [6.7, 3.0, 5.2, 2.3]]}' \
  output.json && cat output.json
```

Response:

```json
{"predictions": [0, 2]}
```

## Resource cleanup

```bash
aws sagemaker delete-endpoint --endpoint-name vimal-sklearn-endpoint
```

Delete the S3 bucket.

## SageMaker Studio Jupyter Notebook

Before running the notebook in SageMaker Studio, make sure your VPC can talk to S3 and SageMaker. Go to the VPC console → Endpoints → Create endpoint, and create these in the same VPC (and subnets/route tables) that Studio/Canvas uses:

- `com.amazonaws.<region>.s3` — Gateway endpoint 
- `com.amazonaws.<region>.sagemaker.api` — Interface endpoint
- `com.amazonaws.<region>.sagemaker.runtime` — Interface endpoint (needed for inference)

Also attach a NAT gateway to the VPC.