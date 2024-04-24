from serpapi import GoogleSearch


def google_search(search_query):
    params = {
    "engine": "google",
    "q": search_query,
    "api_key": "e25c56ffe4d4269ae7b7207ddf8b52efa9440abcdc3f844865486008d028694c"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    # organic_results = results["organic_results"]
    return results["organic_results"]