import colour 
string="DarKTurquoise/(255,255,255)/(255,255,255)"
string=string.replace(" ", "")
string=string.split("/")
#print(string)
if len(string)>3:
    print("too many arguements")
    string=["green","green","black"]
elif len(string)<3:
    print("too less arguements")
    string=["green","green","black"]
else:    
    for clr in string:
        if clr=="":
            if string.index(clr) == 2:
                print("2")
                string[string.index(clr)]="black"
            elif string.index(clr) == 1 or string.index(clr) == 0:
                string[string.index(clr)]="green"
        else:
            try:
                colour.Color(str(clr))
            except:
                if string.index(clr) == 2:
                    print("2")
                    string[string.index(clr)]="black"
                elif string.index(clr) == 1 or string.index(clr) == 0:
                    string[string.index(clr)]="green"
                    #print(f"wrong {clr}")
                #break
print(string)
