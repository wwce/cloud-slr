import os
import sys
import boto3
import pprint
import sqlite3
import os
from sqlite3 import Error
import json

region = 'us-east-1'
#ec2 = boto3.resource('ec2', region_name='us-east-1')
client = boto3.client('ec2', region_name=region)
eni_list = sys.argv[1]
tmt = sys.argv[2]

#output = client.describe_vpcs()

#print( json.dumps(client.describe_vpcs(), indent=4))

pp = pprint.PrettyPrinter(indent=4)
output = client.create_traffic_mirror_filter(
                    Description='Palo Alto Network Mirror',
                    TagSpecifications=[
                        {
                            'ResourceType': 'traffic-mirror-filter',
                            'Tags': [
                                {
                                    'Key': 'Name',
                                    'Value': 'PaloAltoNetworkSLR'
                                },
                            ]
                        }
                    ]
        )
tmf = output['TrafficMirrorFilter']['TrafficMirrorFilterId']

rule = client.create_traffic_mirror_filter_rule(
            TrafficMirrorFilterId=tmf,
            TrafficDirection='ingress',
            RuleNumber=10,
            RuleAction='accept',
            Protocol=0,
            DestinationCidrBlock='0.0.0.0/0',
            SourceCidrBlock='0.0.0.0/0',
            Description='Palo Alto Network Ingress',
        )
rule = client.create_traffic_mirror_filter_rule(
            TrafficMirrorFilterId=tmf,
            TrafficDirection='egress',
            RuleNumber=100,
            RuleAction='accept',
            Protocol=0,
            DestinationCidrBlock='0.0.0.0/0',
            SourceCidrBlock='0.0.0.0/0',
            Description='Palo Alto Network Ingress',
        )

session = 1
for eni in eni_list:
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.create_traffic_mirror_session
    response = client.create_traffic_mirror_session(
        NetworkInterfaceId=eni,
        TrafficMirrorTargetId=tmt,
        TrafficMirrorFilterId=tmf,
        SessionNumber=session,
        Description='Created by aws-mirror.py',
    )
    session += 1
    if args.verbose:
        tms = response['TrafficMirrorSession']['TrafficMirrorSessionId']
        print("Created session " + tms + " for eni " + eni)




