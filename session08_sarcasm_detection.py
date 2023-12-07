#!/usr/bin/env python
# coding: utf-8

# ## sarcasm detection
# source: https://thecleverprogrammer.com/2021/08/24/sarcasm-detection-with-machine-learning/


# https://scikit-learn.org/stable/user_guide.html
# section 6.2.3 Text feature extraction
# section 3.1 Cross Validation
# section 1.9 Naive Bayes
# %%


import pandas as pd     # pandas package imported with an alias. Used for reading json file and working with DataFrame
import numpy as np      # numpy package imported with an alias. Used for working with  numpy arrays
from sklearn.feature_extraction.text import CountVectorizer     # class from sklearn package whose objects tokenize and count occurrences
from sklearn.model_selection import train_test_split        # function that splits data into training and testing sets
from sklearn.naive_bayes import BernoulliNB     # class that implements naive Bayes training and classification algos according to Bernoulli's distribution
from wordcloud import WordCloud     # class from wordcloud package for generating wordclouds
from matplotlib import pyplot as plt    # pyplot interface from matplotlib package imported

# load data
# .read_json() is a function from the pandas package that reads json files as DataFrame objects
# lines= argument instructs it to read each line, there is an error if it is left False
data = pd.read_json("Sarcasm.json", lines=True)
# .head() method returns first 5 rows by default, unless specified with n
print(data.head(n=20))


# Rename categorical variable
# in the json file it is 0 and 1
# .map() method called for a pandas Series to rename the categorical variable
data["is_sarcastic"] = data["is_sarcastic"].map({0: "Not Sarcasm", 1: "Sarcasm"})
print(data.head(n=20))


# Keep only the headline and the classification
# link to article not necessary for the model
data = data[["headline", "is_sarcastic"]]

# change into numpy arrays for vectorization
# pandas Series are converted into numpy arrays with the .array() function from numpy package
# numpy arrays have different functions and methods available that make it better for matrix computation
x = np.array(data["headline"])
y = np.array(data["is_sarcastic"])

# initialize the vectorizer, instantiate an object of the CountVectorizer class
# cv will not be able to convert text into vector of token counts
# tokenization - convert text into small tokens and assign it integer values so that algos can understand
cv = CountVectorizer()

# transform the data, the list of sentences becomes a matrix
# each row represent sentences and there is a column for every word in the data
# the value in each cell represents the number of times a given word appears in that sentence
# parameters of the vectorization can be done in the initialization of the vectorizer... see the documentation.
# .fit_transform() method returns a matrix of the text
X = cv.fit_transform(x)

# split the data in training and test
# y does not need to be modified, because it is just labels sarcastic or not sarcastic
# 4 sets, 2 for the X matrix and 2 for y ndarray, both given in the *arrays arbitrary positional argument
# test_size= argument (between 0 and 1) determines how much of the data used for , the rest is used for training. Has to be given, because default=None
# random_state= ensures reproducibility
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=100)

# Initialize the language model
# instantiates an object of the BernoulliNB class
model = BernoulliNB()
# train the model with the training set with the .fit() method
model.fit(X_train, y_train)
# test the model with the test set with the .score() method
# returns the the accuracy when given testing sets
print(model.score(X_test, y_test))

# Get input from user
user = input("Enter a Text: ")
# process input to feed it to the model
# .transform() is a method for CV class that transforms text to a matrix
# .toarray() is a method to convert matrices to ndarrays that can be fed to the model
new_data = cv.transform([user]).toarray()
# .predict() method of BernoulliNB class predicts the result of an array when it is fed to a trained model
output = model.predict(new_data)
print(output)



## Make word clouds of sarcastic and non sarcastic sentences using different vectorizer setting.

# data is a DataFrame object
# headline is a Series object in the data object
# to_list() is a pandas method for Series objects that returns a list of values
sarcastic_sentences = data[data['is_sarcastic'] == 'Sarcasm'].headline.to_list()
not_sarcastic_sentences = data[data['is_sarcastic'] == 'Not Sarcasm'].headline.to_list()

# 2 more CountVectorizer objects are instantiated
# analyzer= differentiates between word or character n-grams, default is word
# token_pattern= only used for analyzer="word" and it determines the range of word length (it could be useful to exclude short words)
# token_pattern= could be expressed in regex, then it works better for 1-3 letter words
# ngram_range= determines the combinations of n-grams that are tokenized
# in this example, only 4-word sequences are tokenized
# decode_error= determines what the program does if a character that is not in encoding is analyzed
cv2 = CountVectorizer(analyzer='word', token_pattern="[a-z]{5,20}", decode_error='replace')
cv3 = CountVectorizer(analyzer='word', ngram_range=(4, 4), decode_error='replace')

# .fit_transform() method used again to convert list to matrix
x2_s = cv2.fit_transform(sarcastic_sentences)
# get_feature_names_out() method creates an array of all the different words (feature names) found in cv2 vocabulary that it go from previous method
ngrams2_s = cv2.get_feature_names_out()
# frequency of each word sorted in a ndarray
ngrams2_s_freq = sum(x2_s.toarray())
# empty dictionary for now
vocab2_s = {}
# counter
i = 0
# for loop iterates through every element of the array and stores it as a key
# values are the frequency of the word in the frequency ndarray
for k in ngrams2_s:
    vocab2_s[k] = ngrams2_s_freq[i]
    i += 1

x2_ns = cv2.fit_transform(not_sarcastic_sentences)
ngrams2_ns = cv2.get_feature_names_out()
ngrams2_ns_freq = sum(x2_ns.toarray())
vocab2_ns = {}
i = 0
for k in ngrams2_ns:
    vocab2_ns[k] = ngrams2_ns_freq[i]
    i += 1


x3_s = cv3.fit_transform(sarcastic_sentences)
ngrams3_s = cv3.get_feature_names_out()
ngrams3_s_freq = sum(x3_s.toarray())
vocab3_s = {}
i = 0
for k in ngrams3_s:
    vocab3_s[k] = ngrams3_s_freq[i]
    i += 1


x3_ns = cv3.fit_transform(not_sarcastic_sentences)
ngrams3_ns = cv3.get_feature_names_out()
ngrams3_ns_freq = sum(x3_ns.toarray())
vocab3_ns = {}
i = 0
for k in ngrams3_ns:
    vocab3_ns[k] = ngrams3_ns_freq[i]
    i += 1

# creating wordclouds

# instantiates a WordCloud object that can create wordclouds
# objects have a lot of parameters that can be modified from default
wordcloud = WordCloud()

# .generate_from_frequencies() is a WordCloud method used to create a wordcloud from words and frequencies
# wordcloud object has new values under the parameter "words" now
wordcloud.generate_from_frequencies(vocab2_s)

# plot using matplotlib.pyplot
# .figure() function creates a new figure with a unique identified (1)
plt.figure(1)
# .subplot() function places the generated wordcloud on the figure depending on the integers (row, column, index)
plt.subplot(221)
# .imshow() function displays data in the wordcloud object as an image
plt.imshow(wordcloud)
# .plt.show() displays all open figures, sort of like a print function, should only be at the end, no need for it here
"""plt.show()"""
# .axis() function with "off" parameter hides all axis labels etc.
plt.axis('off')

wordcloud.generate_from_frequencies(vocab2_ns)
# plot using matplotlib.pyplot
# .figure() needed to be added to every wordcloud to have them appear in one figure, it didnt before
plt.figure(1)
# I edited the .subplot() arguments so that the 4 pictures fit together nicer
plt.subplot(222)
plt.imshow(wordcloud)
plt.axis('off')

wordcloud.generate_from_frequencies(vocab3_s)
# plot using matplotlib.pyplot
plt.figure(1)
plt.subplot(223)
plt.imshow(wordcloud)
plt.axis('off')

wordcloud.generate_from_frequencies(vocab3_ns)
# plot using matplotlib.pyplot
plt.figure(1)
plt.subplot(224)
plt.imshow(wordcloud)
plt.axis('off')
# only one plt.show function, at the end
plt.show()
