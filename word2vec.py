from gensim.test.utils import common_texts
from gensim.models import Word2Vec
from gensim.models import KeyedVectors

# Beispiel online enthält noch vektor size=100
# wurde hier aber als unerwartetes Argument geflaggt
# Versionsabweichung

model = Word2Vec(sentences=common_texts, window=5, min_count=1, workers=4)
model.save("word2vec.model")

model = Word2Vec.load("word2vec.model")
model.train([["hello", "world"]], total_examples=1, epochs=1)

vector = model.wv['computer']  # get numpy vector of a word

sims = model.wv.most_similar('computer', topn=10)  # get other similar words

# Store just the words + their trained embeddings.

word_vectors = model.wv

word_vectors.save("word2vec.wordvectors")
# Load back with memory-mapping = read-only, shared across processes.

wv = KeyedVectors.load("word2vec.wordvectors", mmap='r')

vector = wv['computer']  # Get numpy vector of a word
