

# Nested dictionary search function 
def dict_search(dictionary: dict, search, list_depth=1):
    
    search = [search] if isinstance(search, str) else search
    values = []
    dict_search.list_depth = 0
    temp = {}
    # Recursive function loops through nesting structure
    def find(d : dict, search):
        # If dict, check if key matches and append value
        if isinstance(d, dict):
            for key, value in d.items():
                if key in search:
                    temp[key] = value
                    if list_depth == 0:
                        values.append(temp)
                # If key doesn't match run search on value
                else:
                    find(value, search)
        # if list loop through list items
        elif isinstance(d, list):
            for i in range(0,len(d)):
                dict_search.list_depth =+ 1
                find(d[i], search)
                if dict_search.list_depth == list_depth:
                    values.append(temp)
  
    find(dictionary, search)
    return values