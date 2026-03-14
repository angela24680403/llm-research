#!/usr/bin/env python3
"""
Personality Distribution Analysis Dashboard
Examines how LLM personalities vary across models, contexts, and configurations.

Research Focus:
- Models are not monolithic: they adopt different personalities in different contexts
- Compare personality distributions across: model types, generations, distilled vs original
- Measure personality consistency and variability within and across use-cases
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
import json
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURATION
# ============================================================================

CSV_PATH = Path(__file__).parent.parent / "demo-notebooks" / "generated_results" / "7000_sampling_emotions.csv"
OUTPUT_DIR = Path(__file__).parent / "outputs"
ALPHA = 0.05

EMOTIONS = [
    "joy", "excitement", "confusion", "curiosity", "admiration",
    "approval", "caring", "nervousness", "optimism", "surprise"
]

# Model groupings for comparison
MODEL_GROUPS = {
    "Base Models": ["llama-8b-base", "mistral", "qwen-moe-base"],
    "Chat Models": ["llama-8b-chat", "llama-70b-chat", "mistral-chat", 
                    "qwen-8b-chat", "qwen-32b-chat", "qwen-moe-chat"],
    "Distilled": ["llama-8b-4b-distill-chat"],
    "MOE Models": ["mistral-chat-moe", "qwen-moe-chat", "qwen-moe-base"],
}

PERSONALITY_TYPES = ["neutral", "school", "reddit", "linkedin", "news", "research", "vlog"]

# ============================================================================
# DATA LOADING & PREPROCESSING
# ============================================================================

def load_data(csv_path):
    """Load and prepare data for analysis."""
    df = pd.read_csv(csv_path)
    print(f"✓ Loaded {len(df)} rows × {len(df.columns)} columns")
    return df


def compute_personality_probability(df, emotion, personality, model=None):
    """
    Compute probability of emotion response for a given personality.
    
    This is the core metric: how likely is a model to express this emotion
    when adopting this personality in different scenarios?
    """
    subset = df[df['personality'] == personality].copy()
    if model:
        subset = subset[subset['model'] == model]
    
    prob_a = subset[f'{emotion}_prob_a']
    prob_b = subset[f'{emotion}_prob_b']
    
    # Combine both conditions for a single distribution
    combined = pd.concat([prob_a, prob_b])
    
    return {
        'emotion': emotion,
        'personality': personality,
        'model': model,
        'mean': combined.mean(),
        'std': combined.std(),
        'median': combined.median(),
        'q25': combined.quantile(0.25),
        'q75': combined.quantile(0.75),
        'iqr': combined.quantile(0.75) - combined.quantile(0.25),
        'range': (combined.min(), combined.max()),
        'n': len(combined),
        'values': combined.values
    }


def compute_personality_profile(df, personality, model=None):
    """
    Compute the complete personality profile (all emotions).
    
    This creates a "personality fingerprint" showing the distribution of
    emotional responses for a given personality across all emotions.
    """
    results = []
    for emotion in EMOTIONS:
        stats_dict = compute_personality_probability(df, emotion, personality, model)
        results.append(stats_dict)
    
    return pd.DataFrame(results)


def compute_personality_consistency(df, emotion, model):
    """
    Measure how consistent a model is in expressing an emotion
    across different personality contexts.
    
    High consistency = model always expresses emotion similarly
    Low consistency = model dramatically changes emotion based on personality
    """
    results = []
    
    for personality in PERSONALITY_TYPES:
        stats_dict = compute_personality_probability(df, emotion, personality, model)
        results.append(stats_dict)
    
    df_consistency = pd.DataFrame(results)
    
    # Calculate coefficient of variation (CV) across personalities
    cv = df_consistency['std'].mean() / df_consistency['mean'].mean() if df_consistency['mean'].mean() > 0 else 0
    
    # Calculate range of means across personalities
    mean_range = df_consistency['mean'].max() - df_consistency['mean'].min()
    
    return {
        'model': model,
        'emotion': emotion,
        'consistency_cv': cv,  # Lower = more consistent
        'mean_range': mean_range,  # Lower = more consistent
        'per_personality': df_consistency
    }


def compute_personality_diversity(df, model):
    """
    Measure how diverse a model's personality expressions are.
    
    Diversity = how much the model changes its emotional profiles
    when adopting different personalities.
    """
    profiles = {}
    for personality in PERSONALITY_TYPES:
        profile = compute_personality_profile(df, personality, model)
        profiles[personality] = profile['mean'].values
    
    # Calculate pairwise distances between personality profiles
    personality_list = list(profiles.keys())
    distances = []
    
    for i, p1 in enumerate(personality_list):
        for j, p2 in enumerate(personality_list[i+1:], i+1):
            dist = np.linalg.norm(profiles[p1] - profiles[p2])
            distances.append({
                'model': model,
                'personality_1': p1,
                'personality_2': p2,
                'euclidean_distance': dist
            })
    
    return {
        'model': model,
        'mean_diversity': np.mean([d['euclidean_distance'] for d in distances]),
        'std_diversity': np.std([d['euclidean_distance'] for d in distances]),
        'distances': distances
    }

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_personality_distributions_by_model(df, output_dir):
    """
    Visualization 1: Distribution of emotions across personalities for each model.
    
    Shows: How does each model vary its emotional expressions across personality types?
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    models = df['model'].unique()
    n_emotions = len(EMOTIONS)
    n_models = len(models)
    
    fig = plt.figure(figsize=(20, 12))
    
    for idx, model in enumerate(sorted(models), 1):
        ax = plt.subplot(3, 4, idx)
        
        model_data = []
        for emotion in EMOTIONS:
            for personality in PERSONALITY_TYPES:
                stats_dict = compute_personality_probability(df, emotion, personality, model)
                model_data.append({
                    'emotion': emotion.capitalize(),
                    'personality': personality.capitalize(),
                    'mean_prob': stats_dict['mean']
                })
        
        model_df = pd.DataFrame(model_data)
        pivot = model_df.pivot(index='emotion', columns='personality', values='mean_prob')
        
        sns.heatmap(
            pivot, 
            cmap='YlOrRd', 
            ax=ax, 
            cbar=False,
            vmin=0, 
            vmax=0.5,
            annot=True,
            fmt='.2f',
            cbar_kws={'label': 'Mean Probability'}
        )
        
        ax.set_title(f'{model}', fontsize=11, fontweight='bold')
        ax.set_ylabel('Emotion', fontsize=9)
        ax.set_xlabel('Personality Type', fontsize=9)
        
        if idx != 1:
            ax.set_ylabel('')
        if idx <= 8:
            ax.set_xlabel('')
    
    plt.suptitle(
        'Personality Profiles: Emotion Distributions by Model\n'
        'Each cell shows mean probability of emotion expression for that personality type',
        fontsize=14,
        fontweight='bold',
        y=0.995
    )
    plt.tight_layout()
    plt.savefig(output_dir / 'viz_01_personality_profiles_by_model.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: viz_01_personality_profiles_by_model.png")
    plt.close()


def plot_personality_consistency(df, output_dir):
    """
    Visualization 2: How consistent is each model across personality contexts?
    
    Shows: Which models maintain consistent emotional profiles vs. adapting to personalities?
    """
    output_dir = Path(output_dir)
    
    models = df['model'].unique()
    consistency_results = []
    
    for model in models:
        for emotion in EMOTIONS:
            result = compute_personality_consistency(df, emotion, model)
            consistency_results.append({
                'model': model,
                'emotion': emotion,
                'consistency_cv': result['consistency_cv'],
                'mean_range': result['mean_range']
            })
    
    consistency_df = pd.DataFrame(consistency_results)
    
    # Aggregate by model
    model_consistency = consistency_df.groupby('model').agg({
        'consistency_cv': 'mean',
        'mean_range': 'mean'
    }).reset_index()
    
    model_consistency = model_consistency.sort_values('mean_range', ascending=False)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Coefficient of Variation (consistency metric)
    colors1 = ['#2ecc71' if x < model_consistency['consistency_cv'].median() else '#e74c3c' 
              for x in model_consistency['consistency_cv']]
    ax1.barh(model_consistency['model'], model_consistency['consistency_cv'], color=colors1)
    ax1.set_xlabel('Mean Coefficient of Variation\n(Lower = More Consistent)', fontsize=11, fontweight='bold')
    ax1.set_title('Personality Consistency Across Emotions\nCoefficient of Variation by Model', 
                  fontsize=12, fontweight='bold')
    ax1.axvline(model_consistency['consistency_cv'].median(), color='black', linestyle='--', 
                linewidth=2, alpha=0.5, label='Median')
    ax1.legend()
    ax1.grid(axis='x', alpha=0.3)
    
    # Plot 2: Range of means
    colors2 = ['#3498db' if x < model_consistency['mean_range'].median() else '#f39c12' 
              for x in model_consistency['mean_range']]
    ax2.barh(model_consistency['model'], model_consistency['mean_range'], color=colors2)
    ax2.set_xlabel('Mean Range (Max - Min Probability)\n(Lower = More Consistent)', 
                   fontsize=11, fontweight='bold')
    ax2.set_title('Personality Adaptability\nRange of Emotion Expression by Model', 
                  fontsize=12, fontweight='bold')
    ax2.axvline(model_consistency['mean_range'].median(), color='black', linestyle='--', 
                linewidth=2, alpha=0.5, label='Median')
    ax2.legend()
    ax2.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'viz_02_personality_consistency.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: viz_02_personality_consistency.png")
    plt.close()
    
    return model_consistency


def plot_personality_diversity(df, output_dir):
    """
    Visualization 3: Personality space diversity.
    
    Shows: How much do models spread their personalities across emotional dimensions?
    """
    output_dir = Path(output_dir)
    
    models = df['model'].unique()
    diversity_results = []
    
    for model in models:
        result = compute_personality_diversity(df, model)
        diversity_results.append({
            'model': model,
            'mean_diversity': result['mean_diversity'],
            'std_diversity': result['std_diversity']
        })
    
    diversity_df = pd.DataFrame(diversity_results).sort_values('mean_diversity', ascending=False)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Color by type
    def get_color(model):
        for group, models_list in MODEL_GROUPS.items():
            if model in models_list:
                if group == "Base Models":
                    return '#3498db'
                elif group == "Chat Models":
                    return '#2ecc71'
                elif group == "Distilled":
                    return '#e74c3c'
                elif group == "MOE Models":
                    return '#f39c12'
    
    colors = [get_color(m) for m in diversity_df['model']]
    
    y_pos = np.arange(len(diversity_df))
    ax.barh(y_pos, diversity_df['mean_diversity'], 
            xerr=diversity_df['std_diversity'], 
            color=colors, alpha=0.8, capsize=5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(diversity_df['model'])
    ax.set_xlabel('Mean Euclidean Distance Between Personality Profiles\n(Higher = More Diverse)', 
                  fontsize=11, fontweight='bold')
    ax.set_title('Personality Diversity: How Much Models Vary Across Personalities\n'
                 'Measured by distance between 7-personality emotional profiles',
                 fontsize=12, fontweight='bold')
    ax.grid(axis='x', alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#3498db', label='Base Models'),
        Patch(facecolor='#2ecc71', label='Chat Models'),
        Patch(facecolor='#e74c3c', label='Distilled'),
        Patch(facecolor='#f39c12', label='MOE Models'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'viz_03_personality_diversity.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: viz_03_personality_diversity.png")
    plt.close()
    
    return diversity_df


def plot_emotion_variability_heatmap(df, output_dir):
    """
    Visualization 4: Emotional variability across contexts.
    
    Shows: Which emotions are most stable vs. variable across personalities?
    """
    output_dir = Path(output_dir)
    
    variability_data = []
    
    for emotion in EMOTIONS:
        for personality in PERSONALITY_TYPES:
            stats_dict = compute_personality_probability(df, emotion, personality)
            variability_data.append({
                'emotion': emotion.capitalize(),
                'personality': personality.capitalize(),
                'std': stats_dict['std'],
                'mean': stats_dict['mean'],
                'cv': stats_dict['std'] / stats_dict['mean'] if stats_dict['mean'] > 0 else 0
            })
    
    var_df = pd.DataFrame(variability_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: Coefficient of Variation
    pivot_cv = var_df.pivot(index='emotion', columns='personality', values='cv')
    sns.heatmap(pivot_cv, annot=True, fmt='.2f', cmap='RdYlGn_r', ax=ax1, cbar_kws={'label': 'CV'})
    ax1.set_title('Emotion Variability: Coefficient of Variation\nAcross Personality Types\n'
                  'Higher CV = More variable across contexts',
                  fontsize=12, fontweight='bold')
    ax1.set_ylabel('Emotion', fontsize=11)
    ax1.set_xlabel('Personality Type', fontsize=11)
    
    # Plot 2: Standard Deviation
    pivot_std = var_df.pivot(index='emotion', columns='personality', values='std')
    sns.heatmap(pivot_std, annot=True, fmt='.3f', cmap='YlOrRd', ax=ax2, cbar_kws={'label': 'SD'})
    ax2.set_title('Emotion Variability: Standard Deviation\nAcross Personality Types\n'
                  'Higher SD = Wider range of expression',
                  fontsize=12, fontweight='bold')
    ax2.set_ylabel('Emotion', fontsize=11)
    ax2.set_xlabel('Personality Type', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'viz_04_emotion_variability.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: viz_04_emotion_variability.png")
    plt.close()
    
    return var_df


def plot_model_type_comparison(df, output_dir):
    """
    Visualization 5: Compare personality distributions across model types.
    
    Shows: Do base models differ from chat models in personality expression?
    """
    output_dir = Path(output_dir)
    
    type_data = []
    
    for model_type, models_list in MODEL_GROUPS.items():
        subset = df[df['model'].isin(models_list)]
        
        for emotion in EMOTIONS:
            for personality in PERSONALITY_TYPES:
                prob_a = subset[subset['personality'] == personality][f'{emotion}_prob_a']
                prob_b = subset[subset['personality'] == personality][f'{emotion}_prob_b']
                combined = pd.concat([prob_a, prob_b])
                
                type_data.append({
                    'model_type': model_type,
                    'emotion': emotion.capitalize(),
                    'personality': personality.capitalize(),
                    'mean': combined.mean(),
                    'std': combined.std()
                })
    
    type_df = pd.DataFrame(type_data)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, model_type in enumerate(sorted(MODEL_GROUPS.keys())):
        ax = axes[idx]
        subset = type_df[type_df['model_type'] == model_type]
        pivot = subset.pivot(index='emotion', columns='personality', values='mean')
        
        sns.heatmap(pivot, annot=True, fmt='.2f', cmap='viridis', ax=ax, 
                   vmin=0, vmax=0.5, cbar_kws={'label': 'Mean Prob'})
        ax.set_title(f'{model_type}\n({len(MODEL_GROUPS[model_type])} models)', 
                    fontsize=12, fontweight='bold')
        ax.set_ylabel('Emotion', fontsize=10)
        ax.set_xlabel('Personality Type', fontsize=10)
    
    plt.suptitle(
        'Personality Expression by Model Type\n'
        'Comparing Base vs Chat vs Distilled vs MOE models',
        fontsize=14, fontweight='bold', y=0.995
    )
    plt.tight_layout()
    plt.savefig(output_dir / 'viz_05_model_type_comparison.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: viz_05_model_type_comparison.png")
    plt.close()
    
    return type_df


def plot_model_generation_comparison(df, output_dir):
    """
    Visualization 6: Compare personality distributions across model generations.
    
    Shows: Do larger models (70B) differ from smaller ones in personality?
    """
    output_dir = Path(output_dir)
    
    # Extract model size/generation
    def categorize_model(model):
        if '70b' in model.lower():
            return '70B'
        elif '32b' in model.lower():
            return '32B'
        elif '8b' in model.lower():
            return '8B'
        elif 'moe' in model.lower():
            return 'MOE'
        else:
            return 'Other'
    
    df['model_category'] = df['model'].apply(categorize_model)
    
    gen_data = []
    
    for cat in ['8B', '32B', '70B', 'MOE', 'Other']:
        subset = df[df['model_category'] == cat]
        if len(subset) == 0:
            continue
        
        for emotion in EMOTIONS:
            for personality in PERSONALITY_TYPES:
                prob_a = subset[subset['personality'] == personality][f'{emotion}_prob_a']
                prob_b = subset[subset['personality'] == personality][f'{emotion}_prob_b']
                combined = pd.concat([prob_a, prob_b])
                
                if len(combined) > 0:
                    gen_data.append({
                        'generation': cat,
                        'emotion': emotion.capitalize(),
                        'personality': personality.capitalize(),
                        'mean': combined.mean(),
                        'std': combined.std()
                    })
    
    gen_df = pd.DataFrame(gen_data)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Plot 1: By personality
    for personality in ['Neutral', 'Vlog', 'Reddit', 'LinkedIn']:
        subset = gen_df[gen_df['personality'] == personality]
        pivot = subset.pivot(index='emotion', columns='generation', values='mean')
        cols_to_keep = [col for col in ['8B', '32B', '70B', 'MOE', 'Other'] if col in pivot.columns]
        pivot = pivot[cols_to_keep]
        
        for col in pivot.columns:
            axes[0].plot(pivot.index, pivot[col], marker='o', linewidth=2, label=col)
        axes[0].set_title('Personality Expression by Model Generation\n(Neutral Personality)', 
                         fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Mean Emotion Probability', fontsize=11)
        axes[0].set_xlabel('Emotion', fontsize=11)
        axes[0].legend(title='Model Size', loc='best')
        axes[0].grid(alpha=0.3)
        break
    
    # Plot 2: Comparison across all personalities
    gen_summary = gen_df.groupby('generation')['mean'].agg(['mean', 'std']).sort_index()
    
    axes[1].bar(gen_summary.index, gen_summary['mean'], yerr=gen_summary['std'], 
               capsize=5, alpha=0.7, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#95a5a6'])
    axes[1].set_ylabel('Mean Emotion Probability (Aggregated)', fontsize=11, fontweight='bold')
    axes[1].set_title('Personality Expression by Model Generation\n(All emotions, all personalities aggregated)', 
                     fontsize=12, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'viz_06_generation_comparison.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: viz_06_generation_comparison.png")
    plt.close()
    
    return gen_df


def plot_personality_radar(df, output_dir):
    """
    Visualization 7: Radar chart comparing personalities.
    
    Shows: What is the unique emotional signature of each personality type?
    """
    output_dir = Path(output_dir)
    
    from math import pi
    
    fig, axes = plt.subplots(2, 4, figsize=(18, 10), subplot_kw=dict(projection='polar'))
    axes = axes.flatten()
    
    for idx, personality in enumerate(PERSONALITY_TYPES):
        ax = axes[idx]
        
        means = []
        for emotion in EMOTIONS:
            stats_dict = compute_personality_probability(df, emotion, personality)
            means.append(stats_dict['mean'])
        
        # Close the plot
        means += means[:1]
        angles = [n / float(len(EMOTIONS)) * 2 * pi for n in range(len(EMOTIONS))]
        angles += angles[:1]
        
        ax.plot(angles, means, 'o-', linewidth=2, color='#3498db', markersize=8)
        ax.fill(angles, means, alpha=0.25, color='#3498db')
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([e.capitalize()[:3] for e in EMOTIONS], size=9)
        ax.set_ylim(0, 0.5)
        ax.set_title(f'{personality.capitalize()}', fontsize=11, fontweight='bold', pad=20)
        ax.grid(True)
    
    # Remove extra subplot
    fig.delaxes(axes[7])
    
    plt.suptitle('Personality Emotional Profiles: Radar Charts\n'
                 'Each polygon represents the emotional expression profile of a personality type',
                 fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.savefig(output_dir / 'viz_07_personality_radar.png', dpi=150, bbox_inches='tight')
    print("✓ Saved: viz_07_personality_radar.png")
    plt.close()


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_analysis(csv_path, output_dir):
    """Run complete personality distribution analysis."""
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n{'='*80}")
    print("PERSONALITY DISTRIBUTION ANALYSIS")
    print(f"{'='*80}\n")
    
    # Load data
    df = load_data(csv_path)
    
    print("\n📊 GENERATING VISUALIZATIONS...\n")
    
    # Generate all visualizations
    plot_personality_distributions_by_model(df, output_dir)
    consistency_df = plot_personality_consistency(df, output_dir)
    diversity_df = plot_personality_diversity(df, output_dir)
    variability_df = plot_emotion_variability_heatmap(df, output_dir)
    type_df = plot_model_type_comparison(df, output_dir)
    gen_df = plot_model_generation_comparison(df, output_dir)
    plot_personality_radar(df, output_dir)
    
    print(f"\n{'='*80}")
    print("✓ Analysis complete!")
    print(f"{'='*80}\n")
    
    return {
        'data': df,
        'consistency': consistency_df,
        'diversity': diversity_df,
        'variability': variability_df,
        'type_comparison': type_df,
        'generation_comparison': gen_df
    }


if __name__ == "__main__":
    results = run_analysis(CSV_PATH, OUTPUT_DIR)
    
    print(f"\n📁 Output directory: {OUTPUT_DIR}")
    print(f"\n✨ Generated 7 visualizations:")
    print("  1. Personality profiles by model")
    print("  2. Personality consistency analysis")
    print("  3. Personality diversity")
    print("  4. Emotion variability heatmap")
    print("  5. Model type comparison")
    print("  6. Model generation comparison")
    print("  7. Personality radar charts")
