# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 18:48:03 2023

@author: DorianGuzman
"""
import pandas as pd


def calculate_expected_power(df: pd.DataFrame, constants:dict,
                             weather_columns:dict)->pd.DataFrame:
    """
    Calculate expected DC and AC power based on weather data and constants.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame containing weather data.

    constants : dict
        A dictionary of constant values including:
        - 'Mcoef': Temperature coefficient (deg C^-1)
        - 'DC_P': DC Power Rating (W)
        - 'AC_P': AC Power Rating (W)
        - 'Tilt': Tilt angle (degrees)
        - 'Azimuth': Azimuth angle (degrees)
        - 'DC_AC_n': DC to AC power conversion factor (1 for 100% efficiency)
        - 'G': Global horizontal irradiance (W/m^2)
        - 'Tcell_ref': Reference cell temperature (deg C)

    weather_columns : dict
        A dictionary mapping weather data columns in the DataFrame
        to their names:
        - 'poa': Photovoltaic power of array (W/m^2).
        - 'tmp_cell': Cell temperature (deg C).

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame with added columns for expected DC and AC power.

    """
    # from the pdf
    # Expected AC Power = DC-AC Inverter Efficiency * DC Power Rating / G
    # * POA Irradiance * ( 1 – Module temperature coefficient *
    # (Reference Temperature - Cell temperature) )
    # • where G = 1000 W/m^2 and Reference temperature = 25 deg C
    
    df['DC_Power_exp'] = (
        constants['DC_P'] / constants['G'] * df[weather_columns['poa']] *
        (1 - constants['Mcoef'] * (constants['Tcell_ref'] -
                                   df[weather_columns['tmp_cell']])
    ))

    df['AC_Power_exp'] = constants['DC_AC_n'] * df['DC_Power_exp']

    return df
