#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "null_checked_allocs.h"

static void sqr_matrix_mult(Py_ssize_t n, double result[n][n], double mat1[n][n], double mat2[n][n]) {
  for (Py_ssize_t i = 0; i < n; i++) {
    for (Py_ssize_t j = 0; j < n; j++) {
      result[i][j] = 0;
      for (Py_ssize_t k = 0; k < n; k++) {
        result[i][j] += mat1[i][k] * mat2[k][j];
      }
    }
  }
}

static void foreign_matrix_power_clean(void *ptr1, void *ptr2, void *ptr3) {
  free(ptr1);
  free(ptr2);
  free(ptr3);
}

static PyObject *foreign_matrix_power(PyObject *self, PyObject *args) {
  PyObject *py_matrix;
  Py_ssize_t power;
  Py_ssize_t n;

  if (!PyArg_ParseTuple(args, "On", &py_matrix, &power)) {
    return NULL;
  }
  n = PyList_Size(py_matrix);

  double (*result)[n] = nc_malloc(n * n * sizeof(double));
  double (*mat1)[n] = nc_malloc(n * n * sizeof(double));
  double (*mat2)[n] = nc_malloc(n * n * sizeof(double));

  for (Py_ssize_t i = 0; i < n; i++) {
    PyObject *line = PyList_GetItem(py_matrix, i);
    for (Py_ssize_t j = 0; j < n; j++) {
      mat1[i][j] = mat2[i][j] = PyFloat_AsDouble(PyList_GetItem(line, j));
      if (PyErr_Occurred()) {
        foreign_matrix_power_clean(result, mat1, mat2);
        return NULL;
      }
    }
  }

  for (Py_ssize_t step = 0; step < power; step++) {
    sqr_matrix_mult(n, result, mat1, mat2);
    double (*temp_ptr)[n] = mat1;
    mat1 = result;
    result = temp_ptr;
  }

  py_matrix = PyList_New(n);
  if (!py_matrix) {
    foreign_matrix_power_clean(result, mat1, mat2);
    return NULL;
  }

  for (Py_ssize_t i = 0; i < n; i++) {
    PyObject *line = PyList_New(n);
    if (!line) {
      foreign_matrix_power_clean(result, mat1, mat2);
      return NULL;
    }

    for (Py_ssize_t j = 0; j < n; j++) {
      PyObject *element = PyFloat_FromDouble(result[i][j]);
      if (!element) {
        foreign_matrix_power_clean(result, mat1, mat2);
        return NULL;
      }
      PyList_SetItem(line, j, element);
    }

    PyList_SetItem(py_matrix, i, line);
  }

  foreign_matrix_power_clean(result, mat1, mat2);

  return py_matrix;
}

static PyMethodDef ForeignMethods[] = {
  {
    "matrix_power",
    foreign_matrix_power, METH_VARARGS,
    "Returns the matrix raised to a power."
  },
  {NULL, NULL, 0, NULL}
};

static struct PyModuleDef foreignmodule = {
  PyModuleDef_HEAD_INIT,
  "foreign",
  NULL,
  -1,

  ForeignMethods
};

PyMODINIT_FUNC PyInit_foreign(void) {
  return PyModule_Create(&foreignmodule);
}