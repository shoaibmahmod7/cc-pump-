from pathlib import Path
import pint


ureg = pint.UnitRegistry()
new_units = Path(__file__).parent / 'new_units.txt'
ureg.load_definitions(str(new_units))
Q_ = ureg.Quantity

units = {'p': 'pascal', 'T': 'degK'}


def check_units(func):
    """Wrapper to check and convert units to base_units."""
    def inner(*args, **kwargs):

        base_unit_kwargs = {}
        for k, v in kwargs.items():
            if k in units:
                try:
                    base_unit_kwargs[k] = v.to_base_units()
                except AttributeError:
                    base_unit_kwargs[k] = Q_(v, units[k])

        return func(*args, **base_unit_kwargs)
    return inner

