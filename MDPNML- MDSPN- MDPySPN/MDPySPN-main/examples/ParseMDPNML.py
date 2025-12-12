import xml.etree.ElementTree as ET
from components import spn


def _as_bool(v):
    if v is None:
        return False
    return str(v).strip().lower() in ("1", "true", "yes")


def parse_mdpnml_to_spn(mdpnml):
    print(f"\nParsing PNML file: {mdpnml}")
    tree = ET.parse(mdpnml)
    root = tree.getroot()
    ns = {'mdpnml': 'http://www.pnml.org/version-2009/grammar/pnml'}

    spn_model = spn.SPN()
    places_dict = {}
    transitions_dict = {}

    # ---- DIMENSIONS (optional) ---------------------------------------------
    dims = []
    for d in root.findall(".//mdpnml:dimensions/mdpnml:dimension", ns):
        name = d.get("name")
        if name:
            dims.append(name)
    if dims:
        spn_model.dimensions = dims  # accessible later if needed

    # ---- PLACES -------------------------------------------------------------
    print("Parsing places.")
    for element in root.findall(".//mdpnml:place", ns):
        place_id = element.get('id')

        # label
        label_el = element.find(".//mdpnml:name/mdpnml:text", ns)
        label = label_el.text if label_el is not None else element.find(".//mdpnml:text", ns).text

        # initial marking
        im_el = element.find(".//mdpnml:initialMarking/mdpnml:text", ns)
        n_tokens = int(im_el.text) if im_el is not None else 0

        # MDPNML extras
        DoT_attr = element.get("DoT")
        dim_tracked = element.get("dimensionTracked") or element.get("dimension_tracked")

        place_kwargs = {}

        # Always keep the tracked dimension if provided
        if dim_tracked:
            place_kwargs["dimension_tracked"] = dim_tracked

        # If DoT is explicitly provided, parse and keep it.
        # Otherwise, if a tracked dimension exists but DoT is missing/empty, default DoT=1.
        if DoT_attr is not None and str(DoT_attr).strip() != "":
            try:
                place_kwargs["DoT"] = float(DoT_attr) if "." in str(DoT_attr) else int(DoT_attr)
            except ValueError:
                place_kwargs["DoT"] = DoT_attr  # leave as string if non-numeric
        elif dim_tracked:
            place_kwargs["DoT"] = 1

        place = spn.Place(label, n_tokens, **place_kwargs)
        places_dict[place_id] = place
        spn_model.add_place(place)

    # ---- TRANSITIONS --------------------------------------------------------
    print("Parsing transitions.")
    for element in root.findall(".//mdpnml:transition", ns):
        transition_id = element.get('id')
        t_type = element.get('type')  # "T" or "I"
        name_el = element.find(".//mdpnml:name/mdpnml:text", ns)
        name = name_el.text if name_el is not None else element.find(".//mdpnml:text", ns).text

        # MDPNML extras (attributes)
        t_kwargs = {}

        transition = spn.Transition(name, t_type, **t_kwargs)

        # Distribution (for timed transitions) or weight (for immediate if you ever add it)
        dist_type, a, b, c = parse_distribution(element, ns)
        if t_type == "T" and dist_type:
            transition.set_distribution(dist_type, a, b, c)
        elif t_type == "I" and dist_type == "weight":
            transition.set_weight(a)

        # Dimension changes (MDPNML)
        dc_parent = element.find(".//mdpnml:impactedDimensions", ns)
        if dc_parent is not None:
            for dc in dc_parent.findall("mdpnml:impactedDimension", ns):
                dname = dc.get("name")
                ctype_el = dc.find("mdpnml:impactType", ns)
                val_el = dc.find("mdpnml:impactValue", ns)
                if dname and ctype_el is not None and val_el is not None:
                    ctype = ctype_el.text.strip()
                    try:
                        val = float(val_el.text)
                    except (ValueError, TypeError):
                        continue
                    # e.g., transition.add_dimension_change("Energy", "rate", 10)
                    transition.add_dimension_change(dname, ctype, val)

        transitions_dict[transition_id] = transition
        spn_model.add_transition(transition)

    # ---- ARCS ---------------------------------------------------------------
    print("Parsing arcs.")
    for element in root.findall(".//mdpnml:arc", ns):
        source_id = element.get('source')
        target_id = element.get('target')
        arc_type = element.get('type')  # "input" | "output" | "inhibitor"
        mult_el = element.find(".//mdpnml:inscription/mdpnml:text", ns)
        multiplicity = int(mult_el.text) if mult_el is not None else 1

        source = places_dict.get(source_id) or transitions_dict.get(source_id)
        target = places_dict.get(target_id) or transitions_dict.get(target_id)

        if source and target:
            if arc_type == "input":
                spn_model.add_input_arc(source, target, multiplicity)
            elif arc_type == "output":
                spn_model.add_output_arc(source, target, multiplicity)
            elif arc_type == "inhibitor":
                # your earlier PNML parser had target/source flipped for inhibitor; keep consistent if needed
                spn_model.add_inhibitor_arc(target, source, multiplicity)

    print("\nSPN model created from PNML.")
    if hasattr(spn_model, "dimensions"):
        print(f"Dimensions: {spn_model.dimensions}")

    return spn_model


def parse_distribution(element, ns):
    dist_elem = element.find(".//mdpnml:distribution", ns)
    if dist_elem is not None:
        dist_type_el = dist_elem.find("mdpnml:type", ns)
        params = dist_elem.find("mdpnml:parameters", ns)

        dist_type = dist_type_el.text.strip() if dist_type_el is not None else None

        def _get(name):
            tag = params.find(f"mdpnml:{name}", ns) if params is not None else None
            if tag is None or tag.text is None:
                return 0.0
            try:
                return float(tag.text)
            except ValueError:
                return 0.0

        a = _get("a")
        b = _get("b")
        c = _get("c")
        return dist_type, a, b, c

    # Optional: <weight> for immediate transitions if you decide to include
    weight_elem = element.find(".//mdpnml:weight", ns)
    if weight_elem is not None and weight_elem.text is not None:
        try:
            return "weight", float(weight_elem.text), 0.0, 0.0
        except ValueError:
            return "weight", 0.0, 0.0, 0.0

    return None, 0.0, 0.0, 0.0
