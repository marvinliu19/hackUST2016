import nltk
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.probability import ConditionalProbDist, ELEProbDist
fichier=open("datatrain2.txt", "r")

lines = fichier.readlines()
print "split\n"
result = []
for line in lines:
    line_split = line.strip().split('*$~#{[||')
    result.append((line_split[0], line_split[1]))

tweets = []


for (words, sentiment) in result:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets.append((words_filtered, sentiment))



def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

def train(labeled_featuresets, estimator=ELEProbDist):
	    # Create the P(label) distribution
	    label_probdist = estimator(label_freqdist)
	    # Create the P(fval|label, fname) distribution
	    feature_probdist = {}
	    return NaiveBayesClassifier(label_probdist, feature_probdist)


word_features = get_word_features(get_words_in_tweets(tweets))
training_set = nltk.classify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)
print classifier.show_most_informative_features(50)


tweet = 'I am so happy! funny ! funny ! happy :))'
print classifier.classify(extract_features(tweet.split()))


