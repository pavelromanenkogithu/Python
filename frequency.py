import string
from collections import Counter

text = input("Enter text: ")
text = text.translate(str.maketrans('', '', string.punctuation))
words = text.lower().split()
counter = Counter(words)

for word, count in counter.most_common(5):
    print(word, count)
