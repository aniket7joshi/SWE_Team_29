from fuzzywuzzy import fuzz
from collections import defaultdict
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def penn_to_wn(tag):
	if tag.startswith('N'):
		#print("PENNNNNN")
		return 'n'
 
	if tag.startswith('V'):
		return 'v'
 
	if tag.startswith('J'):
		return 'a'
 
	if tag.startswith('R'):
		return 'r'
 
	return None
 
def tagged_to_synset(word, tag):
	wn_tag = penn_to_wn(tag)
	#print("TAGGGGGGGG")
	if wn_tag is None:
		#print("NONE")
		return None
 
	try:
		#print(wordnet.synsets(word, wn_tag)[0])
		return wordnet.synsets(word, wn_tag)[0]
	except:
		return None

def main():

	with open('c.txt','r') as file:
		src_content=file.read()
		#print(src_content)
	with open('d.txt','r') as file:
		input_content=file.read()
		#print(input_content)

	#print(src_content,input_content)
	stop_words1 = set(stopwords.words('english'))
	word_tokens1 = word_tokenize(src_content)
	filtered_sentence_src = [w for w in word_tokens1 if not w in stop_words1]
	filtered_sentence_src = []
	for w in word_tokens1: 
		if w not in stop_words1: 
			filtered_sentence_src.append(w)

	stop_words2 = set(stopwords.words('english'))
	word_tokens2 = word_tokenize(input_content)
	filtered_sentence_input = [w for w in word_tokens2 if not w in stop_words2]
	filtered_sentence_input = []
	for w in word_tokens2: 
		if w not in stop_words2: 
			filtered_sentence_input.append(w)

	#print(filtered_sentence)

	src_content_final = ' '.join(filtered_sentence_src)
	input_content_final = ' '.join(filtered_sentence_input)

	#print(src_content_final)
	#print(input_content_final)

	Str1 = src_content_final
	Str2 = input_content_final
	Ratio = fuzz.ratio(Str1.lower(),Str2.lower())
	Partial_Ratio = fuzz.partial_ratio(Str1.lower(),Str2.lower())
	Token_Sort_Ratio = fuzz.token_sort_ratio(Str1,Str2)
	Token_Set_Ratio = fuzz.token_set_ratio(Str1,Str2)
	#print("Ratio: ",end=' ')
	#print(Ratio)
	#print("Partial Ratio: ",end=' ')
	#print(Partial_Ratio)
	#print("Token Sort Ratio: ",end=' ')
	#print(Token_Sort_Ratio)
	print("Fuzzy match score: ",end=' ')
	print(Token_Set_Ratio)

	#POStagging
	sentence1 = pos_tag(word_tokenize(src_content_final))
	sentence2 = pos_tag(word_tokenize(input_content_final))

	#print(sentence1)

	#print(wordnet.synset('Wonderful','j'))
 
	# Get the synsets for the tagged words
	synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
	synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]

	synsets1 = [ss for ss in synsets1 if ss]
	synsets2 = [ss for ss in synsets2 if ss]
	
	#print(synsets1)
	#print(synsets2)

	score, count = 0.0, 0
	for synset in synsets1:
		# Get the similarity value of the most similar word in the other sentence
		simlist = [synset.path_similarity(ss, simulate_root=False) for ss in synsets2 if synset.path_similarity(ss, simulate_root=False) is not None]
		if not simlist:
			continue;
		best_score = max(simlist)

		# Check that the similarity could have been computed
		score += best_score
		count += 1

	if count == 0:
		return 0
	score /= count
	print("Semantic synset similarity score: ",end=' ')
	print(score)

if __name__ == '__main__':
	main()