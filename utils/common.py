



def inRange(max:int, value:int, min:int = 0) -> int:
    """
    Get integers that follow the defined limits.
    Returns:
        result(int): safe int. This help you to make sure that integer is within the limits.
    """
    if min <= value and value <= max:
        return value
    elif value < min:
        return min
    else:
        return max