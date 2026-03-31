def data_types():
    # Create 8 variables of different types
    var_int = 42
    var_str = "Hello"
    var_float = 3.14
    var_bool = True
    var_list = [1, 2, 3]
    var_dict = {"key": "value"}
    var_tuple = (1, 2, 3)
    var_set = {1, 2, 3}
    
    # Get their type names
    types = [
        type(var_int).__name__,
        type(var_str).__name__,
        type(var_float).__name__,
        type(var_bool).__name__,
        type(var_list).__name__,
        type(var_dict).__name__,
        type(var_tuple).__name__,
        type(var_set).__name__
    ]
    
    # Print as required without quotes
    print("[", end="")
    for i, t in enumerate(types):
        if i > 0:
            print(", ", end="")
        print(t, end="")
    print("]")


if __name__ == '__main__':
    data_types()
