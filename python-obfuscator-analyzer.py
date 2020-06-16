import ast
import astor
import keyword
from radon.raw import analyze
import radon.complexity
import radon.metrics
import subprocess
import sys
import os
import gen_dead_code as gen


#main.py


class obf_name(ast.NodeTransformer):
    def __init__(self, tree):
        self.tree = tree

    def run(self):
        for n_stop in ast.walk(self.tree):

            if isinstance(n_stop, ast.ClassDef):
                print(ast.Name, n_stop.name)
                
            if isinstance(n_stop, ast.FunctionDef):
                print(ast.Name, n_stop.name)

            if isinstance(n_stop, ast.ImportFrom):
                print(ast.Name, n_stop)
                    
            if isinstance(n_stop, ast.Import):
                #if n_stop.names[-1].asname is not None:
                print(ast.Name, n_stop.names[-1].name)
                    
            if isinstance(n_stop, ast.Name):
                print(ast.Name, n_stop.id)
                
    def change(self):
        keywords = keyword.kwlist+['abs', 'dict', 'help', 'min', 'setattr', 'all', 'dir', 'hex', 'next', 'slice', 'any', 'divmod', 'id', 'object', 'sorted', 'ascii', 'enumerate', 'input', 'oct', 'staticmethod', 'bin', 'eval', 'int', 'open', 'str', 'bool', 'exec', 'isinstance', 'ord', 'sum', 'bytearray', 'filter', 'issubclass', 'pow', 'super', 'bytes', 'float', 'iter', 'print', 'tuple', 'callable', 'format', 'len', 'property', 'type', 'chr', 'frozenset', 'list', 'range', 'vars', 'classmethod', 'getattr', 'locals', 'repr', 'zip', 'compile', 'globals', 'map', 'reversed', '__import__', 'complex', 'hasattr', 'max', 'round', 'delattr', 'hash', 'memoryview', 'set']
        var_names= dict()
        count = 1
        obf_let = "insight"
        for n_stop in ast.walk(self.tree):

            if isinstance(n_stop, ast.ClassDef):
                if n_stop.name not in var_names:
                    var_names[n_stop.name] = obf_let*count
                    count=count+1
                n_stop.name = var_names[n_stop.name]
                #print(ast.Name, n_stop.name)
                
            if isinstance(n_stop, ast.arguments):
                for arg in n_stop.args:
                    if arg.arg not in var_names:
                        var_names[arg.arg] = obf_let*count
                        count=count+1
                    arg.arg = var_names[arg.arg]
                
            if isinstance(n_stop, ast.FunctionDef):                        
                if n_stop.name not in var_names:
                    var_names[n_stop.name] = obf_let*count
                    count=count+1
                n_stop.name = var_names[n_stop.name]
                #print(ast.Name, n_stop.name)

            if isinstance(n_stop, ast.ImportFrom):
                if n_stop.names[-1].asname not in var_names:
                    var_names[n_stop.names[-1].asname] = obf_let*count
                    count=count+1
                n_stop.names[-1].asname = var_names[n_stop.names[-1].asname]
                #print(ast.Name, n_stop.names[-1].asname)
                    
            if isinstance(n_stop, ast.Import):
                keywords.append(n_stop.names[-1].name)
                if n_stop.names[-1].asname is not None:
                    if n_stop.names[-1].asname not in var_names:
                        var_names[n_stop.names[-1].asname] = obf_let*count
                        count=count+1
                    n_stop.names[-1].asname = var_names[n_stop.names[-1].asname]
                    #print(ast.Name, n_stop.names[-1].asname)
                    
            if isinstance(n_stop, ast.Name):
                if n_stop.id not in keywords:
                    if n_stop.id not in var_names:
                        var_names[n_stop.id] = obf_let*count
                        count=count+1
                    n_stop.id = var_names[n_stop.id]
                #print(ast.Name, n_stop.id)
            '''       
            if isinstance(n_stop, ast.Num):
                #print(n_stop.n)
                if isinstance(n_stop.n, int):
                    number_n="len("
                    #number_n=""
                    #while (True):
                    #    if i == n_stop.n:
                    #        number_n +=""
                    #        break
                    
                    for i in range(10):
                        number_n += "ii"
                    n_stop.n=number_n+")" 
                elif isinstance(n_stop.n, float):
                    n_stop.n = n_stop.n.hex()
                #print(n_stop.n)
                '''
            if isinstance(n_stop, ast.Str):
                r=""
                for i in n_stop.s[:]:
                    r += 'chr('+str(ord(i))+')+'
                n_stop.s=r[:-1]
    '''            
    def getAST(self):
        ast.NodeVisitor.visit(self)
        return self.tree
   ''' 
'''def obs_int(file_obf):
    new_file=""
    for i in file_obf.split("\n"):
        line_new=""
        for character in file_obf.split(" "):
            if isinstance(character, int):
                character = character.hex()
            elif isinstance(character, float):
                character = hex(character)
            line_new+=character+" "
        new_file+=line_new+"\n"
    return new_file
'''
def obs_string(file_obf):
    new_file=""
    for i in file_obf.split("\n"):
        if '"' in i:
            #print(i)
            x=i.split('"')
            x=''.join(x)
            i=x
            #print(i)
        elif "'" in i:
            #print(i)
            x=i.split("'")
            x="".join(x)
            i=x
            #print(i)
        new_file+="\n"+i
    return new_file

def add_deadcode(file_dead):
    new_file=""
    for i in file_dead.split("\n"):
        if ' def ' in i:
            #print(i)
            x=i.split('"')
            x=''.join(x)
            i=x
            #print(i)
        elif "'" in i:
            #print(i)
            x=i.split("'")
            x="".join(x)
            i=x
            #print(i)
        new_file+="\n"+i
    return new_file


#CL-start
if len(sys.argv) > 4:
    print('You have specified too many arguments')
    sys.exit()

if len(sys.argv) < 1:
    print('You need to specify the path to be obfuscated')
    sys.exit()


if len(sys.argv) > 2:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print('''By default the tool will result in:
                    changing variables names
                    , adding dead code
                    , and changing the logic
                    To remove any add the following argument, -v or --variable, -d or --dead, or -l or --logic''')
            sys.exit()
    else:
        for arg in sys.argv:
                if sys.argv[1] == arg or sys.argv[0] == arg:
                    continue
                elif arg == "-h" or arg == "--high":
                    high_obf = True
                    mid_obf = False
                    low_obf = False
                elif arg == "-m" or arg == "--midum":
                    high_obf = False
                    mid_obf = True
                    low_obf = False
                elif arg == "-l" or arg == "--low":
                    high_obf = False
                    mid_obf = False
                    low_obf = True
                else:
                    print(arg)
                    print('''The opetion is not specified please read the follwing:
                            By default the tool will result in:
                    changing variables names
                    , adding dead code
                    , and changing the logic
                    To remove any add the following argument, -h or --high, -m or --midum, or -l or --low''')
                    sys.exit()
                    

input_path = sys.argv[1]    
if not os.path.isfile(input_path) or not input_path[-2:] == "py":
    print("The path specified does not exist or not the same type 'py'")
    sys.exit()
#CL-end
        
#testContent = open(input_path)
'''
result_1 = subprocess.run(["python -m flake8 --select=DUO", testContent], stdout=subprocess.PIPE)
print(result_1)

print("-------analyse--------")
b = analyze(testContent)
c=radon.complexity.cc_visit(testContent)
v=radon.complexity.sorted_results(c)
print(b)
print("-------score compute Cyclomatic Complexity--------")
[print("\n",i.letter, i.name, radon.complexity.cc_rank(i.complexity)) for i in v] 
print("---------------")
print("h visit",radon.metrics.h_visit(testContent))
print("---------------")

print("mi visit",radon.metrics.mi_rank(radon.metrics.mi_visit(testContent, True)))
print("---------------")
print("mi parameters", radon.metrics.mi_parameters(testContent, True))
print("---------------")
'''

if high_obf:
    v = 3#class, function or variables
    n = 3#number of random
if mid_obf:
    v = 2#class, function or variables
    n = 3#number of random
if low_obf:
    v = 1#class, function or variables
    n = 3#number of random

t="" 
if v == 1:
    gen.random_var(t,n)
elif v ==2:
    gen.random_fun(t,n)
elif v ==3:
    gen.random_clss(t,n)

  
input_path_2 = input_path
input_path = input_path[:-3]+"_new.py"
end_loop=True
with open(input_path_2,"r") as input:
    with open(input_path,"w+") as testContent:
        for line in input:
            if end_loop:
                if 'import' in line or 'Import' in line:
                    testContent.write(line)
                else:
                    testContent.write("\n")
                    with open(r'code_dead.txt', "r") as output:
                        for line_2 in output:
                            testContent.write(line_2)
                    end_loop=False
                    testContent.write("\n"+line)
            else:
                testContent.write(line)


with open(input_path, "r") as s:
    t = ast.parse(s.read())
    obf = obf_name(t)
        #obf.run()
    obf.change()
        #print(obf.run())
    root=astor.code_gen.to_source(obf.visit(t))
        #print(root)
        #root = obs_int(root)
    root = obs_string(root)
        
        #print(root)
    


'''
print("-------analyse--------")
b = analyze(root)
c=radon.complexity.cc_visit(root)
v=radon.complexity.sorted_results(c)
print(b)
print("-------score compute Cyclomatic Complexity--------")
[print("\n",i.letter, i.name, radon.complexity.cc_rank(i.complexity)) for i in v] 
print("---------------")
print("h visit",radon.metrics.h_visit(testContent))
print("---------------")

print("mi visit",radon.metrics.mi_rank(radon.metrics.mi_visit(testContent, True)))
print("---------------")
print("mi parameters", radon.metrics.mi_parameters(testContent, True))
print("---------------")
'''

with open(input_path[:-3]+"_obf.py", 'w') as f:
    f.write(root)

print("------------------------------result-----------------------------")
exec(root)
#obf.getAST()))
#print(ast.dump(t))


