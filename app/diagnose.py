import sys
import os

def diagnose():
    print("Python Environment Diagnosis:")
    print("----------------------------")
    print(f"Python Version: {sys.version}")
    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Python Path: {sys.path}")
    
    try:
        import flask
        print(f"Flask Version: {flask.__version__}")
    except ImportError:
        print("Flask not installed")

if __name__ == "__main__":
    diagnose()