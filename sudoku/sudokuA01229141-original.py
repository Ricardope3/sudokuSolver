import time


def cross(A, B):
    "Cross product of elements in A and elements in B."
    "Hace un doble for anidado para concatenar cada elemento de A con cada elemento de B"
    return [a+b for a in A for b in B]


# Inicializa el string con todos los digitos
digits = '123456789'
# Inicializa las filas con 9 letras
rows = 'ABCDEFGHI'
# Inicializa las columnas como el string de digitos
cols = digits
# Inicializa todos los recuadros
squares = cross(rows, cols)
# Unit list es una lista que contiene listas de las columnas y filas del sudoku
# y tambien tiene todos los cuadrados
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
# Units es un diccionario que tiene como llave un recuadro y su valor es una lista de tres listas
# Cada lista es una unidad diferente (fila, columna,)
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
# Peers es un diccionario, la llave es un recuadro, el valor es un set que contiene
# todos los demas valores de las unidades que comparte ese recuadro sin repetidos y sin la llave
peers = dict((s, set(sum(units[s], []))-set([s])) for s in squares)
# Esta es una representacion del sudoku que las siguientes funcines
# podran parcear
example0 = """
4 . . |. . . |8 . 5
. 3 . |. . . |. . .
. . . |7 . . |. . .
------+------+------
. 2 . |. . . |. 6 .
. . . |. 8 . |4 . .
. . . |. 1 . |. . .
------+------+------
. . . |6 . 3 |. 7 .
5 . . |2 . . |. . .
1 . 4 |. . . |. . .
"""
# Inicializa funcion assign


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    # Los valores s no puede tomar porque s ya lo es
    other_values = values[s].replace(d, '')
    # Basicamente si el sudoku es congruente regresa los valores para
    # que sea como un "True"
    if all(eliminate(values, s, d2) for d2 in other_values):
        # Regresar values
        return values
    else:
        # Regresar falso
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    # Si el digito que no esta queremos, no esta entre los digitos de
    # s entonces significa que ese numero es valido
    if d not in values[s]:
        # Regresar values
        return values  # Already eliminated
    # Quita a d de values[s]
    values[s] = values[s].replace(d, '')
    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    # si ya nos quedamos sin valores entonces no es congruente
    if len(values[s]) == 0:
        return False  # Contradiction: removed last value
    # si el length es de uno entonces d2 se vuelve ese valor
    elif len(values[s]) == 1:
        d2 = values[s]
    # Para todo los peers de s elimina este valor d2
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            # Si no se pudo entonces regresa falso
            return False
    # (2) If a unit u is reduced to only one place for a value d, then put it there.
    # Para todas las unidades d s
    for u in units[s]:
        # Hace un arreglo dplaces con todos los recuadros de dicha unidad
        # solo si para el digito actual no esta entre los valores posibles de s
        dplaces = [s for s in u if d in values[s]]
        # si ya nos quedamos sin valores entonces no es congruente
        if len(dplaces) == 0:
            # regresamos false
            return False  # Contradiction: no place for this value
        # Si hay uno entonces intenta asignarlo
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            # Intentamos asignarlo, si no se puede entonces el sudoku es incongruente
            if not assign(values, dplaces[0], d):
                return False
    # regresamos los valores
    return values


def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    # To start, every square can be any digit; then assign values from the grid.
    # values es un diccionario, la llave es cada recuadro
    # el valor es todos los digitos
    values = dict((s, digits) for s in squares)
    # Itera en todos las llaves y valores del input grid parceado
    for s, d in list(grid_values(grid).items()):
        # primero ve si d es un digito excepto el 0
        # luego ve si el sudoku que se dio como input es invalido
        if d in digits and not assign(values, s, d):
            return False  # (Fail if we can't assign d to square s.)
    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    # Itera en todos los caracteres del input grid
    # genera un arreglo con los digitos o vacios que en orden
    chars = [c for c in grid if c in digits or c in '0.']
    # Se sersiora que si tenga un caracter para cada recuadro
    # regresa un diccionario que tiene como llave el recuadro
    # y como valor el carater que le
    return dict(list(zip(squares, chars)))


def search(values):
    "Using depth-first search and propagation, try all possible values."
    # Si valores es falso
    if values is False:
        # Regresar falso
        return False  # Failed earlier
    # Si todos los recuadros solo tienen un valor
    # entonces ya esta resuelto
    if all(len(values[s]) == 1 for s in squares):
        return values  # Solved!
    # Chose the unfilled square s with the fewest possibilities
    # Mediante MRV busca los recuadros con menores posibilidades
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    # Recursivamente buscar los valores si puedes asignar cualquiera de los valores posibles
    # de s
    return some(search(assign(values.copy(), s, d))for d in values[s])


def some(seq):
    "Return some element of seq that is true."
    # recorra la secuencia
    for e in seq:
        # Si el valor es truthly lo regres
        if e:
            return e
    #De no ser asi, regresa falso
    return False


def display(values):
    "Display these values as a 2-D grid."
    # Calcula la anchura del sudoku
    width = 1+max(len(values[s]) for s in squares)
    # Crea un string que es la linea
    # Que divide los cuadros
    line = '+'.join(['-'*(width*3)]*3)
    # Itera en filas
    for r in rows:
        #Imprime una fila del sudoku
        print(("".join(values[r+c].center(width) +
                       ('|' if c in '36' else '') for c in cols)))
        # Para la fila C y F imprime una linea extra que es
        # la que separa tres filas
        if r in 'CF':
            print(line)
    #Imprime un salto de linea
    print()


# Resuelve el sudoku buscando las combinaciones
def solve(grid): return search(parse_grid(grid))

#----------------------------------------------#
easy = """
5 4 7 |. . . |. 9 1
. . 3 |9 2 1 |. . 7
. . . |5 . 4 |. 6 3
------+------+------
. . . |. . . |9 . 5
. 9 . |8 . 6 |. 7 .
8 . 2 |. . . |. . .
------+------+------
9 5 . |3 . 8 |. . .
3 . . |2 9 7 |1 . .
7 2 . |. . . |4 3 9
"""
start = time.time()
display(solve(easy))
end = time.time()
print("Tiempo del easy",(end - start)*1000)
#----------------------------------------------#
medium = """
6 3 . |. 5 . |8 9 .
. 7 9 |. 2 . |. . 6
. 8 . |. . . |. 4 .
------+------+------
3 4 8 |. . 5 |. . .
. . . |. 3 . |. . .
. . . |7 . . |6 8 3
------+------+------
. 5 . |. . . |. 6 .
1 . . |. 4 . |5 3 .
. 6 4 |. 8 . |. 1 2
"""
start = time.time()
display(solve(medium))
end = time.time()
print("Tiempo del medium",(end - start)*1000)
#----------------------------------------------#
hard = """
. . . |. . 2 |. . .
. 4 3 |. . . |. . 1
. 6 . |8 3 . |. 9 .
------+------+------
6 . 5 |. . 3 |. 7 .
. . 9 |. . . |1 . .
. 8 . |2 . . |9 . 5
------+------+------
. 7 . |. 8 9 |. 5 .
5 . . |. . . |4 3 .
. . . |4 . . |. . .
"""
start = time.time()
display(solve(hard))
end = time.time()
print("Tiempo del hard",(end - start)*1000)
#----------------------------------------------#
evil = """
. . 7 |6 . . |. 9 .
. . . |2 . 1 |. . .
. . . |. 5 3 |. . 1
------+------+------
2 . 4 |. . . |3 7 .
6 . . |. . . |. . 9
. 9 8 |. . . |1 . 4
------+------+------
9 . . |3 2 . |. . .
. . . |4 . 7 |. . .
. 3 . |. . 6 |5 . .
"""
start = time.time()
display(solve(evil))
end = time.time()
print("Tiempo del evil",(end - start)*1000)
#----------------------------------------------#
hardest = """
8 . . |. . . |. . .
. . 3 |6 . . |. . .
. 7 . |. 9 . |2 . .
------+------+------
. 5 . |. . 7 |. . .
. . . |. 4 5 |7 . .
. . . |1 . . |. 3 .
------+------+------
. . 1 |. . . |. 6 .
. . 8 |5 . . |. . .
. 9 . |. . . |. . .
"""
start = time.time()
display(solve(hardest))
end = time.time()
print("Tiempo del hardest",(end - start)*1000)
#----------------------------------------------#
otro = """
. . . |. . 6 |. . .
. 5 9 |. . . |. . 8
2 . . |. . 8 |. . .
------+------+------
. 4 5 |. . . |. . .
. . 3 |. . . |. . .
. . 6 |. . 3 |. 5 4
------+------+------
. . . |3 2 5 |. . 6
. . . |. . . |. . .
. . . |. . . |. . .
"""
start = time.time()
display(solve(otro))
end = time.time()
print("Tiempo del otro", (end - start)*1000)
#----------------------------------------------#
