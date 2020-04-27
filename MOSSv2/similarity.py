from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import SpectralClustering
import os
import spacy
import difflib

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
	allsimilarities = []
	for k in range(len(documents)):
	# print(len(documents))
		similarity_particular = []
		doc = documents[k]
		vec_bow = dictionary.doc2bow(doc.lower().split())
		vec_lsi = lsi[vec_bow]
		index = similarities.MatrixSimilarity(lsi[corpus])
		sims = index[vec_lsi]
		# sims = sorted(enumerate(sims), key=lambda item: -item[1])
		for i, s in enumerate(sims):
			similarity_particular.append(s)
		allsimilarities.append(similarity_particular)

	text_difference(documents)
	return allsimilarities
def read_files1(file_list):
	documents = []
	stoplist = set('for a of the and to in'.split())
	for file in file_list:
		filepath = './tests/' + file
		contents = ""
		with open(filepath) as f:
			for line in f.readlines():
				contents += line
		file_content = str(contents)
		documents.append(file_content)
	texts = [
		[word for word in document.lower().split() if word not in stoplist]
		for document in documents
	]

	return documents,texts
def spacy_similarity(file_list):
	nlp = spacy.load('en_core_web_sm')
	documents,_= read_files1(file_list)
	similarity_particular = []
	for k in range(len(documents)):
		doc = documents[k]
		doc = nlp(doc)
		similarity_a = []
		for i in range(len(documents)):
			doc_a = nlp(documents[i])
			similarity_a.append(doc.similarity(doc_a))
		similarity_particular.append(similarity_a)
	return similarity_particular			


def tf_idf_cosine_distance(file_list):
	documents,_ = read_files1(file_list)
	tfidf = TfidfVectorizer().fit_transform(documents)
	pairwise_similarity = tfidf * tfidf.T
	# print(pairwise_similarity.toarray())
	return pairwise_similarity.toarray()
	no_of_files = len(file_list)
	cluster_documents(pairwise_similarity,no_of_files)

def cluster_documents(pairwise_similarity,no_of_files):

	scmodel = SpectralClustering(n_clusters=no_of_files - 1 , affinity='precomputed')
	clusters = scmodel.fit_predict(pairwise_similarity)
	# print(clusters)



def text_difference(documents):
	
	diff = difflib.ndiff(documents[0].split('\n'), documents[1].split('\n'))
	arr = [x for x in diff]
	for x in arr:
		print(x)