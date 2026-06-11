import pandas as pd
import numpy as np
from scipy.stats import pearsonr

def calculate_group_correlations(df, channels, behavior_col, dd_ids, td_ids):
    """
    計算指定通道與行為指標的分組皮爾森相關係數 (完美兼容單一字串、數字與 list 欄位輸入)。
    """
    results = {}
    
    # 確保 channels 統一轉換成 list 格式，避免 Pandas 索引發生 list 加法錯誤
    if not isinstance(channels, list):
        ch_list = [channels]
    else:
        ch_list = channels

    # 確保 behavior_col 也是 list 格式
    if isinstance(behavior_col, list):
        bh_list = behavior_col
        # 如果傳進來是 list，我們取第一個當作主要行為變數名
        main_bh = behavior_col[0] if len(behavior_col) > 0 else None
    else:
        bh_list = [behavior_col]
        main_bh = behavior_col

    if not main_bh:
        return results

    # 撈出需要的欄位並清除缺失值
    req_cols = ['ID'] + ch_list + bh_list
    # 檢查這些欄位是否都存在於 DataFrame 中
    valid_cols = [c for c in req_cols if c in df.columns]
    
    plot_data = df[valid_cols].dropna().copy()
    
    if len(plot_data) <= 2:
        return results
        
    # 強制進行數值型態轉換
    for ch in ch_list:
        if ch in plot_data.columns:
            plot_data[ch] = plot_data[ch].astype(float)
    if main_bh in plot_data.columns:
        plot_data[main_bh] = plot_data[main_bh].astype(float)
    
    # 切分組別
    dd_sub = plot_data[plot_data['ID'].isin(dd_ids)]
    td_sub = plot_data[plot_data['ID'].isin(td_ids)]
    
    # 針對每一個通道進行相關係數計算
    for ch in ch_list:
        res = {
            'dd_r': None, 'dd_p': None, 
            'td_r': None, 'td_p': None, 
            'dd_sub': dd_sub, 'td_sub': td_sub,
            'all_r': None, 'all_p': None,
            'all_data': plot_data
        }
        
        if ch in plot_data.columns and main_bh in plot_data.columns:
            # 1. 計算全體 (60人) 的相關
            r_all, p_all = pearsonr(plot_data[main_bh], plot_data[ch])
            res['all_r'], res['all_p'] = r_all, p_all
            
            # 2. 計算 DD 組相關
            if len(dd_sub) > 2:
                r_dd, p_dd = pearsonr(dd_sub[main_bh], dd_sub[ch])
                res['dd_r'], res['dd_p'] = r_dd, p_dd
                
            # 3. 計算 TD 組相關
            if len(td_sub) > 2:
                r_td, p_td = pearsonr(td_sub[main_bh], td_sub[ch])
                res['td_r'], res['td_p'] = r_td, p_td
                
        results[ch] = res
        
    return results
