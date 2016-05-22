import os
import argparse
import pandas as pd
import xml.etree.ElementTree as ET


def iter_posts(post):
    post_attr = post.attrib
    for row in post.iterfind('.//row'):
        row_dict = post_attr.copy()
        row_dict.update(row.attrib)
        # doc_dict['data'] = doc.text
        yield row_dict


# on AWS download the dataset to root or home folder and
# use absolute path /data/<folder_name>
POSITIVE_HIS = 'positive_history_data.csv'
NEGATIVE_HIS = 'negative_history_data.csv'
ALL_POSTS = 'all_posts_data.csv'


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
    print "-" * 5 + "POSITIVE" + "-" * 5
    print posi_hist_df[:5]
    print "-" * 5 + "NEGATIVE" + "-" * 5
    print neg_hist_df[:5]
    posi_hist_df.to_csv(os.path.join(new_path, POSITIVE_HIS), encoding='utf-8')
    neg_hist_df.to_csv(os.path.join(new_path, NEGATIVE_HIS), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="Relative/Absolute path to the folder")
    args = parser.parse_args()
    print args.folder
    parse(path=args.folder)