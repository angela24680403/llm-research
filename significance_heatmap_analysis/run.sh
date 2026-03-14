#!/bin/bash
# Quick runner script for the significance heatmap pipeline

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "================================"
echo "Significance Heatmap Pipeline"
echo "================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    exit 1
fi

# Install dependencies if needed
echo "📦 Checking dependencies..."
python3 -m pip install -q statsmodels seaborn matplotlib scipy pandas numpy 2>/dev/null || true

# Run the pipeline
echo ""
echo "🚀 Running pipeline..."
python3 significance_heatmap_pipeline.py

# Show output location
echo ""
echo "================================"
echo "✅ Complete!"
echo "================================"
echo ""
echo "📁 Results location: outputs/"
echo "🌐 Open dashboard: outputs/index.html"
echo ""
echo "Tips:"
echo "  - Click emotion cards to switch between views"
echo "  - Tables show top 10 most significant effects"
echo "  - Check README.md for detailed documentation"
