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
    for s, d in grid_values(grid).items():
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
    assert len(chars) == 81
    # regresa un diccionario que tiene como llave el recuadro
    # y como valor el carater que le
    return dict(zip(squares, chars))

def search(values):
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  # Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values  # Solved!
    # Chose the unfilled square s with the fewest possibilities
    n, s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(search(assign(values.copy(), s, d))for d in values[s])


def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e:
            return e
    return False


def display(values):
    "Display these values as a 2-D grid."
    width = 1+max(len(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print("".join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF':
            print line
    print

def solve(grid): return search(parse_grid(grid))


display(solve(example0))