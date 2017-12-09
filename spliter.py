def split_array_of_ten(array):
    """Разбивает список на список списков, в каждом из которых не более 10 элементов"""
    internal_array = []
    external_array = []
    counter = 0
    for item in array:
        if counter < 10:
            internal_array.append(item)
        else:
            external_array.append(internal_array)
            internal_array = [item]
            counter = 0
        counter += 1
    if len(internal_array) > 0:
        external_array.append(internal_array)
    return external_array
