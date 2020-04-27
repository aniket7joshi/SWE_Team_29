from collections import defaultdict
from gensim import corpora
from gensim import models
from gensim import similarities
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import SpectralClustering
import os
import spacy
import nltk
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

	# text_difference(documents)
	sentence_checker(documents[1],documents[1])
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




def sentence_checker(document1,document2):
	document1 = nltk.tokenize.sent_tokenize(document1)
	document2 = nltk.tokenize.sent_tokenize(document2)
	tfidf_transformer = TfidfVectorizer()
	doc1 = tfidf_transformer.fit_transform(document1)
	doc2 = tfidf_transformer.transform(document2)
	cosineSimilarities = cosine_similarity(doc1,doc2)
	print("This is cosine similarity \n")
	print(cosineSimilarities)

	for index in range(len(document1)):
		for index1 in range(len(document2)):
			if cosineSimilarities[index][index1] >= 0.7:
				print("The two matching sentences are \n")
				print("Sentence 1 : ",document1[index])
				print("Sentence 2 : ",document2[index])

def text_difference(file_list):
	documents,_= read_files1(file_list)
	for k in range(len(documents)):
		doc = documents[k]
		for i in range(len(documents)):
			print(file_list[k], file_list[i])
			doc_a = documents[i]
			diff = difflib.ndiff(doc.split('\n'), doc_a.split('\n'))
			arr = [x for x in diff]
			for x in arr:
				print(x)