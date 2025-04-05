from invoke import task
import subprocess
import os
import shutil
import boto3

FUNCTION_NAME = 'BitcoinProgress'
FUNCTION_ARN = 'arn:aws:lambda:us-east-1:901712715767:function:updateBitcoinProgressTwitterBot'  # Replace with your function ARN
ROLE_ARN = os.getenv('aws_lambda_role_arn')
HANDLER = 'src.lambda_function.run'
RUNTIME = 'python3.8'
ZIP_FILE = 'bitcoin_lambda.zip'

@task
def test(ctx):
    """Run tests using pytest"""
    subprocess.run(['python', '-m', 'unittest', 'discover', '-s', 'tests'], check=True)

@task
def build(ctx):
    """Build the deployment package"""
    # Create a directory for the deployment package
    if not os.path.exists('build'):
        os.makedirs('build')

    # Copy the source files to the build directory
    shutil.copytree('src', 'build/src', dirs_exist_ok=True)

    # Install dependencies in the build directory
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt', '-t', 'build'])

    # Zip the contents of the build directory
    shutil.make_archive('bitcoin_lambda', 'zip', 'build')
    print("Deployment package created successfully.")

@task
def deploy(ctx):
    """Deploy the package to AWS Lambda"""
    client = boto3.client('lambda', region_name="")

    with open(ZIP_FILE, 'rb') as f:
        zipped_code = f.read()

    try:
        response = client.update_function_code(
            FunctionName="",
            ZipFile=zipped_code,
            Publish=True
        )
        print(f"Function {FUNCTION_NAME} updated successfully.")
    except client.exceptions.ResourceNotFoundException:
        # Function does not exist, create it
        response = client.create_function(
            FunctionName=FUNCTION_NAME,
            Runtime=RUNTIME,
            Role=ROLE_ARN,
            Handler=HANDLER,
            Code=dict(ZipFile=zipped_code),
            Timeout=300,  # Maximum allowable timeout
            Environment={
                'Variables': {
                    'twitter_access_token': os.getenv('twitter_access_token'),
                    'twitter_access_token_secret': os.getenv('twitter_access_token_secret'),
                    'twitter_consumer_key': os.getenv('twitter_consumer_key'),
                    'twitter_consumer_secret': os.getenv('twitter_consumer_secret')
                }
            },
            Publish=True
        )
        print(f"Function {FUNCTION_NAME} created successfully.")