import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import wordnet
from nltk.metrics import jaccard_distance
from nltk.util import ngrams
from nltk import FreqDist
from nltk import pos_tag

# 下载 NLTK 数据
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# 文本预处理
def preprocess_text(text):
    # 小写化
    text = text.lower()
    # 分词
    words = word_tokenize(text)
    # 去除停用词
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # 词干化
    stemmer = PorterStemmer()
    words = [stemmer.stem(word) for word in words]
    return words

# 计算 Jaccard 相似度
def jaccard_similarity(text1, text2):
    words1 = preprocess_text(text1)
    words2 = preprocess_text(text2)
    # 计算文本的 Jaccard 相似度
    jaccard_sim = 1 - jaccard_distance(set(words1), set(words2))
    return jaccard_sim

# 示例文本
text1 = "NLTK is a leading platform for building Python programs to work with human language data."
text2 = "NLTK is a popular Python library used for natural language processing tasks."

# 计算文本相似度
similarity_score = jaccard_similarity(text1, text2)
print("Jaccard Similarity Score:", similarity_score)
