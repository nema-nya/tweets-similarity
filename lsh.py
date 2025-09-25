from collections import defaultdict
from minhash import MinHash

class LSH:

    def __init__(self, minhash, num_bands=16, rows_per_band=8):
        self.minhash = minhash
        assert minhash.num_hashes == num_bands * rows_per_band
        self.num_bands = num_bands
        self.rows_per_band = rows_per_band
        self.buckets = defaultdict(list)
        self.signatures = {}

    def add_signature(self, tweet_id, signature):
        self.signatures[tweet_id] = signature

        for band in range(self.num_bands):
            start = band * self.rows_per_band
            end = start + self.rows_per_band
            band_signature = tuple(signature[start:end])
            band_hash = hash(band_signature)
            self.buckets[band_hash].append(tweet_id)

    def find_candidates(self, signature):
        candidates = set()

        for band in range(self.num_bands):
            start = band * self.rows_per_band
            end = start + self.rows_per_band
            band_signature = tuple(signature[start:end])
            band_hash = hash(band_signature)

            if band_hash in self.buckets:
                candidates.update(self.buckets[band_hash])
        
        return candidates

    def search_similar(self, signature, min_similarity):
        candidates = self.find_candidates(signature)
        results = []

        for c_id in candidates:
            candidate_sig = self.signatures[c_id]
            sim = self.minhash.similarity(signature, candidate_sig)

            if sim >= min_similarity:
                results.append((c_id, sim))
        
        results = sorted(results, key=lambda x: x[1], reverse=True)
        return results

if __name__ == "__main__":
    text1 = "i am really similar to two"
    text2 = "i am really similar to one"
    text3 = "i am random noise"
    minhash = MinHash()
    sig1 = minhash.compute_signature(text1)
    sig2 = minhash.compute_signature(text2)
    sig3 = minhash.compute_signature(text3)
    lsh = LSH(minhash)
    lsh.add_signature(0, sig1)
    lsh.add_signature(1, sig2)
    lsh.add_signature(2, sig3)
    print(lsh.find_candidates(sig1))
    print(lsh.find_candidates(sig2))
    print(lsh.find_candidates(sig3))
    print(lsh.search_similar(sig1, 0.5))
    print(lsh.search_similar(sig2, 0.5))
    print(lsh.search_similar(sig3, 0.5))