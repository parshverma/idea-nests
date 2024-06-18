import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin_min
from collections import Counter

def gen_sim_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)

def generate_summary(ideas, top_n=3):
    stop_words = stopwords.words('english')
    sentences = ideas
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0 and s not in stop_words]

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    num_clusters = min(len(sentences), 3)
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)

    cluster_sentences = [[] for _ in range(num_clusters)]
    for i, label in enumerate(kmeans.labels_):
        cluster_sentences[label].append(sentences[i])

    cluster_counts = [Counter(cluster) for cluster in cluster_sentences]

    print(cluster_sentences)
    selected_sentences = []
    for cluster_count, cluster in zip(cluster_counts, cluster_sentences):
        selected_cluster = max(cluster_count, key=lambda x: cluster_count[x])
        selected_sentences.append(selected_cluster)

    return ". ".join(selected_sentences[:top_n])

# testing
ideas = [
    "Construct a new playground with inclusive equipment for children of all abilities.",
    "Install outdoor fitness stations along walking trails to promote healthy living.",
    "Organize seasonal sports leagues for residents of all ages to encourage active participation.",
    "Enhance park lighting for increased safety during evening hours.",
    "Introduce guided nature walks and educational programs for environmental awareness.",
    "Host outdoor movie nights and cultural events to bring the community together.",
    "Host outdoor movie nights and cultural events to bring the community together.",#Repeated Idea
    "Introduce guided nature walks and educational programs for environmental awareness.",  # Repeated Idea
    "Enhance park lighting for increased safety during evening hours", #Repeated Idea
    "Construct a new playground with inclusive equipment for children of all abilities.",#Repeated Idea

]

# summary = generate_summary(ideas, top_n=3)
# print(summary)

from better_profanity import profanity

# Sample list of ideas
ideas = [
    "Construct a new fucking playground with inclusive equipment for children of all abilities",
    "Host shitty outdoor movie nights and cultural events to bring the community together",
    "Enhance park lighting for increased safety during evening hours",
    "This is a profane idea with bad language",
    "Another idea with offensive words"
]

# Check for profanity in each idea
for idea in ideas:
    if profanity.contains_profanity(idea):
        print(f"Profanity found in idea: {idea}")
    else:
        print(f"No profanity found in idea: {idea}")
