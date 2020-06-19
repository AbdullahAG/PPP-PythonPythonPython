#main.py
import sys
import random
import keyword
import string

list_str=list()
keywords = keyword.kwlist+['abs', 'dict', 'help', 'min', 'setattr', 'all', 'dir', 'hex', 'next', 'slice', 'any', 'divmod', 'id', 'object', 'sorted', 'ascii', 'enumerate', 'input', 'oct', 'staticmethod', 'bin', 'eval', 'int', 'open', 'str', 'bool', 'exec', 'isinstance', 'ord', 'sum', 'bytearray', 'filter', 'issubclass', 'pow', 'super', 'bytes', 'float', 'iter', 'print', 'tuple', 'callable', 'format', 'len', 'property', 'type', 'chr', 'frozenset', 'list', 'range', 'vars', 'classmethod', 'getattr', 'locals', 'repr', 'zip', 'compile', 'globals', 'map', 'reversed', '__import__', 'complex', 'hasattr', 'max', 'round', 'delattr', 'hash', 'memoryview', 'set']

def gen_random_str(num):
    while (True):
        ran_str = ''.join(random.choice(string.ascii_letters) for i in range(random.randint(1,num)))
        if ran_str not in list_str and ran_str not in keywords:
            list_str.append(ran_str)
            return ran_str
        
def random_oper(t,n,f = open("code_dead.txt", "w")):
    keep_op = False
    #print("open")
    if f.closed:
        print("closed")
        keep_op = True
        f = open("code_dead.txt", "a")
        
    for i in range(n):
        if i%6==0:
            f.write(t+"for "+gen_random_str(5)+" in range("+str(random.randint(1,150))+"):\n"+t+"\t"+gen_random_str(10)+" = "+str(random.randint(1,150))+"\n")
        elif i%5==0:
            f.write(t+"if '"+gen_random_str(5)+"' == '"+gen_random_str(5)+"':\n"+t+"\t"+gen_random_str(5)+"='"+gen_random_str(5)+"'\n")
            f.write(t+"elif '"+gen_random_str(5)+"' == '"+gen_random_str(5)+"':\n"+t+"\t"+gen_random_str(5)+"='"+gen_random_str(5)+"'\n")
            f.write(t+"else:\n"+t+"\t"+gen_random_str(5)+"='"+gen_random_str(5)+"'\n")
        elif i%2==1:
            f.write(t+"while(True):\n"+t+"\timport time;time.sleep(3)\n"+t+"\tbreak\n")
    if keep_op:          
        f.close()
        
def random_var(t, n,f = open("code_dead.txt", "w")):
    keep_op = False
    if f.closed:
        print("closed")
        keep_op = True
        f = open("code_dead.txt", "a")
        
    for i in range(n):
        if i%6==0:
            s = random.randint(0,1)
            if s:
                f.write(t+gen_random_str(3)+' = '+'True\n')
            else:
                f.write(t+gen_random_str(3)+' = '+'False\n')
        elif i%2==0:
            f.write(t+gen_random_str(3)+' = "'+gen_random_str(100)+'"\n')
        elif i%5==0:
            f.write(t+gen_random_str(3)+' = '+str(random.uniform(0.0,100000000.0))+"\n")
        elif i%2==1:
            f.write(t+gen_random_str(3)+' = '+str(random.randint(1,100000000))+"\n")

    if keep_op:          
        f.close()
        
def random_fun(t, n,f = open("code_dead.txt", "w")):
    keep_op = False
    if f.closed:
        print("closed")
        keep_op = True
        f = open("code_dead.txt", "a")
    #write many functions
    for i in range(n):
        num_par = random.randint(0,3)
        par =""
        for x in range(num_par):
            if x > 1:
                par += ', '
            par += gen_random_str(3)
                    
        f.write(t+'def '+gen_random_str(10)+' ('+par+'):\n')
        #write many variables within functions
        while(True):
            random_var(t+"\t",random.randint(1,6),f)
            if random.randint(0,1):
                break
                    
        while(True):
            random_oper(t+"\t",random.randint(1,6),f)
            if random.randint(0,1):
                break          
    if keep_op:          
        f.close()        
        
def random_clss(t, n):
    with open("code_dead.txt", "w") as f:
        #write many functions
        for i in range(n):
            num_par = random.randint(0,3)
            par =""
            for x in range(num_par):
                if x > 1:
                    par += ', '
                par += gen_random_str(3)
                        
            f.write('class '+gen_random_str(10)+':\n')
            if par != "":
                f.write('\tdef __init__('+par+'):\n')
                for i in par.split(", "):
                    if random.randint(0,1): 
                        f.write('\t\t'+i+'= "'+gen_random_str(100)+'"\n')
                    else:
                        f.write('\t\t'+i+'='+str(random.randint(1,1000))+'\n')
            #write many variables within functions
            while(True):
                random_var(t+"\t",random.randint(1,6),f)
                if random.randint(0,1):
                    break
                        
            while(True):
                random_fun(t+"\t",random.randint(1,6),f)
                if random.randint(0,1):
                    break
