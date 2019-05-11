def scale(val, val_min, val_max, scale_min, scale_max):
    return scale_min + (scale_max - scale_min) * ( (val - val_min) / (val_max - val_min))
