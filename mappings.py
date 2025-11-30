def linear_map(value, old_min, old_max, new_min, new_max):
    return new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)

def non_linear_map(value, old_min, old_max, new_min, new_max, function):
    normalized = (value - old_min) * (new_max - new_min) / (old_max - old_min)
    transformed = function(normalized)
    return transformed + old_min