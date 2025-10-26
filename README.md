# Proyecto 2 - Teoría de la Computación 2025
## Algoritmo CYK para Parsing de Gramáticas CFG

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Academic-green.svg)]()

---

## 📋 Descripción

Este proyecto implementa el **algoritmo CYK (Cocke-Younger-Kasami)** para realizar el parsing de frases simples en inglés utilizando una gramática libre de contexto (CFG). El proyecto incluye la conversión automática de gramáticas CFG a su **Forma Normal de Chomsky (CNF)** y la construcción del árbol de derivación (parse tree).

### Características Principales

- ✅ Conversión automática de CFG a Forma Normal de Chomsky (CNF)
- ✅ Implementación del algoritmo CYK con programación dinámica
- ✅ Construcción y visualización del parse tree
- ✅ Medición del tiempo de ejecución del algoritmo
- ✅ Modo interactivo y ejemplos predefinidos
- ✅ Interfaz de línea de comandos amigable

---

## 📁 Estructura del Proyecto

```
Archivo.zip
│
├── main.py                 # Programa principal con interfaz de usuario
├── grammar.py              # Clase Grammar para representar y manipular CFGs
├── cyk_parser.py          # Implementación del algoritmo CYK
├── project_grammar.py     # Definición de la gramática del proyecto
└── README.md              # Este archivo
```

---

## 🎯 Gramática del Proyecto

La gramática utilizada permite analizar frases simples en inglés con la siguiente estructura:

```
S   → NP VP
VP  → VP PP | V NP | cooks | drinks | eats | cuts
PP  → P NP
NP  → Det N | he | she
V   → cooks | drinks | eats | cuts
P   → in | with
N   → cat | dog | beer | cake | juice | meat | soup | fork | knife | oven | spoon
Det → a | the
```

---

## 🚀 Instalación y Uso

### Requisitos

- Python 3.7 o superior
- No requiere librerías externas (solo bibliotecas estándar de Python)

### Ejecución

1. **Extraer el archivo ZIP**
   ```bash
   unzip Archivo.zip
   cd Archivo
   ```

2. **Ejecutar el programa**
   ```bash
   python main.py
   ```

3. **Seleccionar una opción del menú:**
   - **Opción 1**: Ejecutar ejemplos predefinidos
   - **Opción 2**: Modo interactivo (ingresar tus propias sentencias)
   - **Opción 3**: Salir

---

## 📝 Ejemplos de Uso

### Ejemplos de Sentencias Aceptadas

#### ✅ Sintáctica y Semánticamente Correctas

1. **"she eats a cake with a fork"**
   - ✓ Estructura gramatical válida
   - ✓ Tiene sentido semántico
   - Tiempo de ejecución: ~0.001s

2. **"the cat drinks the beer"**
   - ✓ Estructura gramatical válida
   - ✓ Tiene sentido semántico
   - Tiempo de ejecución: ~0.001s

#### ⚠️ Sintácticamente Correctas pero Semánticamente Incorrectas

3. **"the fork eats a cat"**
   - ✓ Estructura gramatical válida
   - ✗ No tiene sentido semántico (un tenedor no puede comer)

4. **"he drinks the oven"**
   - ✓ Estructura gramatical válida
   - ✗ No tiene sentido semántico (no se puede beber un horno)

### Ejemplos de Sentencias NO Aceptadas

5. **"she eats"**
   - ✗ Frase incompleta (falta objeto directo)

6. **"cat the drinks"**
   - ✗ Orden incorrecto de palabras

---

## 🛠️ Implementación Técnica

### Conversión a CNF (Forma Normal de Chomsky)

El algoritmo implementa los siguientes pasos:

1. **Eliminación de reglas unitarias** (A → B)
2. **Conversión de reglas terminales** (creación de variables auxiliares T_x)
3. **Binarización de reglas** (división de producciones con más de 2 símbolos)

**Ejemplo de conversión:**
```
Original:  VP → V NP PP
CNF:       VP → V X0
           X0 → NP PP
```

### Algoritmo CYK

- **Complejidad temporal**: O(n³ · |G|), donde n es la longitud de la sentencia y |G| es el tamaño de la gramática
- **Técnica**: Programación dinámica con tabla bidimensional
- **Tabla CYK**: `table[i][j]` contiene las variables que pueden derivar la subcadena desde la posición `i` con longitud `j+1`

### Construcción del Parse Tree

El árbol de derivación se construye simultáneamente durante el proceso CYK, almacenando:
- Nodos terminales (palabras)
- Nodos no terminales (variables)
- Referencias a subárboles izquierdo y derecho

---

## 📊 Ejemplo de Salida

```
Analizando: 'she eats a cake with a fork'
   Tokens: ['she', 'eats', 'a', 'cake', 'with', 'a', 'fork']
   Longitud: 7 palabras

Llenando tabla CYK...
  Posición 0 ('she'): {'NP'}
  Posición 1 ('eats'): {'V', 'VP'}
  Posición 2 ('a'): {'Det'}
  ...

----------------------------------------------------------------------
✓ SÍ - La sentencia es aceptada
Tiempo de ejecución: 0.002341 segundos

Parse Tree:
└── S
    ├── Left:
       └─ NP
          └─ 'she'
    └── Right:
       └─ VP
          ├─ Left:
             └─ VP
                ├─ Left:
                   └─ V
                      └─ 'eats'
                └─ Right:
                   └─ NP
                      ...
```

## 📚 Referencias

- [CFG to CNF Converter](https://devimam.github.io/cfgtocnf/)
- [CYK Algorithm - Wikipedia](https://en.wikipedia.org/wiki/CYK_algorithm)
- [GeeksforGeeks - CYK Algorithm](https://www.geeksforgeeks.org/cyk-algorithm-for-context-free-grammar/)
- [UC Davis - CYK Tutorial](https://web.cs.ucdavis.edu/~rogaway/classes/120/winter12/CYK.pdf)

---

## 👨‍💻 Autor

**Proyecto 2 - Teoría de la Computación**  
Universidad del Valle de Guatemala  
Septiembre - Octubre 2025
Camila Richter 23183
Marinés García 23391
Carlos Alburez 231311

---

## 📄 Licencia

Este proyecto es parte de un curso académico y está destinado únicamente para fines educativos.

## ⚠️ Notas Importantes

- Las frases aceptadas son **sintácticamente correctas** pero no necesariamente **semánticamente correctas**
- El algoritmo requiere que la gramática esté en Forma Normal de Chomsky (CNF)
- La conversión a CNF se realiza automáticamente al iniciar el programa
- El tiempo de ejecución puede variar según la longitud de la sentencia

---