#!/usr/bin/python3
import boto3
import pprint
import sys


region = 'us-west-1'
client = boto3.client('ec2', region_name=region)


resource = sys.argv[1]
print(resource)
intf_list = resource.split(",") 
intf_list = list(filter(None, intf_list))
#print(tmp)
response = client.create_tags(
    Resources= intf_list,
    Tags=[
        {
            'Key': 'PanSLRMirror',
            'Value': 'yes'
        },
    ]
)
