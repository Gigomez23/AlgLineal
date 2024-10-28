"""
Archivo: clase_matriz_fact_LU.py 1.0.0
Descripción: Este archivo contiene la clase de gestión de calculos para encontra Ax=b por LU.
"""
from fractions import Fraction


class LUFactorization:
    def __init__(self, matrix_A, vector_b):
        """
        Clase para realizar la factorización LU de una matriz y resolver Ax = b.

        Args:
            matrix_A (list of list of str): Matriz A (en formato de fracción).
            vector_b (list of str): Vector b (en formato de fracción).
        """
        # Almacena la matriz y el vector original
        self.original_matrix_A = matrix_A
        self.original_vector_b = vector_b
        self.L = None
        self.U = None
        self.solution_x = None
        self.steps = []  # Almacena los pasos intermedios

    def format_matrix(self, matrix):
        """Devuelve la matriz en formato de string legible con fracciones."""
        return '\n'.join(['\t'.join([self.format_fraction(element) for element in row]) for row in matrix])

    def format_vector(self, vector):
        """Devuelve el vector en formato de string legible con fracciones."""
        return '\t'.join([self.format_fraction(element) for element in vector])

    def format_fraction(self, number):
        """Devuelve un número en formato de fracción si no es entero."""
        if number.denominator == 1:
            return str(number.numerator)  # Si es entero, solo mostrar el numerador
        else:
            return f"{number.numerator}/{number.denominator}"  # Mostrar como fracción

    def lu_decomposition(self):
        """Realiza la factorización LU de la matriz A sin numpy y guarda los pasos."""
        n = len(self.original_matrix_A)
        L = [[Fraction(0) if i != j else Fraction(1) for j in range(n)] for i in range(n)]  # Matriz identidad
        U = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        A = [row[:] for row in self.original_matrix_A]  # Copia de la matriz original

        # Guardar pasos iniciales
        self.steps.append("Matriz A:\n" + self.format_matrix(self.original_matrix_A))

        # Método de Doolittle para la factorización LU
        for i in range(n):
            # Almacenar valores de U
            for j in range(i, n):
                U[i][j] = A[i][j] - sum(L[i][k] * U[k][j] for k in range(i))

            # Almacenar valores de L
            for j in range(i + 1, n):
                L[j][i] = (A[j][i] - sum(L[j][k] * U[k][i] for k in range(i))) / U[i][i]

        self.L = L
        self.U = U

        # Guardar pasos
        self.steps.append("\nFactorización LU:\n")
        self.steps.append("L:\n" + self.format_matrix(L))
        self.steps.append("U:\n" + self.format_matrix(U))

    def forward_substitution(self, L, b):
        """Resuelve Ly = b mediante sustitución hacia adelante."""
        n = len(L)
        y = [Fraction(0) for _ in range(n)]
        for i in range(n):
            # Cambiar b[i] a b[i][0] para acceder al valor de la fracción dentro de la lista
            y[i] = b[i][0] - sum(L[i][j] * y[j] for j in range(i))
        return y

    def backward_substitution(self, U, y):
        """Resuelve Ux = y mediante sustitución hacia atrás."""
        n = len(U)
        x = [Fraction(0) for _ in range(n)]
        for i in range(n - 1, -1, -1):
            x[i] = (y[i] - sum(U[i][j] * x[j] for j in range(i + 1, n))) / U[i][i]
        return x

    def solve(self):
        """Resuelve el sistema de ecuaciones Ax = b usando la factorización LU."""
        self.lu_decomposition()

        # Resolver Ly = b
        y = self.forward_substitution(self.L, self.original_vector_b)
        self.steps.append(f"\nSolución intermedia (y) resolviendo Ly = b:\n{self.format_vector(y)}")

        # Resolver Ux = y
        x = self.backward_substitution(self.U, y)
        self.solution_x = [Fraction(xi).limit_denominator() for xi in x]

        self.steps.append(f"\nSolución final (x) resolviendo Ux = y:\n{self.format_vector(self.solution_x)}")
        return self.solution_x

    def get_original_data(self):
        """Devuelve la matriz y vector originales."""
        return self.original_matrix_A, self.original_vector_b

    def get_solution(self):
        """Devuelve la solución del sistema Ax = b."""
        return self.solution_x

    def get_steps(self):
        """Devuelve el proceso paso a paso como un string."""
        return "\n\n".join(self.steps)
