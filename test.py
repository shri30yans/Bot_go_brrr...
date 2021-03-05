import random 
word="Roses are red"
shuffled_words = ""
word=word.split(" ")
for x in word:
    x=list(x)
    random.shuffle(x)
    shuffled_words = shuffled_words + "".join(x) + " "  
#random.shuffle(word)
#word = "".join(word)
print(str(shuffled_words))