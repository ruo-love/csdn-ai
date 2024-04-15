import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# 中文文本分词
def chinese_tokenize(text):
    words = jieba.lcut(text)
    return words


# 计算文本相似度
def chinese_similarity(text1, text2):
    # 分词
    words1 = chinese_tokenize(text1)
    words2 = chinese_tokenize(text2)

    # 将单词列表转换为字符串
    text1_str = " ".join(words1)
    text2_str = " ".join(words2)

    # 构建词袋模型
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([text1_str, text2_str])

    # 计算余弦相似度
    similarity_matrix = cosine_similarity(X)
    similarity_score = similarity_matrix[0, 1]
    return similarity_score

