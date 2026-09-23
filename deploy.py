from sagemaker.core import image_uris
from sagemaker.core.training.configs import SourceCode
from sagemaker.serve import ModelBuilder

# Fetch the scikit-learn serving image for your region
image_uri = image_uris.retrieve(
    framework="sklearn",
    region="ap-south-1",      
    version="1.9-0",
    instance_type="ml.t2.medium",
    image_scope="inference",
)
print(image_uri)

inference_source_code = SourceCode(
    source_dir=".",         # local folder containing inference.py
    entry_script="inference.py",
)

model_builder = ModelBuilder(
    image_uri=image_uri,
    source_code=inference_source_code,
    s3_model_data_url="s3://vimal-jupy/model-artifacts/model.tar.gz",
    role_arn="arn:aws:iam::943755222667:role/sagemaker-sudo-access",
    instance_type="ml.t2.medium",
)

model_builder.build(model_name="my-sklearn-model")

predictor = model_builder.deploy(
    endpoint_name="vimal-sklearn-endpoint",
    initial_instance_count=1,
)
