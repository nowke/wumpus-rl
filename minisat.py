# minisat.py
# ----------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

from logic import *
from subprocess import call
from tempfile import NamedTemporaryFile

# The following is a fairly direct adaptation of the very nice,
# slim wrapper to minisat provided by https://github.com/netom/satispy
# I'm not using satispy directly b/c it implements its own cnf rep.
# so I'm adapting the aima rep to communication with minisat.

class AIMA_to_Dimacs_Translator(object):

    def __init__(self):
        self.varname_dict = {}
        self.varobj_dict = {}

    def varname(self, vo):
        return self.varname_dict[vo]

    def varobj(self, v):
        return self.varobj_dict[v]

    def to_dimacs_string(self, clauses):
        """Convert AIMA cnf expression to Dimacs cnf string
        
        clauses: list of clauses in AIMA cnf
        
        In the converted Cnf there will be only numbers for
        variable names. The conversion guarantees that the
        variables will be numbered alphabetically.
        """
        self.varname_dict = {}
        self.varobj_dict = {}
        variables = prop_symbols_from_clause_list(clauses)
        ret = 'p cnf %d %d' % (len(variables), len(clauses))
        varis = dict(zip(sorted(variables, key=lambda v: v.op),
                         map(str, range(1, len(variables) + 1))))
        for var in varis:
            self.varname_dict[var] = varis[var]
            self.varobj_dict[varis[var]] = var

        for clause in clauses:
            ret += '\n'
            dimacs_vlist = []
            if clause.op == '|':
                for var in clause.args:
                    dimacs_vlist.append(('-' if var.op == '~' else '') \
                                        + self.varname_dict[var.args[0]
                                                            if var.op == '~' else var])

                ret += ' '.join(dimacs_vlist)
            elif clause.op == '~':
                ret += '-' + self.varname_dict[clause.args[0]]
            else:
                ret += self.varname_dict[clause]
            ret += ' 0'

        return ret

    def to_dimacs_string_set_variable_value(self, clauses, variable, value):
        """
        Same as above, but returns dimacs for the clauses for SAT test
             with variable set to value as follows:
        (1) If value = True, then all clauses containing a literal made true
             by that value will be removed
             (because any disjunctive clause with a True literal is SAT)
        (2) If value = False, then any clauses containing that literal have
             the literal removed ; if the literal is singular, then return
             no clauses, indicating that setting to that value is UNSAT
        """
        self.varname_dict = {}
        self.varobj_dict = {}
        variables = prop_symbols_from_clause_list(clauses)
        if variable in variables:
            variables.remove(variable)
        varis = dict(zip(sorted(variables, key=lambda v: v.op),
                         map(str, range(1, len(variables) + 1))))
        for var in varis:
            self.varname_dict[var] = varis[var]
            self.varobj_dict[varis[var]] = var

        ret_clauses = ''
        clause_count = 0
        for clause in clauses:
            clause_exists = True
            dimacs_vlist = []
            ret_clause = ''
            if clause.op == '|':
                for var in clause.args:
                    if literal_name(var) == literal_name(variable):
                        if value and not var.op == '~' or not value and var.op == '~':
                            clause_exists = False
                    else:
                        dimacs_vlist.append(('-' if var.op == '~' else '') \
                                            + self.varname_dict[var.args[0]
                                                                if var.op == '~' else var])

                if clause_exists:
                    ret_clause += ' '.join(dimacs_vlist)
            elif clause.op == '~':
                if literal_name(clause) == literal_name(variable):
                    if value:
                        return None
                    clause_exists = False
                else:
                    ret_clause += '-' + self.varname_dict[clause.args[0]]
            elif literal_name(clause) == literal_name(variable):
                if value:
                    clause_exists = False
                else:
                    return None
            else:
                ret_clause += self.varname_dict[clause]
            if clause_exists:
                clause_count += 1
                ret_clauses += ret_clause + ' 0\n'

        ret_header = 'p cnf %d %d\n' % (len(variables), clause_count)
        ret = ret_header + ret_clauses
        return ret

class Solution(object):

    def __init__(self, success = False, varmap = {}):
        self.success = success
        self.varmap = varmap

    def __repr__(self):
        return '<mSat.Sol {0}>'.format(self.success)

    def __getitem__(self, i):
        return self.varmap[i]

    def pprint(self):
        print self.success
        print self.varmap


class Minisat(object):
    COMMAND = 'minisat %s %s > /dev/null'

    def __init__(self, command = COMMAND):
        self.command = command

    def solve(self, cnf, variable = None, value = True,
              translator = AIMA_to_Dimacs_Translator):

        # if there are no clauses, then can't infer anything, so by default query result is unknown
        # return Solution with success == None
        # Note that this could be treated the same as failure.
        # In PropKB_SAT.ask, this is OK as it will test if sT.success == sF.success
        #     and therefore will also return None
        if not cnf: return Solution(None)
        
        s = Solution()
        infile = NamedTemporaryFile(mode='w')
        outfile = NamedTemporaryFile(mode='r')
        io = translator()
        if variable:
            dimacs = io.to_dimacs_string_set_variable_value(cnf, variable, value)
            if dimacs:
                infile.write(dimacs)
            else:
                return s
        else:
            infile.write(io.to_dimacs_string(cnf))
        infile.flush()
        ret = call(self.command % (infile.name, outfile.name), shell=True)
        infile.close()
        if ret != 10:
            return s
        s.success = True
        lines = outfile.readlines()[1:]
        for line in lines:
            varz = line.split(' ')[:-1]
            for v in varz:
                v = v.strip()
                value = v[0] != '-'
                v = v.lstrip('-')
                vo = io.varobj(v)
                s.varmap[vo] = value

        outfile.close()
        return s
