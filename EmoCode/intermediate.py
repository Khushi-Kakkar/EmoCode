temp_counter = 0
label_counter = 0

def new_temp():
    global temp_counter
    temp_counter += 1
    return f"t{temp_counter}"

def new_label():
    global label_counter
    label_counter += 1
    return f"L{label_counter}"

def generate_intermediate_code(node):
    """
    Recursively traverses the AST (node) and returns a tuple (code, result)
    where 'code' is a list of TAC instructions and 'result' is the temporary
    variable holding the expression's value (if applicable).
    """
    if node is None:
        return [], None

    node_type = node[0]

    if node_type == "program":
        code = []
        for stmt in node[1]:
            stmt_code, _ = generate_intermediate_code(stmt)
            code.extend(stmt_code)
        return code, None

    elif node_type == "assign":
        var_name = node[1]
        code_expr, result = generate_intermediate_code(node[2])
        code = code_expr + [f"{var_name} = {result}"]
        return code, var_name

    elif node_type == "number":
        return [], str(node[1])

    elif node_type == "string":
        return [], f"\"{node[1]}\""

    elif node_type == "var":
        return [], node[1]

    elif node_type == "binop":
        code_left, left_temp = generate_intermediate_code(node[2])
        code_right, right_temp = generate_intermediate_code(node[3])
        temp = new_temp()
        code = code_left + code_right + [f"{temp} = {left_temp} {node[1]} {right_temp}"]
        return code, temp

    elif node_type == "relop":
        code_left, left_temp = generate_intermediate_code(node[2])
        code_right, right_temp = generate_intermediate_code(node[3])
        temp = new_temp()
        code = code_left + code_right + [f"{temp} = {left_temp} {node[1]} {right_temp}"]
        return code, temp

    elif node_type == "print":
        code_expr, result = generate_intermediate_code(node[1])
        code = code_expr + [f"print {result}"]
        return code, None

    elif node_type == "if_else":
        code_cond, cond_temp = generate_intermediate_code(node[1])
        label_else = new_label()
        label_end = new_label()
        code_true = []
        for stmt in node[2]:
            stmt_code, _ = generate_intermediate_code(stmt)
            code_true.extend(stmt_code)
        code_false = []
        for stmt in node[3]:
            stmt_code, _ = generate_intermediate_code(stmt)
            code_false.extend(stmt_code)
        code = (
            code_cond +
            [f"ifFalse {cond_temp} goto {label_else}"] +
            code_true +
            [f"goto {label_end}", f"{label_else}:"] +
            code_false +
            [f"{label_end}:"]
        )
        return code, None

    elif node_type == "if":
        code_cond, cond_temp = generate_intermediate_code(node[1])
        label_end = new_label()
        code_true = []
        for stmt in node[2]:
            stmt_code, _ = generate_intermediate_code(stmt)
            code_true.extend(stmt_code)
        code = code_cond + [f"ifFalse {cond_temp} goto {label_end}"] + code_true + [f"{label_end}:"]
        return code, None

    elif node_type == "function_def":
        func_name = node[1]
        params = node[2]
        code = [f"function {func_name}:"]
        for stmt in node[3]:
            stmt_code, _ = generate_intermediate_code(stmt)
            for line in stmt_code:
                code.append("    " + line)
        code.append("end function")
        return code, None

    elif node_type == "return":
        code_expr, result = generate_intermediate_code(node[1])
        code = code_expr + [f"return {result}"]
        return code, None

    elif node_type == "class_def":
        class_name = node[1]
        code = [f"class {class_name}:"]
        for stmt in node[2]:
            stmt_code, _ = generate_intermediate_code(stmt)
            for line in stmt_code:
                code.append("    " + line)
        code.append("end class")
        return code, None

    elif node_type == "call_function":
        arg_codes = []
        arg_results = []
        for arg in node[2]:
            code_arg, res = generate_intermediate_code(arg)
            arg_codes.extend(code_arg)
            arg_results.append(res)
        # This produces an instruction like: call add(t3, t4)
        return arg_codes + [f"call {node[1]}({', '.join(arg_results)})"], None


    elif node_type == "call_method":
        return [f"call {node[1]}.{node[2]}"], None

    elif node_type == "call":
        return generate_intermediate_code(node[1])

    else:
        return [], None

# Module exposes generate_intermediate_code() function.
if __name__ == '__main__':
    pass
