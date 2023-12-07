"""CountVectorizer objects and wordclouds for points 2,3 and 4 in the exam"""

import pandas as pd     # pandas package imported with an alias. Used for reading json file and working with DataFrame
from sklearn.feature_extraction.text import CountVectorizer     # class from sklearn package whose objects tokenize and count occurrences
from wordcloud import WordCloud     # class from wordcloud package for generating wordclouds
from matplotlib import pyplot as plt    # pyplot interface from matplotlib package imported
import numpy as np      # numpy package imported with an alias. Used for working with  numpy arrays, here used for mask

### loading the data
data = pd.read_json("Sarcasm.json", lines=True)

# in the json file it is 0 and 1
# .map() method called for a pandas Series to rename the categorical variable
data["is_sarcastic"] = data["is_sarcastic"].map({0: "Not Sarcasm", 1: "Sarcasm"})

# link to article not necessary for the model
data = data[["headline", "is_sarcastic"]]

### 3 different CountVectorizer objects from task #2

# words between 5 and 20 letters long
# analyzer="word" by default
cv_520 = CountVectorizer(token_pattern=r"\b\w{5,20}\b", decode_error='replace')
# words with 3 letters or fewer
# see how token_pattern= changed
cv_13 = CountVectorizer(token_pattern=r"\b\w{1,3}\b", decode_error='replace')
# combinations of 3 to 6 words
# token_pattern= is default, because word length is not given
# dtype= argument was needed for this instance, otherwise I was getting a MemoryError, because of the array size
cv_36 = CountVectorizer(ngram_range=(3, 6), decode_error='replace', dtype='uint8')


### creating wordclouds

# data is a DataFrame object
# headline is a Series object in the data object
# to_list() is a pandas method for Series objects that returns a list of values
sarcastic_sentences = data[data['is_sarcastic'] == 'Sarcasm'].headline.to_list()
not_sarcastic_sentences = data[data['is_sarcastic'] == 'Not Sarcasm'].headline.to_list()

# cv_520
# .fit_transform() method used again to convert list to matrix
x520_sarcasm = cv_520.fit_transform(sarcastic_sentences)
# get_feature_names_out() method creates an array of all the different words (feature names) found in cv vocabulary that it go from previous method
ngrams520_sarcasm = cv_520.get_feature_names_out()
# frequency of each word sorted in a ndarray
ngrams520_sarcasm_freq = sum(x520_sarcasm.toarray())
# empty dictionary for now
vocab520_sarcasm = {}
# counter
i = 0
# for loop iterates through every element of the array and stores it as a key
# values are the frequency of the word in the frequency ndarray
for k in ngrams520_sarcasm:
    vocab520_sarcasm[k] = ngrams520_sarcasm_freq[i]
    i += 1

x520_not_sarcasm = cv_520.fit_transform(not_sarcastic_sentences)
ngrams520_not_sarcasm = cv_520.get_feature_names_out()
ngrams520_not_sarcasm_freq = sum(x520_not_sarcasm.toarray())
vocab520_not_sarcasm = {}
i = 0
for k in ngrams520_not_sarcasm:
    vocab520_not_sarcasm[k] = ngrams520_not_sarcasm_freq[i]
    i += 1

# cv_13
x13_sarcasm = cv_13.fit_transform(sarcastic_sentences)
ngrams13_sarcasm = cv_13.get_feature_names_out()
ngrams13_sarcasm_freq = sum(x13_sarcasm.toarray())
vocab13_sarcasm = {}
i = 0
for k in ngrams13_sarcasm:
    vocab13_sarcasm[k] = ngrams13_sarcasm_freq[i]
    i += 1

x13_not_sarcasm = cv_13.fit_transform(not_sarcastic_sentences)
ngrams13_not_sarcasm = cv_13.get_feature_names_out()
ngrams13_not_sarcasm_freq = sum(x13_not_sarcasm.toarray())
vocab13_not_sarcasm = {}
i = 0
for k in ngrams13_not_sarcasm:
    vocab13_not_sarcasm[k] = ngrams13_not_sarcasm_freq[i]
    i += 1

# cv_36
x36_sarcasm = cv_36.fit_transform(sarcastic_sentences)
ngrams36_sarcasm = cv_36.get_feature_names_out()
ngrams36_sarcasm_freq = sum(x36_sarcasm.toarray())
vocab36_sarcasm = {}
i = 0
for k in ngrams36_sarcasm:
    vocab36_sarcasm[k] = ngrams36_sarcasm_freq[i]
    i += 1

x36_not_sarcasm = cv_36.fit_transform(not_sarcastic_sentences)
ngrams36_not_sarcasm = cv_36.get_feature_names_out()
ngrams36_not_sarcasm_freq = sum(x36_not_sarcasm.toarray())
vocab36_not_sarcasm = {}
i = 0
for k in ngrams36_not_sarcasm:
    vocab36_not_sarcasm[k] = ngrams36_not_sarcasm_freq[i]
    i += 1

# wordclouds

# circle mask
# mask ndarray defined
# np.ogrid() function returns an open meshgrid
x, y = np.ogrid[:300, :300]
mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
mask = 255 * mask.astype(int)

# instantiates a WordCloud object that can create wordclouds
# wordcloud objects have a lot of parameters that can be modified from default
# mask is defined for the object, so all plots generated with it will have it
wordcloud = WordCloud(mask=mask,
                      background_color="white",
                      min_font_size=5,
                      contour_color="yellow",
                      contour_width=0.1
                      )

# .generate_from_frequencies() is a WordCloud method used to create a wordcloud from words and frequencies
# wordcloud object has new values under the parameter "words" now
wordcloud.generate_from_frequencies(vocab520_sarcasm)
# .figure() function creates a new figure with a unique identified (1)
plt.figure(1)
# .subplot() function places the generated wordcloud on the figure depending on the integers (row, column, index)
plt.subplot(121)
# .title() function adds a title to the figure
plt.title("5-20 letters - sarcasm")
# .imshow() function displays data in the wordcloud object as an image
plt.imshow(wordcloud)
# .axis() function with "off" parameter hides all axis labels etc.
plt.axis('off')

wordcloud.generate_from_frequencies(vocab520_not_sarcasm)
plt.figure(1)
plt.subplot(122)
plt.title("5-20 letters - not sarcasm")
plt.imshow(wordcloud)
plt.axis('off')

wordcloud.generate_from_frequencies(vocab13_sarcasm)
plt.figure(2)
plt.subplot(121)
plt.title("1-3 letters - sarcasm")
plt.imshow(wordcloud)
plt.axis('off')

wordcloud.generate_from_frequencies(vocab13_not_sarcasm)
plt.figure(2)
plt.subplot(122)
plt.title("1-3 letters - not sarcasm")
plt.imshow(wordcloud)
plt.axis('off')

wordcloud.generate_from_frequencies(vocab36_sarcasm)
plt.figure(3)
plt.subplot(121)
plt.title("3-6 words - sarcasm")
plt.imshow(wordcloud)
plt.axis('off')

wordcloud.generate_from_frequencies(vocab36_not_sarcasm)
plt.figure(3)
plt.subplot(122)
plt.title("3-6 words - not sarcasm")
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

print("Here are the clouds!")
