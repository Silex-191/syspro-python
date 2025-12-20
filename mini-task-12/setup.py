from setuptools import Extension, setup

setup(
  name="foreign",
  version="1.0.0",
  description="Python interface for raising a matrix to a power.",
  ext_modules=[
    Extension(
      name="foreign",
      sources=["foreignmodule.c",
               "null_checked_allocs.c"],
    ),
  ]
)
