import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

from nltk.corpus import stopwords
from tester import lem

# Скачиваем русские стоп-слова
import nltk
nltk.download('stopwords')

# def get_news_summary():

russian_stopwords = stopwords.words("russian")

# Предположим, что у вас есть DataFrame pandas с одной колонкой "News" в которой хранятся тексты новостей.
data = pd.read_csv("113.csv")
print(data["news"])

vectorizer = TfidfVectorizer(stop_words=russian_stopwords)
X = vectorizer.fit_transform(data["news"])

# Настройка модели KMeans. Выберите подходящее количество кластеров (n_clusters)
true_k = 10
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

# Выводим топовые слова для каждого кластера
print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()
for i in range(true_k):
    print("Cluster %d:" % i),
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind]),
    print("\n")

# Используйте полученную модель для прогнозирования кластера новой новости

# new_news = "они организовывать книжный магазин чарли июнь проходить встреча посвящать вселенная гарри поттер лектор елена хомухина рассказывать джоан роулинг понимать добро зло размещать детский книга отсылка мифология разный страна"
Y = vectorizer.transform([new_news])
prediction = model.predict(Y)
print(prediction)