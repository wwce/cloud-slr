"""
/*****************************************************************************
 * Copyright (c) 2019, Palo Alto Networks. All rights reserved.              *
 *                                                                           *
 * This Software is the property of Palo Alto Networks. The Software and all *
 * accompanying documentation are copyrighted.                               *
 *****************************************************************************/

Copyright 2019 Palo Alto Networks

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


jharris@paloaltonetworks.com

"""

import logging
import ssl
import urllib
import urllib3
import boto3
import requests
import json




urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_client = boto3.client('lambda')
ec2_client = boto3.client('ec2')

def add_grp_profile_to_policy(hostname, api_key, rulebase_policy, group_profile):
    """
    Adds existing security group profile to existing security rulebase policy
    """""
    xpath = "/config/devices/entry[@name='localhost.localdomain']" \
             "/vsys/entry[@name='vsys1']/rulebase/security/rules/entry[@name='{0}']/profile-setting/group".format(rulebase_policy)
    element = "<member>{0}</member>".format(group_profile)

    return panSetConfig(hostname, api_key, xpath, element)

def panSetConfig(hostname, api_key, xpath, element):
    """Function to make API call to "set" a specific configuration
    """
    data = {
        'type': 'config',
        'action': 'set',
        'key': api_key,
        'xpath': xpath,
        'element': element
    }
    logger.info("Updating set config with xpath \n{} and element \n{} ".format(xpath, element))
    response = makeApiCall(hostname, data)
    # process response and return success or failure?
    return response

def makeApiCall(hostname, data):
    """
    Makes the API call to the firewall interface.  We turn off certificate checking before making the API call.
    Returns the API response from the firewall.
    :param hostname:
    :param data:
    :return: Expected response
    <response status="success">
        <result>
            <![CDATA[yes\n]]>
        </result>
    </response>
    """

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    # No certificate check
    ctx.verify_mode = ssl.CERT_NONE
    url = "https://" + hostname + "/api"
    payload = json.dumps(data)
    encoded_data = urllib.parse.urlencode(data).encode('utf-8')
    response = requests.post(url, data=data, verify=False,)
    if response.text.find('success'):
        return True
    else:
        return False



def lambda_handler(event, context):
    '''
    event ={
        fw_mgt_ip : 'x.x.x.x'
        api_key : 'xxxxxxxxxxxxxxxxx
        }
    :return event
        event ={
            fw_mgt_ip : 'x.x.x.x'
            api_key : 'xxxxxxxxxxxxxxxxx
            Action:'fw_ready'
            }
    '''
    logger.info("Got Event {}".format(event))
    fw_mgt_ip = event['fw_mgt_ip']
    api_key = event['api_key']
    rulebase_policy = 'log-all'
    group_profile = 'slr-log-all'
    if add_grp_profile_to_policy(fw_mgt_ip, api_key, rulebase_policy, group_profile):
        event.update({'Action': 'fw_policy_updated'})

    event.update({'Action':'fw_ready'})
    logger.info('Firewall is ready')

    return event





if __name__ == '__main__':
    event = {'fw_mgt_ip': '52.30.202.126'}
    context = ''
    lambda_handler(event, context)







