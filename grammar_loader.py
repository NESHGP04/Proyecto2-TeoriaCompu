
from grammar import Grammar


def load_grammar_from_file(filename: str) -> Grammar:
  
    print(f"\nCargando gramática desde '{filename}'...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError(f"❌ No se encontró el archivo '{filename}'")
    
    grammar = Grammar()
    line_number = 0
    rules_loaded = 0
    
    for line in lines:
        line_number += 1
        
        # Limpiar espacios en blanco
        line = line.strip()
        
        # Ignorar líneas vacías o comentarios
        if not line or line.startswith('#'):
            continue
        
        # Verificar que tenga el formato correcto
        if '->' not in line:
            raise ValueError(
                f"Error en línea {line_number}: '{line}'\n"
                f"   Formato esperado: Variable -> produccion1 | produccion2"
            )
        
        # Dividir en variable y producciones
        parts = line.split('->')
        if len(parts) != 2:
            raise ValueError(
                f"Error en línea {line_number}: '{line}'\n"
                f"   Debe haber exactamente una flecha '->'"
            )
        
        variable = parts[0].strip()
        productions_str = parts[1].strip()
        
        # Validar que la variable no esté vacía
        if not variable:
            raise ValueError(
                f"Error en línea {line_number}: La variable está vacía"
            )
        
        # Dividir las producciones por |
        productions_list = productions_str.split('|')
        
        # Procesar cada producción
        for production_str in productions_list:
            production_str = production_str.strip()
            
            if not production_str:
                continue
            
            # Dividir la producción en símbolos (por espacios)
            symbols = production_str.split()
            
            # Agregar la regla a la gramática
            grammar.add_rule(variable, symbols)
            rules_loaded += 1
            
            print(f"  ✓ {variable} -> {' '.join(symbols)}")
    
    print(f"\nGramática cargada exitosamente:")
    print(f"   - {len(grammar.variables)} variables")
    print(f"   - {len(grammar.terminals)} terminales")
    print(f"   - {rules_loaded} reglas")
    
    return grammar


def load_grammar_from_string(grammar_text: str) -> Grammar:
   
    print("\nCargando gramática desde texto...")
    
    grammar = Grammar()
    lines = grammar_text.strip().split('\n')
    rules_loaded = 0
    
    for line_number, line in enumerate(lines, 1):
        line = line.strip()
        
        if not line or line.startswith('#'):
            continue
        
        if '->' not in line:
            continue
        
        parts = line.split('->')
        if len(parts) != 2:
            continue
        
        variable = parts[0].strip()
        productions_str = parts[1].strip()
        
        productions_list = productions_str.split('|')
        
        for production_str in productions_list:
            production_str = production_str.strip()
            
            if not production_str:
                continue
            
            symbols = production_str.split()
            grammar.add_rule(variable, symbols)
            rules_loaded += 1
    
    print(f"{rules_loaded} reglas cargadas")
    
    return grammar


# Función de conveniencia para cargar la gramática del proyecto
def load_project_grammar(filename: str = "grammar.txt") -> Grammar:
    """
    Carga la gramática del proyecto desde un archivo
    
    Args:
        filename: Nombre del archivo (por defecto 'grammar.txt')
        
    Returns:
        Grammar: Gramática cargada y lista para usar
    """
    return load_grammar_from_file(filename)