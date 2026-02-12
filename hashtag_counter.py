tweets = [
    "Loving the new X update! #tech #update",
    "Had a great coffee today #coffee #morning",
    "X platform is amazing! #tech #social"
]

hashtags_count = {}

for tweet in tweets:
    words = tweet.split()
    for word in words:
        if word.startswith("#"):
            hashtags_count[word] = hashtags_count.get(word, 0) + 1

# Sort by hashtag count (descending)
sorted_hashtags = dict(sorted(hashtags_count.items(), key=lambda x: x[1], reverse=True))

print(sorted_hashtags)
