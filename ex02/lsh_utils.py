import string
from itertools import combinations
import mmh3
from heapq import heapify, heappush, heappop 


from constants import *

# regex = re.compile(r'\W+', re.UNICODE)
translator = str.maketrans('', '', string.punctuation + '«»—ºª')

# Convert json document to tuple and convert text to shingles
def shingles(document):
    # Remove punctuation leaving spaces (Later test if also removing spaces is better)
    document['text'] = document['text'].translate(translator).lower()
    
    shingles = set()
    for i in range(len(document['text']) - SHINGLE_SIZE + 1):
        shingles.add(mmh3.hash(document['text'][i:i+SHINGLE_SIZE]))
    return (document['tweet_id'], shingles)

# Universal hash function
def universal_hash(x: int, a: int, b: int, p: int, N: int): # a - random number, x - shingle, b - random number, p - prime number, N - number of buckets
    return ((a * x + b) % p) % N

# Generate the signature for a document
def min_hash(document):
    # for each hash function, calculate the hash of each shingle, and keep the minimum
    min_hashes = []
    heap = [] 
    heapify(heap)
    for _, (a, b) in enumerate(AB):
        # clear heap
        heap = [float('inf')]
        for shingle in document[1]:
            hash_value = universal_hash(shingle, a, b, PRIME, N_SHINGLES)
            heappush(heap, hash_value)
        min_hashes.append(heappop(heap))
    
    return (document[0], min_hashes)

# Convert signatures to buckets
def signatures_to_buckets(document):
    buckets = []
    for i in range(0, N_HASH, N_ROWS):
        buckets.append(mmh3.hash(",".join(map(str,document[1][i:i+N_ROWS])))%BUCKET_SIZE)
    return (document[0], buckets)
    
# Generate the all the candidate pairs
def get_candidates(document):
    return set(combinations(document[1], 2))

# Generate the candidate pairs iterator
def get_candidates_iterator(documents):
    return combinations(documents, 2)

def jaccard_similarity(s1: set, s2: set):
    union_length = len(s1.union(s2))
    return len(s1.intersection(s2)) / union_length if union_length > 0 else 1

def list_jaccard_similarity(l1: list, l2: list):
    l1 = set(l1)
    l2 = set(l2)
    return len(l1.intersection(l2)) / len(l1.union(l2))

