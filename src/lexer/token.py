def create_token(token_type, lexeme, line, column):
    return {
        "type": token_type,
        "lexeme": lexeme,
        "line": line,
        "column": column
    }