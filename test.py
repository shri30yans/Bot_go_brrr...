import random 
word="Roses are red"
new=[]
word=word.split(" ")
for x in word:
    x=list(x)
    random.shuffle(x)
    new.append("".join(x))
#random.shuffle(word)
#word = "".join(word)
print(str(new))