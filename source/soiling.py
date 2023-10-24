# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24

@author: DorianGuzman
"""
import pandas as pd


def instantaneous_soiling_ratio(df: pd.DataFrame)->pd.DataFrame:
    """
    Calculate the Instantaneous Soiling Ratio (SRatio) and apply filters.
    Based on this paper:
    https://doi.org/10.1016/j.energy.2022.123173

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame containing ac_power and AC_Power_exp as columns.

    Returns:
    --------
    filtered_df : pandas.DataFrame
        The filtered DataFrame with calculated SRatio values.

    Notes:
    ------
    The function calculates the SRatio based on AC power measured 
    and AC power reference.
     It applies three filters:
    1. Filter #1: SRatio data obtained between 11 a.m. and 1 p.m.
    2. Filter #2: Reduce noise by including data points with GPOA >= 700 W/m2.
    3. Filter #3: Two-sigma filter based on SRatio values.

    The returned DataFrame contains the SRatio values that pass all applied
     filters.
    """
    # Calculate the Soiling Ratio (S_ratio)
    df['S_ratio'] = df['ac_power'] / df['AC_Power_exp']

    # Filter #1: SRatio data obtained between 11 a.m. and 1 p.m.
    df_filtered = df.between_time('11:00:00', '13:00:00')

    # Filter #2: Reduce noise in the soiling extraction (GPOA >= 700 W/m2)
    df_filtered = df_filtered[df_filtered['poa'] >= 700]

    # Calculate mean and standard deviation based on the filtered data
    mean_s_ratio = df_filtered['S_ratio'].mean()
    std_s_ratio = df_filtered['S_ratio'].std()

    # Filter #3: Two-sigma filter
    df_filtered = df_filtered[(df_filtered['S_ratio'] >= mean_s_ratio - 2 * std_s_ratio) &
                              (df_filtered['S_ratio'] <= mean_s_ratio + 2 * std_s_ratio)]

    return df_filtered