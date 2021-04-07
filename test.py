a=[45,67,43,4,5]
sorted_A=[]
while a:
    mina=a[0]
    for y in a:
        if y < mina:
            mina = y
    sorted_A.append(mina)
    a.remove(mina)

print(sorted_A)
