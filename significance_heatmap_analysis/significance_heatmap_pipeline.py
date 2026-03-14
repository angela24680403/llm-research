#!/usr/bin/env python3
"""
Significance Heatmap Pipeline
Generates statistical significance heatmaps for all emotions/traits.
Creates interactive HTML dashboard for exploration.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_1samp
from statsmodels.stats.multitest import multipletests
import matplotlib.patches as mpatches
from pathlib import Path
import json
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

CSV_PATH = Path(__file__).parent / "demo-notebooks" / "generated_results" / "7000_sampling_emotions.csv"
OUTPUT_DIR = Path(__file__).parent / "generated_results" / "significance_heatmaps"
ALPHA = 0.05

EMOTIONS = [
    "joy",
    "excitement",
    "confusion",
    "curiosity",
    "admiration",
    "approval",
    "caring",
    "nervousness",
    "optimism",
    "surprise"
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def compute_statistics(df, trait_name, alpha=0.05):
    """
    Compute statistical significance for a trait across all model × personality groups.
    
    Returns:
        pd.DataFrame with columns:
        - model, personality, mean_diff, p_value, ci_low, ci_high, n, p_adj, significant
    """
    df = df.copy()
    df[f"{trait_name}_diff"] = df[f"{trait_name}_prob_a"] - df[f"{trait_name}_prob_b"]
    
    results = []
    
    for (model, personality), group in df.groupby(["model", "personality"]):
        diffs = group[f"{trait_name}_diff"]
        
        if len(diffs) < 2:
            continue
        
        mean = diffs.mean()
        n = len(diffs)
        
        t_stat, p_val = ttest_1samp(diffs, 0)
        
        se = diffs.std(ddof=1) / np.sqrt(n)
        ci_low = mean - 1.96 * se
        ci_high = mean + 1.96 * se
        
        results.append({
            "model": model,
            "personality": personality,
            "mean_diff": mean,
            "p_value": p_val,
            "ci_low": ci_low,
            "ci_high": ci_high,
            "n": n
        })
    
    results_df = pd.DataFrame(results)
    
    # FDR correction
    if len(results_df) > 0:
        rejected, p_adj, _, _ = multipletests(
            results_df["p_value"],
            method="fdr_bh",
            alpha=alpha
        )
        results_df["p_adj"] = p_adj
        results_df["significant"] = rejected
    
    return results_df.sort_values("p_adj")


def plot_significance_heatmap(results_df, trait_name, alpha=0.05, output_path=None):
    """
    Generate a publication-quality heatmap for a single trait.
    
    Args:
        results_df: DataFrame from compute_statistics()
        trait_name: Name of the trait (for title)
        alpha: Significance threshold
        output_path: If provided, save to PNG file
    
    Returns:
        fig object or saves to file
    """
    
    # Pivot tables
    pivot_mean = results_df.pivot(
        index="model",
        columns="personality",
        values="mean_diff"
    )
    
    pivot_sig = results_df.pivot(
        index="model",
        columns="personality",
        values="significant"
    )
    
    pivot_n = results_df.pivot(
        index="model",
        columns="personality",
        values="n"
    )
    
    pivot_ci_low = results_df.pivot(
        index="model",
        columns="personality",
        values="ci_low"
    )
    
    pivot_ci_high = results_df.pivot(
        index="model",
        columns="personality",
        values="ci_high"
    )
    
    n_rows = pivot_mean.shape[0]
    n_cols = pivot_mean.shape[1]
    
    # Scale figure size
    cell_h = 1.4
    cell_w = 1.8
    fig_w = max(12, n_cols * cell_w + 4)
    fig_h = max(6, n_rows * cell_h + 2)
    
    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    
    vmax = max(abs(pivot_mean.min().min()), abs(pivot_mean.max().max()))
    
    sns.heatmap(
        pivot_mean,
        cmap="RdBu_r",
        center=0,
        vmin=-vmax,
        vmax=vmax,
        annot=False,
        linewidths=0.8,
        linecolor='#cccccc',
        cbar_kws={
            'label': f'Mean Difference in {trait_name} Probability\n(Condition A − Condition B)',
            'shrink': 0.75,
            'pad': 0.02,
        },
        ax=ax
    )
    
    # Annotation positions
    Y_MEAN = 0.30
    Y_CI = 0.55
    Y_N = 0.76
    
    # Add text annotations
    for i in range(n_rows):
        for j in range(n_cols):
            mean_val = pivot_mean.iloc[i, j]
            sig = pivot_sig.iloc[i, j]
            n_val = pivot_n.iloc[i, j]
            ci_low = pivot_ci_low.iloc[i, j]
            ci_high = pivot_ci_high.iloc[i, j]
            
            if pd.isnull(mean_val):
                continue
            
            dark_cell = abs(mean_val) >= 0.3 * vmax
            ink = "white" if dark_cell else "black"
            ink_soft = "lightgray" if dark_cell else "#555555"
            
            cx = j + 0.5
            cy = i
            
            # Main text
            main_text = f"{mean_val:+.3f}"
            if sig:
                main_text += "  ***"
            
            ax.text(
                cx, cy + Y_MEAN,
                main_text,
                ha="center", va="center",
                color=ink,
                fontsize=10,
                fontweight="bold" if sig else "normal",
            )
            
            # CI
            ax.text(
                cx, cy + Y_CI,
                f"[{ci_low:+.2f}, {ci_high:+.2f}]",
                ha="center", va="center",
                color=ink_soft,
                fontsize=7.5,
            )
            
            # Sample size
            ax.text(
                cx, cy + Y_N,
                f"n = {int(n_val)}",
                ha="center", va="center",
                color=ink_soft,
                fontsize=6.5,
                style="italic",
            )
    
    # Labels and title
    ax.set_title(
        f"Statistical Analysis: {trait_name.capitalize()} Signal Strength Comparison\n"
        f"Mean Difference (A − B) by Model and Personality Type",
        fontsize=13,
        fontweight="bold",
        pad=16,
    )
    
    ax.set_ylabel("AI Model", fontsize=11, fontweight="bold", labelpad=10)
    ax.set_xlabel("Personality Type", fontsize=11, fontweight="bold", labelpad=10)
    
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=30,
        ha="right",
        fontsize=9,
    )
    ax.set_yticklabels(
        ax.get_yticklabels(),
        rotation=0,
        fontsize=9,
    )
    
    # Legend
    legend_elements = [
        mpatches.Patch(color="none", label=f"*** Significant (FDR-corrected p < {alpha})"),
        mpatches.Patch(color="none", label="Values: mean difference (A − B)"),
        mpatches.Patch(color="none", label="Brackets: 95 % confidence interval"),
        mpatches.Patch(color="none", label="n: sample size per cell"),
    ]
    
    ax.legend(
        handles=legend_elements,
        loc="upper left",
        bbox_to_anchor=(1.18, 1.02),
        frameon=True,
        fancybox=True,
        shadow=True,
        title="Legend",
        title_fontsize=10,
        fontsize=8.5,
        borderpad=0.8,
        labelspacing=0.6,
    )
    
    # Footer
    fig.text(
        0.5, 0.005,
        "Positive values (red) → higher probability in Condition A  |  "
        "Negative values (blue) → higher probability in Condition B",
        ha="center",
        fontsize=8.5,
        style="italic",
        color="#444444",
    )
    
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f"✓ Saved: {output_path}")
    
    plt.close()
    
    return fig


def print_summary(results_df, trait_name, alpha=0.05):
    """Print console summary of results."""
    print("\n" + "=" * 80)
    print(f"SUMMARY: {trait_name.upper()}")
    print("=" * 80)
    print(f"Total comparisons            : {len(results_df)}")
    print(f"Significant (FDR-corrected)  : {results_df['significant'].sum()}")
    print(f"Correction method            : Benjamini-Hochberg FDR")
    print(f"Significance level (α)       : {alpha}")
    
    if results_df['significant'].sum() > 0:
        print("\nTop 5 Most Significant Effects:")
        print("-" * 80)
        top_results = results_df.nsmallest(5, "p_adj")[
            ["model", "personality", "mean_diff", "p_adj", "ci_low", "ci_high"]
        ]
        for _, row in top_results.iterrows():
            print(
                f"  {row['model']:<18} × {row['personality']:<18}: "
                f"Δ = {row['mean_diff']:+.3f} "
                f"[{row['ci_low']:+.2f}, {row['ci_high']:+.2f}], "
                f"p_adj = {row['p_adj']:.3e}"
            )
    else:
        print("\nNo significant effects found after FDR correction.")


def run_pipeline(csv_path, output_dir, emotions, alpha=0.05):
    """
    Main pipeline: compute statistics and generate plots for all emotions.
    """
    csv_path = Path(csv_path)
    output_dir = Path(output_dir)
    
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print("SIGNIFICANCE HEATMAP PIPELINE")
    print(f"{'='*80}")
    print(f"Loading data from: {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows × {len(df.columns)} columns")
    
    # Verify emotion columns exist
    missing_cols = []
    for emotion in emotions:
        if f"{emotion}_prob_a" not in df.columns or f"{emotion}_prob_b" not in df.columns:
            missing_cols.append(emotion)
    
    if missing_cols:
        raise ValueError(f"Missing columns for emotions: {missing_cols}")
    
    print(f"Processing {len(emotions)} emotions...\n")
    
    # Store results for HTML generation
    all_results = {}
    metadata = {}
    
    for emotion in emotions:
        print(f"[{emotion.upper()}]", end=" ")
        
        # Compute statistics
        results_df = compute_statistics(df, emotion, alpha=alpha)
        all_results[emotion] = results_df
        
        # Print summary
        print_summary(results_df, emotion, alpha=alpha)
        
        # Generate plot
        png_path = output_dir / f"{emotion}_heatmap.png"
        plot_significance_heatmap(results_df, emotion, alpha=alpha, output_path=png_path)
        
        # Store metadata
        metadata[emotion] = {
            "n_comparisons": len(results_df),
            "n_significant": int(results_df['significant'].sum()),
            "max_effect": float(results_df['mean_diff'].abs().max()),
            "png_file": f"{emotion}_heatmap.png"
        }
    
    print("\n" + "=" * 80)
    print(f"✓ Pipeline complete! Generated {len(emotions)} heatmaps.")
    print(f"✓ Output directory: {output_dir}")
    
    return all_results, metadata, output_dir


# ============================================================================
# HTML GENERATION
# ============================================================================

def generate_html_dashboard(results_dict, metadata, output_dir):
    """
    Generate an interactive HTML dashboard for exploring all heatmaps.
    
    Args:
        results_dict: Dict[emotion_name -> DataFrame]
        metadata: Dict[emotion_name -> dict with statistics]
        output_dir: Path to save HTML
    """
    output_dir = Path(output_dir)
    html_path = output_dir / "index.html"
    
    emotions = list(results_dict.keys())
    
    # Build emotion card HTML
    emotion_cards = ""
    for emotion in emotions:
        meta = metadata[emotion]
        png_file = meta["png_file"]
        n_sig = meta["n_significant"]
        n_total = meta["n_comparisons"]
        max_effect = meta["max_effect"]
        
        sig_pct = 100 * n_sig / n_total if n_total > 0 else 0
        
        emotion_cards += f"""
    <div class="emotion-card" onclick="switchEmotion('{emotion}')">
        <h3>{emotion.capitalize()}</h3>
        <div class="card-stats">
            <p>Significant: <span class="stat-value">{n_sig}/{n_total}</span></p>
            <p>Max Effect: <span class="stat-value">{max_effect:.3f}</span></p>
            <p>Coverage: <span class="stat-value">{sig_pct:.0f}%</span></p>
        </div>
    </div>
"""
    
    # Build image gallery HTML
    image_gallery = ""
    for i, emotion in enumerate(emotions):
        png_file = metadata[emotion]["png_file"]
        display = "block" if i == 0 else "none"
        image_gallery += f"""
    <div class="image-container" id="image-{emotion}" style="display: {display};">
        <h2>{emotion.upper()} Significance Heatmap</h2>
        <img src="{png_file}" alt="{emotion} heatmap" />
    </div>
"""
    
    # Create table summaries
    table_html = ""
    for emotion in emotions:
        results_df = results_dict[emotion]
        
        if len(results_df) > 0:
            # Get top 10 most significant
            top = results_df.nsmallest(10, "p_adj")
            
            table_html += f"""
    <div class="results-table" id="table-{emotion}" style="display: none;">
        <h3>{emotion.upper()} - Top 10 Significant Effects</h3>
        <table>
            <thead>
                <tr>
                    <th>Model</th>
                    <th>Personality</th>
                    <th>Mean Diff</th>
                    <th>95% CI</th>
                    <th>p_adj</th>
                </tr>
            </thead>
            <tbody>
"""
            for _, row in top.iterrows():
                table_html += f"""
                <tr>
                    <td>{row['model']}</td>
                    <td>{row['personality']}</td>
                    <td class="value">{row['mean_diff']:+.3f}</td>
                    <td class="ci">[{row['ci_low']:+.2f}, {row['ci_high']:+.2f}]</td>
                    <td class="pval">{row['p_adj']:.3e}</td>
                </tr>
"""
            table_html += """
            </tbody>
        </table>
    </div>
"""
    
    # Generate full HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Significance Heatmap Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            overflow: hidden;
        }}
        
        header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}
        
        header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .content {{
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 30px;
            padding: 30px;
        }}
        
        .sidebar {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            height: fit-content;
            position: sticky;
            top: 20px;
        }}
        
        .sidebar h3 {{
            margin-bottom: 20px;
            color: #667eea;
            font-size: 1.1em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .emotion-cards {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        
        .emotion-card {{
            background: white;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        
        .emotion-card:hover {{
            border-color: #667eea;
            background: #f0f4ff;
            transform: translateX(5px);
        }}
        
        .emotion-card.active {{
            background: #667eea;
            color: white;
            border-color: #667eea;
        }}
        
        .emotion-card h3 {{
            margin-bottom: 8px;
            font-size: 1em;
        }}
        
        .card-stats {{
            font-size: 0.85em;
        }}
        
        .card-stats p {{
            margin: 5px 0;
            display: flex;
            justify-content: space-between;
        }}
        
        .stat-value {{
            font-weight: bold;
            color: #667eea;
        }}
        
        .emotion-card.active .stat-value {{
            color: #fff;
        }}
        
        .main-content {{
            display: flex;
            flex-direction: column;
            gap: 30px;
        }}
        
        .image-container {{
            text-align: center;
        }}
        
        .image-container h2 {{
            margin-bottom: 20px;
            color: #333;
            font-size: 1.8em;
        }}
        
        .image-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }}
        
        .results-table {{
            margin-top: 30px;
        }}
        
        .results-table h3 {{
            margin-bottom: 15px;
            color: #333;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}
        
        thead {{
            background: #667eea;
            color: white;
        }}
        
        th {{
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9em;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        tbody tr:hover {{
            background: #f5f7fa;
        }}
        
        .value {{
            font-weight: 600;
            color: #667eea;
        }}
        
        .ci {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        .pval {{
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
        }}
        
        footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
        }}
        
        @media (max-width: 768px) {{
            .content {{
                grid-template-columns: 1fr;
            }}
            
            .sidebar {{
                position: static;
            }}
            
            header h1 {{
                font-size: 1.8em;
            }}
            
            .emotion-cards {{
                flex-direction: row;
                flex-wrap: wrap;
            }}
            
            .emotion-card {{
                flex: 1;
                min-width: 150px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Significance Heatmap Dashboard</h1>
            <p>Interactive exploration of statistical significance across emotions and personality types</p>
        </header>
        
        <div class="content">
            <div class="sidebar">
                <h3>Emotions</h3>
                <div class="emotion-cards">
{emotion_cards}
                </div>
            </div>
            
            <div class="main-content">
{image_gallery}
{table_html}
            </div>
        </div>
        
        <footer>
            <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Statistical significance computed using FDR-corrected t-tests</p>
        </footer>
    </div>
    
    <script>
        function switchEmotion(emotion) {{
            // Hide all images and tables
            document.querySelectorAll('.image-container').forEach(el => {{
                el.style.display = 'none';
            }});
            document.querySelectorAll('.results-table').forEach(el => {{
                el.style.display = 'none';
            }});
            
            // Show selected emotion
            document.getElementById('image-' + emotion).style.display = 'block';
            document.getElementById('table-' + emotion).style.display = 'block';
            
            // Update active card
            document.querySelectorAll('.emotion-card').forEach(el => {{
                el.classList.remove('active');
            }});
            event.target.closest('.emotion-card').classList.add('active');
        }}
        
        // Initialize first emotion as active
        document.querySelector('.emotion-card').classList.add('active');
    </script>
</body>
</html>
"""
    
    with open(html_path, 'w') as f:
        f.write(html_content)
    
    print(f"\n✓ HTML Dashboard created: {html_path}")
    return html_path


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Run pipeline
    all_results, metadata, output_dir = run_pipeline(
        CSV_PATH,
        OUTPUT_DIR,
        EMOTIONS,
        alpha=ALPHA
    )
    
    # Generate HTML dashboard
    html_path = generate_html_dashboard(all_results, metadata, output_dir)
    
    print(f"\n{'='*80}")
    print("✓ ALL DONE!")
    print(f"{'='*80}")
    print(f"\n📁 Output location: {output_dir}")
    print(f"📊 Open in browser: {html_path}")
    print(f"\nGenerated files:")
    print(f"  - {len(EMOTIONS)} PNG heatmaps (one per emotion)")
    print(f"  - index.html (interactive dashboard)")
