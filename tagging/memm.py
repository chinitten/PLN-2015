from tagging.features import (History, word_lower, word_istitle, word_isupper,
word_isdigit, prev_tags, NPrevTags, PrevWord)

from featureforge.vectorizer import Vectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.pipeline import Pipeline

class MEMM:

    def __init__(self, n, tagged_sents):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n

        words = []
        for sent in tagged_sents:
            if sent != []:
                w , t = zip(*sent)
                words += list(w)

        self.v = set(words)

        features = [word_lower, word_istitle, word_isupper, word_isdigit, prev_tags, NPrevTags(n)]
        prevword = []
        for f in features:
             prevword += [PrevWord(f)]
        features += prevword
        vectorizer = Vectorizer(features)
        self.pipeline = Pipeline([('vect', vectorizer),
                            ('classifier', LogisticRegression())])
        histories = self.sents_histories(tagged_sents)
        tags = self.sents_tags(tagged_sents)
        self.pipeline.fit(histories, tags)

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        histories = []
        for sent in tagged_sents:
            histories += self.sent_histories(sent)

        return histories


    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n
        result = []
        if tagged_sent != []:
            words , tags = zip(*tagged_sent)
            tags = ['<s>']*(n - 1)+ list(tags)
            upto = len(words)
            for i in range(0, upto):
                result.append(History(list(words),tuple(tags[i:n-1+i]),i))
        return result

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        result = []
        if tagged_sents != []:
            for sent in tagged_sents:
                result += self.sent_tags(sent)
        return result

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        tags = []
        if tagged_sent != []:
            words , tags = zip(*tagged_sent)
        return list(tags)

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        n = self.n
        result = []
        history = History(sent,('<s>',)*(n-1),0)
        prev_tag = ('<s>',)*(n-1)
        for i in range(1, len(sent)+1):
            tag = self.tag_history(history)
            result.append(tag)
            prev_tag = prev_tag + (tag,)
            prev_tag = prev_tag[1:]
            history = History(sent, prev_tag, i)
        return result

    def tag_history(self, h):
        """Tag a history.

        h -- the history.
        """
        return self.pipeline.predict([h])

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        result = False
        if w not in self.v:
            result = True

        return result
