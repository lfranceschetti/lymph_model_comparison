original_graph = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['I', 'III', 'V', 'VII'],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): [],
    ('lnl', 'VII'): [],
}

minimal_graph = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['III', 'V'],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): [],
    ('lnl', 'VII'): [],
}

add_12 = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): ["II"],
    ('lnl', 'II'): ['I', 'III', 'V', 'VII'],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): [],
    ('lnl', 'VII'): [],
}

rm_21 = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['III', 'V', "VII"],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): [],
    ('lnl', 'VII'): [],
}

rm_27 = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['I', 'III', 'V'],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): ["IV"],
    ('lnl', 'VII'): [],
}


add_52 = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['I', 'III', 'V', 'VII'],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): ["II"],
    ('lnl', 'VII'): [],
}

add_35 = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['I', 'III', 'V', 'VII'],
    ('lnl', 'III'): ['IV', "V"],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): [],
    ('lnl', 'VII'): [],
}

add_53 = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['I', 'III', 'V', 'VII'],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): ["III"],
    ('lnl', 'VII'): [],
}

add_45 = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['I', 'III', 'V', 'VII'],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): ["V"],
    ('lnl', 'V'): [],
    ('lnl', 'VII'): [],
}

add_54 = {
    ('tumor', 'primary'): ['I', 'II', 'III', 'IV', 'V', 'VII'],
    ('lnl', 'I'): [],
    ('lnl', 'II'): ['I', 'III', 'V', 'VII'],
    ('lnl', 'III'): ['IV'],
    ('lnl', 'IV'): [],
    ('lnl', 'V'): ["IV"],
    ('lnl', 'VII'): [],
}

all_graphs = [original_graph, minimal_graph,
              add_12, add_35, add_45, add_52, add_53, add_54]
