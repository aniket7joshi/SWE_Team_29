# Plagiarism Detection for Assignments
A project done for the Software Engineering course in IIIT-H.

## Team Members
1. Aniket Joshi
2. Anupam Misra
3. Ramanjaneyulu Payala
4. Sahil Bakshi
5. Saurabh Chand
6. Tanmai Khanna
7. Utsav Agarwal 

## Problem Statement
Developing a software for the detection of plagiarism in handwritten or typed documents like reports, essays, written assignments, etc. using NLP for assessing similarity and CV for handwriting recognition

## Abstract
Plagiarism is an unethical activity that is not trivial to detect due to the high number of assignments that a professor receives. Apart from it leading to students who invest their time and effort feeling wrong, it gives undue reward to the person that commits the act, and is unfair to the professor that painstakingly crafts assignments for the benefit of students. To aid in detecting plagiarism, we propose a modular plagiarism detector that works on typed as well as hand-written assignments. The detector will accept as input all assignments in bulk, and will return in pairs assignments in which plagiarism has been detected in several levels - exact matches, fuzzy matches, as well as similar semantic content. The software will be available as a distributed system that can accepts requests from multiple sources. Since there doesn’t need to be any shared database for the users, only isolated personal databases - we will focus on availability as consistency is trivial. Our implementation will also be scalable, not only in terms of concurrent requests but also with respect to the size and number of assignments it can check. We will be following test-driven development for this project and aim to produce a free open source software 


## Setup
Framework:
* Install django : pip3 install django

For file input plugin:
* Install npm : sudo apt install npm
* Install bower: sudo npm install -g bower
* Install bower install bootstrap-fileinput

Running project
* Clone the repository
 
 Run terminal in project root directory
* Runserver using: python3 manage.py runserver
* Go to the url: localhost:8000/moss

#### The project home page should appear.