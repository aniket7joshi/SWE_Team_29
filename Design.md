# Design Flow

- The proposed application works as follows:
- The professor logs into the application portal.
- They upload the assignments to the server through the “Upload Assignments” section.
- We will also have an option to upload hand-written assignments that will be converted into text documents and then used as input for our plagiarism checker. A professor can directly upload typed text documents as well.
- Our application to check plagiarism takes as input a set of documents in English, and then checks for plagiarism on several levels:
  - Exact matches between pairs, creating clusters.
  - Fuzzy matches between pairs.
  - Synonym matches using WordNet.
  - Comparing flow of the documents using topic/focus matches.
  - Experimental text similarity using pre-trained NLP models.
- The application then outputs pairs which have a degree of match higher than a pre-decided threshold. The documents are colour coded for easy readability. The professor can then decide to act on certain types of plagiarism also taking into account the degree of match and the confidence of match in case of similarity calculations.
- It also outputs valuable metadata about the plagiarism in the set of assignments.
- The professor can then download the generated report and the plagiarised pairs of assignments. They will also have the option to save the report on the cloud for future reference. 
