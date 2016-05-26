import argparse
import os

import pandas as pd

folder = ''
input_file = ''
output_file = ''
global_path = '/data/'


def create_data(path):
    path = os.path.join(path, 'cleaned')
    input_g_path = os.path.join(global_path, 'input')
    output_g_path = os.path.join(global_path, 'output')
    positive_hist_data = ''


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Relative/Absolute path to the folder")
    args = parser.parse_args()
    print args.folder
    create_data(path=args.folder)
