from grammar import Grammar
from cyk_parser import CYKParser
from grammar_loader import load_grammar_from_file
from project_grammar import create_project_grammar
import os


def print_header():
    print("=" * 70)
    print("   PROYECTO 2 - TEORIA DE LA COMPUTACION")
    print("   Algoritmo CYK para Parsing de Gramaticas CFG")
    print("=" * 70)


def mostrar_menu_gramatica():
    print("\n" + "=" * 70)
    print("SELECCIONAR GRAMATICA")
    print("=" * 70)
    print("1. Cargar gramática desde archivo 'grammar.txt'")
    print("2. Usar gramática predefinida del proyecto (código)")
    print("=" * 70)


def cargar_gramatica():
    while True:
        mostrar_menu_gramatica()
        
        try:
            opcion = input("\nSelecciona una opción (1-2): ").strip()
            
            if opcion == '1':
                if not os.path.exists('grammar.txt'):
                    print("\nEl archivo 'grammar.txt' no existe.")
                    print("    Puedes crearlo o usar la opción 2.")
                    input("\nPresiona Enter para continuar...")
                    continue
                
                return load_grammar_from_file('grammar.txt'), True
            
            elif opcion == '2':
                print("\nCargando gramática predefinida del proyecto...")
                return create_project_grammar(), False
            
            else:
                print("\nOpción inválida. Por favor selecciona 1 o 2.")
                input("Presiona Enter para continuar...")
        
        except Exception as e:
            print(f"\nError al cargar la gramática: {e}")
            input("\nPresiona Enter para continuar...")


def mostrar_menu_principal(desde_archivo):
    print("\n" + "=" * 70)
    print("MENU PRINCIPAL")
    print("=" * 70)
    
    # si es la gramatica del proyecto, mostrar los ejemplos
    if not desde_archivo:
        print("1. Ejecutar ejemplos de prueba predefinidos")
        print("2. Modo interactivo (ingresar sentencias)")
        print("3. Cambiar gramática")
        print("4. Ver gramática actual en CNF")
        print("5. Salir")
    else:
        # si cargamos desde archivo, mejor no mostrar ejemplos
        print("1. Modo interactivo (ingresar sentencias)")
        print("2. Cambiar gramática")
        print("3. Ver gramática actual en CNF")
        print("4. Salir")
    
    print("=" * 70)


def ejecutar_ejemplos(grammar):
    # ejemplos de frases para probar con la gramatica del proyecto
    ejemplos = [
        ("she eats a cake with a fork", "Sintactica y semanticamente correcta"),
        ("the cat drinks the beer", "Sintactica y semanticamente correcta"),
        ("the fork eats a cat", "Sintacticamente correcta, semanticamente incorrecta"),
        ("he drinks the oven", "Sintacticamente correcta, semanticamente incorrecta"),
        ("cat the drinks", "No aceptada (orden incorrecto)"),
        ("eats she a cake", "No aceptada (verbo antes del sujeto)")
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


def ver_gramatica_cnf(grammar):
    print("\n" + "=" * 70)
    print("GRAMATICA ACTUAL EN CNF")
    print("=" * 70)
    
    grammar._print_cnf_grammar()
    
    print("\n" + "=" * 70)
    input("\nPresiona Enter para volver al menu principal...")


# programa principal
print_header()

gramatica, desde_archivo = cargar_gramatica()
gramatica.to_cnf()

# loop principal del programa
while True:
    mostrar_menu_principal(desde_archivo)
    
    try:
        opcion = input("\nSelecciona una opcion: ").strip()
        
        # menu cuando se usa la gramatica predefinida
        if not desde_archivo:
            if opcion == '1':
                ejecutar_ejemplos(gramatica)
            elif opcion == '2':
                modo_interactivo(gramatica)
            elif opcion == '3':
                gramatica, desde_archivo = cargar_gramatica()
                gramatica.to_cnf()
            elif opcion == '4':
                ver_gramatica_cnf(gramatica)
            elif opcion == '5':
                print("\n" + "=" * 70)
                print("Gracias por usar el parser CYK!")
                print("=" * 70)
                break
            else:
                print("\nOpcion invalida. Por favor selecciona 1-5.")
                input("Presiona Enter para continuar...")
        
        # menu cuando se carga desde archivo
        else:
            if opcion == '1':
                modo_interactivo(gramatica)
            elif opcion == '2':
                gramatica, desde_archivo = cargar_gramatica()
                gramatica.to_cnf()
            elif opcion == '3':
                ver_gramatica_cnf(gramatica)
            elif opcion == '4':
                print("\n" + "=" * 70)
                print("Gracias por usar el parser CYK!")
                print("=" * 70)
                break
            else:
                print("\nOpcion invalida. Por favor selecciona 1-4.")
                input("Presiona Enter para continuar...")
    
    except KeyboardInterrupt:
        print("\n\nHasta luego!")
        break
    except Exception as error:
        print(f"\nError: {error}")
        input("Presiona Enter para continuar...")