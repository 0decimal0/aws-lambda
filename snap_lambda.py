import boto3

def snapshot_lambda_handler(event,context):
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()

    for r in response['Reservations']:
        for i in r['Instances']:
            for b in i['BlockDeviceMappings']: 
                vol_id = b['Ebs']['VolumeId']


    snap_create_response = ec2_client.create_snapshot(
        Description = 'The snapshot taken when the instance stopped',
        VolumeId = vol_id
        )