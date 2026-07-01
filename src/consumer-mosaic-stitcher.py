print("importing packages")

import os
import json

from crucible import CrucibleClient
from crucible.models import Dataset
import mfid
import glob

from utils import setup_pika_client, get_raw_data, get_secret
from dotenv import load_dotenv
import logging

# Set up logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Vars ===========================
load_dotenv()
rmq_host = os.environ.get("RMQ_HOST", "localhost")
rmq_port = int(os.environ.get("RMQ_PORT", 5672))
rmq_pw = get_secret("RABBITMQ_DEFAULT_PW", "rabbitmq_default_pw/versions/1")

crucible_api_url = os.environ.get("CRUCIBLE_API_URL", "https://crucible.lbl.gov/api/v2")
crucible_api_key = get_secret("ADMIN_APIKEY", "crucible_admin_apikey/versions/4")

num_cores = os.cpu_count()
print(f"{num_cores=}")

# RMQ Setup ===========================
connection, channel = setup_pika_client(rmq_host, rmq_port, rmq_pw)
queues_needed = ['rga-analysis', 'rga-analysis-failed']
for q in queues_needed:
    channel.queue_declare(queue=q)

# Crucible  ===========================
client = CrucibleClient(api_url=crucible_api_url, api_key=crucible_api_key)


def run_stitch():
    return


def callback(ch, method, properties, body):
    '''
    Expects a RMQ message with: 
    dsid:     The dataset ID that the processing request was made for
              and that the new data will be uploaded to

    '''
    run_stitch()                                                                                                                             
    

# subscribe to the queue
channel.basic_consume(queue='mosaic-stitcher',
                      auto_ack=False,
                      on_message_callback=callback)

# always be listening
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()