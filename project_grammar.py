"""
project_grammar.py
Define la gramática específica del Proyecto 2
Proyecto 2 - Teoría de la Computación
"""

from grammar import Grammar


def create_project_grammar() -> Grammar:
    """
    Crea la gramática del proyecto según las especificaciones:
    
    S → NP VP
    VP → VP PP | V NP | cooks | drinks | eats | cuts
    PP → P NP
    NP → Det N | he | she
    V → cooks | drinks | eats | cuts
    P → in | with
    N → cat | dog | beer | cake | juice | meat | soup | fork | knife | oven | spoon
    Det → a | the
    
    Returns:
        Grammar: Objeto Grammar con todas las reglas del proyecto
    """
    g = Grammar()
    
    # S → NP VP
    g.add_rule('S', ['NP', 'VP'])
    
    # VP rules
    g.add_rule('VP', ['VP', 'PP'])
    g.add_rule('VP', ['V', 'NP'])
    g.add_rule('VP', ['cooks'])
    g.add_rule('VP', ['drinks'])
    g.add_rule('VP', ['eats'])
    g.add_rule('VP', ['cuts'])
    
    # PP rules
    g.add_rule('PP', ['P', 'NP'])
    
    # NP rules
    g.add_rule('NP', ['Det', 'N'])
    g.add_rule('NP', ['he'])
    g.add_rule('NP', ['she'])
    
    # V rules
    g.add_rule('V', ['cooks'])
    g.add_rule('V', ['drinks'])
    g.add_rule('V', ['eats'])
    g.add_rule('V', ['cuts'])
    
    # P rules (preposiciones)
    g.add_rule('P', ['in'])
    g.add_rule('P', ['with'])
    
    # N rules - Animales
    g.add_rule('N', ['cat'])
    g.add_rule('N', ['dog'])
    
    # N rules - Bebidas y comidas
    g.add_rule('N', ['beer'])
    g.add_rule('N', ['cake'])
    g.add_rule('N', ['juice'])
    g.add_rule('N', ['meat'])
    g.add_rule('N', ['soup'])
    
    # N rules - Utensilios
    g.add_rule('N', ['fork'])
    g.add_rule('N', ['knife'])
    g.add_rule('N', ['oven'])
    g.add_rule('N', ['spoon'])
    
    # Det rules (determinantes)
    g.add_rule('Det', ['a'])
    g.add_rule('Det', ['the'])
    
    return g