def optimize_intermediate_code(code):
    """
    Performs basic constant propagation and constant folding on the intermediate code.
    :param code: List of TAC instructions (strings)
    :return: List of optimized TAC instructions (strings)
    """
    constants = {}
    optimized_code = []

    for line in code:
        instr = line.strip()
        
        # If the line is a label, leave it unchanged.
        if instr.endswith(':'):
            optimized_code.append(instr)
            continue
        
        # Skip optimization for call instructions.
        if instr.startswith("call"):
            optimized_code.append(instr)
            continue

        # For control flow instructions, propagate constants.
        if instr.startswith("ifFalse") or instr.startswith("goto") or instr.startswith("print"):
            for var, const in constants.items():
                instr = instr.replace(var, str(const))
            optimized_code.append(instr)
            continue

        # Process assignment instructions.
        if '=' in instr:
            left, right = instr.split('=', 1)
            left = left.strip()
            right = right.strip()

            # Try to evaluate a direct integer assignment.
            try:
                value = int(right)
                constants[left] = value
                optimized_code.append(f"{left} = {value}")
                continue
            except ValueError:
                pass

            # Check for binary operations.
            for op in ['➕', '➖', '✖️', '➗']:
                if op in right:
                    op_parts = right.split(op)
                    if len(op_parts) == 2:
                        op1 = op_parts[0].strip()
                        op2 = op_parts[1].strip()
                        if op1 in constants:
                            op1 = str(constants[op1])
                        if op2 in constants:
                            op2 = str(constants[op2])
                        try:
                            num1 = int(op1)
                            num2 = int(op2)
                            if op == '➕':
                                result = num1 + num2
                            elif op == '➖':
                                result = num1 - num2
                            elif op == '✖️':
                                result = num1 * num2
                            elif op == '➗':
                                result = num1 // num2
                            constants[left] = result
                            optimized_code.append(f"{left} = {result}")
                            break
                        except ValueError:
                            new_right = f"{op1} {op} {op2}"
                            optimized_code.append(f"{left} = {new_right}")
                            break
            else:
                for var, const in constants.items():
                    if var in right:
                        right = right.replace(var, str(const))
                optimized_code.append(f"{left} = {right}")
            continue

        for var, const in constants.items():
            if var in instr:
                instr = instr.replace(var, str(const))
        optimized_code.append(instr)

    return optimized_code
