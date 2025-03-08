def generate_target_code(intermediate_code):
    python_code = '''\
# Generated Target Code from EmoCode Intermediate Representation
definitions = {}
main_instructions = []
instructions = [
'''
    for line in intermediate_code:
        escaped_line = line.replace('"', '\\"')
        python_code += f'    "{escaped_line}",\n'
    python_code += ''']

pc = 0
# Partition instructions into definitions and main code.
while pc < len(instructions):
    inst = instructions[pc].strip()
    if inst == "":
        pc += 1
        continue
    # Process function definitions.
    if inst.startswith("function"):
        parts = inst.split()
        func_name = parts[1].rstrip(":")
        block = []
        pc += 1
        while pc < len(instructions) and not instructions[pc].strip().startswith("end function"):
            block.append(instructions[pc])
            pc += 1
        definitions[func_name] = block
        pc += 1  # Skip the "end function" line.
    # Process class definitions.
    elif inst.startswith("class"):
        parts = inst.split()
        class_name = parts[1].rstrip(":")
        block = []
        pc += 1
        while pc < len(instructions) and not instructions[pc].strip().startswith("end class"):
            block.append(instructions[pc])
            pc += 1
        definitions[class_name] = block
        pc += 1  # Skip the "end class" line.
    else:
        main_instructions.append(inst)
        pc += 1

def execute_instructions(instr_list, initial_vars=None):
    vars = {} if initial_vars is None else initial_vars.copy()
    pc = 0
    labels = {}
    for i, line in enumerate(instr_list):
        if line.endswith(":"):
            labels[line[:-1]] = i
    while pc < len(instr_list):
        inst = instr_list[pc].strip()
        if inst == "" or inst.endswith(":"):
            pc += 1
            continue
        if inst.startswith("ifFalse"):
            parts = inst.split()
            cond = parts[1]
            goto_label = parts[3]
            try:
                cond_val = float(cond)
            except:
                cond_val = vars.get(cond, 0)
            if not cond_val:
                pc = labels.get(goto_label, pc+1)
                continue
        elif inst.startswith("goto"):
            parts = inst.split()
            goto_label = parts[1]
            pc = labels.get(goto_label, pc+1)
            continue
        elif inst.startswith("print"):
            expr = inst[len("print"):].strip()
            if expr.startswith('"') and expr.endswith('"'):
                print(expr[1:-1])
            else:
                print(vars.get(expr, expr))
        elif inst.startswith("call"):
            execute_call(inst, vars)
        elif " = " in inst:
            left, right = inst.split(" = ", 1)
            left = left.strip()
            right = right.strip()
            right = right.replace("➕", "+").replace("➖", "-")
            right = right.replace("✖️", "*").replace("➗", "/")
            right = right.replace("📈", ">").replace("📉", "<")
            right = right.replace("🟰", "==").replace("🚫🟰", "!=")
            try:
                value = eval(right, vars)
            except Exception as e:
                value = right
            vars[left] = value
        elif inst.startswith("return"):
            expr = inst[len("return"):].strip()
            try:
                value = eval(expr, vars)
            except:
                value = expr
            print("Function returned:", value)
            return value
        pc += 1

def execute_call(inst, outer_vars):
    call_expr = inst[len("call"):].strip()
    if call_expr.endswith(";"):
        call_expr = call_expr[:-1].strip()
    # Function call with arguments.
    if "(" in call_expr and call_expr.endswith(")"):
        func_name, arg_str = call_expr.split("(", 1)
        func_name = func_name.strip()
        arg_str = arg_str[:-1].strip()  # Remove trailing ")"
        args = [arg.strip() for arg in arg_str.split(",") if arg.strip() != ""]
        if func_name in definitions:
            func_block = definitions[func_name]
            header = func_block[0].strip() if func_block else ""
            if "(" in header and header.endswith("):"):
                param_str = header.split("(", 1)[1].rstrip("):")
                params = [p.strip() for p in param_str.split(",") if p.strip() != ""]
            else:
                params = []
            local_vars = {}
            for param, arg in zip(params, args):
                # If the argument exists in outer_vars, pass its value.
                if arg in outer_vars:
                    local_vars[param] = outer_vars[arg]
                else:
                    try:
                        local_vars[param] = float(arg)
                    except:
                        local_vars[param] = arg
            ret_val = execute_instructions(func_block[1:], initial_vars=local_vars)
            print("Function returned:", ret_val)
        else:
            print(f"Function {func_name} not defined")
    else:
        # Method call handling.
        if "." in call_expr:
            obj, remainder = call_expr.split(".", 1)
            if "(" in remainder:
                method_name = remainder.split("(", 1)[0].strip()
            else:
                method_name = remainder.strip()
            if obj in definitions:
                class_def = definitions[obj]
                method_block = []
                in_method = False
                for line in class_def:
                    stripped = line.strip()
                    if stripped.startswith("function"):
                        parts = stripped.split()
                        if parts[1].rstrip(":") == method_name:
                            in_method = True
                            continue
                    if in_method:
                        if stripped.startswith("end function"):
                            break
                        method_block.append(line)
                if method_block:
                    execute_instructions(method_block)
                else:
                    print(f"Method {method_name} not found in {obj}")
            else:
                print(f"Class {obj} not defined")

execute_instructions(main_instructions)
'''
    return python_code

if __name__ == '__main__':
    pass
