from lxml import html
import xml.etree.ElementTree as ET
import ujson  # using ujson for speed
import HTMLParser


# consumes a lot of memory, have to optimize it
def create():
    old_path = 'data/android.stackexchange.com/'
    new_p_path = 'data/cleaned/positive/json/'
    new_n_path = 'data/cleaned/negative/json/'
    try:
        posts = ET.parse(old_path + 'Posts.xml').getroot()
        post_history = ET.parse(old_path + 'PostHistory.xml').getroot()
    except Exception, e:
        print e
        return
    for post_row in posts.findall('row'):
        is_reopned = False
        if post_row.get('PostTypeId') == '1':  # question
            if post_row.get('ClosedDate'):

                postid = post_row.get('Id')
                print "________________________________________________________________________"
                print postid
                postTypeId = post_row.get('PostTypeId')
                AcceptedAnswerId = post_row.get('AcceptedAnswerId')
                Body = post_row.get('Body')
                CreationDate = post_row.get('CreationDate')
                Score = post_row.get('Score')
                ViewCount = post_row.get('ViewCount')
                OwnerUserId = post_row.get('OwnerUserId')
                Title = post_row.get('Title')
                Tags = post_row.get('Tags')
                AnswerCount = post_row.get('AnswerCount')
                CommentCount = post_row.get('CommentCount')
                FavoriteCount = post_row.get('FavoriteCount')
                ClosedDate = post_row.get('ClosedDate')
                LastActivityDate = post_row.get('LastActivityDate')
                LastEditorUserId = post_row.get('LastEditorUserId')
                LastEditorDisplayName = post_row.get('LastEditorDisplayName')
                LastEditDate = post_row.get('LastEditDate')
                CommunityOwnedDate = post_row.get('CommunityOwnedDate')

                Body = HTMLParser.HTMLParser().unescape(Body)
                Body = html.fromstring(Body).text_content()
                Body = Body.replace('\n', '').replace('\r', '').replace('\t', ' ')
                Title = HTMLParser.HTMLParser().unescape(Title)
                Title = html.fromstring(Title).text_content()
                Title = Title.replace('\n', '').replace('\r', '').replace('\t', ' ')
                if Tags is not None:
                    try:
                        Tags = HTMLParser.HTMLParser().unescape(Tags)
                        Tags = html.fromstring(Tags).text_content()
                        Tags = Tags.replace('\n', '').replace('\r', '').replace('\t', ' ')
                    except Exception, e:
                        print e
                history = []
                for posth in post_history.findall('row'):
                    if posth.get('PostId') == str(postid):
                        Id = posth.get('Id')
                        PostHistoryTypeId = posth.get('PostHistoryTypeId')
                        PostId = posth.get('PostId')
                        RevisionGUID = posth.get('RevisionGUID')
                        CreationDate1 = posth.get('CreationDate')
                        UserId = posth.get('UserId')
                        UserDisplayName = posth.get('UserDisplayName')
                        Comment = posth.get('Comment')
                        Text = posth.get('Text')
                        CloseReasonId = posth.get('CloseReasonId')
                        if Text:
                            try:
                                Text = HTMLParser.HTMLParser().unescape(Text)
                                Text = html.fromstring(Text).text_content()
                                Text = Text.replace('\n', '').replace('\r', '').replace('\t', ' ')
                            except Exception, e:
                                print e
                        if Comment:
                            try:
                                Comment = html.fromstring(Comment).text_content()
                                Comment = HTMLParser.HTMLParser().unescape(Comment)
                                Comment = Comment.replace('\n', '').replace('\r', '').replace('\t', ' ')
                            except Exception, e:
                                print e
                        if str(PostHistoryTypeId) == '11':
                            is_reopned = True

                        his_data = {"Id": Id, "PostHistoryTypeId": PostHistoryTypeId, "PostId": PostId,
                                    "RevisionGUID": RevisionGUID, "CreationDate": CreationDate1, "UserId": UserId,
                                    "UserDisplayName": UserDisplayName, "Comment": Comment, "Text": Text,
                                    "CloseReasonId": CloseReasonId}
                        history.append(his_data)
                if is_reopned:
                    path = new_p_path
                else:
                    path = new_n_path

                data = {"Id": postid, "PostTypeId": postTypeId, "AcceptedAnswerId": AcceptedAnswerId, "Title": Title,
                        "Body": Body, "CreationDate": CreationDate, "Score": Score, "ViewCount": ViewCount,
                        "OwnerUserId": OwnerUserId, "Tags": Tags, "AnswerCount": AnswerCount,
                        "CommentCount": CommentCount, "FavoriteCount": FavoriteCount, "ClosedDate": ClosedDate,
                        "LastActivityDate": LastActivityDate, "LastEditorUserId": LastEditorUserId,
                        "LastEditorDisplayName": LastEditorDisplayName, "LastEditDate": LastEditDate,
                        "CommunityOwnedDate": CommunityOwnedDate, "history": history}
                datafile = open(path + postid + ".json", "w+")
                datafile.write(ujson.dumps(data, indent=4))
                datafile.close()


if __name__ == '__main__':
    create()
