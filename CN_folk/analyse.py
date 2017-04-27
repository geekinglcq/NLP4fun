import jieba.analyse
from collections import Counter
from gensim import corpora
from pprint import pprint
from gensim.models.ldamodel import LdaModel
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.ndimage import imread
from PIL import Image

def key_words(content, num=20):
    """Return the key words of content based on TF-IDF
    Args:
        content: 2-d list of words generate by prepro.cut
    """
    text = ''
    for i in content:
        text += ' '.join(i) + '\n'
    return jieba.analyse.extract_tags(text, topK=num)

def text_rank(content, num=20):
    """Return the key words of content based on textrank
    Args:
        content: 2-d list of words generate by prepro.cut
    """
    text = ''
    for i in content:
        text += ' '.join(i) + '\n'
    return jieba.analyse.extract_tags(text, topK=num)

def gen_dict_counter_corpus(content):
    """Return the gensim_dictionary counter, and gensim_corpus
    Args:
        content: 2-d list of words generate by prepro.cut
    """
    dictionary = corpora.Dictionary(content)
    corpus = [dictionary.doc2bow(text) for text in content]
    counter = Counter()
    for line in content:
        counter.update(line)
    return dictionary, counter, corpus

def lda_analyse(corpus, dictionary):
    """Return the topic distribution
    Args:
        corpus: gensim_corpus
    """
    lda = LdaModel(corpus, num_topics=10, id2word=dictionary)
    pprint(lda.show_topics())

    return lda

def gen_wordcloud(png, counter, filename, font_path='msyh.ttc'):
    image = np.array(Image.open(png))
    wc = WordCloud(font_path=font_path, background_color='white', mask=image)
    wc.generate_from_frequencies(counter)

    wc.to_file(filename + '.png')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.shoe()




