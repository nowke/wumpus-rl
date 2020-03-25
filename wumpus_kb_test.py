from wumpus_kb import *


def test_axiom_generation():
    print 'axiom_generator_percept_sentence:'
    print axiom_generator_percept_sentence(0, (True, True, False, True, False))

    print '\naxiom_generator_initial_location_assertions(2, 3):'
    print axiom_generator_initial_location_assertions(2, 3)

    print '\naxiom_generator_pits_and_breezes(2, 3, 0, 4, 0, 4):'
    print axiom_generator_pits_and_breezes(2, 3, 0, 4, 0, 4)

    print '\ngenerate_pit_and_breeze_axioms(0, 2, 0, 2):'
    print generate_pit_and_breeze_axioms(0, 2, 0, 2)

    print '\naxiom_generator_wumpus_and_stench(2, 3, 0, 4, 0, 4):'
    print axiom_generator_wumpus_and_stench(2, 3, 0, 4, 0, 4)

    print '\ngenerate_wumpus_and_stench_axioms(0, 2, 0, 2):'
    print generate_wumpus_and_stench_axioms(0, 2, 0, 2)

    print '\naxiom_generator_at_least_one_wumpus(0, 2, 0, 2):'
    print axiom_generator_at_least_one_wumpus(0, 2, 0, 2)

    print '\naxiom_generator_at_most_one_wumpus(0, 2, 0, 2):'
    at_most_one = axiom_generator_at_most_one_wumpus(0, 2, 0, 2)
    print 'num clauses [(3x3) x (3x3)-1 / 2]:', len(at_most_one.split('&'))
    print at_most_one

    print '\naxiom_generator_only_in_one_location(2, 3, 0, 4, 0, 4, t=5)'
    only_in_one_loc = axiom_generator_only_in_one_location(2, 3, 0, 4, 0, 4, t=5)
    print 'num clauses:', len(only_in_one_loc.split('&'))
    print only_in_one_loc

    print '\naxiom_generator_only_one_heading(heading="east", t=8)'
    print axiom_generator_only_one_heading(heading="east", t=8)

    print '\naxiom_generator_have_arrow_and_wumpus_alive(t=8)'
    print axiom_generator_have_arrow_and_wumpus_alive(t=8)

    print '\naxiom_generator_location_OK(2, 3, 8)'
    print axiom_generator_location_OK(2, 3, 8)

    print '\naxiom_generator_breeze_percept_and_location_property(2, 3, 8)'
    print axiom_generator_breeze_percept_and_location_property(2, 3, 8)

    print '\naxiom_generator_stench_percept_and_location_property(2, 3, 8)'
    print axiom_generator_stench_percept_and_location_property(2, 3, 8)

    print '\naxiom_generator_at_location_ssa(8, 2, 3, 0, 5, 0, 5)'
    print axiom_generator_at_location_ssa(8, 2, 3, 0, 5, 0, 5)

    print '\naxiom_generator_have_arrow_ssa(8)'
    print axiom_generator_have_arrow_ssa(8)

    print '\naxiom_generator_wumpus_alive_ssa(8)'
    print axiom_generator_wumpus_alive_ssa(8)

    print '\naxiom_generator_heading_north_ssa(8)'
    print axiom_generator_heading_north_ssa(8)
    print 'axiom_generator_heading_east_ssa(8)'
    print axiom_generator_heading_east_ssa(8)
    print 'axiom_generator_heading_south_ssa(8)'
    print axiom_generator_heading_south_ssa(8)
    print 'axiom_generator_heading_west_ssa(8)'
    print axiom_generator_heading_west_ssa(8)

    print '\naxiom_generator_heading_only_north(8)'
    print axiom_generator_heading_only_north(8)
    print 'axiom_generator_heading_only_east(8)'
    print axiom_generator_heading_only_east(8)
    print 'axiom_generator_heading_only_south(8)'
    print axiom_generator_heading_only_south(8)
    print 'axiom_generator_heading_only_west(8)'
    print axiom_generator_heading_only_west(8)

    print '\naxiom_generator_only_one_action_axioms(8)'
    only_one_action = axiom_generator_only_one_action_axioms(8)
    print 'num clauses:', len(only_one_action.split(') & ('))
    for elm in only_one_action.split(') & ('):
        print '    {0}'.format(elm)
    print only_one_action


test_axiom_generation()
