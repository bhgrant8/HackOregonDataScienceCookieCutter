# -*- coding: utf-8 -*-
from utils import bq_client

import click
import logging

from dotenv import find_dotenv, load_dotenv
from pathlib import Path

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

@click.command()
@click.option('--dataset_id', prompt='Bigquery dataset id',
              help='Your Bigquery Dataset Id')
def main(dataset_id):
    """ Extract, transfer, and load for downloaded data.
    """
    logger = logging.getLogger("get_raw -- {}".format(__name__))
    client = bq_client.start_client()
    created = bq_client.create_dataset(client,dataset_id)
    if created:
        print("Dataset {} created".format(dataset_id))
    else:
        print("Dataset {} failed to create".format(dataset_id))

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
