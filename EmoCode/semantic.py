class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.errors = []

    def analyze(self, node):
        if node is None:
            return

        node_type = node[0]

        if node_type == 'program':
            for stmt in node[1]:
                self.analyze(stmt)

        elif node_type == 'assign':
            var_name = node[1]
            expr = node[2]
            expr_type = self.analyze(expr)
            self.symbol_table[var_name] = expr_type
            return expr_type

        elif node_type == 'number':
            return 'number'

        elif node_type == 'string':
            return 'string'

        elif node_type == 'var':
            var_name = node[1]
            if var_name not in self.symbol_table:
                self.errors.append(f"Undefined variable: {var_name}")
                return None
            return self.symbol_table[var_name]

        elif node_type == 'binop':
            left_type = self.analyze(node[2])
            right_type = self.analyze(node[3])
            if left_type != 'number' or right_type != 'number':
                self.errors.append(f"Type error in binary operation: {node}")
                return None
            return 'number'

        elif node_type == 'relop':
            left_type = self.analyze(node[2])
            right_type = self.analyze(node[3])
            if left_type != right_type:
                self.errors.append(f"Type mismatch in relational operation: {node}")
            return 'boolean'

        elif node_type == 'if_else':
            self.analyze(node[1])
            for stmt in node[2]:
                self.analyze(stmt)
            for stmt in node[3]:
                self.analyze(stmt)

        elif node_type == 'if':
            self.analyze(node[1])
            for stmt in node[2]:
                self.analyze(stmt)

        elif node_type == 'print':
            self.analyze(node[1])
            return None

        elif node_type == 'return':
            return self.analyze(node[1])

        elif node_type == 'function_def':
            func_name = node[1]
            self.symbol_table[func_name] = 'function'
            local_symbols = {}
            for param in node[2]:
                local_symbols[param] = 'number'
            old_table = self.symbol_table.copy()
            self.symbol_table.update(local_symbols)
            for stmt in node[3]:
                self.analyze(stmt)
            self.symbol_table = old_table

        elif node_type == 'class_def':
            class_name = node[1]
            self.symbol_table[class_name] = 'class'
            for stmt in node[2]:
                self.analyze(stmt)

        # New support for call nodes:
        elif node_type == 'call':
            # A generic call node that wraps a call expression.
            self.analyze(node[1])
            return None

        elif node_type == 'call_function':
            # For function calls: ('call_function', function_name, arg_list)
            func_name = node[1]
            if func_name not in self.symbol_table:
                self.errors.append(f"Undefined function: {func_name}")
            for arg in node[2]:
                self.analyze(arg)
            return None

        elif node_type == 'call_method':
            # For method calls: ('call_method', object_name, method_name, arg_list)
            obj_name = node[1]
            method_name = node[2]
            if obj_name not in self.symbol_table:
                self.errors.append(f"Undefined object: {obj_name}")
            for arg in node[3]:
                self.analyze(arg)
            return None

        else:
            self.errors.append(f"Unknown node type: {node_type}")

        return None

if __name__ == '__main__':
    parsed_ast = ('program', [
        ('class_def', '🚗', [
            ('function_def', '🚦', [], [('print', ('string', 'Car is moving'))])
        ]),
        ('function_def', 'add', ['😀', '🔥'], [
            ('assign', '💰', ('binop', '➕', ('var', '😀'), ('var', '🔥'))),
            ('return', ('var', '💰'))
        ]),
        ('assign', '😀', ('number', 5)),
        ('assign', '🔥', ('number', 10)),
        ('if_else', ('relop', '📈', ('var', '😀'), ('var', '🔥')),
            [('print', ('string', '😀 is greater'))],
            [('print', ('string', '🔥 is greater'))]
        ),
        ('call', ('call_function', 'add', [('var', '😀'), ('var', '🔥')])),
        ('call', ('call_method', '🚗', '🚦', []))
    ])

    analyzer = SemanticAnalyzer()
    analyzer.analyze(parsed_ast)

    if analyzer.errors:
        print("Semantic errors found:")
        for error in analyzer.errors:
            print(error)
    else:
        print("Semantic analysis passed!")
