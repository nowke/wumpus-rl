# wumpus.py
# ---------
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

from wumpus_agent import *
from time import clock
import wumpus_environment


#-------------------------------------------------------------------------------
# Wumpus World Scenarios
#-------------------------------------------------------------------------------

class WumpusWorldScenario(object):
    """
    Construct a Wumpus World Scenario
    Objects that can be added to the environment:
        Wumpus()
        Pit()
        Gold()
        Wall()
        HybridWumpusAgent(heading)  # A propositional logic Wumpus World agent
        Explorer(program, heading)  # A non-logical Wumpus World agent (mostly for debugging)
    Provides methods to load layout from file
    Provides step and run methods to run the scenario
        with the provided agent's agent_program
    """
    
    def __init__(self, layout_file=None, agent=None, objects=None,
                 width=None, height=None, entrance=None, trace=True):
        """
        layout_file := (<string: layout_file_name>, <agent>)
        """
        if agent != None and not isinstance(agent, Explorer):
            raise Exception("agent must be type Explorer, got instance of class\n" \
                            + " {0}".format(agent.__class__))
        if layout_file:
            objects, width, height, entrance = self.load_layout(layout_file)
            
        self.width, self.height = width, height
        self.entrance = entrance
        self.agent = agent
        self.objects = objects
        self.trace = trace
        self.env = self.build_world(width, height, entrance, agent, objects)

    def build_world(self, width, height, entrance, agent, objects):
        """
        Create a WumpusEnvironment with dimensions width,height
        Set the environment entrance
        objects := [(<wumpus_environment_object>, <location: (<x>,<y>) >, ...]
        """
        env = WumpusEnvironment(width, height, entrance)
        if self.trace:
            agent = wumpus_environment.TraceAgent(agent)
        agent.register_environment(env)
        env.add_thing(agent, env.entrance)
        for (obj, loc) in objects:
            env.add_thing(obj, loc)
        return env

    def load_layout(self, layout_file):
        """
        Load text file specifying Wumpus Environment initial configuration
        Text file is N (rows) by M (columns) grid where each cell in a row
        consists of M comma-separated cells specs, where each cell contains
        either:
           '.' : space (really just a placeholder)
        or a one or more of (although typically just have one per cell):
           'W' : wumpus
           'P' : pit
           'G' : gold
           'A' : wumpus hunter agent (heading specified in agent object)
        """
        
        if layout_file.endswith('.lay'):
            layout = self.tryToLoad('layouts/' + layout_file)
            if not layout: layout = self.tryToLoad(layout_file)
        else:
            layout = self.tryToLoad('layouts/' + layout_file + '.lay')
            if not layout: layout = self.tryToLoad(layout_file + '.lay')

        if not layout:
            raise Exception("Could not find layout file: {0}".format(layout_file))

        print "Loaded layout '{0}'".format(layout_file)

        objects = []
        entrance = (1,1) # default entrance location
        
        ri = len(layout)
        largest_ci = 0
        for row in layout:
            ci = 0
            if row:
                ri -= 1
                row = row.split(',')
                for cell in row:
                    ci += 1
                    if ci > largest_ci: largest_ci = ci
                    for char in cell:
                        if char == 'W':
                            objects.append((Wumpus(),(ci,ri)))
                        elif char == 'P':
                            objects.append((Pit(),(ci,ri)))
                        elif char == 'G':
                            objects.append((Gold(),(ci,ri)))
                        elif char == 'A':
                            entrance = (ci,ri)

        return objects, largest_ci, len(layout)-ri, entrance

    def tryToLoad(self, fullname):
        if (not os.path.exists(fullname)): return None
        f = open(fullname)
        try: return [line.strip() for line in f]
        finally: f.close()

    def step(self):
        self.env.step()
        print
        print "Current Wumpus Environment:"
        print self.env.to_string()

    def run(self, steps = 1000):
        print self.env.to_string()
        for step in range(steps):
            if self.env.is_done():
                print "DONE."
                slist = []
                if len(self.env.agents) > 0:
                    slist += ['Final Scores:']
                for agent in self.env.agents:
                    slist.append(' {0}={1}'.format(agent, agent.performance_measure))
                    if agent.verbose:
                        if hasattr(agent, 'number_of_clauses_over_epochs'):
                            print "number_of_clauses_over_epochs:" \
                                  +" {0}".format(agent.number_of_clauses_over_epochs)
                        if hasattr(agent, 'belief_loc_query_times'):
                            print "belief_loc_query_times:" \
                                  +" {0}".format(agent.belief_loc_query_times)
                print ''.join(slist)
                return
            self.step()

    def to_string(self):
        s = "Environment width={0}, height={1}\n".format(self.width, self.height)
        s += "Initial Position: {0}\n".format(self.entrance)
        s += "Actions: {0}\n".format(self.actions)
        return s

    def pprint(self):
        print self.to_string()
        print self.env.to_string()



#-------------------------------------------------------------------------------

def world_scenario_hybrid_wumpus_agent_from_layout(layout_filename):
    """
    Create WumpusWorldScenario with an automated agent_program that will
        try to solve the Hunt The Wumpus game on its own.
    layout_filename := name of layout file to load
    """
    return WumpusWorldScenario(layout_file = layout_filename,
                               agent = HybridWumpusAgent('north', verbose=True),
                               trace=False)

#------------------------------------
# examples of constructing HybridWumpusAgent scenario
# specifying objects as list

def wscenario_4x4_HybridWumpusAgent():
    return WumpusWorldScenario(agent = HybridWumpusAgent('north', verbose=True),
                               objects = [(Wumpus(),(1,3)),
                                          (Pit(),(3,3)),
                                          (Pit(),(3,1)),
                                          (Gold(),(2,3))],
                               width = 4, height = 4, entrance = (1,1),
                               trace=True)

#-------------------------------------------------------------------------------

def world_scenario_manual_with_kb_from_layout(layout_filename):
    """
    Create WumpusWorldScenario with a manual agent_program and Knowledge Base
        (see with_manual_kb_program)
    layout_filename := name of layout file to load
    """
    return WumpusWorldScenario(layout_file = layout_filename,
                               agent = with_manual_kb_program(HybridWumpusAgent('north',
                                                                                verbose=True)),
                               trace=False)

#------------------------------------
# examples of constructing manual wumpus agent with KB scenario
# specifying objects as list

def wscenario_4x4_manual_HybridWumpusAgent():
    return WumpusWorldScenario(agent = with_manual_kb_program(HybridWumpusAgent('north', verbose=True)),
                               objects = [(Wumpus(),(1,3)),
                                          (Pit(),(3,3)),
                                          (Pit(),(3,1)),
                                          (Gold(),(2,3))],
                               width = 4, height = 4, entrance = (1,1),
                               trace=True)

#-------------------------------------------------------------------------------

def world_scenario_manual_from_layout(layout_filename):
    """
    Create WumpusWorldScenario with a manual agent_program (see with_manual_program)
    layout_filename := name of layout file to load
    """
    return WumpusWorldScenario(layout_file = layout_filename,
                               agent = with_manual_program(Explorer(heading='north', verbose=True)),
                               trace=False)

#------------------------------------
# examples of constructing manually-playable scenarios
# specifying objects as list or from layout file

def wscenario_4x4_manual():
    return WumpusWorldScenario(agent = with_manual_program(Explorer(heading='north', verbose=True)),
                               objects = [(Wumpus(),(1,3)),
                                          (Pit(),(3,3)),
                                          (Pit(),(3,1)),
                                          (Gold(),(2,3))],
                               width = 4, height = 4, entrance = (1,1),
                               trace=False)

def wscenario_4x4_manual_book_from_layout():
    return WumpusWorldScenario(layout_file = "wumpus_4x4_book",
                               agent = with_manual_program(Explorer(heading='north', verbose=True)),
                               trace=False)

def wscenario_4x4_manual_layout2_from_layout():
    return WumpusWorldScenario(layout_file = "wumpus_4x4_2",
                               agent = with_manual_program(Explorer(heading='north', verbose=True)),
                               trace=False)

#-------------------------------------------------------------------------------
# Manual agent program
#-------------------------------------------------------------------------------

def with_manual_program(agent):
    """
    Take <agent> and replaces its agent_program with manual_program.
    manual_program waits for keyboard input and executes command.
    This uses a closure.  Three cheers for closures !!!
    (if you don't know what a closure is, read this:
       http://en.wikipedia.org/wiki/Closure_(computer_science) )
    """

    helping  = ['?', 'help']
    stopping = ['quit', 'stop', 'exit']
    actions  = ['TurnRight', 'TurnLeft', 'Forward', 'Grab', 'Climb', 'Shoot', 'Wait']

    def show_commands():
        print "   The following are valid Hunt The Wumpus action:"
        print "     {0}".format(', '.join(map(lambda a: '\'{0}\''.format(a), actions)))
        print "   Enter {0} to get this command info" \
              .format(' or '.join(map(lambda a: '\'{0}\''.format(a), helping)))
        print "   Enter {0} to stop playing" \
              .format(' or '.join(map(lambda a: '\'{0}\''.format(a), stopping)))
        print "   Enter 'env' to display current wumpus environment"

    def manual_program(percept):
        print "[{0}] You perceive: {1}".format(agent.time,agent.pretty_percept_vector(percept))
        action = None
        while not action:
            val = raw_input("Enter Action ('?' for list of commands): ")
            val = val.strip()
            if val in helping:
                print
                show_commands()
                print
            elif val in stopping:
                action = 'Stop'
            elif val == 'env':
                print
                print "Current wumpus environment:"
                print agent.env.to_string()
            elif val in actions:
                action = val
            else:
                print "'{0}' is an invalid command;".format(val) \
                      + " try again (enter '?' for list of commands)"
        agent.time += 1
        return action

    agent.program = manual_program
    return agent

#-------------------------------------------------------------------------------
# Manual agent program with Knowledge Base
#-------------------------------------------------------------------------------

def with_manual_kb_program(agent):
    """
    Take <agent> and replaces its agent_program with manual_kb_program.
    Assumes the <agent> is a HybridWumpusAgent.
    (TODO: separate out logical agent from HybridWumpusAgent)
    Agent program that waits for keyboard input and executes command.
    Also provides interface for doing KB queries.
    Closures rock!
    """

    helping = ['?', 'help']
    stopping = ['quit', 'stop', 'exit']
    actions = ['TurnRight', 'TurnLeft', 'Forward', 'Grab', 'Climb', 'Shoot', 'Wait']
    queries = [('qp','Query a single proposition;\n' \
                + '           E.g. \'qp B1_1\' or \'qp OK1_1_3\', \'qp HeadingWest4\''),
               ('qpl','Query a-temporal location-based proposition at all x,y locations;\n' \
                + '           E.g., \'qpl P\' runs all queries of P<x>_<y>'),
               ('qplt','Query temporal and location-based propositions at all x,y locations;\n' \
                + '           E.g., \'qplt OK 4\' runs all queries of the OK<x>_<y>_4'),
               ('q!','Run ALL queries for optionally specified time (default is current time);\n'\
                + '           (can be time consuming!)')]

    def show_commands():
        print "Available Commands:"
        print "   The following are valid Hunt The Wumpus actions:"
        print "     {0}".format(', '.join(map(lambda a: '\'{0}\''.format(a), actions)))
        print "   Enter {0} to get this command info" \
              .format(' or '.join(map(lambda a: '\'{0}\''.format(a), helping)))
        print "   Enter {0} to stop playing" \
              .format(' or '.join(map(lambda a: '\'{0}\''.format(a), stopping)))
        print "   Enter 'env' to display current wumpus environment"
        print "   Enter 'kbsat' to check if the agent's KB is satisfiable"
        print "      If the KB is NOT satisfiable, then there's a contradiction that needs fixing."
        print "      NOTE: A satisfiable KB does not mean there aren't other problems."
        print "   Enter 'save-axioms' to save all of the KB axioms to 'kb-axioms.txt'"
        print "      This will overwrite any existing 'kb-axioms.txt'"
        print "   Enter 'save-clauses' to save all of the KB clauses to text file 'kb-clauses.txt'"
        print "      This will overwrite any existing 'kb-clauses.txt'"
        print "   Enter 'props' to list all of the proposition bases"
        print "   Queries:"
        for query,desc in queries:
            print "      {0} : {1}".format(query,desc)

    def show_propositions():
        print "Proposition Bases:"
        print "   Atemporal location-based propositions (include x,y index: P<x>_<y>)"
        print "     '" + '\', \''.join(proposition_bases_atemporal_location) + '\''
        print "   Perceptual propositions (include time index: P<t>)"
        print "     '" + '\', \''.join(proposition_bases_perceptual_fluents) + '\''
        print "   Location fluent propositions (include x,y and time index: P<x>_<y>_<t>)"
        print "     '" + '\', \''.join(proposition_bases_location_fluents) + '\''
        print "   State fluent propositions (include time index: P<t>)"
        print "     '" + '\', \''.join(proposition_bases_state_fluents[:4]) + '\','
        print "     '" + '\', \''.join(proposition_bases_state_fluents[4:]) + '\''
        print "   Action propositions (include time index: P<t>)"
        print "     '" + '\', \''.join(proposition_bases_actions) + '\''

    def write_list_to_text_file(filename,list):
        outfile = file(filename, 'w')
        for item in list:
            outfile.write('{0}\n'.format(item))
        outfile.close()

    def check_kb_status():
        """
        Tests whether the agent KB is satisfiable.
        If not, that means the KB contains a contradiction that needs fixing.
        However, being satisfiable does not mean the KB is correct.
        """
        result = minisat(agent.kb.clauses)
        if result:
            print "Agent KB is satisfiable"
        else:
            print "Agent KB is NOT satisfiable!!  There is contradiction that needs fixing!"

    def simple_query(proposition):
        """
        Executes a simple query to the agent KB for specified proposition.
        """
        result = agent.kb.ask(expr(proposition))
        if result == None:
            print "{0}: Unknown!".format(proposition)
        else:
            print "{0}: {1}".format(proposition,result)

    def location_based_query(proposition_base):
        """
        Executes queries for the specified type of proposition, for
        each x,y location.
        proposition_base := as all of the propositions include in their
        name 1 or more indexes (for time and/or x,y location), the
        proposition_base is the simple string representing the base
        of the proposition witout the indexes, which are added in
        code, below.
        time := the time index of the propositions being queried
        """
        display_env = WumpusEnvironment(agent.width, agent.height)
        start_time = clock()
        print "Running queries for: {0}<x>_<y>".format(proposition_base)
        for x in range(1,agent.width+1):
            for y in range(1,agent.height+1):
                query = expr('{0}{1}_{2}'.format(proposition_base,x,y))
                result = agent.kb.ask(query)
                if result == None:
                    display_env.add_thing(Proposition(query,'?'),(x,y))
                else:
                    display_env.add_thing(Proposition(query,result),(x,y))
        end_time = clock()
        print "          >>> time elapsed while making queries:" \
              + " {0}".format(end_time-start_time)
        print display_env.to_string(agent.time,
                                    title="All {0}<x>_<y> queries".format(proposition_base))

    def location_time_based_query(proposition_base, time):
        """
        Executes queries for the specified type of proposition, for
        each x,y location, at the specified time.
        proposition_base := as all of the propositions include in their
        name 1 or more indexes (for time and/or x,y location), the
        proposition_base is the simple string representing the base
        of the proposition witout the indexes, which are added in
        code, below.
        time := the time index of the propositions being queried
        """
        display_env = WumpusEnvironment(agent.width, agent.height)
        start_time = clock()
        print "Running queries for: {0}<x>_<y>_{1}".format(proposition_base,time)
        for x in range(1,agent.width+1):
            for y in range(1,agent.height+1):
                query = expr('{0}{1}_{2}_{3}'.format(proposition_base,x,y,time))
                result = agent.kb.ask(query)
                if result == None:
                    display_env.add_thing(Proposition(query,'?'),(x,y))
                else:
                    display_env.add_thing(Proposition(query,result),(x,y))
        end_time = clock()
        print "          >>> time elapsed while making queries:" \
              + " {0}".format(end_time-start_time)
        print display_env.to_string(agent.time,
                                    title="All {0}<x>_<y>_{1} queries".format(proposition_base,
                                                                              time))

    def run_all_queries(time):
        check_kb_status()
        for p in proposition_bases_perceptual_fluents:
            simple_query(p + '{0}'.format(time))
        for p in proposition_bases_atemporal_location:
            location_based_query(p)
        for p in proposition_bases_location_fluents:
            location_time_based_query(p,time)
        for p in proposition_bases_state_fluents:
            simple_query(p + '{0}'.format(time))
        # remove the quotes below and add quotes to the following if-statement
        # in order to query all actions from time 0 to now
        '''
        print "Querying actions from time 0 to {0}".format(time)
        for p in propositions_actions:
            for t in range(time+1):
                simple_query(p + '{0}'.format(t))
        '''
        if time-1 > 0:
            print "Actions from previous time: {0}".format(time-1)
            for p in proposition_bases_actions:
                simple_query(p + '{0}'.format(time-1))
            
        print "FINISHED running all queries for time {0}".format(time)

    def manual_kb_program(percept):

        print "------------------------------------------------------------------"
        print "At time {0}".format(agent.time)
        
        percept_sentence = agent.make_percept_sentence(percept)
        print "     HWA.agent_program(): kb.tell(percept_sentence):"
        print "         {0}".format(percept_sentence)
        agent.kb.tell(percept_sentence)  # update the agent's KB based on percepts

        # update current location and heading based on current KB knowledge state
        print "     HWA.infer_and_set_belief_location()"
        agent.infer_and_set_belief_location()
        print "     HWA.infer_and_set_belief_heading()"
        agent.infer_and_set_belief_heading()

        clauses_before = len(agent.kb.clauses)
        print "     HWA.agent_program(): Prepare to add temporal axioms"
        print "         Number of clauses in KB before: {0}".format(clauses_before)
        agent.add_temporal_axioms()
        clauses_after = len(agent.kb.clauses)
        print "         Number of clauses in KB after: {0}".format(clauses_after)
        print "         Total clauses added to KB: {0}".format(clauses_after - clauses_before)
        agent.number_of_clauses_over_epochs.append(len(agent.kb.clauses))

        action = None
        while not action:
            print "[{0}] You perceive: {1}".format(agent.time,
                                                   agent.pretty_percept_vector(percept))
            val = raw_input("Enter Action ('?' for list of commands): ")
            val = val.strip()
            if val in helping:
                print
                show_commands()
                print
            elif val in stopping:
                action = 'Stop'
            elif val in actions:
                action = val
            elif val == 'env':
                print
                print "Current wumpus environment:"
                print agent.env.to_string()
            elif val == 'props':
                print
                show_propositions()
                print
            elif val == 'kbsat':
                check_kb_status()
                print
            elif val == 'save-axioms':
                write_list_to_text_file('kb-axioms.txt',agent.kb.axioms)
                print "   Saved to 'kb-axioms.txt'"
                print
            elif val == 'save-clauses':
                write_list_to_text_file('kb-clauses.txt',agent.kb.clauses)
                print "   Saved to 'kb-clauses.txt'"
                print
            else:
                q = val.split(' ')
                if len(q) == 2 and q[0] == 'qp':
                    simple_query(q[1])
                    print
                elif len(q) == 2 and q[0] == 'qpl':
                    location_based_query(q[1])
                    print
                elif len(q) == 3 and q[0] == 'qplt':
                    location_time_based_query(q[1],q[2])
                    print
                elif q[0] == 'q!':
                    if len(q) == 2:
                        t = int(q[1])
                        run_all_queries(t)
                    else:
                        run_all_queries(agent.time)
                    print
                else:
                    print "'{0}' is an invalid command;".format(val) \
                          + " try again (enter '?' for list of commands)"
                    print

        # update KB with selected action
        agent.kb.tell(add_time_stamp(action, agent.time))

        agent.time += 1
        
        return action

    agent.program = manual_kb_program
    return agent

#-------------------------------------------------------------------------------
# Test MiniSat connection
#-------------------------------------------------------------------------------

def run_minisat_test():
    """
    Test connection to MiniSat
    """
    import logic

    queries = [("(P | ~P)", True), # SAT
               ("(P & ~P)", False), # UNSAT
               ("(P | R) <=> (~(Q | R) & (R >> ~(S <=> T)))", True) # SAT
               ]
    
    print "Running simple MiniSat test:"
    t = 1
    failed = []
    for query, expected_result in queries:
        print "-----------------------------------------------------"
        print "Test {0}".format(t)
        print "  Query:      '{0}'".format(query)
        query = logic.conjuncts(logic.to_cnf(logic.expr(query)))
        result = minisat(query, None, variable=None, value=True, verbose=False)
        print "  Query CNF:  {0}".format(query)
        print "  Result:     {0}   (Expected: {1})".format(result.success, expected_result)
        if result.success != expected_result:
            print "    FAILURE: unexpected result."
            failed.append(t)
        if result.success:
            print "  Variable Assignment: {0}".format(result.varmap)
        t += 1
    print "-----------------------------------------------------"
    if not failed:
        print "Successfully passed {0} tests.".format(len(queries))
    else:
        print "Passed {0} test(s).".format(len(queries) - len(failed))
        print "The following tests failed: {0}".format(failure)
    print "DONE."

#-------------------------------------------------------------------------------
# Command-line interface
#-------------------------------------------------------------------------------

def default(str):
  return str + ' [Default: %default]'

def readCommand( argv ):
    """
    Processes the command used to run wumpus.py from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:     python wumpus.py <options>
    EXAMPLES:  (1) python wumpus.py
                   - starts simple manual Hunt The Wumpus game
               (2) python wumpus.py -k OR python wumpus.py --kb
                   - starts simple manual Hunt The Wumpus game with
                   knowledge base and interactive queries possible
    """
    parser = OptionParser(usageStr)

    parser.add_option('-k', '--kb', action='store_true', dest='kb', default=False,
                      help=default("Instantiate a queriable knowledge base"))
    parser.add_option('-y', '--hybrid', action='store_true', dest='hybrid', default=False,
                      help=default("Run hybrid wumpus agent" \
                                   + " (takes precedence over -k option)"))
    parser.add_option('-l', '--layout', dest='layout', default=None,
                      help=default("Load layout file"))

    parser.add_option('-t', '--test', action='store_true', dest='test_minisat',
                      default=False,
                      help=default("Test connection to command-line MiniSat"))

    options, otherjunk = parser.parse_args(argv)
    
    if len(otherjunk) != 0:
        raise Exception("Command line input not understood: " + str(otherjunk))

    return options

def run_command(options):
    if options.test_minisat:
        run_minisat_test()
        return
    if options.hybrid:
        if options.layout:
            s = world_scenario_hybrid_wumpus_agent_from_layout(options.layout)
        else:
            s = wscenario_4x4_HybridWumpusAgent()
    elif options.kb:
        if options.layout:
            s = world_scenario_manual_with_kb_from_layout(options.layout)
        else:
            s = wscenario_4x4_manual_HybridWumpusAgent()
    else:
        if options.layout:
            s = world_scenario_manual_from_layout(options.layout)
        else:
            s = wscenario_4x4_manual()
    s.run()

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    """
    The main funciton called when wumpus_test.py is run from the command line:
    > python wumpus_test.py <options>
    """
    options = readCommand( sys.argv[1:] )
    run_command( options )
