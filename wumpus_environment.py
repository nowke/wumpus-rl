# wumpus_environment.py
# ---------------------
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

from utils import *
import agents
import sys

class Wumpus(agents.Thing):

    def __init__(self):
        self.alive = True

    def to_string(self):
        if self.alive:
            return 'W'
        else:
            return 'X'


class Wall(agents.Obstacle):

    def to_string(self):
        return '#'


class Pit(agents.Thing):

    def to_string(self):
        return 'P'


class Gold(agents.Thing):

    def to_string(self):
        return 'G'


class Arrow(agents.Thing):
    pass


class Explorer(agents.Agent):

    heading_num_to_str = {0: 'north', 1: 'west', 2: 'south', 3: 'east'}
    heading_str_to_num = {'north': 0, 'west': 1, 'south': 2, 'east': 3}

    def __init__(self, program = None, heading = 'east', environment = None, verbose=True):
        """
        NOTE: AIMA Ch7 example defaults to agent initially facing east,
        which is heading=3
        """
        self.verbose = verbose
        super(Explorer, self).__init__(program)
        if isinstance(heading, str):
            heading = self.heading_str_to_num[heading]
        self.initial_heading = heading
        self.has_arrow = True
        self.has_gold = False
        self.performance_measure = 0
        if environment:
            self.register_environment(environment)

    def register_environment(self, environment):
        if self.verbose:
            print "{0}.register_environment()".format(self.__class__.__name__)
        # NOTE: agent.location is the true, environment-registered location
        #       agent.location is also set by env.add_thing(agent)
        self.location = environment.entrance
        # agent.initial_location stores the original location, here same as env.entrance
        self.initial_location = environment.entrance
        # dimensions of environment
        # subtract 1 b/c env constructor always adds one for outer walls
        self.width, self.height = environment.width - 1, environment.height - 1
        self.env = environment
        self.reset()

    def reset(self):
        """
        NOTE: Eventually move belief_locaiton and belief_heading to a knowledge-based agent.
        """
        if self.verbose:
            print "{0}.reset()".format(self.__class__.__name__)
        if hasattr(self,'initial_location'):
            # self.location is the true agent location in the environment
            self.location = self.initial_location
            # self.belief_locataion is location the agent believes it is in
            self.belief_location = self.initial_location
        else:
            print "{0}.reset(): agent has no initial_location;".format(self.__class__.__name__)
            print "     Need to first call Explorer.register_environment(env)"
        # self.heading is the true agent heading in the environment
        self.heading = self.initial_heading
        # self.belief_heading is the heading the agent believes it has
        self.belief_heading = self.initial_heading
        self.time = 0

    def heading_str(self, heading):
        """Overkill!  But once I got started, I couldn't stop making it safe...
        Ensure that heading is a valid heading 'string' (for the logic side),
        as opposed to the integer form for the WumpusEnvironment side.
        """
        if isinstance(heading,int):
            if 0 <= heading <= 3:
                return self.heading_num_to_str[heading]
            else:
                print "Not a valid heading int (0 <= heading <= 3), got: {0}".format(heading)
                sys.exit(0)
        elif isinstance(heading,str):
            headings = self.heading_str_to_num.keys()
            if heading in headings:
                return heading
            else:
                print "Not a valid heading str (one of {0}), got: {1}".format(headings,heading)
                sys.exit(0)
        else:
            print "Not a valid heading:", heading
            sys.exit(0)

    def heading_int(self, heading):
        """ Same commend in doc for heading_str applies...
        Ensure that heading is a valid integer (for the WumpusEnvironment side).
        """
        if isinstance(heading,int):
            if 0 <= heading <= 3:
                return heading
            else:
                print "Not a valid heading int (0 <= heading <= 3), got: {0}".format(heading)
                sys.exit(0)
        elif isinstance(heading,str):
            headings = self.heading_str_to_num.keys()
            if heading in headings:
                return self.heading_str_to_num[heading]
            else:
                print "Not a valid heading str (one of {0}), got: {1}".format(headings,heading)
                sys.exit(0)
        else:
            print "Not a valid heading:", heading
            sys.exit(0)

    def to_string(self):
        """
        String representation of TRUE agent heading
        NOTE: This should really be the responsibility of the environment,
              refactor at some point
        """
        if self.heading == 0:
            return '^'
        if self.heading == 1:
            return '<'
        if self.heading == 2:
            return 'v'
        if self.heading == 3:
            return '>'

    def pretty_percept_vector(self, pvec):
        """ percept_vector: [<Stench?>, <Breeze?>, <Glitter?>, <Bump?>, <Scream?>] """
        percept_vector = [] #= [ 'None' for i in range(len(pvec)) ]
        if pvec[0]: percept_vector.append('Stench')
        else: percept_vector.append('~Stench')
        if pvec[1]: percept_vector.append('Breeze')
        else: percept_vector.append('~Breeze')
        if pvec[2]: percept_vector.append('Glitter')
        else: percept_vector.append('~Glitter')
        if pvec[3]: percept_vector.append('Bump')
        else: percept_vector.append('~Bump')
        if pvec[4]: percept_vector.append('Scream')
        else: percept_vector.append('~Scream')
        return percept_vector

    def raw_percepts_to_percept_vector(self, percepts):
        """
        raw percepts are: [<time_step>,
                           <Things in range>...,
                           <exogenous events ('Bump', 'Scream')>...]
        percept_vector: [<Stench?>, <Breeze?>, <Glitter?>, <Bump?>, <Scream?>]
        """
        percept_vector = [ False for i in range(5) ]
        # print 'raw percepts:', percepts
        for rawp in percepts:
            if rawp == 'Wumpus':
                percept_vector[0] = True
            if rawp == 'Pit':
                percept_vector[1] = True
            if rawp == 'Gold':
                percept_vector[2] = True
            if rawp == 'Bump':
                percept_vector[3] = True
            if rawp == 'Scream':
                percept_vector[4] = True

        return percept_vector

def TraceAgent(agent):
    """
    Wrap the agent's program to print its input and output. This will let
    you see what the agent is doing in the environment.
    
    This is still used in wumpus.WumpusWorldEnvironment.build_world,
    although it is now largley redundant b/c WumpusEnvironment has a
    verbose flag, and the with_manual*_program wrapper do lots of
    printing of state.
    """
    old_program = agent.program

    def new_program(percept):
        action = old_program(percept)
        print '%s perceives %s and does %s' % (agent,
                                               agent.pretty_percept_vector(percept),
                                               action)
        return action

    agent.program = new_program
    return agent


class WumpusEnvironment(agents.XYEnvironment):

    def __init__(self, width = 4, height = 4, entrance = (1, 1)):
        """ NOTE: range from 1 to {width or height} contains map,
        anything outside, 0 and {width+1 or height+1} becomes a wall """
        super(WumpusEnvironment, self).__init__(width + 1, height + 1)
        self.entrance = entrance
        self.add_walls()
        self.time_step = 0
        self.done = False
        self.global_percept_events = []

    def thing_classes(self):
        return [agents.Wall,
                Pit,
                Arrow,
                Gold,
                Wumpus,
                Explorer]

    def exogenous_change(self):
        """ Handle special outcomes """
        for agent in self.agents:
            colocated_wumpi = [ wumpus.is_alive()
                                for wumpus in self.list_things_at(agent.location,
                                                                  tclass=Wumpus) ]
            colocated_pit = self.list_things_at(agent.location, tclass=Pit)
            if any(colocated_wumpi):
                print 'A Wumpus ate {0}!'.format(agent)
                agent.performance_measure -= 1000
                self.done = True
            elif colocated_pit:
                print '{0} fell into a bottomless pit!'.format(agent)
                agent.performance_measure -= 1000
                self.done = True

    def is_done(self):
        return self.done or not any((agent.is_alive() for agent in self.agents))

    def step(self):
        super(WumpusEnvironment, self).step()
        self.time_step += 1

    def turn_heading(self, heading, inc):
        """ Return the heading to the left (inc=+1) or right (inc=-1) of heading.
        Only 4 directions, so mod(heading+inc,4) """
        return (heading + inc) % 4

    def heading_to_vector(self, heading):
        """ Convert heading into vector that can be added to location
        if agent moves Forward """
        if heading == 0:
            v = (0, 1)
        elif heading == 1:
            v = (-1, 0)
        elif heading == 2:
            v = (0, -1)
        elif heading == 3:
            v = (1, 0)
        return v

    def percept(self, agent):
        """ Each percept is a list beginning with the time_step (integer) """
        percepts = [self.time_step]
        for thing in self.things_near(agent.location):
            if isinstance(thing, Gold):
                if agent.location == thing.location:
                    percepts.append('Gold')
            else:
                percepts.append(self.thing_percept(thing, agent))

        if agent.bump:
            percepts.append('Bump')
        percepts += self.global_percept_events
        agent.bump = False
        self.global_percept_events = []
        return agent.raw_percepts_to_percept_vector(percepts)

    def execute_action(self, agent, action):
        """ Execute action taken by agent """
        agent.bump = False
        agent.performance_measure -= 1
        if action == 'TurnRight':
            agent.heading = self.turn_heading(agent.heading, -1)
        elif action == 'TurnLeft':
            agent.heading = self.turn_heading(agent.heading, +1)
        elif action == 'Forward':
            self.move_to(agent, vector_add(self.heading_to_vector(agent.heading),
                                           agent.location))
        elif action == 'Grab':
            if self.some_things_at(agent.location, tclass=Gold):
                try:
                    gold = self.list_things_at(agent.location, tclass=Gold)[0]
                    agent.has_gold = True
                    self.delete_thing(gold)
                except:
                    print "Error: Gold should be here, but couldn't find it!"
                    print 'All things:', self.list_things_at(agent.location)
                    print 'Gold?:', self.list_things_at(agent.location, tclass=Gold)
                    sys.exit(-1)

        elif action == 'Climb':
            if agent.location == self.entrance:
                if agent.has_gold:
                    agent.performance_measure += 1000
                self.done = True
        elif action == 'Shoot':
            if agent.has_arrow:
                agent.has_arrow = False
                agent.performance_measure -= 10
                self.shoot_arrow(agent)
        elif action == 'Stop':
            self.done = True

    def shoot_arrow(self, agent):
        dvec = self.heading_to_vector(agent.heading)
        aloc = agent.location
        while True:
            aloc = vector_add(dvec, aloc)
            if self.some_things_at(aloc, tclass=Wumpus):
                try:
                    poor_wumpus = self.list_things_at(aloc, tclass=Wumpus)[0]
                    poor_wumpus.alive = False
                    self.global_percept_events.append('Scream')
                except:
                    print "Error: Wumpus should be here, but couldn't find it!"
                    print 'All things:', aloc, self.list_things_at(aloc)
                    print 'Wumpus?:', aloc, self.list_things_at(aloc, tclass=Wumpus)
                    sys.exit(-1)

                break
            if self.some_things_at(aloc, tclass=Wall):
                break
            if 0 > aloc[0] > self.width or 0 > aloc[1] > self.height:
                break

    def run_verbose(self, steps = 1000):
        """Run environment while displaying ascii map, for given number of steps."""
        for step in range(steps):
            if self.is_done():
                print 'Done, stopping.'
                print self.to_string()
                return
            print self.to_string()
            self.step()

    def add_walls(self):
        """Put walls around the entire perimeter of the grid."""
        for x in range(self.width + 1):
            if not self.some_things_at((x, 0), Wall):
                self.add_thing(Wall(), (x, 0))
            if not self.some_things_at((x, self.height), Wall):
                self.add_thing(Wall(), (x, self.height))

        for y in range(self.height + 1):
            if not self.some_things_at((0, y), Wall):
                self.add_thing(Wall(), (0, y))
            if not self.some_things_at((self.width, y), Wall):
                self.add_thing(Wall(), (self.width, y))

    def max_cell_print_len(self):
        """Find the max print-size of all cells"""
        m = 0
        for r in range(1, self.height + 1):
            for c in range(1, self.width + 1):
                l = 0
                for item in self.list_things_at((r, c)):
                    #print 'max_cell_print_len:', item
                    l += len(item.to_string())
                if l > m:
                    m = l
        return m

    def to_string(self, t = None, title = None):
        """ Awkward implementation of quick-n-dirty ascii display of Wumpus Environment
        Uses R&N AIMA roome coordinates: (0,0) is bottom-left in ascii display """
        if title:
            print title
        column_width = self.max_cell_print_len()
        cell_hline = [ '-' for i in range(column_width + 2) ] + ['|']
        cell_hline = ''.join(cell_hline)
        hline = ['|'] + [ cell_hline for i in range(self.width + 1) ] + ['\n']
        hline = ''.join(hline)
        slist = []
        if len(self.agents) > 0:
            slist += ['Scores:']
        for agent in self.agents:
            slist.append(' {0}={1}'.format(agent, agent.performance_measure))

        if len(self.agents) > 0:
            slist.append('\n')
        for c in range(0, self.width + 1):
            spacer = ''.join([ ' ' for i in range(column_width - 1) ])
            slist.append('  {0}{1} '.format(c, spacer))

        slist.append('   time_step={0}'.format(t if t else self.time_step))
        slist.append('\n')
        slist.append(hline)
        for r in range(self.height, -1, -1):
            for c in range(0, self.width + 1):
                things_at = self.list_things_at((c, r))
                cell_width = 0
                for thing_at in things_at:
                    cell_width += len(thing_at.to_string())

                spacer = ''.join([ ' ' for i in range(column_width - cell_width) ])
                slist.append('| ')
                for thing in things_at:
                    slist.append(thing.to_string())

                slist.append(spacer + ' ')

            slist.append('| {0}\n'.format(r))
            slist.append(hline)

        return ''.join(slist)
