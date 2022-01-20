from functools import wraps


# Nested dictionary search function
def dict_search(dictionary: dict, search, list_depth=1):
    '''Nested dictionary search
    ------
    Allows user to recursively search a nested dictionary for specified key\n
    The depth at which any list nesting is collapsed can be specified using 'list_depth'

    Parameters
    ----------
    dictionary : dict
        Nested dictionary or list
    search : str or list
        Search 'key' string or list
    list_depth : int, optional
        Allows user to specify depth at which to collapse nested list, by default 1

    Returns
    -------
    list
        Function returns a list of dictionaries
    '''
    # Ensure search is a list
    search = [search] if isinstance(search, str) else search
    # Initiate data structures
    values = []
    temp = {}
    # Set list depth counter to zero
    dict_search.list_depth = 0
    # Recursive function loops through nesting structure

    def find(d: dict, search):
        # If dict, check if key matches and append key-value pair to values list
        if isinstance(d, dict):
            for key, value in d.items():
                if key in search:
                    temp[key] = value
                    # if user specified that list depth starts at zero add to values
                    if list_depth == 0:
                        values.append(temp.copy())
                # If key doesn't match run find on value
                else:
                    find(value, search)
        # If list, loop through list items and run find
        elif isinstance(d, list):
            for i in range(0, len(d)):
                # Increment list depth by one to keep track of depth
                dict_search.list_depth = + 1
                find(d[i], search)
                # Apend temp dict at list depth specified by user
                if dict_search.list_depth == list_depth:
                    values.append(temp.copy())

    find(dictionary, search)
    return values


# Decorator function to expand paginated responses
def paginated(max_pages):
    def decorate(func, combined=[], page=1):
        # Function wrapper
        # Recursively runs wrapped function while amending pageToken until max page limit reached
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal page
            try:
                # Loop pages
                while page <= max_pages:
                    try:
                        # Run api function, increment page count and append next page token to kwargs
                        # Execute wrapped function
                        response = func(*args, **kwargs)
                        combined.append(response)
                        page += 1
                        kwargs['pageToken'] = response['nextPageToken']
                    except:
                        break
                response = combined.copy()  # Create copy so cache can be cleared for next query
                return response
            finally:
                # Reset combined cache and page count
                combined.clear()
                page = 1
        return wrapper
    return decorate


# Function to chunk list
def chunked_list(lst: list, n: int):
    return [lst[i:i + n] for i in range(0, len(lst), n)]
