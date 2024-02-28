"""Module to keep everything that is common to ccp_app_straight_through and ccp_app_back_to_back."""
import io
import pandas as pd

# parameters with name and label
flow_m_units = ["kg/h", "kg/min", "kg/s", "lbm/h", "lbm/min", "lbm/s"]
flow_v_units = ["m³/h", "m³/min", "m³/s"]
flow_units = flow_m_units + flow_v_units
pressure_units = ["bar", "kgf/cm²", "barg", "Pa", "kPa", "MPa", "psi", "mm*H2O*g0"]
temperature_units = ["degK", "degC", "degF", "degR"]
speed_units = ["rpm", "Hz"]
length_units = ["m", "mm", "ft", "in"]

parameters_map = {
    "flow": {
        "label": "Flow",
        "units": flow_units,
        "help": "Flow can be mass flow or volumetric flow depending on the selected unit.",
    },
    "suction_pressure": {
        "label": "Suction Pressure",
        "units": pressure_units,
    },
    "suction_temperature": {
        "label": "Suction Temperature",
        "units": temperature_units,
    },
    "discharge_pressure": {
        "label": "Discharge Pressure",
        "units": pressure_units,
    },
    "discharge_temperature": {
        "label": "Discharge Temperature",
        "units": temperature_units,
    },
    "casing_delta_T": {
        "label": "Casing ΔT",
        "units": temperature_units,
        "help": "Temperature difference between the casing and the ambient temperature.",
    },
    "speed": {
        "label": "Speed",
        "units": speed_units,
    },
    "balance_line_flow_m": {
        "label": "Balance Line Flow",
        "units": flow_m_units,
    },
    "end_seal_upstream_pressure": {
        "label": "Pressure Upstream End Seal",
        "units": pressure_units,
        "help": "Second section suction pressure.",
    },
    "end_seal_upstream_temperature": {
        "label": "Temperature Upstream End Seal",
        "units": temperature_units,
        "help": "Second section suction temperature.",
    },
    "div_wall_flow_m": {
        "label": "Division Wall Flow",
        "units": flow_m_units,
        "help": "Flow through the division wall if measured. Otherwise it is calculated from the First Section Discharge Flow.",
    },
    "div_wall_upstream_pressure": {
        "label": "Pressure Upstream Division Wall",
        "units": pressure_units,
        "help": "Second section discharge pressure.",
    },
    "div_wall_upstream_temperature": {
        "label": "Temperature Upstream Division Wall",
        "units": temperature_units,
        "help": "Second section discharge temperature.",
    },
    "first_section_discharge_flow_m": {
        "label": "First Section Discharge Flow",
        "units": flow_m_units,
        "help": "If the Division Wall Flow is not measured, we use this value to calculate it.",
    },
    "seal_gas_flow_m": {
        "label": "Seal Gas Flow",
        "units": flow_m_units,
    },
    "seal_gas_temperature": {
        "label": "Seal Gas Temperature",
        "units": temperature_units,
    },
    "head": {
        "label": "Head",
        "units": ["kJ/kg", "J/kg", "m*g0", "ft"],
    },
    "eff": {
        "label": "Efficiency",
        "units": [""],
    },
    "power": {
        "label": "Gas Power",
        "units": ["kW", "hp", "W", "Btu/h", "MW"],
    },
    "b": {
        "label": "First Impeller Width",
        "units": length_units,
    },
    "D": {
        "label": "First Impeller Diameter",
        "units": length_units,
    },
    "surface_roughness": {
        "label": "Surface Roughness",
        "units": length_units,
        "help": "Mean surface roughness of the gas path.",
    },
    "casing_area": {
        "label": "Casing Area",
        "units": ["m²", "mm²", "ft²", "in²"],
    },
    "outer_diameter_fo": {
        "label": "Outer Diameter",
        "units": ["mm", "m", "ft", "in"],
        "help": "Outer diameter of orifice plate.",
    },
    "inner_diameter_fo": {
        "label": "Inner Diameter",
        "units": ["mm", "m", "ft", "in"],
        "help": "Inner diameter of orifice plate.",
    },
    "upstream_pressure_fo": {
        "label": "Upstream Pressure",
        "units": pressure_units,
        "help": "Upstream pressure of orifice plate.",
    },
    "upstream_temperature_fo": {
        "label": "Upstream Temperature",
        "units": temperature_units,
        "help": "Upstream temperature of orifice plate.",
    },
    "pressure_drop_fo": {
        "label": "Pressure Drop",
        "units": pressure_units,
        "help": "Pressure drop across orifice plate.",
    },
    "tappings_fo": {
        "label": "Tappings",
        "units": ["flange", "corner", "D D/2"],
        "help": "Pressure tappings type.",
    },
    "mass_flow_fo": {
        "label": "Mass Flow (Result)",
        "units": ["kg/h", "lbm/h", "kg/s", "lbm/s"],
    },
}


def get_gas_composition(gas_name, gas_compositions_table, default_components):
    """Get gas composition from gas name.

    Parameters
    ----------
    gas_name : str
        Name of gas.

    Returns
    -------
    gas_composition : dict
        Gas composition.
    """
    gas_composition = {}
    for gas in gas_compositions_table.keys():
        if gas_compositions_table[gas]["name"] == gas_name:
            for i in range(len(default_components)):
                component = gas_compositions_table[gas][f"component_{i}"]
                molar_fraction = float(
                    gas_compositions_table[gas][f"molar_fraction_{i}"]
                )
                if molar_fraction != 0:
                    gas_composition[component] = molar_fraction

    return gas_composition


def to_excel(df):
    """Function to convert pandas dataframe to excel file to be downloaded."""
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1")
    writer.close()
    processed_data = output.getvalue()
    return processed_data
