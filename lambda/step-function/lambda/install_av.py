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
import urllib3
import os
import boto3
import time
import requests
from collections import OrderedDict
import xmltodict
import xml.etree.ElementTree as ET


logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_client = boto3.client('lambda')
ec2_client = boto3.client('ec2')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

subnets = []

def send_request(call):
    """
    Handles sending requests to API
    :param call: url
    :return: Retruns result of call. Will return response for codes between 200 and 400.
             If 200 response code is required check value in response
    """
    headers = {'Accept-Encoding': 'None', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        r = requests.get(call, headers=headers, verify=False, timeout=5)
        r.raise_for_status()
    except requests.exceptions.HTTPError as errh:
        '''
        Firewall may return 5xx error when rebooting.  Need to handle a 5xx response 
        '''
        logger.debug("DeployRequestException Http Error:")
        raise DeployRequestException("Http Error:")
    except requests.exceptions.ConnectionError as errc:
        logger.debug("DeployRequestException Connection Error:")
        raise DeployRequestException("Connection Error")
    except requests.exceptions.Timeout as errt:
        logger.debug("DeployRequestException Timeout Error:")
        raise DeployRequestException("Timeout Error")
    except requests.exceptions.RequestException as err:
        logger.debug("DeployRequestException RequestException Error:")
        raise DeployRequestException("Request Error")
    else:
        return r


class DeployRequestException(Exception):
    pass



def walkdict(dict, match):
    """
    Finds a key in a dict or nested dict and returns the value associated with it
    :param d: dict or nested dict
    :param key: key value
    :return: value associated with key
    """
    for key, v in dict.items():
        if key == match:
            jobid = v
            return jobid
        elif isinstance(v, OrderedDict):
            found = walkdict(v, match)
            if found is not None:
                return found



def check_pending_jobs(fwMgtIP, api_key):
    type = "op"
    cmd = "<show><jobs><all></all></jobs></show>"
    call = "https://%s/api/?type=%s&cmd=%s&key=%s" % (fwMgtIP, type, cmd, api_key)
    key = 'result'
    jobs = ''
    try:
        r = send_request(call)
        logger.info('Got response {} to request for content upgrade '.format(r.text))
        dict = xmltodict.parse(r.text)
        if isinstance(dict, OrderedDict):
            jobs = walkdict(dict, key)
        else:
            logger.info('Didnt get a dict')
        if not jobs:
            # No jobs pending
            return False
        else:
            # Jobs pending
            return True

    except:
        logger.info('Didnt get response to check pending jobs')
        return False


def install_av(fwMgtIP, api_key):
    """
    Applies latest AppID, Threat and AV updates to firewall after launch
    :param fwMgtIP: Firewall management IP
    :param api_key: API key

    """

    # Download latest anti-virus update without committing
    getjobid = 0
    jobid = ''
    type = "op"
    cmd = "<request><anti-virus><upgrade><download><latest></latest></download></upgrade></anti-virus></request>"
    key = 'job'
    while getjobid == 0:
        try:
            call = "https://%s/api/?type=%s&cmd=%s&key=%s" % (fwMgtIP, type, cmd, api_key)
            r = send_request(call)
            logger.info('Got response to request AV install {}'.format(r.text))
        except:
            DeployRequestException
            logger.info("Didn't get http 200 response.  Try again")
        else:
            try:
                dict = xmltodict.parse(r.text)
                if isinstance(dict, OrderedDict):
                    jobid = walkdict(dict, key)
            except Exception as err:
                logger.info("Got exception {} trying to parse jobid from Dict".format(err))
            if not jobid:
                logger.info('Got http 200 response but didnt get jobid')
                time.sleep(30)
            else:
                getjobid = 1

    completed = 0
    while (completed == 0):
        time.sleep(45)
        call = "https://%s/api/?type=op&cmd=<show><jobs><id>%s</id></jobs></show>&key=%s" % (
            fwMgtIP, jobid, api_key)
        r = send_request(call)
        tree = ET.fromstring(r.text)
        logger.debug('Got response for show job {}'.format(r.text))
        if tree.attrib['status'] == 'success':
            try:
                if (tree[0][0][5].text == 'FIN'):
                    logger.info("AV Download Status Complete ")
                    completed = 1
                else:
                    status = "Status - " + str(tree[0][0][5].text) + " " + str(tree[0][0][12].text) + "% complete"
                    print('{0}\r'.format(status))
            except:
                logger.info('Could not parse output from show jobs, with jobid {}'.format(jobid))
                completed = 1
        else:
            logger.info('Unable to determine job status')
            completed = 1

        # Install latest anti-virus
        getjobid = 0
        jobid = ''
        type = "op"
        cmd = "<request><anti-virus><upgrade><install><commit>yes</commit><version>latest</version></install></upgrade></anti-virus></request>"
        key = 'job'
        while getjobid == 0:
            try:
                call = "https://%s/api/?type=%s&cmd=%s&key=%s" % (fwMgtIP, type, cmd, api_key)
                r = send_request(call)
                logger.info('Got response to request AV install {}'.format(r.text))
            except:
                DeployRequestException
                logger.info("Didn't get http 200 response.  Try again")
            else:
                try:
                    dict = xmltodict.parse(r.text)
                    if isinstance(dict, OrderedDict):
                        jobid = walkdict(dict, key)
                except Exception as err:
                    logger.info("Got exception {} trying to parse jobid from Dict".format(err))
                if not jobid:
                    logger.info('Got http 200 response but didnt get jobid')
                    time.sleep(30)
                else:
                    getjobid = 1

        completed = 0
        while (completed == 0):
            time.sleep(45)
            call = "https://%s/api/?type=op&cmd=<show><jobs><id>%s</id></jobs></show>&key=%s" % (
                fwMgtIP, jobid, api_key)
            r = send_request(call)
            tree = ET.fromstring(r.text)
            logger.debug('Got response for show job {}'.format(r.text))
            if tree.attrib['status'] == 'success':
                try:
                    if (tree[0][0][5].text == 'FIN'):
                        logger.info("AV install Status Complete ")
                        completed = 1
                    else:
                        status = "Status - " + str(tree[0][0][5].text) + " " + str(tree[0][0][12].text) + "% complete"
                        print('{0}\r'.format(status))
                except:
                    logger.info('Could not parse output from show jobs, with jobid {}'.format(jobid))
                    completed = 1
            else:
                logger.info('Unable to determine job status')
                completed = 1


def lambda_handler(event, context):
    logger.info("Got Event {}".format(event))
    fw_mgt_ip = event['fw_mgt_ip']
    api_key = event['api_key']


    install_av(fw_mgt_ip, api_key)

    event.update({'AV-Update': 'Success'})
    logger.info('AV Update Installed')

    return event




if __name__ == '__main__':
    event = {}
    context = ''
    lambda_handler(event, context)







