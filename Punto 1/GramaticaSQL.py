def generate_sql_attribute_grammar():

    G = {
        'S': {
            'productions': [['stmt_list']],
            'attributes': {'inherited': [], 'synthesized': ['env']}
        },
        'stmt_list': {
            'productions': [['stmt', 'stmt_list'], []],
            'attributes': {'inherited': ['env_in'], 'synthesized': ['env_out']},
            'semantic_actions': [
                "if production == ['stmt','stmt_list']: env_out = merge(stmt.env_out, stmt_list.env_out)"
            ]
        },
        'stmt': {
            'productions': [['create_stmt'], ['insert_stmt'], ['select_stmt'], ['update_stmt'], ['delete_stmt']],
            'attributes': {'inherited': ['env_in'], 'synthesized': ['env_out']}
        },
        'create_stmt': {
            'productions': [['CREATE','TABLE','ID','(', 'col_defs',')']],
            'attributes': {'inherited': ['env_in'], 'synthesized': ['env_out']},
            'semantic_actions': [
                "# add new table schema to env_in -> env_out; check duplicate table name"
            ]
        },
        'insert_stmt': {
            'productions': [['INSERT','INTO','ID','(', 'col_list',')','VALUES','(', 'val_list',')']],
            'attributes': {'inherited': ['env_in'], 'synthesized': ['env_out']},
            'semantic_actions': [
                "# lookup table schema; check arity and types; append row"
            ]
        },
        'select_stmt': {
            'productions': [['SELECT','select_list','FROM','ID','where_opt']],
            'attributes': {'inherited': ['env_in'], 'synthesized': ['result_set']},
            'semantic_actions': [
                "# validate columns, evaluate where, produce result_set"
            ]
        },
    }
    return G

if __name__ == "__main__":
    import json
    G = generate_sql_attribute_grammar()
    print(json.dumps(G, indent=2, ensure_ascii=False))
