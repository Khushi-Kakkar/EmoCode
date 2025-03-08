import sys
from lexy import lexer  # your lexer module
from parsey import parser  # your parser module
from semantic import SemanticAnalyzer  # your semantic analyzer module
from intermediate import generate_intermediate_code  # intermediate code generator
from optimizer import optimize_intermediate_code  # code optimizer
from codegen import generate_target_code  # target code generator

def main():
    # Read the EmoCode source file
    try:
        with open("test.ec", "r", encoding="utf-8") as source_file:
            source_code = source_file.read()
    except FileNotFoundError:
        print("Error: 'test.ec' file not found.")
        sys.exit(1)

    # Parse the source code into an AST
    ast = parser.parse(source_code)
    if ast is None:
        print("Parsing failed.")
        sys.exit(1)

    # Perform semantic analysis
    analyzer = SemanticAnalyzer()
    analyzer.analyze(ast)
    if analyzer.errors:
        print("Semantic errors found:")
        for error in analyzer.errors:
            print(error)
        sys.exit(1)

    # Generate intermediate code (TAC) from the AST
    intermediate_code, _ = generate_intermediate_code(ast)

    # Optimize the intermediate code
    optimized_code = optimize_intermediate_code(intermediate_code)

    # Generate target code (Python code) from the optimized intermediate code
    target_code = generate_target_code(optimized_code)

    # Write the generated target code to a file
    with open("target.py", "w", encoding="utf-8") as target_file:
        target_file.write(target_code)
    print("Target code generated successfully in 'target.py'.")

if __name__ == '__main__':
    main()
