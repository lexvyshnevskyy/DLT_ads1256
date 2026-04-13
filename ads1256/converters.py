def lm335(volts: float = 0.0, celsius: bool = True):
    temp_c = 38.24 * volts - 25.91
    if celsius:
        return temp_c
    return temp_c + 273.15


def lm335_kelvin_direct(v_meas: float) -> float:
    v_sensor = v_meas / 0.4773  # Undo divider.
    return v_sensor * 100.0 + 7.0
