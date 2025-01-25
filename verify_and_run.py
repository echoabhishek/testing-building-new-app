import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def verify_test_md():
    with open('/home/user/testing-building-new-app/test.md', 'r') as f:
        content = f.read()
    
    required_lines = [
        "This is a new line 1",
        "The sum of 2 + 3 = 5"
    ]
    
    for line in required_lines:
        if line not in content:
            print(f"Error: '{line}' not found in test.md")
            return False
    
    print("test.md verification successful")
    return True

def run_jupyter_notebook():
    with open('/home/user/testing-building-new-app/sum_calculation.ipynb', 'r') as f:
        nb = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': '/home/user/testing-building-new-app/'}})
    
    print("Jupyter notebook execution successful")
    
    # Print the output of the notebook
    for cell in nb.cells:
        if cell.cell_type == 'code' and cell.outputs:
            for output in cell.outputs:
                if output.output_type == 'stream':
                    print(output.text)

if __name__ == "__main__":
    if verify_test_md():
        run_jupyter_notebook()
    else:
        print("Verification failed. Please check test.md")
