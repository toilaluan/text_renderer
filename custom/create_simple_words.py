internet_word_path = "Viet74K.txt"
all_vietnamese_words = "all-vietnamese-syllables.txt"
train_annotation_file = "../../train_gt.txt"

import random

random.seed(42)

with open(all_vietnamese_words) as f:
    lines = f.readlines()
    lines = [line.strip() for line in lines]
    vietnamese_words = lines

# load and tokenize vietnamese words
with open(internet_word_path) as f:
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
viet74k_words = _words
# load train set words
with open(train_annotation_file) as f:
    public_words = f.readlines()
public_words = [x.strip().replace(" ", "\t").split("\t")[1] for x in public_words]


words = viet74k_words + public_words + vietnamese_words
words = [word.lower() for word in words]
lower_words = list(set(words))
print("Total words", len(lower_words))

# upper all words
cap_words = [word.upper() for word in lower_words]

# upper only first character
cap_first_words = [word[0].upper() + word[1:] for word in lower_words]
# upper after '-' character
cap_after_dash_words = []
for word in lower_words:
    if "-" in word:
        _word = ""
        for i, c in enumerate(word):
            if i == 0:
                _word += c.upper()
                continue
            if word[i - 1] == "-":
                _word += c.upper()
            else:
                _word += c
        cap_after_dash_words.append(_word)

# # random upper char in word with probability 0.2
# random_upper_words = []
# for word in lower_words:
#     _word = ""
#     for c in word:
#         if random.random() < 0.2:
#             _word += c.upper()
#         else:
#             _word += c
#     random_upper_words.append(_word)

total_words = (
    lower_words
    + cap_words
    + cap_first_words
    + cap_after_dash_words
    # + random_upper_words
)
total_words = list(set(total_words))
print("Total words", len(total_words))
print(cap_after_dash_words[:10])
print(cap_first_words[:10])
print(cap_words[:10])
print(lower_words[:10])
# print(random_upper_words[:10])

with open("synthentic_words.txt", "w") as f:
    for word in total_words:
        f.write(word + "\n")
