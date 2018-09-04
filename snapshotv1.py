import boto3
import json

lambda_client = boto3.client('lambda')
event_client = boto3.client('events')

fn_name = "snap_lambda"

#with open('snap_lambda.zip','rb') as content_file:
 #   content = content_file.read()

snapshot_response =lambda_client.create_function(
    FunctionName = fn_name,
    Runtime = 'python3.6',
    Role ='arn:aws:iam::[account_id]:role/lambdafullaccess',
    Handler='{0}.snapshot_lambda_handler'.format(fn_name),
    Code={'ZipFile':open('{0}.zip'.format(fn_name),'rb').read(), },
    Timeout=30,
        )

fn_arn = snapshot_response['FunctionArn']

rule_response = event_client.put_rule(
    Name='{0}-Trigger'.format(fn_name),
    EventPattern=json.dumps({
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Instance State-change Notification"
  ],
  "detail": {
    "state": [
      "stopped"
    ]
  }
}),
    State="ENABLED",
)

lambda_client.add_permission(
    FunctionName=fn_name,
    StatementId="{0}-Event".format(fn_name),
    Action='lambda:InvokeFunction',
    Principal='events.amazonaws.com',
    SourceArn=rule_response['RuleArn'],
)

event_client.put_targets(
    Rule='{0}-Trigger'.format(fn_name),
    Targets=[
        {
            'Id': "1",
            'Arn': fn_arn,
        },
    ]
)
