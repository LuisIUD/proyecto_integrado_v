from setuptools import setup, find_packages

setup(
    name="piv_2025",
    version="0.0.1",
    author="Luis Pachon - Cristhian Pachon",
    author_email="",
    description="Análisis y predicción del Goog con enriquecimiento de datos",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas==2.2.3",
        "openpyxl",
        "requests==2.32.3",
        "beautifulsoup4==4.13.3",
        "scikit-learn>=0.24.0"
    ],
    include_package_data=True,
)
