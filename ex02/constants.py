import random

random.seed(42)

# Function to calculate the probability of finding a pair of documents in the same bucket given the similarity between them
def calculate_findings_percentage(similarity: float, b: int, r: int):
    # 1 − (1 − s**r )**b - Probability that at least 1 band identical
    return 1 - (1 - similarity**r)**b

# Function to find the best combination of b and r that finds at least max_findings_percentage of pairs with max_similarity and less than min_findings_percentage of pairs with min_similarity
def b_and_r_tunning(bs: list, rs: list, max_similarity: float, min_similarity: float, max_probability: float, min_probability: float):
    
    best_params = None # (b, r)
    
    for b in bs:
        for r in rs:
            max_p = calculate_findings_percentage(max_similarity, b, r)
            min_p = calculate_findings_percentage(min_similarity, b, r)
            
            if max_p >= max_probability and min_p <= min_probability:
                if best_params is None:
                    best_params = (b, r)
                elif b*r < best_params[0]*best_params[1]:
                        best_params = (b, r)
                elif b*r == best_params[0]*best_params[1] and b < best_params[0]:
                    best_params = (b, r)
                        
    return best_params

# Input file
INPUT_FILE = "data/covid_news_full.json.bz2"

# Output folder
OUTPUT_FOLDER = "output"

# shingle size - k
SHINGLE_SIZE = 9

BEST_PARAMS = b_and_r_tunning(list(range(1, 20)), list(range(1, 20)), 0.85, 0.60, 0.90, 0.05)

# Number of bands - b
N_BANDS = BEST_PARAMS[0]    # 13

# Number of rows per band - r
N_ROWS = BEST_PARAMS[1]    # 11

# Number of hash functions - b*r
N_HASH = N_BANDS * N_ROWS

# Bucket size
BUCKET_SIZE = 100000

# Get number of shingles (N)
N_SHINGLES = 4294967296 # 2^32

# Prime Value > N_SHINGLES, the number of shingles used in full dataset is approximately 500000
PRIME = 4294967311  #next_prime(N_SHINGLES)

# Random hash functions values (Use high value to avoid repetition)
AB = [(random.randint(1, PRIME), random.randint(0, PRIME)) for _ in range(N_HASH)]

# Function to plot the Probability of sharing a bucket given b and r and the Similarity
def plot_findings_percentage(b: int, r:int, max_similarity: float, min_similarity: float, max_findings_percentage: float, min_findings_percentage: float):
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.size': 10})
    
    x = [i for i in range(1, 100)]
    y = [calculate_findings_percentage(i/100, b, r) for i in x]
    plt.plot(x, y)
    # add two horizontal lines for max and min similarity
    plt.axhline(y=max_findings_percentage, color='r', linestyle=':', label=f"p={max_findings_percentage*100}% sharing a bucket")
    plt.axhline(y=min_findings_percentage, color='g', linestyle=':', label=f"p={min_findings_percentage*100}% sharing a bucket")
    
    # add two vertical lines for max and min findings percentage
    plt.axvline(x=max_similarity*100, color='r', linestyle='--', label=f"{max_similarity*100}% similarity")
    plt.axvline(x=min_similarity*100, color='g', linestyle='--', label=f"{min_similarity*100}% similarity")
    
    plt.legend()
    
    plt.xlabel("Similarity")
    plt.ylabel("Probability of sharing a bucket")
    plt.title(f"Expected Locality Sensitive Hashing for b={b}, r={r}")
    plt.savefig(f"best_b_and_r_expected.png", dpi=700)

if __name__ == "__main__":
    # Select a combination that finds as candidates at least 90% of pairs with 85% similarity and less than 5% of pairs with 60% similarity.
    # Find the combination of b and r that checks the previous condition with the minimum number of hash functions (More efficient, even if it is not the most accurate)
    best_params = b_and_r_tunning(list(range(1, 100)), list(range(1, 100)), 0.85, 0.60, 0.90, 0.05)
    if best_params is not None:
        print(f"Best parameters: b={best_params[0]}, r={best_params[1]}")
    else:
        print("No parameters found")
    
    plot_findings_percentage(best_params[0], best_params[1], 0.85, 0.60, 0.90, 0.05)
    
