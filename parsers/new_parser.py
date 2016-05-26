import HTMLParser
import argparse
import os
import xml.etree.ElementTree as ET

import pandas as pd
import re

from difflib import SequenceMatcher
from constants import ALL_POSTS, POSITIVE_HIS, NEGATIVE_HIS


def iter_posts(post):
    post_attr = post.attrib
    for row in post.iterfind('.//row'):
        row_dict = post_attr.copy()
        row_dict.update(row.attrib)
        # doc_dict['data'] = doc.text
        yield row_dict


def remove_tags(text):
    passtext = HTMLParser.HTMLParser().unescape(text)
    shortenedText = [e.lower() and e.translate(passtext.maketrans("", ""), passtext.punctuation) for e in text.split()
                     if len(e) >= 3 and not e.startswith('http')]
    print shortenedText


# on AWS download the dataset to root or home folder and
# use absolute path /data/<folder_name>

def parse(path):
    new_path = os.path.join(path, 'cleaned')
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    posts_file = 'Posts.xml'
    posts_his_file = 'PostHistory.xml'
    posts_path = os.path.join(path, posts_file)
    posts_his_path = os.path.join(path, posts_his_file)
    print posts_path, posts_his_path

    # posts_path = path + 'Posts.xml'
    # load the xml
    posts_tree = ET.parse(posts_path).getroot()
    # print type(posts_tree)
    # convert into dataframes
    post_df = pd.DataFrame(list(iter_posts(posts_tree)))
    # save the dataframe as CSV
    post_df.to_csv(os.path.join(new_path, ALL_POSTS), encoding='utf-8')
    """
    to store the dataframe as json. But not memory efficient
    JSon takes 90MB for a 86.22MB file. Whereas CSV takes only 65.37MB
    """
    # post_df.reset_index().to_json(orient='index')
    # remove NaN values in the dataframe. use inplace to replace values in the original dataframe
    post_df["ClosedDate"].fillna(0, inplace=True)

    # get all the questions from posts
    # q_df = post_df.loc[(post_df['PostTypeId'] == '1')]
    # only get questions which Has a closing date. ie, it is closed at least once.
    closed_q_df = post_df.loc[(post_df['ClosedDate'] != 0) & (post_df['PostTypeId'] == '1')]
    # print closed_q_df

    # load the posthistory xml
    posts_his_tree = ET.parse(posts_his_path).getroot()
    # print type(posts_tree)
    # convert into dataframes
    post_history_df = pd.DataFrame(list(iter_posts(posts_his_tree)))
    # print post_his_df

    i = 0
    j = 0
    neg_post_history_list = []
    pos_post_history_list = []
    for index, row in closed_q_df.iterrows():

        data = post_history_df.loc[(post_history_df["PostId"] == row["Id"])]
        ls = data["PostHistoryTypeId"].values.tolist()
        if '11' in ls:
            for x in data.index:
                i += 1
                lst = data.loc[x].values.tolist()
                pos_post_history_list.append(lst)
        else:
            for x in data.index:
                j += 1
                lst = data.loc[x].values.tolist()
                neg_post_history_list.append(lst)

    print post_history_df.columns
    posi_hist_df = pd.DataFrame(pos_post_history_list, index=[x for x in xrange(i)], columns=post_history_df.columns)
    neg_hist_df = pd.DataFrame(neg_post_history_list, index=[x for x in xrange(j)], columns=post_history_df.columns)
    # print "-" * 5 + "POSITIVE" + "-" * 5
    # print posi_hist_df[:5]
    # print "-" * 5 + "NEGATIVE" + "-" * 5
    # print neg_hist_df[:5]
    posi_hist_df.to_csv(os.path.join(new_path, POSITIVE_HIS), encoding='utf-8')
    neg_hist_df.to_csv(os.path.join(new_path, NEGATIVE_HIS), encoding='utf-8')


def remove_url(str):
    str = re.sub(r'https?:\S+', '', str, flags=re.MULTILINE)
    return str


def remove_brackets(str):
    str = re.sub(r'\([^)]*\)', ' ', str)
    return str


def remove_duplicate_tag(str):
    str = re.sub('> \*\*Possible Duplicate:\*\*.*?\-\->', '\n', str, flags=re.DOTALL)
    return str


def check_language(str):
    return str


def remove_noise(str):
    if check_language(str):
        str = remove_duplicate_tag(str)
        str = remove_brackets(str)
        str = remove_url(str)  # remove all URLs from the screen
        str = str.strip()  # remove \n from start and end of the screen
        str = str.replace('\n', ' ').replace('\r', '')
        str = re.sub(' *, *', ', ', str)  # replace "     ,     " with ", "
        str = re.sub(' *\. *', '. ', str)  # replace "     .     " with ". "
        str = re.sub('\( *\)', ' ', str)
        str = re.sub('\[ *\]', ' ', str)
        str = re.sub(' +', ' ', str)
        return str


def test_similarity(str1, str2):
    if str1 == str2:
        return True
    else:
        return False


# check if the 2 strings are at least 98% similar
def similar(a, b):
    val = SequenceMatcher(None, a, b).ratio()
    val = round(val, 2)
    if val <= 0.98:
        return False
    else:
        return True


# Creating dataset
folder = ''
input_file_name = 'all_posts.input'
output_file_name = 'all_posts.output'
global_path = 'data/in_out/'


def isEnglish(s):
    try:
        s.decode('ascii')
    except UnicodeDecodeError:
        return False
    except UnicodeEncodeError:
        return False
    else:
        return True


def create_data(path, global_path):
    new_path = os.path.join(path, 'cleaned')
    posi_hist_df = pd.read_csv(os.path.join(new_path, POSITIVE_HIS), encoding='utf-8')
    # neg_hist_df = pd.read_csv(os.path.join(new_path, NEGATIVE_HIS), encoding='utf-8')
    input_g_path = os.path.join(global_path, 'input')
    output_g_path = os.path.join(global_path, 'output')
    if not os.path.exists(input_g_path):
        os.makedirs(input_g_path)
    if not os.path.exists(output_g_path):
        os.makedirs(output_g_path)
    input_file = open(os.path.join(input_g_path, input_file_name), 'a+')
    output_file = open(os.path.join(output_g_path, output_file_name), 'a+')

    postids = posi_hist_df['PostId'].unique().tolist()
    for postid in postids:
        post_df = posi_hist_df.loc[posi_hist_df.PostId == postid]

        print "*" * 10 + "original title" + "*" * 10
        d = post_df.loc[post_df.PostHistoryTypeId == 1]['Text']
        l = len(d.index)
        d.index = range(l)
        original_title = remove_noise(d.ix[0])

        print original_title

        print "*" * 10 + "edited title" + "*" * 10
        d = post_df.loc[post_df.PostHistoryTypeId == 4]['Text']
        l = len(d.index)
        d.index = range(l)
        for x in xrange(l):
            edited_title = remove_noise(d.ix[x])
            if (isEnglish(edited_title) & isEnglish(original_title)):
                print similar(original_title, edited_title)
                if not similar(original_title, edited_title):
                    input_file.write((original_title + "\n"))  # .encode('utf8')
                    output_file.write((edited_title + "\n"))
                    print edited_title
        print "*" * 10 + "original body" + "*" * 10
        d = post_df.loc[post_df.PostHistoryTypeId == 2]['Text']
        l = len(d.index)
        d.index = range(l)
        original_body = remove_noise(d.ix[0])
        print original_body

        print "*" * 10 + "edited body" + "*" * 10
        d = post_df.loc[post_df.PostHistoryTypeId == 5]['Text']
        l = len(d.index)
        d.index = range(l)
        for x in xrange(l):
            edited_body = remove_noise(d.ix[x])
            if (isEnglish(original_body) & isEnglish(edited_body)):
                print similar(original_body, edited_body)
                if not similar(original_body, edited_body):
                    input_file.write((original_body + "\n"))
                    output_file.write((edited_body + "\n"))
                    print edited_body
        print "+0" * 20

    input_file.close()
    output_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Relative/Absolute path to the folder")
    parser.add_argument("global_folder", help="Relative/Absolute path to the global output folder")

    args = parser.parse_args()
    print args.folder
    print args.global_folder
    # parse(path=args.folder)
    create_data(path=args.folder, global_path=args.global_folder)
