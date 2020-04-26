from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
from sklearn.feature_extraction.text import TfidfVectorizer
import os


def read_files(file_list):
	documents = []

	stoplist = set('for a of the and to in'.split())
	for files in file_list:
		
		file_content = str(files.read().decode())
		documents.append(file_content)
	texts = [
		[word for word in document.lower().split() if word not in stoplist]
		for document in documents
	]

	return documents,texts
def check_gensim_similarity(file_list):

	'''Add similarities for all pairs in this matrix and return'''
	similarity_matrix = defaultdict()
	documents , texts = read_files(file_list)
	
	frequency = defaultdict(int)
	for text in texts:
		for token in text:
			frequency[token] += 1

	texts = [
		[token for token in text if frequency[token] > 1]
		for text in texts
	]

	dictionary = corpora.Dictionary(texts)
	corpus = [dictionary.doc2bow(text) for text in texts]

	lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=4)
	doc = documents[0]
	vec_bow = dictionary.doc2bow(doc.lower().split())
	vec_lsi = lsi[vec_bow]

	index = similarities.MatrixSimilarity(lsi[corpus])

	sims = index[vec_lsi]
	sims = sorted(enumerate(sims), key=lambda item: -item[1])
	for i, s in enumerate(sims):
		# print(i,s)
		print(s, documents[s[0]])




def tf_idf_cosine_distance(file_list):
	documents,_ = read_files(file_list)
	tfidf = TfidfVectorizer().fit_transform(documents)
	pairwise_similarity = tfidf * tfidf.T
	print(pairwise_similarity)