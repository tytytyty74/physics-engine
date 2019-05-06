'''
********************************************************************************

    Function: title

    Definition:

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
'''
def title(s):
    l = 79-(len(s)+4)
    test = l%2
    l=l/2
    retval = "#"+("="*l)+("  "+s+"  ")+("="*l)
    if test == 1:
        retval +="="
    return retval

'''
********************************************************************************

    Function: comment

    Definition:

    Author: Tyler Silva

    Date: 4-29-2019

    History:

********************************************************************************
'''
def comment(filename):
    from datetime import datetime
    from os import chdir
    from copy import deepcopy
    now = datetime.now()
    comment = ["""'''
********************************************************************************

    Function: """, """

    Definition:

    Author: Jeremy Patrick

    Date: """, """

    History:

********************************************************************************\n""",
    """'''\n"""]
    comment2 = ["""'''
********************************************************************************

    Class: """, """

    Definition:

    Author: Jeremy Patrick

    Date: """, """

    History:

********************************************************************************\n""",
    """'''\n"""]
    f = open(filename)
    contents = f.readlines()
    f.close()
    finalContents = deepcopy(contents)
    add = 0
    for i in range(0, len(contents)):
        if contents[i].strip().startswith("def "):
            if i-1 < 0 or not contents[i-1].strip() == "'''":
                end = contents[i].strip().find("(")
                spaces = (len(contents[i])-len(contents[i].strip()))-1
                finalContents.insert(i+add, (" "*spaces)
                                     +comment[0]+contents[i].strip()[4:end]+
                                     comment[1]+(str(now.month)+"-"+str(now.day)
                                     +"-"+str(now.year))+comment[2]+(" "*spaces)+
                                     comment[3])
                add+=1
        elif contents[i].strip().startswith("class "):
            if i-1 < 0 or not contents[i-1].strip() == "'''":
                end = contents[i].strip().find("(")
                spaces = (len(contents[i])-len(contents[i].strip()))-1
                finalContents.insert(i+add, (" "*spaces)
                                     +comment2[0]+contents[i].strip()[6:end]+
                                     comment2[1]+(str(now.month)+"-"+str(now.day)
                                     +"-"+str(now.year))+comment2[2]+(" "*spaces)+
                                     comment2[3])
                add+=1
            
    f = open(filename, "w")
    f.write("".join(finalContents))
    f.close()

print ("which file to comment")
try:
    x = raw_input("> ")
except:
    x = input("> ")
try:
    f=open(x)
    f.close()
except:
    print ("file doesn't exist")
