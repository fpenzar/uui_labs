class klauzula:

    def __init__(self, literals, parent1, parent2, row=None):
        self.row = row
        self.parent1 = parent1
        self.parent2 = parent2
        self.literals = [l.lower() for l in literals]
        self.factorize()
        self.literals.sort()
        self.literals_set = set(self.literals)
    

    def add_row(self, row):
        self.row = row
    

    def factorize(self):
        self.literals = list(set(self.literals))
    

    def is_nil(self):
        return len(self.literals) == 0
    

    def is_tautology(self):
        for literal in self.literals:
            if f"~{literal}" in self.literals_set:
                return True
    

    def __hash__(self):
        return hash(" v ".join(self.literals))
    

    def __repr__(self):
        if self.is_nil():
            return "NIL"
        if len(self.literals) == 1:
            return self.literals[0]
        return " v ".join(self.literals)


    def __str__(self):
        if self.is_nil():
            return "NIL"
        if len(self.literals) == 1:
            return self.literals[0]
        return " v ".join(self.literals)


    def __eq__(self, other):
        return hash(self) == hash(other)


    def __lt__(self, other):
        return self.row < other.row


    def get_literals(self):
        return self.literals_set

    
    def negate(self):
        negated = []
        for l in self.literals:
            if l.startswith("~"):
                negated.append(l[1:])
            else:
                negated.append(f"~{l}")
        negated_clauses = [klauzula([l], self.parent1, self.parent2) for l in negated]
        return negated_clauses

    def print_format(self):
        parents = ""
        if self.parent1:
            parents = f" ({self.parent1.row}, {self.parent2.row})"
        return f"{self.row}. {str(self)}{parents}"



class logic_tree:

    def __init__(self, premises):
        self.premises = premises
    

    def remove(self, klauzula):
        self.premises.remove(klauzula)
    

    def add(self, klauzula):
        self.premises.append(klauzula)
    

    # strategija brisanja
    # uklanjanje nevažnih (tautologija)
    def remove_unimportant(self, klauzule):
        no_tautology = set()
        for klauzula in klauzule:
            if not klauzula.is_tautology():
                no_tautology.add(klauzula)
        return no_tautology
    

    # strategija brisanja
    # uklanjanje redundantnih klauzula
    def remove_subsumed(self, clauses):
        to_remove = []
        for i, current in enumerate(clauses):
            for j, other in enumerate(clauses):
                if i == j:
                    continue
                if other.get_literals().issubset(current.get_literals()):
                    to_remove.append(current)
                    break
        
        # remove subsests
        for k in to_remove:
            clauses.remove(k)
    

    # TODO ovjde je potencijalna greska ako se duplo dodaje
    def selectClauses(self, sos, clauses):
        pairs = []
        for c1 in clauses:
            for c2 in sos:
                pairs.append((c1, c2))
        
        for c1 in sos:
            for c2 in sos:
                if c1 == c2:
                    continue
                pairs.append((c1, c2))
        return pairs
    

    # algoritam rezolucije opovrgavanja
    def plResolution(self, test_klauzula: klauzula):
        self.test_clause = test_klauzula
        self.negated_test_clauses = test_klauzula.negate()
        # set row for negated test clauses
        for i, clause in enumerate(self.negated_test_clauses):
            clause.add_row(i + len(self.premises) + 1)
        
        new = set(self.negated_test_clauses) # sluzi kao SoS
        clauses = set(self.premises)
        row = len(self.negated_test_clauses) + len(self.premises) + 1
        while True:
            self.remove_subsumed(clauses)
            clauses = self.remove_unimportant(clauses)
            self.remove_subsumed(new)
            new = self.remove_unimportant(new)
            if new.issubset(clauses):
                self.solution = None
                return False
            resolvents = set()
            for c1, c2 in self.selectClauses(new, clauses):
                # adding the row just to keep track of which clause is older
                temp_resolvents = self.plResolve(c1, c2, row)
                for res in temp_resolvents:
                    if res.is_nil():
                        self.solution = res
                        return True
                resolvents = resolvents.union(temp_resolvents)
            clauses = clauses.union(new)
            new = resolvents
            row += 1
            

    # izvodi nove klauzule iz dvije postojeće
    def plResolve(self, klauzula1: klauzula, klauzula2: klauzula, row):
        new_clauses = set()
        for l1 in klauzula1.get_literals():
            add = False
            if l1.startswith("~"):
                if l1[1:] in klauzula2.get_literals():
                    add = True
                    other = l1[1:]
            else:
                if f"~{l1}" in klauzula2.get_literals():
                    add = True
                    other = f"~{l1}"
            
            if not add:
                continue
            literals = set()
            for literal_to_add in klauzula1.get_literals():
                if literal_to_add == l1:
                    continue
                literals.add(literal_to_add)
            for literal_to_add in klauzula2.get_literals():
                if literal_to_add == other:
                    continue
                literals.add(literal_to_add)
            new_clauses.add(klauzula(literals, klauzula1, klauzula2, row))
        return new_clauses
    

    def print(self):
        if not self.solution:
            for i, premise in enumerate(self.premises):
                print(f"{i + 1}. {premise}")
            for i, negated in enumerate(self.negated_test_clauses):
                print(f"{i + 1 + len(self.premises)}. {negated}")
            print("===============")
            print(f"[CONCLUSION]: {self.test_clause.original_text} is unknown")
            return

        to_print = set()
        open = {self.solution}
        while len(open):
            current = open.pop()
            to_print.add(current)
            if current.parent1:
                if current.parent1 not in open and current.parent1 not in to_print:
                    open.add(current.parent1)
                if current.parent2 not in open and current.parent2 not in to_print:
                    open.add(current.parent2)
        to_print = to_print.union(set(self.premises))
        to_print = to_print.union(set(self.negated_test_clauses))
        to_print = sorted(list(to_print))
        for i, clause in enumerate(to_print):
            clause.add_row(i + 1)
        for i, clause in enumerate(to_print):
            if i == len(self.premises) + len(self.negated_test_clauses):
                print("===============")
            print(clause.print_format())
        print("===============")
        print(f"[CONCLUSION]: {self.test_clause} is true")
