import xml.etree.ElementTree as ET
from components import spn


def parse_pnml_to_spn(pnml):

    print(f"\nParsing PNML file: {pnml}")
    tree = ET.parse(pnml)
    root = tree.getroot()
    namespace = {'pnml': 'http://www.pnml.org/version-2009/grammar/pnml'}

    spn_model = spn.SPN()
    places_dict = {}
    transitions_dict = {}

    print("Parsing places.")
    for element in root.findall(".//pnml:place", namespace):
        place_id = element.get('id')
        label = element.find(".//pnml:text", namespace).text
        n_tokens = int(element.find(".//pnml:initialMarking/pnml:text", namespace).text)
            
        place = spn.Place(label, n_tokens)
        places_dict[place_id] = place
        spn_model.add_place(place)

    print("Parsing transitions.")
    for element in root.findall(".//pnml:transition", namespace):
        transition_id = element.get('id')
        t_type = element.get('type')
        name = element.find(".//pnml:text", namespace).text

        transition = spn.Transition(name, t_type)
            
        dist_type, a, b, c = parse_distribution(element, namespace)
            
        if t_type == "T" and dist_type:
            transition.set_distribution(dist_type, a, b, c)
        elif t_type == "I" and dist_type == "weight":
            transition.set_weight(a)
                
        transitions_dict[transition_id] = transition
        spn_model.add_transition(transition)

    print("Parsing arcs.")
    for element in root.findall(".//pnml:arc", namespace):
        source_id = element.get('source')
        target_id = element.get('target')
        arc_type = element.get('type')
        multiplicity = int(element.find(".//pnml:inscription/pnml:text", namespace).text)

        source = places_dict.get(source_id) or transitions_dict.get(source_id)
        target = places_dict.get(target_id) or transitions_dict.get(target_id)

        if source and target:
            if arc_type == "input":
                spn_model.add_input_arc(source, target, multiplicity)
            elif arc_type == "output":
                spn_model.add_output_arc(source, target, multiplicity)
            elif arc_type == "inhibitor":
                spn_model.add_inhibitor_arc(target, source, multiplicity)

    print(f"\nSPN model created from PNML.")
        
    return spn_model
    
def parse_distribution(element, namespace):
    dist_elem = element.find(".//pnml:distribution", namespace)
    if dist_elem is not None:
        dist_type = dist_elem.find("pnml:type", namespace).text
        params = dist_elem.find("pnml:parameters", namespace)

        a = float(params.find("pnml:a", namespace).text) if params.find("pnml:a", namespace) is not None else 0.0
        b = float(params.find("pnml:b", namespace).text) if params.find("pnml:b", namespace) is not None else 0.0
        c = float(params.find("pnml:c", namespace).text) if params.find("pnml:c", namespace) is not None else 0.0
            
        return dist_type, a, b, c
        
    weight_elem = element.find(".//pnml:weight", namespace)
    if weight_elem is not None:
        return "weight", float(weight_elem.text), 0.0, 0.0
        
    return None, 0.0, 0.0, 0.0
