from grammar import Grammar
from cyk_parser import CYKParser
from project_grammar import create_project_grammar


def print_header():
    print("=" * 70)
    print("   PROYECTO 2 - TEORIA DE LA COMPUTACION")
    print("   Algoritmo CYK para Parsing de Gramaticas CFG")
    print("=" * 70)


def mostrar_menu():
    print("\n" + "=" * 70)
    print("MENU PRINCIPAL")
    print("=" * 70)
    print("1. Ejecutar ejemplos de prueba predefinidos")
    print("2. Modo interactivo (ingresar sentencias)")
    print("3. Salir")
    print("=" * 70)


def ejecutar_ejemplos(grammar):
    
    # Ejemplos de prueba del proyecto
    ejemplos = [
        ("she eats a cake with a fork", "Sintactica y semanticamente correcta"),
        ("the cat drinks the beer", "Sintactica y semanticamente correcta"),
        ("the fork eats a cat", "Sintacticamente correcta, semanticamente incorrecta"),
        ("he drinks the oven", "Sintacticamente correcta, semanticamente incorrecta"),
        ("she eats", "No aceptada (incompleta)"),
        ("cat the drinks", "No aceptada (orden incorrecto)")
    ]
    
    print("\n" + "=" * 70)
    print("EJEMPLOS DE PRUEBA")
    print("=" * 70)
    
    for sentencia, descripcion in ejemplos:
        print(f"\n{descripcion}")
        parser = CYKParser(grammar)
        es_aceptada, tiempo = parser.parse(sentencia)
        
        print("\n" + "-" * 70)
        if es_aceptada:
            print(f"SI - La sentencia es aceptada")
            print(f"Tiempo de ejecucion: {tiempo:.6f} segundos")
            
            arbol = parser.build_parse_tree()
            parser.print_parse_tree_compact(arbol)
        else:
            print(f"NO - La sentencia NO es aceptada")
            print(f"Tiempo de ejecucion: {tiempo:.6f} segundos")
        print("-" * 70)
    
    print("\nEjemplos completados!")
    input("\nPresiona Enter para volver al menu principal...")


def modo_interactivo(grammar):
    print("\n" + "=" * 70)
    print("MODO INTERACTIVO")
    print("=" * 70)
    print("Ingresa tus propias sentencias para probar")
    print("(escribe 'salir' o 'menu' para volver al menu principal)\n")
    
    while True:
        sentencia = input("\nIngresa una sentencia: ").strip()
        
        if sentencia.lower() in ['salir', 'exit', 'quit', 'q', 'menu']:
            print("\nVolviendo al menu principal...")
            break
        
        if not sentencia:
            print("Por favor ingresa una sentencia valida")
            continue
        
        parser = CYKParser(grammar)
        es_aceptada, tiempo = parser.parse(sentencia)
        
        print("\n" + "-" * 70)
        if es_aceptada:
            print(f"SI - La sentencia es aceptada")
            print(f"Tiempo de ejecucion: {tiempo:.6f} segundos")
            
            arbol = parser.build_parse_tree()
            parser.print_parse_tree_compact(arbol)
        else:
            print(f"NO - La sentencia NO es aceptada")
            print(f"Tiempo de ejecucion: {tiempo:.6f} segundos")
        print("-" * 70)


# Programa principal
print_header()

print("\nCargando gramatica del proyecto...")
gramatica = create_project_grammar()

# Convertir a CNF
gramatica.to_cnf()

# Loop del menu
while True:
    mostrar_menu()
    
    try:
        opcion = input("\nSelecciona una opcion (1-3): ").strip()
        
        if opcion == '1':
            ejecutar_ejemplos(gramatica)
        
        elif opcion == '2':
            modo_interactivo(gramatica)
        
        elif opcion == '3':
            print("\n" + "=" * 70)
            print("Gracias por usar el parser CYK!")
            print("=" * 70)
            break
        
        else:
            print("\nOpcion invalida. Por favor selecciona 1, 2 o 3.")
            input("Presiona Enter para continuar...")
    
    except KeyboardInterrupt:
        print("\n\nHasta luego!")
        break
    except Exception as error:
        print(f"\nError: {error}")
        input("Presiona Enter para continuar...")