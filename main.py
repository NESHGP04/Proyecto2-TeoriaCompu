"""
main.py
Programa principal para el Proyecto 2 - Teoría de la Computación
Algoritmo CYK para Parsing de Gramáticas CFG

Autores: Camila Richter 23183, Marinés García 23391, Carlos Alburez 231311
Fecha: Septiembre 2025
"""

from grammar import Grammar
from cyk_parser import CYKParser
from project_grammar import create_project_grammar


def print_header():
    """Imprime el encabezado del programa"""
    print("=" * 70)
    print("   PROYECTO 2 - TEORÍA DE LA COMPUTACIÓN")
    print("   Algoritmo CYK para Parsing de Gramáticas CFG")
    print("=" * 70)


def run_test_examples(grammar: Grammar):
    """
    Ejecuta los ejemplos de prueba requeridos por el proyecto
    
    Ejemplos incluidos:
    - 2 sintáctica y semánticamente correctas
    - 2 sintácticamente correctas pero semánticamente incorrectas
    - 2 no aceptadas por la gramática
    """
    
    # Ejemplos de prueba
    test_sentences = [
        # Sintáctica y semánticamente correctas
        ("she eats a cake with a fork", "✅ Sintáctica y semánticamente correcta"),
        ("the cat drinks the beer", "✅ Sintáctica y semánticamente correcta"),
        
        # Sintácticamente correctas, semánticamente incorrectas
        ("the fork eats a cat", "⚠️ Sintácticamente correcta, semánticamente incorrecta"),
        ("he drinks the oven", "⚠️ Sintácticamente correcta, semánticamente incorrecta"),
        
        # No aceptadas por la gramática
        ("she eats", "❌ No aceptada (incompleta)"),
        ("cat the drinks", "❌ No aceptada (orden incorrecto)")
    ]
    
    print("\n" + "=" * 70)
    print("EJEMPLOS DE PRUEBA")
    print("=" * 70)
    
    for sentence, description in test_sentences:
        print(f"\n📝 {description}")
        parser = CYKParser(grammar)
        accepted, exec_time = parser.parse(sentence)
        
        print("\n" + "-" * 70)
        if accepted:
            print(f"✅ SÍ - La sentencia es aceptada")
            print(f"⏱️  Tiempo de ejecución: {exec_time:.6f} segundos")
            
            # Construir y mostrar árbol
            tree = parser.build_parse_tree()
            parser.print_parse_tree(tree)
        else:
            print(f"❌ NO - La sentencia NO es aceptada")
            print(f"⏱️  Tiempo de ejecución: {exec_time:.6f} segundos")
        print("-" * 70)


def interactive_mode(grammar: Grammar):
    """
    Modo interactivo para probar sentencias personalizadas
    
    Permite al usuario ingresar sus propias sentencias y ver
    si son aceptadas por la gramática
    """
    print("\n" + "=" * 70)
    print("MODO INTERACTIVO")
    print("=" * 70)
    print("Ingresa tus propias sentencias para probar")
    print("(escribe 'salir' para terminar)\n")
    
    while True:
        sentence = input("📝 Ingresa una sentencia: ").strip()
        
        if sentence.lower() in ['salir', 'exit', 'quit', 'q']:
            print("\n👋 ¡Hasta luego!")
            break
        
        if not sentence:
            continue
        
        parser = CYKParser(grammar)
        accepted, exec_time = parser.parse(sentence)
        
        print("\n" + "-" * 70)
        if accepted:
            print(f"✅ SÍ - La sentencia es aceptada")
            print(f"⏱️  Tiempo de ejecución: {exec_time:.6f} segundos")
            
            tree = parser.build_parse_tree()
            parser.print_parse_tree(tree)
        else:
            print(f"❌ NO - La sentencia NO es aceptada")
            print(f"⏱️  Tiempo de ejecución: {exec_time:.6f} segundos")
        print("-" * 70 + "\n")


def main():
    """
    Función principal del programa
    
    Flujo:
    1. Crear gramática del proyecto
    2. Convertir a CNF
    3. Ejecutar ejemplos de prueba
    4. Modo interactivo
    """
    # Imprimir encabezado
    print_header()
    
    # Crear gramática del proyecto
    print("\n📚 Cargando gramática del proyecto...")
    grammar = create_project_grammar()
    
    # Convertir a CNF
    grammar.to_cnf()
    
    # Ejecutar ejemplos de prueba
    run_test_examples(grammar)
    
    # Modo interactivo
    interactive_mode(grammar)


if __name__ == "__main__":
    main()