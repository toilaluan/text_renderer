import random

random.seed(42)

# load and tokenize vietnamese words
with open("Viet74K.txt") as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
words = []
for line in lines:
    words.extend(line.split(" "))
words = list(set(words))
_words = []
for word in words:
    _word = ""
    for c in word:
        if c.isalpha() or c == "-":
            _word += c
    if _word == "":
        continue
    _words.append(_word)
words = _words


# randommize combine words

random_combine_words = []

for _ in range(50000):
    if random.random() < 0.2:
        random_combine_words.append(random.choice(words) + "-" + random.choice(words))
    else:
        random_combine_words.append(random.choice(words) + random.choice(words))

words = words + random_combine_words
words = list(set(words))

with open("/home/luantranthanh/hust/ocr/handwriting_recognition/dataset/train_gt.txt") as f:
    public_words = f.readlines()
public_words = [x.strip().replace(" ", "\t").split("\t")[1] for x in public_words]
words = words + public_words
words = list(set(words))

# CAPITAL all words
cap_words = [word.upper() for word in words]
words = words + cap_words

words = list(set(words))


with open("synthentic_words.txt", "w") as f:
    for word in words:
        f.write(word + "\n")

print("Total Synthentic Words", len(words))
print("Done!")
