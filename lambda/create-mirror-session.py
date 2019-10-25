import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client=boto3.client('ec2', region_name='eu-west-1')



def create_mirror_session(tmf, tmt, eni_list):
    client = boto3.client('ec2', region_name='eu-west-1')
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


def list_instances(panos_image_id, VpcId):
    instance_list = []
    eni_list = []
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'instance-type',
                'Values': [
                    'a1*',
                    'c5*',
                    'c5d*',
                    'm5*',
                    'm5a*',
                    'm5d*',
                    'r5*',
                    'r5a*',
                    'r5d*',
                    't3*',
                    'z1d*',
                ]
            }
        ]
    )
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance['ImageId'] != panos_image_id and instance['VpcId'] == VpcId:
                for network in instance["NetworkInterfaces"]:
                    instance_list.append(instance["InstanceId"])
                    eni_list.append(network.get('NetworkInterfaceId'))
    return (instance_list, eni_list)


def lambda_handler(event, context):
    logger.info("Got event {} ".format(event))
    tmf = os.environ['tmf']
    tmt = os.environ['tmt']
    VpcId = 'vpc-0e4817a00f4e8be36'
    panos_image_id = os.environ['panos_image_id']
    instances, eni_list = list_instances(panos_image_id,VpcId)
    create_mirror_session(tmf, tmt, eni_list)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == '__main__':
    event = {}
    context = ''
    lambda_handler(event, context)