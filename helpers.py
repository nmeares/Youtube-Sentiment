

# Nested dictionary search function 
def dict_search(dictionary: dict, search, list_depth=1):
    
    # Ensure search is a list
    search = [search] if isinstance(search, str) else search
    # Initiate data structures
    values = []
    temp = {}
    # Set list depth counter to zero
    dict_search.list_depth = 0
    # Recursive function loops through nesting structure
    def find(d : dict, search):
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
        # If list, loop through list items
        elif isinstance(d, list):
            for i in range(0,len(d)):
                # Increment list depth by one to keep track of depth
                dict_search.list_depth =+ 1
                find(d[i], search)
                if dict_search.list_depth == list_depth:
                    values.append(temp.copy())
  
    find(dictionary, search)
    return values