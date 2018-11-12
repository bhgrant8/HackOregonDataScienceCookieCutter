# -*- coding: utf-8 -*-
import click
import logging

from pathlib import Path
import glob
from dotenv import find_dotenv, load_dotenv

import boto as aws

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from utils import gcs_client as gcs
from utils import md5_handler as md5

def verify_download(output_dir, prefix):
    logger = logging.getLogger("verify")
    logger.info('Verifying files in {} with prefix {}.'.format(output_dir, prefix))
    paths = Path(output_dir)
    verified_all = True
    pass_verified = []
    fail_verified = []
    no_md5 = []
    for path in paths.iterdir():
        path_in_str = str(path)
        if 'md5' not in path_in_str:
            verified = md5.verify_file(path_in_str)
            if isinstance(verified, bool):
                if verified == True:
                    pass_verified.append(path_in_str)
                    print("File {} passed md5 verification".format(path_in_str))
                else:
                    fail_verified.append(path_in_str)
                    error = "File {} did not pass md5 verification".format(path_in_str)
                    print(error)
                    verified_all = False
                    logger.error(error)
            else:
                error = "No md5 for file {}".format(path_in_str)
                no_md5.append(path_in_str)
                verified_all = False
                print(error)
                logger.error(error)
    if verified_all == True:
        print("All files passed verification")
        print('----------------------------\n')
        print("Files:")
        for file in passed_verified:
            print(file)
        print('\n')
    else:
        if len(fail_verified) > 0:
            print("The following files did not pass verification:")
            print('----------------------------\n')
            for file in fail_verified:
                print(file)
            print('\n')

        if len(no_md5) > 0:
            print("The following files did not have md5s:")
            print('----------------------------\n')
            for file in no_md5:
                print(file)
            print('\n')
        if len(pass_verified) > 0:
            print("The following files did pass verification:")
            print('----------------------------\n')
            for file in pass_verified:
                print(file)
            print('\n')

def gcs_download(bucket_name, output_dir, prefix):
    """ Downloads files from Google Cloud Storage bucket, allows one to specify a prefix
    """
    logger = logging.getLogger("get_raw -- {}".format("gcs_download"))
    logger.info('Getting Conntents of bucket {} with prefix {}.'.format(bucket_name, prefix))
    if prefix == "":
        blobs = gcs.list_blobs(bucket_name)
    else:
        blobs = gcs.list_blobs_with_prefix(bucket_name, prefix, delimiter=None)
    for blob in blobs:
        logger.info('Downloading {} from bucket {} ...'.format(blob, bucket_name))
        gcs.download_blob(bucket_name, blob, output_dir+"/"+blob)
        logger.info('Finished downloading {} from bucket {} ...'.format(blob, bucket_name))

@click.command()
@click.option('--provider', prompt='Cloud Storage Provider [aws, gcs]', default="gcs", help='Cloud Storage Provider: Options: [aws, gcs]')
@click.option('--bucket_name', prompt='Name of bucket',
              help='Your Cloud Storage Bucket Name')
@click.option('--output_dir', prompt='Output directory: ', default="./data/raw", type=click.Path())
@click.option('--prefix', prompt='Filename prefix', default="",
              help='Will only search in bucket for files with this prefix')
@click.option('--verify_only', default=False, help='Whether to run md5 validation only')
@click.option('--verify', default=True, help='Whether to run md5 validation on downloaded files (assumes md5 file present with pattern filename.original_extension.md5')
def main(provider, bucket_name, output_dir, prefix, verify_only, verify):
    """ Runs data download to pull raw data from cloud storage provider.
    """
    logger = logging.getLogger("get_raw -- {}".format(__name__))
    if verify_only == False:
        logger.info('Downloading raw data from provider: ' + provider)
        if provider == 'gcs':
            gcs_download(bucket_name, output_dir, prefix)
        elif provider == 'aws':
            logger.info('Getting Conntents of bucket {} ..'.format(bucket_name))
            print("Not yet built")
        else:
            print('Provider not valid')
            logger.error('Invalid Cloud Provider: ' + provider)
    verify_download(output_dir, prefix)



if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
