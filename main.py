import sys
import glob
from lexy import lexer
from parsey import parser
from semantic import SemanticAnalyzer
from intermediate import generate_intermediate_code
from optimizer import optimize_intermediate_code
from codegen import generate_target_code

def process_file(filename):
    with open(filename, "r", encoding="utf-8") as source_file:
        source_code = source_file.read()
    print(f"\nProcessing {filename} ...")
    
    # Parsing
    ast = parser.parse(source_code)
    if ast is None:
        print("Parsing failed.")
        return
    # Semantic Analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    if analyzer.errors:
        print("Semantic errors found:")
        for error in analyzer.errors:
            print(error)
        return
    # Intermediate Code Generation
    intermediate_code, _ = generate_intermediate_code(ast)
    # Optimization
    optimized_code = optimize_intermediate_code(intermediate_code)
    # Target Code Generation
    target_code = generate_target_code(optimized_code)
    # Write the target code to a file (or you could run it directly)
    target_filename = filename.replace(".ec", ".py")
    with open(target_filename, "w", encoding="utf-8") as target_file:
        target_file.write(target_code)
    print(f"Target code generated successfully in '{target_filename}'.")
    # Optionally, you can run the generated target code here.
    
def main():
    # If file names are passed as arguments, process them
    if len(sys.argv) > 1:
        files = sys.argv[1:]
    else:
        # Otherwise, process all .ec files in the current directory.
        files = glob.glob("*.ec")
    
    for filename in files:
        process_file(filename)

if __name__ == '__main__':
    main()
