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

#output = client.describe_vpcs()
resource = sys.argv[1]
subnet_list = resource.split(',')

#print( json.dumps(client.describe_vpcs(), indent=4))

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
        return conn
    except Error as e:
        print(e)


def create_table(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """

    create_table_sql = """ CREATE TABLE IF NOT EXISTS awsINTERFACE (
                                        INTERFACE_id text NOT NULL,
                                        INTERFACE_desc text,
                                        INTERFACE_instanceid text
                                    ); """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_entry(conn, interface_id, interface_desc, instance_id):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO awsINTERFACE(INTERFACE_id, INTERFACE_desc, INTERFACE_instanceid)
              VALUES(?,?,?) '''
    project = (interface_id , interface_desc, instance_id) 
    cur = conn.cursor()
    cur.execute(sql, project)
    return cur.lastrowid


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM awsINTERFACE")

    rows = cur.fetchall()


database = 'test.db'
if os.path.exists(database):
    os.remove(database)
conn = create_connection(database)
create_table(conn)



#print(subnet_list)
filters = [{'Name':'vpc-id', 'Values':subnet_list}]
output = client.describe_network_interfaces(Filters=filters)
#print(output)

for interface in output['NetworkInterfaces']:
    interface_id = interface['NetworkInterfaceId']
    print(interface_id)
    interface_desc = 'None'
    instance_id = 'None'
    if 'TagSet' in interface.keys():
        for tag in interface['TagSet']:
            if tag['Key'] == 'Name':
                interface_desc = tag['Value']
                #print(interface_desc)
    if 'Attachment' in interface.keys():
        if 'InstanceId' in interface['Attachment'].keys():
            instance_id = interface['Attachment']['InstanceId']
    insert_entry(conn, interface_id, interface_desc, instance_id)


select_all_tasks(conn)
conn.commit()
os.chmod('test.db', 0o777)

