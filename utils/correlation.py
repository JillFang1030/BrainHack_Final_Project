import pandas as pd
import numpy as np
from scipy.stats import pearsonr

def calculate_group_correlations(df, channels, behavior_col, dd_ids, td_ids):
    """
    【修正版】不再鎖第一個元素，動態精確抓取主程式迴圈丟進來的行為指標！
    """
    results = {}
    
    # 1. 統一將 channels 轉成標準 list 清單
    if isinstance(channels, list):
        ch_list = channels
    else:
        ch_list = [channels]

    # 2. 🔥【徹底消滅鬼打牆的核心修正】
    # 如果傳進來的是單一元素的 list (例如 ['C_RAN'])，拆開拿它
    # 如果是字串 (例如 'C_RAN')，直接用它
    if isinstance(behavior_col, list) and len(behavior_col) == 1:
        main_bh = behavior_col[0]
    elif isinstance(behavior_col, str):
        main_bh = behavior_col
    else:
        main_bh = behavior_col

    # 防呆
    if not main_bh or main_bh not in df.columns:
        return results

    # 3. 針對每一個通道獨立且乾淨地處理
    for ch in ch_list:
        res = {
            'dd_r': None, 'dd_p': None, 
            'td_r': None, 'td_p': None, 
            'dd_sub': pd.DataFrame(), 'td_sub': pd.DataFrame(),
            'all_r': None, 'all_p': None,
            'all_data': pd.DataFrame()
        }
        
        if ch not in df.columns:
            results[ch] = res
            continue
            
        # 撈出當前特定通道與特定行為的乾淨資料
        plot_data = df[['ID', ch, main_bh]].dropna().copy()
        
        if len(plot_data) > 2:
            try:
                plot_data[ch] = plot_data[ch].astype(float)
                plot_data[main_bh] = plot_data[main_bh].astype(float)
                
                # 計算全體相關
                r_all, p_all = pearsonr(plot_data[main_bh], plot_data[ch])
                res['all_r'], res['all_p'] = r_all, p_all
                
                # 切分組別（每次迴圈根據正確的 main_bh 動態切分）
                dd_sub = plot_data[plot_data['ID'].isin(dd_ids)]
                td_sub = plot_data[plot_data['ID'].isin(td_ids)]
                res['dd_sub'], res['td_sub'] = dd_sub, td_sub
                res['all_data'] = plot_data
                
                # 計算 DD 組相關
                if len(dd_sub) > 2:
                    r_dd, p_dd = pearsonr(dd_sub[main_bh], dd_sub[ch])
                    res['dd_r'], res['dd_p'] = r_dd, p_dd
                    
                # 計算 TD 組相關
                if len(td_sub) > 2:
                    r_td, p_td = pearsonr(td_sub[main_bh], td_sub[ch])
                    res['td_r'], res['td_p'] = r_td, p_td
            except Exception:
                pass
                
        results[ch] = res
        
    return results
