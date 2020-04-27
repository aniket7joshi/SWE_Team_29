from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import similarity, exact, bloom_filter, aho, fuzzy
import numpy as np
import pandas as pd
import os
# import json
# from json import JSONEncoder

# class NumpyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return json.JSONEncoder.default(self, obj)

def index(request):
	return render(request, "MOSSv2/index.html", {"title": "Home"})


@login_required
def special(request):
	return HttpResponse("You are logged in!")


@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse("moss:index"))

@login_required
def upload(request):
	return render(request, "MOSSv2/upload.html", {"title": "Upload"})


def register(request):
	registered = False
	if request.method == "POST":
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileInfoForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			profile = profile_form.save(commit=False)
			profile.user = user
			if "profile_pic" in request.FILES:
				print("found profile picture")
				profile.profile_pic = request.FILES["profile_pic"]
			profile.save()
			registered = True
		else:
			print(user_form.errors, profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileInfoForm()
	return render(
		request,
		"MOSSv2/registration.html",
		{
			"user_form": user_form,
			"profile_form": profile_form,
			"registered": registered,
			"title": "Register",
		},
	)


def user_login(request):
	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(reverse("moss:user_login"))
			else:
				return HttpResponse("Your account was inactive.")
		else:
			print("Invalid username: {} or password: {}".format(username, password))
			return render(request, "MOSSv2/login.html", {"username":username, 
			"password":password,
			"title": "Login",
			"error_msg" : "Invalid login details"})
	else:
		return render(request, "MOSSv2/login.html", {"title": "Login"})

@login_required
def upload_files(request):

	if request.method == "POST":
		file_list = [x.name for x in request.FILES.getlist('file')]
		files = request.FILES.getlist('file')
		print("{} files received.".format(len(file_list)))
		print(files)
		# print("Document type: ", request.POST.get('documentType'))
		gensim_similarity_matrix = similarity.check_gensim_similarity(files)
		# contents = ""
		# with open('./tests/' + file_list[0]) as f:
		# 	for line in f.readlines():
		# 		contents += line
# <<<<<<< Updated upstream
# =======
# 		print('****************** GENSIM *********************')
# 		print(np.array(gensim_similarity_matrix))
# >>>>>>> Stashed changes
		# print(contents)
		# print('*****')
		# contents = ""
		# with open('./tests/' + file_list[1]) as f:
		# 	for line in f.readlines():
		# 		contents += line
		# print(contents)
		# print('*****')
		# print(files)
		tf_idf_matrix = similarity.tf_idf_cosine_distance(file_list)
# 		print('\nTFIDF mat:\n', tf_idf_matrix)
# =======
# 		print('****************** TF IDF **********************')
# 		print(tf_idf_matrix)
		spacy_similarity = similarity.spacy_similarity(file_list)
		print('****************** SPACY ***********************')
		print(np.array(spacy_similarity))
		all_fuzzy_scores = []
		for i in range(len(file_list)):
			curr_fuzzy = []
			for j in range(len(file_list)):
				# print(file_list[i],file_list[j])
				# exact.input_all(file_list[i],file_list[j])
				curr_fuzzy.append(fuzzy.input_all(file_list[i], file_list[j]))
			all_fuzzy_scores.append(curr_fuzzy)
		# similarity.text_difference(file_list)		
		gen_arr, spacy_arr, fuzzy_arr = np.array(gensim_similarity_matrix), np.array(spacy_similarity), np.array(all_fuzzy_scores)
		print('\nFuzzy mat:\n', fuzzy_arr)
		print('\nGenism mat:\n', gen_arr)
		print('\nSpacy mat:\n', spacy_arr)
		print('***************** FUZZY *************************')
		print(np.array(all_fuzzy_scores))
		print('***************** text difference ******************')
		similarity.text_difference(file_list)
		print('***************** sentence similarity *****************')
		similarity.check_each_sentence(file_list)
		write_mat(gen_arr, "gen")
		write_mat(spacy_arr, "spacy")
		write_mat(fuzzy_arr, "fuzz")
		write_mat(tf_idf_matrix, "tfidf")
		request.session['files'] = file_list
	return render(request, "MOSSv2/upload.html", {"msg":"Similarity Scores",
	"title": "Upload",
	"file_list": file_list,
	"tfidf_mat": np.around(tf_idf_matrix, decimals=3),
	"genism_mat": np.around(gen_arr, decimals=3),
	"spacy_mat": np.around(spacy_arr, decimals=3),
	"fuzzy_mat": fuzzy_arr})


@login_required
def check_treshold(request):
	if request.method == "POST":
		print("Threshold: ", request.POST.get('threshold'))
		tf_mat, gen_mat = read_mat('tfidf'), read_mat('gen')
		spacy_mat, fuzzy_mat = read_mat('spacy'), read_mat('fuzz')
		file_list = request.session['files']
		thres_fuzzy, thres_other = int(request.POST.get('threshold')), int(request.POST.get('threshold')) / 100
		op_files, fuzz_score, spacy_score, tfidf_score, gen_score = [], [], [], [], []
		for i in range(len(file_list)):
			for j in range(len(file_list) - i):
				if i == j:
					continue
				if fuzzy_mat[i][j] >= thres_fuzzy or spacy_mat[i][j] >= thres_other or gen_mat[i][j] >= thres_other or tf_mat[i][j] >= thres_other:
					op_files.append((file_list[i], file_list[j]))
					fuzz_score.append(fuzzy_mat[i][j])
					spacy_score.append(spacy_mat[i][j])
					tfidf_score.append(tf_mat[i][j])
					gen_score.append(gen_mat[i][j])
		# print(op_files)
		# print(tfidf_score)	
	return render(request, "MOSSv2/results.html", {"title": "Results",
	"files": op_files,
	"fuzz": fuzz_score,
	"spacy": spacy_score,
	"tf_idf": tfidf_score,
	"gen": gen_score})

def write_mat(mat, name):
	path = os.getcwd()
	print("Path: ", path)
	df = pd.DataFrame(mat)
	df.to_csv(path + '/MOSSv2/mats/' + name + '.csv', index = False, header = False)

def read_mat(name):
	path = os.getcwd()
	df = pd.read_csv(path + '/MOSSv2/mats/' + name + '.csv', header = None)
	return np.array(df)

