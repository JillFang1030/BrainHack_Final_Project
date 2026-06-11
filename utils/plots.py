import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

def plot_whole_brain_sanity_check(channels, behavior_col, stats_results, roi_channels=[6, 16, 21]):
    """
    繪製全腦 32 通道雙組對比散佈圖網格。
    """
    num_plots = len(channels)
    cols = 4
    rows = int(np.ceil(num_plots / cols))
    
    fig, axes = plt.subplots(rows, cols, figsize=(24, 34))
    axes = axes.flatten()
    
    for i, ch_col in enumerate(channels):
        ax = axes[i]
        
        if stats_results and ch_col in stats_results:
            res = stats_results[ch_col]
            dd_sub, td_sub = res['dd_sub'], res['td_sub']
            
            dd_title_part = f"DD r={res['dd_r']:.2f}(p={res['dd_p']:.2f})" if res['dd_r'] is not None else "DD: N/A"
            td_title_part = f"TD r={res['td_r']:.2f}(p={res['td_p']:.2f})" if res['td_r'] is not None else "TD: N/A"
            full_sub_title = f"{dd_title_part}\n{td_title_part}"
            
            # 畫 DD 組
            if len(dd_sub) > 0:
                ax.scatter(dd_sub[behavior_col], dd_sub[ch_col], color='#e74c3c', s=45, alpha=0.7, edgecolors='w', label='DD Group')
                if res['dd_r'] is not None:
                    m, b = np.polyfit(dd_sub[behavior_col], dd_sub[ch_col], 1)
                    ax.plot(dd_sub[behavior_col], m * dd_sub[behavior_col] + b, color='#e74c3c', linestyle='--', linewidth=1.5)
            
            # 畫 TD 組
            if len(td_sub) > 0:
                ax.scatter(td_sub[behavior_col], td_sub[ch_col], color='#3498db', s=45, alpha=0.7, edgecolors='w', label='TD Group')
                if res['td_r'] is not None:
                    m, b = np.polyfit(td_sub[behavior_col], td_sub[ch_col], 1)
                    ax.plot(td_sub[behavior_col], m * td_sub[behavior_col] + b, color='#3498db', linestyle='-', linewidth=1.5)
            
            # 標記 ROI 通道
            if ch_col in roi_channels:
                ax.set_title(f"⭐ CH {ch_col} (ROI)\n{full_sub_title}", fontsize=10, color='crimson', fontweight='bold')
                ax.set_facecolor('#fff9f9')
            else:
                ax.set_title(f"CH {ch_col}\n{full_sub_title}", fontsize=9)
                
            if i == 3:
                ax.legend(loc='upper right', fontsize=10)
        else:
            ax.text(0.5, 0.5, "No Data", ha='center', va='center', color='gray')
            
        ax.set_xlabel(behavior_col, fontsize=8)
        ax.set_ylabel('HbO Beta', fontsize=8)
        ax.grid(True, linestyle=':', alpha=0.5)
        
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
        
    plt.suptitle(f'Sanity Check: Whole-Brain 32-Channel Scatter Plots vs. {behavior_col}\n(Red/Dashed = DD Group, Blue/Solid = TD Group | ⭐ Highlights ROI Channels)', y=1.01, fontsize=18, fontweight='bold')
    plt.tight_layout()
    plt.show()


def plot_subgroup_heatmaps(df, channels, behaviors, dd_ids, td_ids, channels_labels=['CH 6', 'CH 16', 'CH 21']):
    """
    繪製 3✕9 雙組獨立熱圖矩陣。
    """
    def build_matrix(sub_df):
        mat_r = pd.DataFrame(index=channels_labels, columns=behaviors, dtype=float)
        mat_annot = pd.DataFrame(index=channels_labels, columns=behaviors, dtype=str)
        for ch, ch_lab in zip(channels, channels_labels):
            for bh in behaviors:
                if ch in sub_df.columns and bh in sub_df.columns:
                    valid = sub_df[[ch, bh]].dropna()
                    if len(valid) > 2:
                        r_val, p_val = pearsonr(valid[ch], valid[bh])
                    else:
                        r_val, p_val = np.nan, np.nan
                else:
                    r_val, p_val = np.nan, np.nan
                mat_r.loc[ch_lab, bh] = r_val if not np.isnan(r_val) else 0.0
                if not np.isnan(p_val) and p_val < 0.05:
                    mat_annot.loc[ch_lab, bh] = f"{r_val:.2f}*"
                else:
                    mat_annot.loc[ch_lab, bh] = f"{r_val:.2f}"
        return mat_r, mat_annot

    df_dd_only = df[df['ID'].isin(dd_ids)]
    df_td_only = df[df['ID'].isin(td_ids)]
    
    dd_r, dd_annot = build_matrix(df_dd_only)
    td_r, td_annot = build_matrix(df_td_only)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 5.5))
    
    sns.heatmap(dd_r, annot=dd_annot.values, fmt="", cmap='RdBu_r', vmin=-0.6, vmax=0.6, center=0.0, linewidths=1.0, cbar_kws={'label': "Pearson's r"}, ax=ax1)
    ax1.set_title('DD (Dyslexia Group) Correlation Matrix\n(* indicates raw p < 0.05)', fontsize=13, fontweight='bold', pad=10)
    ax1.set_xticklabels(behaviors, rotation=30, ha='right')
    ax1.set_yticklabels(channels_labels, rotation=0)
    
    sns.heatmap(td_r, annot=td_annot.values, fmt="", cmap='RdBu_r', vmin=-0.6, vmax=0.6, center=0.0, linewidths=1.0, cbar_kws={'label': "Pearson's r"}, ax=ax2)
    ax2.set_title('TD (Typically Developing Group) Correlation Matrix\n(* indicates raw p < 0.05)', fontsize=13, fontweight='bold', pad=10)
    ax2.set_xticklabels(behaviors, rotation=30, ha='right')
    ax2.set_yticklabels(channels_labels, rotation=0)
    
    plt.suptitle('Subgroup Comparison: Brain-Behavior Mapping for DD vs. TD Groups', y=1.02, fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
