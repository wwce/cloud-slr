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
subnet_list = resource.split()

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

    create_table_sql = """ CREATE TABLE IF NOT EXISTS awsSUBNET (
                                        SUBNET_id text NOT NULL,
                                        SUBNET_desc text
                                    ); """

    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_entry(conn, subnet_id, subnet_desc):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO awsSUBNET(SUBNET_id, SUBNET_desc)
              VALUES(?,?) '''
    project = (subnet_id , subnet_desc) 
    #project = ('testing', 'testing2', 'testing3', 'testing4', 'testing5', 'testing6')
    #project = ('testing1', 'testing2', 'testing3', 'testing4', 'testing5', 'testing6')
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
    cur.execute("SELECT * FROM awsSUBNET")

    rows = cur.fetchall()


database = 'test.db'
if os.path.exists(database):
    os.remove(database)
conn = create_connection(database)
create_table(conn)



#print(subnet_list)
filters = [{'Name':'vpc-id', 'Values':subnet_list}]
output = client.describe_subnets(Filters=filters)
#print(output)

for subnet in output['Subnets']:
    subnet_id = subnet['SubnetId']
    print(subnet_id)
    subnet_desc = 'None'
    if 'Tags' in subnet.keys():
        for tag in subnet['Tags']:
            if tag['Key'] == 'Name':
                subnet_desc = tag['Value']
                print(subnet_desc)
    insert_entry(conn, subnet_id, subnet_desc)


select_all_tasks(conn)
conn.commit()
os.chmod('test.db', 0o777)

