import sys
import platform

def diagnose():
    print("Sistema de Diagnóstico:")
    print("----------------------")
    print(f"Python Version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Python Implementation: {platform.python_implementation()}")
    
    modules_to_check = [
        'numpy', 
        'pandas', 
        'flask', 
        'sidrapy', 
        'requests', 
        'plotly'
    ]
    
    for module in modules_to_check:
        try:
            mod = __import__(module)
            print(f"{module.capitalize()} Version: {mod.__version__}")
        except ImportError:
            print(f"{module.capitalize()} não instalado")

if __name__ == "__main__":
    diagnose()