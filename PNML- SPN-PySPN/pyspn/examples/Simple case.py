import sys
sys.path.append('.../pyspn')


from components.spn import *
from components.spn_simulate import simulate
from components.spn_io import print_petri_net
from components.spn_visualization import *
from examples.ParsePNML import *

spn = parse_pnml_to_spn("MDPNML.pnml")



simulate(spn, max_time = 10, verbosity = 0, protocol = True)

#print_petri_net(spn)

draw_spn(spn, show=True, rankdir ="LR")
