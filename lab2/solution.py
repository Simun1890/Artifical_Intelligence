import sys

def load_clauses(file_path):
    clauses = []
    with open(file_path, 'r') as file:
        for line in file:
            # Ignore comments
            if line.startswith('#'):
                continue
            # Split line into literals
            literals = line.strip().lower().split(' v ')
            # Add processed literals to clauses
            set1 = set()
            for literal in literals:
                set1.add(literal)
            clauses.append(set1)
    target = clauses[-1]
    SOS = []
    del clauses[-1]
    pom1 = set()
    for t in target:
        if(t.startswith('~')):
            pom1.add(t[1:])
        else:
            pom1.add(str('~'+t))
    SOS.append(pom1)
    return clauses,SOS,target

def load_commands(file_path):
    commands = []
    with open(file_path, 'r') as file:
        for line in file:
            # Ukloni bijele znakove s početka i kraja retka
            line = line.strip()
            # Podijeli redak na klauzulu i identifikator namjere
            clause, intention = line[:-2], line[-1]
            commands.append((clause, intention))
    return commands

def user_commands(commands,clauses,target):
    clauses.append(target)
    for c in commands:
        print("\nUser's  command: "," ".join(c),)
        if c[-1]=='?':
            target = c[0].lower().split(" v ")
            SOS = []
            pom1 = set()
            for t in target:
                if(t.startswith('~')):
                    pom1.add(t[1:])
                else:
                    pom1.add(str('~'+t))
            SOS.append(pom1)
            resolution_result = plResolution(clauses,SOS)
            target1=" v ".join(target)
            print_clauses(clauses)            
            if resolution_result:
                print(f"[CONCLUSION]: {target1} is true")
            else:
                print(f"[CONCLUSION]: {target1} is unknown")
        if c[-1] == '+':
            target = c[0].lower().split(" v ")
            if(set(target) not in clauses):
                clauses.append(set(target))
        if c[-1] == '-':
            target = c[0].lower().split(" v ")
            if(set(target) in clauses):
                clauses.remove(set(target))
            
        
    
    

                
def plResolution(clauses,SOS):
    
    while True:
        for c1 in SOS:
            new =[]
            pom1 = len(SOS)
            for c2 in clauses:
                #print("C1",c1,"C2",c2)
                if c2!= c1 :
                    bol= False
                    resolvents = plResolve(c1,c2)
                    if resolvents=="NIL":
                        print(" v ".join(c1)," , "," v ".join(c2))
                        return True
                    broj=True
                    if len(resolvents)!=0:
                        for clause in clauses+SOS:
                            if clause <= resolvents :
                                broj= False
##                            if resolvents <= clause:
##                                if clause in clauses:
##                                    print("\t\tMičem clause",clause,resolvents)
##                                    clauses.remove(clause)
##                                else:
##                                    print("\t\tMičem clause",clause,resolvents)
##                                    SOS.remove(clause)
##                                broj=True
##                                break
                    if(len(resolvents) != 0 and broj):
                        bol= True
                        new.append(resolvents)
                if(len(new)!=0 and bol):
                    print(" v ".join(new[-1])," => "," v ".join(c1)," , "," v ".join(c2))
                    #print("novi",new)
            for n in new:
                if n not in SOS:
                    SOS.append(n)
            #print("sos",SOS)
        if len(SOS)==pom1:
            return False
def tautologija(resolvents):
    for l1 in resolvents:
        for l2 in resolvents:
            if l1.startswith('~') and l1[1:]==l2:
                return False
            if l2.startswith('~') and l2[1:]==l1:
                return False
    return True

    
def plResolve(c1, c2):
    resolvents = set()
    for literal1 in c1:
        for literal2 in c2:
            if literal1.startswith('~') and literal1[1:]==literal2:
                new_clause = c1.union(c2) - {literal1, literal2}
                if tautologija(new_clause): 
                    resolvents.update(tuple(new_clause))
                if(resolvents==set()):
                    return "NIL"
                return resolvents
            if literal2.startswith('~') and literal2[1:]==literal1:
                new_clause = c1.union(c2) - {literal1, literal2}
                resolvents.update(tuple(new_clause))
                if(resolvents==set()):
                    return "NIL"
                return resolvents
    return resolvents
            

def print_clauses(clauses):
    for idx, clause in enumerate(clauses, start=1):
        clause_str = ''
        for literal in clause:
            clause_str += f' {literal}'
            clause_str += " v"
        # Remove the last " v "
        clause_str = clause_str[:-2]
        print(f"{idx}.{clause_str}")
    print("=" * 15)

if __name__ == "__main__":
    if sys.argv[1]=="resolution":
        clauses_file_path = sys.argv[2]
        clauses, SOS,target = load_clauses(clauses_file_path)
        target1=" v ".join(target)
        print_clauses(clauses)
        resolution_result = plResolution(clauses,SOS)
        print("=" * 15)
        if resolution_result:
            print(f"[CONCLUSION]: {target1} is true")
        else:
            print(f"[CONCLUSION]: {target1} is unknown")
    else:
        clauses_file_path = sys.argv[2]
        user_file_path = sys.argv[3]
        clauses, SOS, target = load_clauses(clauses_file_path)
        commands = load_commands(user_file_path)
        user_commands(commands, clauses,target)
        
        


