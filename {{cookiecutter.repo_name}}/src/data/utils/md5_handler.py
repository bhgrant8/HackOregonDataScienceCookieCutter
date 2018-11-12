import argparse
import datetime
import pprint
import hashlib
import os

# Added a md5 format to generate hash from file
def create_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

## Verifies the md5 checksum based on original value
def verify_file(downloaded_file_name):
    print("File to verify: {}".format(downloaded_file_name))
    md5_file_name = downloaded_file_name+".md5"
    print(md5_file_name)
    try:
        original_md5 = open(md5_file_name, "r").read()
        new_md5 = create_md5(downloaded_file_name)

        if original_md5 == new_md5:
            print("Original md5: {}".format(original_md5))
            print("New md5: {}".format(new_md5))
            return True
        else:
            print("Original md5: {}".format(original_md5))
            print("New md5: {}".format(new_md5))
            return False
    except FileNotFoundError:
        return "No md5 found for file {}".format(downloaded_file_name)
