import time
from typing import Tuple
from grammar import Grammar


class CYKParser:
    
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = None
        self.parse_tree = None
    
    def parse(self, sentence: str) -> Tuple[bool, float]:
    
        start_time = time.time()
        
        # Tokenizar la sentencia
        words = sentence.lower().split()
        n = len(words)
        
        print(f"\nAnalizando: '{sentence}'")
        print(f"   Tokens: {words}")
        print(f"   Longitud: {n} palabras\n")
        
        # Inicializar tabla CYK (programación dinámica)
        # table[i][j] contiene el conjunto de variables que pueden derivar
        # la subcadena desde posición i con longitud j+1
        self.table = [[set() for _ in range(n)] for _ in range(n)]
        self.parse_tree = [[{} for _ in range(n)] for _ in range(n)]
        
        # Paso 1: Llenar la diagonal (subcadenas de longitud 1)
        print("Llenando tabla CYK...")
        for i in range(n):
            word = words[i]
            # Buscar todas las variables que producen esta palabra
            for variable, productions in self.grammar.rules.items():
                for prod in productions:
                    if len(prod) == 1 and prod[0] == word:
                        self.table[i][0].add(variable)
                        self.parse_tree[i][0][variable] = (word,)
            
            print(f"  Posición {i} ('{word}'): {self.table[i][0]}")
        
        # Paso 2: Llenar el resto de la tabla (subcadenas de longitud > 1)
        for length in range(2, n + 1):  # Longitud de subcadena
            for i in range(n - length + 1):  # Posición inicial
                j = length - 1  # Índice en la tabla
                
                # Probar todas las particiones posibles
                for k in range(1, length):  # Punto de partición
                    # Subcadena izquierda: table[i][k-1]
                    # Subcadena derecha: table[i+k][j-k]
                    left_vars = self.table[i][k-1]
                    right_vars = self.table[i+k][j-k]
                    
                    # Buscar reglas A -> BC donde B ∈ left_vars y C ∈ right_vars
                    for variable, productions in self.grammar.rules.items():
                        for prod in productions:
                            if len(prod) == 2:
                                B, C = prod
                                if B in left_vars and C in right_vars:
                                    self.table[i][j].add(variable)
                                    self.parse_tree[i][j][variable] = (B, C, k)
                
                if self.table[i][j]:
                    print(f"  Posición {i}, longitud {length}: {self.table[i][j]}")
        
        # Verificar si S (símbolo inicial) está en table[0][n-1]
        accepted = self.grammar.start_symbol in self.table[0][n-1]
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        return accepted, execution_time
    
    def build_parse_tree(self, i: int = 0, j: int = None, variable: str = None) -> dict:
        
        if j is None:
            j = len(self.table) - 1
        if variable is None:
            variable = self.grammar.start_symbol
        
        if variable not in self.parse_tree[i][j]:
            return {"node": variable, "children": None}
        
        derivation = self.parse_tree[i][j][variable]
        
        # Caso base: terminal
        if len(derivation) == 1 and isinstance(derivation[0], str):
            return {
                "node": variable,
                "terminal": derivation[0]
            }
        
        # Caso recursivo: dos variables
        if len(derivation) == 3:
            B, C, k = derivation
            left_tree = self.build_parse_tree(i, k-1, B)
            # CORRECCIÓN: Calcular correctamente la longitud para el subárbol derecho
            length = j + 1  # j es length-1, así que length = j+1
            right_tree = self.build_parse_tree(i+k, length-k-1, C)
            return {
                "node": variable,
                "left": left_tree,
                "right": right_tree
            }
        
        return {"node": variable}
    
    def print_parse_tree_compact(self, tree: dict = None, prefix: str = "", is_tail: bool = True):
        
        if tree is None:
            tree = self.build_parse_tree()
            print("\nParse Tree:")
        
        node = tree["node"]
        
        # Elegir el conector apropiado
        connector = "└── " if is_tail else "├── "
        
        # Caso terminal
        if "terminal" in tree:
            print(f"{prefix}{connector}{node} → '{tree['terminal']}'")
            return
        
        # Caso no terminal
        print(f"{prefix}{connector}{node}")
        
        if "left" in tree and "right" in tree:
            # Calcular nuevo prefijo
            extension = "    " if is_tail else "│   "
            new_prefix = prefix + extension
            
            # Imprimir hijos
            self.print_parse_tree_compact(tree["left"], new_prefix, False)
            self.print_parse_tree_compact(tree["right"], new_prefix, True)
    
    def print_parse_tree_improved(self, indent: int = 0, tree: dict = None):
        
        if tree is None:
            tree = self.build_parse_tree()
            print("\nParse Tree:")
        
        node = tree["node"]
        prefix = "  " * indent
        
        # Caso terminal
        if "terminal" in tree:
            print(f"{prefix}└─ {node}")
            print(f"{prefix}   └─ '{tree['terminal']}'")
            return
        
        # Caso con hijos
        print(f"{prefix}└─ {node}")
        
        if "left" in tree and "right" in tree:
            # Imprimir hijo izquierdo
            print(f"{prefix}   ├─ Left:")
            self.print_parse_tree_improved(indent + 2, tree["left"])
            
            # Imprimir hijo derecho
            print(f"{prefix}   └─ Right:")
            self.print_parse_tree_improved(indent + 2, tree["right"])