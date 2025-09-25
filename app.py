from flask import Flask, redirect, url_for, render_template, jsonify, request
import pandas as pd
from minhash import MinHash
from lsh import LSH
import os

app = Flask(__name__)

DATA_PATH = "tweets.csv"

minhash = None
lsh = None
df = pd.read_csv(DATA_PATH, encoding="latin", header=None)
df.columns = ["sentiment", "id", "date", "query", "user_id", "text"]
df = df.drop(["sentiment", "id", "date", "query", "user_id"], axis=1)
data = [tweet for tweet in df["text"]]

@app.route("/")
def index():
    global minhash, lsh
    if minhash == None or lsh == None:
        return redirect(url_for("setup"))
    return render_template("index.html")

@app.route("/setup")
def setup():
    global minhash, lsh
    if minhash != None and lsh != None:
        return redirect(url_for("index"))
    global data

    minhash = MinHash()
    lsh = LSH(minhash)
    print("setup starting")
    for i, tweet in enumerate(data):
        sig = minhash.compute_signature(tweet)
        lsh.add_signature(i, sig)
    print("setup complete")

    return redirect(url_for("index"))

@app.route("/api/search", methods=["POST"])
def search_tweets():
    global minhash, lsh, data

    if minhash is None or lsh is None or data is None:
        return jsonify({"error": "Run setup first"}), 500

    request_data = request.get_json()
    query = request_data.get("query", "").strip()
    if not query:
        return jsonify({"error" : "...Well there is nothing to query"}), 400
    min_similarity = float(request_data.get("min_similarity", 0.7))
    max_results = int(request_data.get("max_results", 10))
    formatted_results = []
    try:
        query_sig = minhash.compute_signature(query)
        results = lsh.search_similar( query_sig, min_similarity)
        for tweet_index, similarity in results[:max_results]:
            if tweet_index < len(data):
                formatted_results.append({
                    "tweet": data[tweet_index],
                    "similarity": round(similarity, 4),
                    "index": tweet_index
                })

        return jsonify({
            "query": query,
            "results": formatted_results,
            "total_found": len(results),
            "showing": len(formatted_results)
        })

    except Exception as e:
        return jsonify({"error" : f"{str(e)}"}), 500

