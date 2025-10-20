"""
cyk_parser.py
Implementación del algoritmo CYK (Cocke-Younger-Kasami) para parsing de CFG
Proyecto 2 - Teoría de la Computación
"""

import time
from typing import Tuple
from grammar import Grammar


class CYKParser:
    """Implementa el algoritmo CYK para parsing"""
    
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.table = None
        self.parse_tree = None
    
    def parse(self, sentence: str) -> Tuple[bool, float]:
        """
        Ejecuta el algoritmo CYK para determinar si la sentencia pertenece al lenguaje
        
        Args:
            sentence: La sentencia a analizar
            
        Returns:
            Tuple con (aceptada: bool, tiempo_ejecución: float)
        """
        start_time = time.time()
        
        # Tokenizar la sentencia
        words = sentence.lower().split()
        n = len(words)
        
        print(f"\n🔍 Analizando: '{sentence}'")
        print(f"   Tokens: {words}")
        print(f"   Longitud: {n} palabras\n")
        
        # Inicializar tabla CYK (programación dinámica)
        # table[i][j] contiene el conjunto de variables que pueden derivar
        # la subcadena desde posición i con longitud j+1
        self.table = [[set() for _ in range(n)] for _ in range(n)]
        self.parse_tree = [[{} for _ in range(n)] for _ in range(n)]
        
        # Paso 1: Llenar la diagonal (subcadenas de longitud 1)
        print("📊 Llenando tabla CYK...")
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
    
    def build_parse_tree(self, i: int = 0, j: int = None, variable: str = None) -> str:
        """
        Construye y retorna el árbol de parsing como string
        
        Args:
            i: Posición inicial en la tabla
            j: Longitud - 1 en la tabla
            variable: Variable a expandir
            
        Returns:
            String representando el árbol de parsing
        """
        if j is None:
            j = len(self.table) - 1
        if variable is None:
            variable = self.grammar.start_symbol
        
        if variable not in self.parse_tree[i][j]:
            return f"{variable}(?)"
        
        derivation = self.parse_tree[i][j][variable]
        
        # Caso base: terminal
        if len(derivation) == 1 and isinstance(derivation[0], str):
            return f"{variable}({derivation[0]})"
        
        # Caso recursivo: dos variables
        if len(derivation) == 3:
            B, C, k = derivation
            left_tree = self.build_parse_tree(i, k-1, B)
            right_tree = self.build_parse_tree(i+k, j-k, C)
            return f"{variable}[{left_tree}, {right_tree}]"
        
        return f"{variable}"
    
    def print_parse_tree(self, tree_str: str, indent: int = 0):
        """
        Imprime el árbol de parsing de forma legible
        
        Args:
            tree_str: String del árbol generado por build_parse_tree()
            indent: Nivel de indentación (para recursión)
        """
        print("\n🌳 Parse Tree:")
        self._print_tree_recursive(tree_str, indent)
    
    def _print_tree_recursive(self, tree_str: str, indent: int = 0):
        """Imprime recursivamente el árbol"""
        if '(' in tree_str:
            # Terminal: Variable(terminal)
            var, rest = tree_str.split('(', 1)
            terminal = rest.rstrip(')')
            print("  " * indent + f"├─ {var}")
            print("  " * indent + f"│  └─ '{terminal}'")
        
        elif '[' in tree_str:
            # No terminal: Variable[left, right]
            var, rest = tree_str.split('[', 1)
            print("  " * indent + f"├─ {var}")
            
            # Dividir left y right
            bracket_count = 0
            split_pos = 0
            for i, char in enumerate(rest):
                if char == '[':
                    bracket_count += 1
                elif char == ']':
                    bracket_count -= 1
                elif char == ',' and bracket_count == 0:
                    split_pos = i
                    break
            
            left = rest[:split_pos]
            right = rest[split_pos+2:-1]  # +2 para saltar ", "
            
            self._print_tree_recursive(left, indent + 1)
            self._print_tree_recursive(right, indent + 1)