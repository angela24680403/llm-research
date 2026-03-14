#!/bin/bash
# Quick runner for personality distribution analysis

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Personality Distribution Analysis"
echo "=========================================="
echo ""

# Check dependencies
echo "📦 Checking dependencies..."
python3 -m pip install -q statsmodels seaborn matplotlib scipy pandas numpy 2>/dev/null || true

# Run pipeline
echo ""
echo "🚀 Running analysis..."
python3 personality_distribution_pipeline.py

echo ""
echo "=========================================="
echo "✅ Complete!"
echo "=========================================="
echo ""
echo "📁 Results: outputs/"
echo ""
echo "📊 Visualizations generated:"
echo "  1️⃣  Personality profiles (all models)"
echo "  2️⃣  Personality consistency analysis"
echo "  3️⃣  Personality diversity comparison"
echo "  4️⃣  Emotion variability heatmap"
echo "  5️⃣  Model type comparison"
echo "  6️⃣  Model generation comparison"
echo "  7️⃣  Personality radar charts"
echo ""
echo "📖 Documentation:"
echo "  • METHODOLOGY.md - Full research methodology"
echo "  • README.md - Quick reference"
echo ""
