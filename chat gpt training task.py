count = 0
with open("training.txt") as f:
    for line in f:
        count += 1
print(count)

res = 0
with open("hello_words.txt") as f:
    for line in f:
        words = line.split()
        count += len(words)

result = ""
with open("words.txt", "r") as f:
    for line in f:
        word = line.strip()
        if len(word) > len(result):
            word = result
print(result)


result_1 = 0
with open("numbers.txt") as f:
    for line in f:
        result_1 += int(line)


maximum = float("-inf")
with open("numbers.txt", "r") as f:
    for line in f:
        numb = int(line)
        if numb > maximum:
            maximum = numb

countss = {}
with open("text.txt") as f:
    for line in f:
        word = line.strip()
        for word in words:
            if word not in countss:
                countss[word] = 0
            else:
                countss[word] += 1


import json
with open("words.json") as f:
    users = json.load(f)

for user in users:
    print(user["name"])


import json
with open("text.json") as f:
    users = json.load(f)
for user in users:
    if user["age"] > 21:
        print(user["name"])


resalt = {}
with open("text.txt") as f:
    for word in f:
        laters = word.strip().split()
        for later in laters:
            if later not in resalt:
                resalt[later] = 1
            else:
                resalt[later] += 1
