
# coding: utf-8

# In[2]:

import os, sys
import math
import numpy as np
lib_path = os.path.abspath(os.path.join('D:\projects\spamEmailClassifier'))
sys.path.append(lib_path)
from Preprocesser import * 
from NaiveBayes import *


# # My Naive Bayes Classifier

# In[3]:

trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList = getTrainingTestSet("D:\\projects\\spamEmailClassifier\\spamDataset", "D:\\projects\\spamEmailClassifier\\nonspamDataset")
trainingSpamTokenList, testSpamTokenList, trainingNonSpamTokenList, testNonSpamTokenList = getNormalizedEmailList(trainingSetSpamFileList, testSetSpamFileList, trainingSetNonSpamFileList, testSetNonSpamFileList)


# In[4]:

wordList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability =  getSpamWordList(trainingSpamTokenList,trainingNonSpamTokenList, 4, 9, 3, 99)
print len(wordList)


# ### Prediction 

# In[5]:

p,x,y = predict(trainingSpamTokenList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability)
s =  sum(p) / float(len(p))
print "training set spam: ", s
p,x,y = predict(trainingNonSpamTokenList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability)
ns =  1 - sum(p) / float(len(p))
print "training set non-spam: ", ns
print "training set overall: ", s * spamProbability + ns * (1 - spamProbability)

print ""
p,x,y = predict(testSpamTokenList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability)
s =  sum(p) / float(len(p))
print "test set spam: ", s
p,x,y = predict(testNonSpamTokenList, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability)
ns =  1 - sum(p) / float(len(p))
print "test set non-spam: ", ns
print "test set overall: ", s * spamProbability + ns * (1 - spamProbability)


# In[6]:

myEmails = ["I like ml", "here is a good offer to make millions dollars from littel investment", "what are you doing"]
x = map(lambda x : getTokensFromStr(x), myEmails)
p,xs,yds = predict(x, wordDistributionInSpam, wordDistributionInNonSpam, spamProbability)
print p


# # Skkit-learn Naive Bayes

# In[7]:

from sklearn.feature_extraction.text import CountVectorizer
def readFileListAndNormalize(fileList):
    res = []
    for i in fileList:
        with open(i, 'r') as file :
            data=file.read()
            res = res + [data]
    return res


# In[8]:

trainingSpamEmails = readFileListAndNormalize(trainingSetSpamFileList)
testSpamEmails = readFileListAndNormalize(testSetSpamFileList)
trainingNonSpamEmails = readFileListAndNormalize(trainingSetNonSpamFileList)
testNonSpamEmails = readFileListAndNormalize(testSetNonSpamFileList)


# In[9]:

count_vect = CountVectorizer()


# In[10]:

X_train_counts = count_vect.fit_transform(trainingSpamEmails + trainingNonSpamEmails)


# In[11]:

print X_train_counts[0].shape


# In[12]:

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


# In[77]:

target = map (lambda x : 1, trainingSpamEmails)
target += map(lambda x : 0, trainingNonSpamEmails)

testTarget = map (lambda x : 1, testSpamEmails)
testTarget += map(lambda x : 0, testNonSpamEmails)
print len(target), len(trainingSpamEmails) + len(trainingNonSpamEmails)


# In[14]:

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
clf = BernoulliNB().fit(X_train_tfidf, target)


# ### predict new emails

# In[15]:

X_train_spam_count =  count_vect.transform(trainingSpamEmails)
X_train_nonspam_count =  count_vect.transform(trainingNonSpamEmails)
X_train_spam_tfidf =  tfidf_transformer.transform(X_train_spam_count)
X_train_nonspam_tfidf =  tfidf_transformer.transform(X_train_nonspam_count)

X_test_spam_count =  count_vect.transform(testSpamEmails)
X_test_nonspam_count =  count_vect.transform(testNonSpamEmails)
X_test_spam_tfidf =  tfidf_transformer.transform(X_test_spam_count)
X_test_nonspam_tfidf =  tfidf_transformer.transform(X_test_nonspam_count)


# In[16]:

X_train_spam_predicted = clf.predict(X_train_spam_tfidf) 
print "training spam set: ", float(np.sum(X_train_spam_predicted)) / len(X_train_spam_predicted)

X_train_nonspam_predicted = clf.predict(X_train_nonspam_tfidf) 
print "training nonspam set: ", float(np.sum(X_train_nonspam_predicted)) / len(X_train_nonspam_predicted)


# In[17]:

X_test_spam_predicted = clf.predict(X_test_spam_tfidf) 
print "test spam set: ", float(np.sum(X_test_spam_predicted)) / len(X_test_spam_predicted)

X_test_nonspam_predicted = clf.predict(X_test_nonspam_tfidf) 
print "test nonspam set: ", float(np.sum(X_test_nonspam_predicted)) / len(X_test_nonspam_predicted)


# In[ ]:




# ### Instead of using tfidf,  my wordList generate better result.  SHOULD FIGURE OUT tfidf

# In[22]:

trainingSpamNormalizedEmails = map(lambda x : ' '.join(x), trainingSpamTokenList)
testSpamNormalizedEmails = map(lambda x : ' '.join(x), testSpamTokenList)
trainingNonSpamNormalizedEmails = map(lambda x : ' '.join(x), trainingNonSpamTokenList)
testNonSpamNormalizedEmails = map(lambda x : ' '.join(x), testNonSpamTokenList)


# In[29]:

count_vect_normalized = CountVectorizer()
count_vect_normalized.vocabulary = wordList
X_train_counts_normalized = count_vect_normalized.transform(trainingSpamNormalizedEmails + trainingNonSpamNormalizedEmails)
clf_normalized = BernoulliNB().fit(X_train_counts_normalized, target)



# In[32]:

X_train_spam_normalized_predicted = clf_normalized.predict(count_vect_normalized.transform(trainingSpamNormalizedEmails)) 
print "training spam set: ", float(np.sum(X_train_spam_normalized_predicted)) / len(X_train_spam_normalized_predicted)

X_train_nonspam_normalized__predicted = clf_normalized.predict(count_vect_normalized.transform(trainingNonSpamNormalizedEmails))
print "training nonspam set: ", 1- float(np.sum(X_train_nonspam_normalized__predicted)) / len(X_train_nonspam_normalized__predicted)


predict = clf_normalized.predict(count_vect_normalized.transform(testSpamNormalizedEmails)) 
print "test spam set: ", float(np.sum(predict)) / len(predict)

predict = clf_normalized.predict(count_vect_normalized.transform(testNonSpamNormalizedEmails))
print "test nonspam set: ", 1- float(np.sum(predict)) / len(predict)


# ### use pipeline

# In[43]:

from sklearn.pipeline import Pipeline
text_clf = Pipeline([('vect', CountVectorizer()),
     ('tfidf', TfidfTransformer()),
     ('clf', MultinomialNB()),
])
text_clf = text_clf.fit(trainingSpamNormalizedEmails + trainingNonSpamNormalizedEmails, target)  


# In[45]:

predicted = text_clf.predict(trainingSpamNormalizedEmails + trainingNonSpamNormalizedEmails)
print predicted
np.mean(predicted == target)    


# In[48]:

from sklearn import metrics
print(metrics.classification_report(target, predicted,
    target_names=['non-spam', 'spam']))


# # Sklearn SVM 

# In[74]:

from sklearn import svm
clf = svm.SVC(class_weight = 'auto', kernel = 'linear')
clf.fit(X_train_counts_normalized, target)


# In[75]:

predict = clf.predict(count_vect_normalized.transform(trainingSpamNormalizedEmails))
print float(sum(predict)) / len(predict)

predict = clf.predict(count_vect_normalized.transform(trainingNonSpamNormalizedEmails))
print 1- float(sum(predict)) / len(predict)


# In[78]:

predicted = clf.predict(count_vect_normalized.transform(testSpamNormalizedEmails + testNonSpamNormalizedEmails))
print(metrics.classification_report(testTarget, predicted,
    target_names=['non-spam', 'spam']))

