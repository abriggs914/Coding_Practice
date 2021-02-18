

class Term:

    def __init__(self, term, val):
        self.term = term
        self.val = self.attempt_eval(term)

        self.is_var = str(term) != str(val)
        print("term: {t}=>{st}\tval: {v}=>{sv}\tis_var: {iv}".format(t=term, st=self.term, v=val, sv=self.val, iv=self.is_var))
        # self.is_solvable =

    def val(self):
        return self.val

    def attempt_eval(self, val):
        try:
            e = eval(val)
        except SyntaxError:
            e = val
        except NameError:
            e = val

        return e


    def __repr__(self):
        return self.term

