import random
import re

class MinHash:

    def __init__(self, num_hashes=128, shingle_size=2):
        self.num_hashes = num_hashes
        self.shingle_size = shingle_size
        self.prime = 4294967311
        self.hash_functions = self.generate_hash_functions()

    def generate_hash_functions(self):
        hash_functions = []
        for _ in range(self.num_hashes):
            a = random.randint(1, self.prime - 1)
            b = random.randint(0, self.prime - 1)
            hash_functions.append((a, b))
        return hash_functions

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r"http\S+|www\S+|https\S+", "", text)
        text = re.sub(r"@\w+|#\w+", "", text)
        text = re.sub(r"\s+", " ", text)
        text = text.strip()
        return text

    def get_shingles(self, text):
        text = self.clean_text(text)

        if len(text) < self.shingle_size:
            return {text}

        shingles = set()
        for i in range(len(text) - self.shingle_size + 1):
            shingles.add(text[i:i + self.shingle_size])
        
        return shingles

    def apply_hash(self, a, b, shingle):
        shingle_hash = hash(shingle) % self.prime
        return (a * shingle_hash + b) % self.prime

    def compute_signature(self, text):
        shingles = self.get_shingles(text)
        if not shingles:
            return [0] * self.num_hashes

        signatures = []
        for a,b in self.hash_functions:
            minhash = min(self.apply_hash(a, b, shingle) for shingle in shingles)
            signatures.append(minhash)
        return signatures

    def similarity(self, sig1, sig2):
        return sum(1 for a,b in zip(sig1, sig2) if a == b) / len(sig1)

if __name__ == "__main__":
    text1 = "i am really similar to two"
    text2 = "i am really similar to one"
    text3 = "i am random noise"
    minhash = MinHash()
    sig1 = minhash.compute_signature(text1)
    sig2 = minhash.compute_signature(text2)
    sig3 = minhash.compute_signature(text3)
    print(sig1, sig2, sig3)
    print(minhash.similarity(sig1, sig2))
    print(minhash.similarity(sig1, sig3))
    print(minhash.similarity(sig2, sig3))