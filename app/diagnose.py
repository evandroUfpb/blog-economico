import sys
import platform

def diagnose():
    print("Sistema de Diagnóstico:")
    print("----------------------")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Python Implementation: {platform.python_implementation()}")
    
    try:
        import numpy
        print(f"NumPy Version: {numpy.__version__}")
    except ImportError:
        print("NumPy não instalado")
    
    try:
        import pandas
        print(f"Pandas Version: {pandas.__version__}")
    except ImportError:
        print("Pandas não instalado")

if __name__ == "__main__":
    diagnose()