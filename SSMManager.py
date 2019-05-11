import boto3

# AWS SSM
client = boto3.client('ssm')

class SSM():
    def __init__(self, ssm_path):
        self.ssm_path = ssm_path
    
    def check_ssm_value(self, value):
        ssm_response = client.get_parameter(
            Name=self.ssm_path,
            WithDecryption=False
        )
        return ssm_response['Parameter']['Value'].find(str(value))

    def update_ssm_value(self, value):
        ssm_response = client.put_parameter(
            Name=self.ssm_path,
            Description='',
            Value=str(value),
            Type='String',
            Overwrite=True
        )
