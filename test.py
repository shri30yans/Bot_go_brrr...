import os, random
c=random.choice(os.listdir("D:\\Py Programs\\Discord Python Programs\\Server Bot\\utils")) #change dir name to whatever
print(os.path.dirname(os.path.abspath(c)))