import re
import codecs
import jieba


def remove_timestamp(raw):
    """Remove the timestamp in the raw lyrics
    Returns:
        Content after handling
    """
    re_timestap = re.compile(r'\[.*\]')
    content = []
    for line in raw:
        content.append(re_timestap.sub('', line.strip()))
    return content
def read_content(file):
    content = []
    for line in codecs.open(file, 'r', 'utf-8'):
        content.append(line.strip())
    return content

def remove_punct(raw):
    """Remove the punctuations in the raw content
    Returns:
        Content after handling
    """
    re_punct = re.compile(r'[。～，；‘’“”【】！~@#￥%……&*（）——+、《》？|:"]')
    content = [re_punct.sub('', line) for line in raw]
    return content

def cut(raw, remove_stop_word=True):
    """Cut the sentence into words
    Args:
        remove_stop_word: if or not to remove stop words
    Returns:
        2-d list of words
    """
    content = []
    if not remove_stop_word:
        stop_words = []
    else:
        stop_words = [u'的', u'了', u'和', u'呢', u'而' ,u'就', u'是' ,u'都', u'及' ,u'或' ,u'且' ,u'这' ,u'着' ,u'那', u'作词', u'作曲', u'赵雷', u'雷子' ,u'在' ,u'有', '']
    for sent in raw:
        cut_sent = [i for i in jieba.cut(sent, cut_all=False) if not i.strip() in stop_words]
        if len(cut_sent) > 0:
            content.append(cut_sent)
    return content

def prepro(file):
    content = read_content(file)

    pipeline = ['remove_timestamp', 'remove_punct', 'cut']
    for task in pipeline:
        content = eval(task)(content)

    return content
