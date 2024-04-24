def inferencing(index,user_query):
    query_engine = index.as_query_engine()
    response = query_engine.query(user_query)
    # display(Markdown(f"<b>{response}</b>"))
    return response