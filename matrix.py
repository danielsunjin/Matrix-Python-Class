#my custom matrix class

class Matrix:
    def __init__(self, rows):
        if isinstance(rows, list):
            if all(isinstance(i, int) or isinstance(i, float) for i in rows):
                self.m = len(rows)
                self.n = 1
                self.rows = [[j] for j in rows]
            elif all(isinstance(i, list) for i in rows):
                cols = len(rows[0])
                if all(len(k) == cols for k in rows):
                    if all(all(isinstance(l, int) or isinstance(l, float) for l in h) for h in rows):
                        self.m = len(rows)
                        self.n = cols
                        self.rows = rows
                    else:
                        raise TypeError("All elements in the rows must be numbers")
                else:
                    raise ValueError('All matrix rows must be of the same length')
            else:
                raise TypeError('Elements within the initializing list argument must either all be numbers or all be lists of numbers')
        else:
            raise TypeError('Matrices must be initialized using lists')

    def Identity(dimension):
        if isinstance(dimension, int):
            res_matrix = []
            for i in range(dimension):
                res_row = []
                for j in range(dimension):
                    if j == i:
                        res_row.append(1)
                    else:
                        res_row.append(0)
                res_matrix.append(res_row)
            return Matrix(res_matrix)
        else:
            raise TypeError('The argument must be an integer')

    def __str__(self):
        str_columns = []
        for i in range(self.n):
            max_len = 0
            for j in self.rows:
                if isinstance(j[i], float):
                    if len('{:.2f}'.format(j[i])) > max_len:
                        max_len = len('{:.2f}'.format(j[i]))
                else:
                    if len(str(j[i])) > max_len:
                        max_len = len(str(j[i]))
            str_column = []
            for j in self.rows:
                if isinstance(j[i], float):
                    str_column.append('{:.2f}'.format(j[i]).ljust(max_len))
                else:
                    str_column.append(str(j[i]).ljust(max_len))
            str_columns.append(str_column)
        str_rep = ''
        for i in range(self.m):
            str_rep += '|'
            for j in range(self.n):
                if j != self.n - 1:
                    str_rep += str_columns[j][i] + ' '
                else:
                    str_rep += str_columns[j][i]
            str_rep += '|\n'
        str_rep = str_rep.rstrip('\n')
        return str_rep

    def __repr__(self):
        return "'" + str(self) + "'"

    def dimensions(self):
        print(self.m, 'x', self.n)

    def transpose(self):
        res_matrix = []
        for i in range(self.n):
            res_row = []
            for j in self.rows:
                res_row.append(j[i])
            res_matrix.append(res_row)
        return Matrix(res_matrix)

    def __add__(self, other):
        if isinstance(self, Matrix) and isinstance(other, Matrix):
            if self.m == other.m and self.n == other.n:
                res_matrix = []
                for i in range(self.m):
                    res_row = []
                    for j in range(self.n):
                        res_row.append(self.rows[i][j] + other.rows[i][j])
                    res_matrix.append(res_row)
                return Matrix(res_matrix)
            else:
                raise ValueError('The matrices must have the same dimensions')
        else:
            raise TypeError('Both objects must be matrices to do matrix addition')

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(self, Matrix) and isinstance(other, Matrix):
            if self.m == other.m and self.n == other.n:
                res_matrix = []
                for i in range(self.m):
                    res_row = []
                    for j in range(self.n):
                        res_row.append(self.rows[i][j] - other.rows[i][j])
                    res_matrix.append(res_row)
                return Matrix(res_matrix)
            else:
                raise ValueError('The matrices must have the same dimensions')
        else:
            raise TypeError('Both objects must be matrices to do matrix addition')

    __rsub__ = __sub__

    def __neg__(self):
        res_matrix = []
        for i in self.rows:
            res_row = []
            for j in range(self.n):
                res_row.append(-i[j])
            res_matrix.append(res_row)
        return Matrix(res_matrix)

    def __mul__(self, other):
        if isinstance(self, Matrix) and (isinstance(other, int) or isinstance(other, float)):
            res_matrix = []
            for i in self.rows:
                res_row = []
                for j in i:
                    res_row.append(j*other)
                res_matrix.append(res_row)
            return Matrix(res_matrix)
        else:
            raise TypeError('The * operator is used for scalar multiplication... one object must be a Matrix and the other object must be a number')

    __rmul__ = __mul__

    def __getitem__(self, key):
        if isinstance(key, int):
            if key >= -self.m and key < self.m:
                return self.rows[key]
            else:
                raise IndexError("Index out of range")
        else:
            raise TypeError("The index must be an integer")

    def __setitem__(self, key, new_val):
        if isinstance(key, int):
            if key >= -self.m and key < self.m:
                if isinstance(new_val, list):
                    if all(isinstance(i, int) or isinstance(i, float) for i in new_val):
                        if len(new_val) == self.n:
                            self.rows[key] = new_val
                        else:
                            raise ValueError("New row must be the same length as the width of the matrix")
                    else:
                        raise TypeError("All elements in the row should be numbers")
                elif isinstance(new_val, int) or isinstance(new_val, float):
                    if self.n == 1:
                        self.rows[key] = [new_val]
                    else:
                        raise ValueError("New row must be the same length as the width of the matrix")
                else:
                    raise TypeError("New row must be a list, integer, or float input")
            else:
                raise IndexError("Index out of range")
        else:
            raise TypeError("The index must be an integer")

    def dot(self, other):
        if self.n == other.m:
            res_matrix = []
            for i in self.rows:
                res_row = []
                for j in range(other.n):
                    res_elem = 0
                    for k in range(self.n):
                        res_elem += i[k] * other.rows[k][j]
                    res_row.append(res_elem)
                res_matrix.append(res_row)
            if len(res_matrix) == 1 and len(res_matrix[0]) == 1:
                return res_matrix[0][0]
            else:
                return Matrix(res_matrix)
        else:
            raise ValueError('The number of columns in the first matrix must be equal the number of rows in the second matrix')

    def determinant(self):
        if (self.n == self.m) and (self.m > 1):
            if self.n == 2:
                return self.rows[0][0] * self.rows[1][1] - self.rows[0][1] * self.rows[1][0]
            else:
                sign = 1
                res_det = 0
                for i in range(self.n):
                    res_matrix = []
                    for j in self.rows[1:]:
                        res_row = []
                        for k in range(self.n):
                            if i == k:
                                continue
                            res_row.append(j[k])
                        res_matrix.append(res_row)
                    res_det += sign * self.rows[0][i] * Matrix(res_matrix).determinant()
                    sign *= -1
                return res_det
        else:
            raise ValueError('Calculating determinants only works with square matrices with dimensions greater than 1 x 1')

    def minors(self):
        if (self.n == self.m) and (self.m > 2):
            res_matrix = []
            for i in range(self.m):
                res_row = []
                for j in range(self.n):
                    det_matrix = []
                    for k in range(self.m):
                        det_row = []
                        if k == i:
                            continue
                        for h in range(self.n):
                            if h == j:
                                continue
                            det_row.append(self.rows[k][h])
                        det_matrix.append(det_row)
                    res_row.append(Matrix(det_matrix).determinant())
                res_matrix.append(res_row)
            return Matrix(res_matrix)
        else:
            raise ValueError('Calculating a matrix of minors only works with square matrices with dimensions greater than 2 x 2')

    def cofactors(self):
        res_matrix = []
        sign = 1
        for i in self.rows:
            res_row = []
            for j in i:
                res_row.append(sign*j)
                sign *= -1
            res_matrix.append(res_row)
        return Matrix(res_matrix)

    def inverse(self):
        if (self.n == self.m):
            if self.n == 1:
                return Matrix([1 / self.rows[0][0]])
            elif self.n == 2:
                det = self.determinant()
                if det == 0:
                    print('The inverse does not exist as the determinant equals 0')
                else:
                    return (1 / det) * Matrix([[self.rows[1][1], -self.rows[0][1]], [-self.rows[1][0], self.rows[0][0]]])
            else:
                det = self.determinant()
                if det == 0:
                    print('The inverse does not exist as the determinant equals 0')
                else:
                    return (1 / det) * (self.minors().cofactors().transpose())
        else:
            raise ValueError('Calculating inverses only works with square matrices')

    def div(self, other):
        return self.dot(other.inverse())

#examples:

X = Matrix([[1, 2], [3, 4]])
Y = Matrix([[5, 6], [7, 8]])

print(X)
print(Y)
print(X + Y)
print(X - Y)
print(4*X)
print(X.determinant())
print(X.transpose())
print(X.inverse())
print(X.inverse().dot(X))

A = Matrix([[1, 2]])
B = Matrix([3, 4])

print(A)
print(B)
print(A.dot(B))
