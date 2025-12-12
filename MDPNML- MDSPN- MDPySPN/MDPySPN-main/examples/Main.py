if __name__ == "__main__":
    import sys
    sys.path.append('.../MDPySPN-main')

    from components.spn import SPN
    from components.spn_simulate import simulate
    from components.spn_visualization import draw_spn
    from ParseMDPNML import parse_mdpnml_to_spn

    spn = parse_mdpnml_to_spn("MDPNML.pnml")

    try:
        Total_Dimensions = spn.dimensions
    except AttributeError:
        Total_Dimensions = ['time']


    simulate(spn, max_time=60, verbosity=1, protocol="event_log.csv")
    draw_spn(spn, show=True)
