import pandas as pd
import numpy as np
from scipy.stats import pearsonr

def calculate_group_correlations(df, channels, behavior_col, dd_ids, td_ids):
    """
    【金剛防防呆版】完美相容純數字、字串、List 傳入，絕不噴 unhashable 錯誤。
    """
    results = {}
    
    # 1. 統一將 channels 轉成標準 list 清單
    if isinstance(channels, list):
        ch_list = channels
    else:
        ch_list = [channels]

    # 2. 統一將 behavior_col 轉成標準單一字串
    if isinstance(behavior_col, list):
        main_bh = behavior_col[0] if len(behavior_col) > 0 else None
    else:
        main_bh = behavior_col

    if not main_bh or main_bh not in df.columns:
        return results

    # 3. 針對每一個通道獨立且乾淨地處理，徹底避開 Pandas 欄位 list 相加的 bug
    for ch in ch_list:
        res = {
            'dd_r': None, 'dd_p': None, 
            'td_r': None, 'td_p': None, 
            'dd_sub': pd.DataFrame(), 'td_sub': pd.DataFrame(),
            'all_r': None, 'all_p': None,
            'all_data': pd.DataFrame()
        }
        
        # 檢查這個通道是否存在於資料庫中
        if ch not in df.columns:
            results[ch] = res
            continue
            
        # 乾淨撈出單一通道與單一行為的資料，避免多個欄位打包衝突
        plot_data = df[['ID', ch, main_bh]].dropna().copy()
        
        if len(plot_data) > 2:
            try:
                plot_data[ch] = plot_data[ch].astype(float)
                plot_data[main_bh] = plot_data[main_bh].astype(float)
                
                # 計算全體相關
                r_all, p_all = pearsonr(plot_data[main_bh], plot_data[ch])
                res['all_r'], res['all_p'] = r_all, p_all
                
                # 切分組別
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
