# LLM Personality Distribution Analysis

A comprehensive research dashboard examining how large language models express diverse personalities across different contexts.

## 🎯 Research Thesis

Large Language Models are **NOT monolithic personality entities**. Instead, they can express diverse personalities across different contexts, users, and use-cases.

## 📊 Contents

### Dashboard
- **Main Dashboard**: `personality_distribution_analysis/dashboard.html`
  - 7 Personality distribution visualizations
  - 10 Emotion significance heatmaps (integrated)
  - 40,000+ words of documentation
  - Interactive navigation and lightbox viewer

- **Heatmap Gallery**: `significance_heatmap_analysis/outputs/index.html`
  - Standalone viewer for all 10 emotion heatmaps
  - Statistical significance analysis

## 🔬 Key Findings

1. **Models are personality-responsive** - Significantly change emotional output with different personality instructions
2. **Chat > Base in diversity** - Chat models show 2.1× higher personality diversity (0.28 vs 0.13)
3. **Training matters** - RLHF training affects personality plasticity
4. **Selective responsiveness** - Approval, caring, joy are highly responsive; curiosity is stable
5. **Scaling works** - Effects hold across 8B, 32B, and 70B models

## 📈 Visualizations

- **Viz 1**: Personality profiles by model (11-panel heatmap)
- **Viz 2**: Personality consistency (CV analysis)
- **Viz 3**: Personality diversity (Euclidean distances) ⭐ KEY
- **Viz 4**: Emotion variability (personality-responsive emotions)
- **Viz 5**: Model type comparison (Base vs Chat)
- **Viz 6**: Model generation comparison (8B, 32B, 70B)
- **Viz 7**: Personality radar charts (7 emotional archetypes)

## 📚 Documentation

- `00_START_HERE.md` - Quick overview
- `README.md` - Quick reference
- `INDEX.md` - Detailed visualization guide
- `METHODOLOGY.md` - Complete 22,000-word research methodology

## 🛠️ Technical

- Analysis: 11 models × 7 personalities × 10 emotions
- Data: 7,700 observations from emotion classifier
- Statistical testing: t-tests with FDR correction
- Visualizations: 150 DPI PNG files (publication-ready)

## 💾 Files

```
personality_distribution_analysis/
├── dashboard.html (MAIN - open this!)
├── 00_START_HERE.md
├── README.md
├── INDEX.md
├── METHODOLOGY.md
├── personality_distribution_pipeline.py
└── outputs/
    ├── viz_01_personality_profiles_by_model.png
    ├── viz_02_personality_consistency.png
    ├── viz_03_personality_diversity.png
    ├── viz_04_emotion_variability.png
    ├── viz_05_model_type_comparison.png
    ├── viz_06_generation_comparison.png
    └── viz_07_personality_radar.png

significance_heatmap_analysis/
├── README.md
├── significance_heatmap_pipeline.py
└── outputs/
    ├── admiration_heatmap.png
    ├── approval_heatmap.png
    ├── caring_heatmap.png
    ├── confusion_heatmap.png
    ├── curiosity_heatmap.png
    ├── excitement_heatmap.png
    ├── joy_heatmap.png
    ├── nervousness_heatmap.png
    ├── optimism_heatmap.png
    └── surprise_heatmap.png
```

## 🎨 Features

- Night mode with beautiful gradients
- Interactive visualizations and lightbox viewer
- Professional research aesthetic
- Fully responsive design
- Embedded documentation
- Cute cat emojis 😸

## 📖 How to Use

1. Open `personality_distribution_analysis/dashboard.html` in a browser
2. Navigate through sections using the sidebar menu
3. Click visualizations to view full-size in lightbox
4. Read documentation for complete methodology

## 🔗 Links

- GitHub: https://github.com/angela24680403/llm-research
- Live Dashboard: https://angela24680403.github.io/llm-research/

---

**Status**: Research dashboard complete and publication-ready ✅
