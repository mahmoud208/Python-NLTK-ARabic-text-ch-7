# -*- coding: utf-8 -*-


#############CH7###########################

import nltk
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree
Quran_sents=[]
Quran_words=[]
sent=''' bi/P somi/N {ll~ahi/PN {l/DET r~aHoma`ni/ADJ {l/DET r~aHiymi/ADJ {lo/DET Hamodu/N'''
#READ Quran Corpus------------------------
corpus_root = "quran.txt"
files=open(corpus_root,"r")
sents=files.read()
files.close()
#############################################
#------ Load Tagged text ---------------------
tagged_text =[nltk.tag.str2tuple(t) for t in sents.split()[:1000]]
tagged_textt =[nltk.tag.str2tuple(t) for t in sent.split()]
#-------FreqDist of the tagged text------------
tag_fd = nltk.FreqDist(tag for (word, tag) in tagged_text)
#----------- extract words from tegged text----------
for worde, tag in tagged_text:
    Quran_words.append(worde)
i=0

while i<len(Quran_words):
  Quran_sents.append(Quran_words[i:i+9])
  i+=9
i=0
Quran_tagged_sents=[]
while i<len(tagged_text):
  Quran_tagged_sents.append(tagged_text[i:i+9])
  i+=9

#############################################
def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

grammar = "NP: {<DET>?<ADJ>*<DET>?<N>}"
cp = nltk.RegexpParser(grammar)
result = cp.parse(tagged_textt)
print result
print result.draw()

grammar = r"""
NP: {<DT|PP\$>?<JJ>*<NN>} # chunk determiner/possessive, adjectives and nouns
{<NNP>+} # chunk sequences of proper nouns
"""
cp = nltk.RegexpParser(grammar)

print cp.parse(tagged_textt)

grammar = "NP: {<NN><NN>}"
cp = nltk.RegexpParser(grammar)
print cp.parse(tagged_textt)

cp = nltk.RegexpParser("NP: {<DET><N>}")
brown = nltk.corpus.brown
for sent in Quran_tagged_sents:
    tree = cp.parse(sent)
    for subtree in tree.subtrees():
     #   if subtree.node == "NP":
            print  subtree
#########Chinking###############
grammar = r"""
NP:
{<.*>+} # Chunk everything
}<P|N>+{ # Chink sequences of VBD and IN
"""
cp = nltk.RegexpParser(grammar)


print cp.parse(tagged_textt)



class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents):
        train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)]
            for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data)

    def parse(self, sentence):
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                in zip(sentence, chunktags)]
        return nltk.chunk.conlltags2tree(conlltags)
from nltk.corpus import conll2000
###############NEED CHUNKE ARABIC CORPUS###############################
test_sents = conll2000.chunked_sents('test.txt', chunk_types=['NP'])###
train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])#
#######################################################################
unigram_chunker = UnigramChunker(train_sents)
print unigram_chunker.evaluate(test_sents)
grammar = r"""
NP: {<DET|ADJ|N.*>+} # Chunk sequences of DT, JJ, NN
PP: {<P><NP>} # Chunk prepositions followed by NP
VP: {<V.*><NP|PP|CLAUSE>+$} # Chunk verbs and their arguments
CLAUSE: {<PN><NP>} # Chunk NP, VP
"""
cp = nltk.RegexpParser(grammar)
print cp.parse(tagged_textt)
tree1 = nltk.Tree('NP', [unicode('عمر','utf-8')])
print tree1
tree2 = nltk.Tree('NP',[ unicode('ال','utf-8'),unicode('أرنب','utf-8') ])
tree3 = nltk.Tree('VP', [ unicode('يطارد','utf-8'), tree2])
tree4 = nltk.Tree('S', [tree1, tree3])
print tree4.leaves()
print tree4[1]
print tree4.draw()

























