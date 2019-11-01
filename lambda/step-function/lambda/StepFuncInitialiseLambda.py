"""
Paloaltonetworks TransitGatewayInitialiseLambda.py

Script triggered from a custom resource.  The script performs two funcitons

Starts the step function passing in the firewall mgt ip

This software is provided without support, warranty, or guarantee.
Use at your own risk.

jharris@paloaltonetworks.com
"""

import logging
import os
import time
import json
import boto3
import cfnresponse


ec2_client = boto3.client('ec2', )

logger = logging.getLogger()
logger.setLevel(logging.INFO)

defroutecidr = '0.0.0.0/0'




def start_state_function(state_machine_arn, fw_mgt_ip, api_key):
    input_data = {
        'fw_mgt_ip': fw_mgt_ip,
        'api_key' : api_key
    }
    sfnConnection = boto3.client('stepfunctions')
    success_count = len(
        sfnConnection.list_executions(stateMachineArn=state_machine_arn, statusFilter='SUCCEEDED')['executions'])
    running_count = len(
        sfnConnection.list_executions(stateMachineArn=state_machine_arn, statusFilter='RUNNING')['executions'])

    logger.info('State machine running count is {} and success count is {}'.format(running_count, success_count))
    step_function_arns = []
    time.sleep(30)
    result = sfnConnection.start_execution(stateMachineArn=state_machine_arn, input=json.dumps(input_data))
    logger.info('State maching ARN is {}'.format(result.get('executionArn')))
    step_function_arns.append(result.get('executionArn'))
    logger.info("Started StateMachine")
    time.sleep(30)
    success_count = len(
        sfnConnection.list_executions(stateMachineArn=state_machine_arn, statusFilter='SUCCEEDED')['executions'])
    running_count = len(
        sfnConnection.list_executions(stateMachineArn=state_machine_arn, statusFilter='RUNNING')['executions'])
    failed_count = len(
        sfnConnection.list_executions(stateMachineArn=state_machine_arn, statusFilter='FAILED')['executions'])

    logger.info('State machine running count is {}, failed count is {} and success count is {}'
                .format(running_count, failed_count, success_count))
    if running_count == 0 and failed_count > 0:
        logger.info('Problems starting the step function')


def lambda_handler(event, context):
    """
    Start the step function to configure the firewall
    """

    init_fw_state_machine_arn = os.environ['InitFWStateMachine']
    fw_mgt_ip = os.environ['fw_mgt_ip']
    api_key = os.environ['api_key']
    logger.info('Got event {}'.format(event))


    responseData = {}
    responseData['data'] = 'Success'
    if event['RequestType'] == 'Create':

        start_resp = start_state_function(init_fw_state_machine_arn, fw_mgt_ip, api_key)
        logger.info("Calling start state function {} ".format(start_resp))
        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalID")
        logger.info("Sending cfn success message ")

    elif event['RequestType'] == 'Update':
        print("Update something")
        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalID")

    elif event['RequestType'] == 'Delete':
        print("Got Delete event")
        pass

        cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "CustomResourcePhysicalID")
