import pandas as pd
from scipy.stats import pearsonr

def calculate_group_correlations(df, channels, behavior_col, dd_ids, td_ids):
    """
    計算指定通道與行為指標的分組皮爾森相關係數 (支援任意數量通道)。
    """
    results = {}
    plot_data = df[['ID'] + channels + [behavior_col]].dropna().copy()
    
    if len(plot_data) <= 2:
        return results
        
    for ch in channels:
        plot_data[ch] = plot_data[ch].astype(float)
    plot_data[behavior_col] = plot_data[behavior_col].astype(float)
    
    dd_sub = plot_data[plot_data['ID'].isin(dd_ids)]
    td_sub = plot_data[plot_data['ID'].isin(td_ids)]
    
    for ch in channels:
        res = {
            'dd_r': None, 'dd_p': None, 
            'td_r': None, 'td_p': None, 
            'dd_sub': dd_sub, 'td_sub': td_sub
        }
        if len(dd_sub) > 2:
            r_dd, p_dd = pearsonr(dd_sub[behavior_col], dd_sub[ch])
            res['dd_r'], res['dd_p'] = r_dd, p_dd
        if len(td_sub) > 2:
            r_td, p_td = pearsonr(td_sub[behavior_col], td_sub[ch])
            res['td_r'], res['td_p'] = r_td, p_td
        results[ch] = res
        
    return results
