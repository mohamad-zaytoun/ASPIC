class Literal:
    def __init__(self, name, is_negativ=False):
        assert isinstance(name, str), "name should be a string"
        assert isinstance(is_negativ, bool), "is_negativ should be a booleean"
        self.name = name
        self.is_negativ = is_negativ

    def __repr__(self):
        if self.is_negativ:
            return f"!{self.name}"
        else:
            return self.name

    def __eq__(self, other):
        return (
            isinstance(other, Literal) and
            self.name == other.name and
            self.is_negativ == other.is_negativ
        )

    def __hash__(self):
        return hash((self.name, self.is_negativ))

    def negate(self):
        self.is_negativ = not self.is_negativ

    def copy(self):
        return Literal(self.name, self.is_negativ)

class Rule:
    def __init__(self,premises, conclusion, is_defeasible=False, reference=None):
        assert isinstance(premises, list), "premises should be a list"
        assert all([isinstance(p, Literal) for p in premises]), "premises should be a list of Literal"
        assert isinstance(conclusion, Literal), "conclusion should be a Literal"
        assert isinstance(is_defeasible, bool), "is_defeasible should be a boolean"
        assert reference is None or isinstance(reference, Literal), "reference must be a Literal or None"

        self.premises = premises
        self.conclusion = conclusion
        self.is_defeasible = is_defeasible
        self.reference = reference

    def __repr__(self):
            premises_str = ", ".join(map(str, self.premises))
            conclusion_str = str(self.conclusion)
            reference_str = f"[{self.reference}]" if self.reference is not None else "None"
            if self.is_defeasible: # 0 is defeasible and 1 is not defeasible
                defeasibility_str = "0"
                return f"{reference_str}: {premises_str} => {conclusion_str} ({defeasibility_str})"
            else:
                defeasibility_str = "1"
                return f"{reference_str}: {premises_str} -> {conclusion_str} ({defeasibility_str})"

    def __eq__(self, other):
        return (
            isinstance(other, Rule) and
            self.premises == other.premises and
            self.conclusion == other.conclusion and
            self.is_defeasible == other.is_defeasible and
            self.reference == other.reference
        )

    def __hash__(self):
        return hash((tuple(self.premises), self.conclusion, self.is_defeasible, self.reference))
    

def contraposition(rule):
    global it
    if rule.is_defeasible:
        raise ValueError("Contraposition rules can only be created for strict rules.")
    it = 0  # Initialize or reset the counter if needed
    premises = rule.premises
    conclusion = rule.conclusion
    contrapositives = []
    for premise in premises:
        conclusion_neg = conclusion.copy()
        conclusion_neg.negate()

        premise_neg = premise.copy()
        premise_neg.negate()

        premise_temp = [conclusion_neg]
        for prem in premises:
            if prem != premise:
                premise_temp.append(prem)
        contra_name = "c" + str(it)
        contrapositives.append(Rule(premise_temp, premise_neg, is_defeasible=False, reference=Literal(contra_name)))
        it += 1

    return contrapositives
