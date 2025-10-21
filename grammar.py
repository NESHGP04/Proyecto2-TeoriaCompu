"""
grammar.py
Clase para representar y manipular gramáticas libres de contexto (CFG)
Proyecto 2 - Teoría de la Computación
"""

from collections import defaultdict
from typing import Dict, List, Set, Tuple


class Grammar:
    """Representa una gramática libre de contexto (CFG)"""
    
    def __init__(self):
        self.variables = set()
        self.terminals = set()
        self.rules = defaultdict(list)  # Variable -> [(producción)]
        self.start_symbol = 'S'
        
    def add_rule(self, variable: str, production: list):
        """Agrega una regla a la gramática"""
        self.variables.add(variable)
        
        # Verificar si es terminal o no
        is_terminal = len(production) == 1 and production[0].islower()
        
        if is_terminal:
            self.terminals.add(production[0])
        else:
            for symbol in production:
                if symbol.isupper() or symbol == symbol.upper():
                    self.variables.add(symbol)
        
        self.rules[variable].append(tuple(production))
    
    def to_cnf(self):
        """Convierte la gramática a Forma Normal de Chomsky (CNF)"""
        print("\nConvirtiendo gramática a CNF...")
        
        # Paso 1: Eliminar reglas unitarias (A -> B)
        self._eliminate_unit_rules()
        
        # Paso 2: Convertir a formato CNF estricto
        new_rules = defaultdict(list)
        new_var_counter = 0
        terminal_vars = {}  # Mapeo de terminales a variables nuevas
        
        for variable, productions in self.rules.items():
            for prod in productions:
                if len(prod) == 1:
                    # Regla A -> a (terminal): Ya está en CNF
                    if prod[0].islower() or prod[0] in self.terminals:
                        new_rules[variable].append(prod)
                
                elif len(prod) == 2:
                    # Verificar si ambos son no-terminales
                    if all(p.isupper() or p.startswith('X') or p.startswith('T_') for p in prod):
                        # Ya está en CNF: A -> BC
                        new_rules[variable].append(prod)
                    else:
                        # Tiene terminales mezclados: reemplazar terminales con variables
                        new_prod = []
                        for symbol in prod:
                            if symbol.islower() or symbol in self.terminals:
                                # Es terminal, crear variable nueva si no existe
                                if symbol not in terminal_vars:
                                    terminal_vars[symbol] = f"T_{symbol}"
                                    self.variables.add(terminal_vars[symbol])
                                    new_rules[terminal_vars[symbol]].append((symbol,))
                                new_prod.append(terminal_vars[symbol])
                            else:
                                new_prod.append(symbol)
                        new_rules[variable].append(tuple(new_prod))
                
                else:
                    # Regla con más de 2 símbolos: A -> X1 X2 X3 ... Xn
                    # Convertir a: A -> X1 Y1, Y1 -> X2 Y2, ..., Yn-2 -> Xn-1 Xn
                    
                    # Primero, reemplazar terminales con variables
                    prod_list = []
                    for symbol in prod:
                        if symbol.islower() or symbol in self.terminals:
                            if symbol not in terminal_vars:
                                terminal_vars[symbol] = f"T_{symbol}"
                                self.variables.add(terminal_vars[symbol])
                                new_rules[terminal_vars[symbol]].append((symbol,))
                            prod_list.append(terminal_vars[symbol])
                        else:
                            prod_list.append(symbol)
                    
                    # Ahora dividir en reglas binarias
                    current_var = variable
                    for i in range(len(prod_list) - 2):
                        new_var = f"X{new_var_counter}"
                        new_var_counter += 1
                        self.variables.add(new_var)
                        
                        new_rules[current_var].append((prod_list[i], new_var))
                        current_var = new_var
                    
                    # Última regla
                    new_rules[current_var].append((prod_list[-2], prod_list[-1]))
        
        self.rules = new_rules
        print("Gramática convertida a CNF")
        self._print_cnf_grammar()
    
    def _eliminate_unit_rules(self):
        """Elimina reglas unitarias (A -> B)"""
        changed = True
        while changed:
            changed = False
            new_rules = defaultdict(list)
            
            for variable, productions in self.rules.items():
                for prod in productions:
                    if len(prod) == 1 and prod[0].isupper() and prod[0] in self.rules:
                        # Es regla unitaria A -> B, expandir con las reglas de B
                        for b_prod in self.rules[prod[0]]:
                            if b_prod not in new_rules[variable]:
                                new_rules[variable].append(b_prod)
                                changed = True
                    else:
                        # No es unitaria, mantener
                        if prod not in new_rules[variable]:
                            new_rules[variable].append(prod)
            
            self.rules = new_rules
    
    def _print_cnf_grammar(self):
        """Imprime la gramática en CNF"""
        print("\nGramática en CNF:")
        for var in sorted(self.rules.keys()):
            productions = [' '.join(prod) for prod in self.rules[var]]
            print(f"  {var} → {' | '.join(productions)}")