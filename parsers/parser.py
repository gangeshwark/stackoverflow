import xml.etree.ElementTree as ET


def parse_posts():
    try:
        e = ET.parse('data/android.stackexchange.com/Posts.xml').getroot()
        print "Success"
        cf = open('data/Posts-closed.txt', 'w+')
        with open('data/Posts-full.txt', 'w+') as f:
            for atype in e.findall('row'):
                if atype.get('PostTypeId') == '1':  # question
                    string = "Post id: %s\nAcceptedAnswerId: %s\nCreationDate: %s\nTags: %s\nAnswerCount: %s\nTitle: %s\nBody:\n%s" % (
                        atype.get('Id'), atype.get('AcceptedAnswerId'), atype.get('CreationDate'), atype.get('Tags'),
                        atype.get('AnswerCount'), atype.get('Title'), atype.get('Body'))
                    if atype.get('ClosedDate'):
                        string += "Closed: Yes"
                        cf.write("\n-------------Question--------------\n" + string.encode('ascii', 'ignore'))
                    f.write("\n-------------Question--------------\n" + string.encode('ascii', 'ignore'))
                elif atype.get('PostTypeId') == '2':  # answer
                    string = "Post id: %s\nParentId: %s\nCreationDate: %s\nOwnerUserId:%s\nBody:\n%s" % (
                        atype.get('Id'), atype.get('ParentId'), atype.get('CreationDate'), atype.get('OwnerUserId'),
                        atype.get('Body'))
                    f.write("\n-------------Answer--------------\n" + string.encode('ascii', 'ignore'))
        f.close()
        cf.close()
    except Exception, ex:
        print ex


# parse post history
def parse_posthistory():
    try:
        e = ET.parse('data/android.stackexchange.com/PostHistory.xml').getroot()

        with open('data/PostsHistory-closed.txt', 'w+') as f:
            for atype in e.findall('row'):
                if atype.get('PostHistoryTypeId') in ['10', '11', '12',
                                                      '13']:  # A post voted to be closed, reopened, deleted, restored.

                    string = """Id=%s\nPostHistoryTypeId=%s\nPostId=%s\nCreationDate=%s\nUserId=%s\nText=%s\n""" % (
                        atype.get('Id'), atype.get('PostHistoryTypeId'), atype.get('PostId'), atype.get('CreationDate'),
                        atype.get('UserId'), atype.get('Text'))
                    if atype.get('Comment'):
                        string += "Comment: %s\n" % atype.get('Comment')
                    if atype.get('CloseReasonId'):
                        string += "CloseReasonId: %s\n" % atype.get('CloseReasonId')

                    f.write("\n---------------------------\n" + string.encode('ascii', 'ignore'))

        f.close()
        print "Done!"
    except Exception, ex:
        print "Error: " + str(ex)


if __name__ == '__main__':
    parse_posts()
    parse_posthistory()
