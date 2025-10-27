# Quick Start Guide - Substack Profile Finder

Get started in 3 minutes!

## Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt
```

## Quick Test

### Option 1: Test with Sample URLs (Recommended First Test)

```bash
# Check a few known tech/product Substacks
python substack_finder.py --urls https://lenny.substack.com https://digitalnative.substack.com
```

Expected output:
- Script will scan the provided URLs
- Extract bios and check for keywords
- Display matches in real-time
- Export results to `results/` directory

### Option 2: Auto-Discovery Mode

```bash
# Discover profiles from Substack's explore pages
python substack_finder.py
```

This will take longer (5-10 minutes) as it:
- Scans multiple category pages
- Checks the leaderboard
- Processes all discovered URLs

### Option 3: Use Sample URLs File

```bash
# Uncomment URLs in sample_urls.txt first
python substack_finder.py --urls-file sample_urls.txt
```

## Customize Keywords

Edit `config.json` to search for different terms:

```json
{
  "keywords": ["your", "custom", "keywords"]
}
```

Example configurations:

**For SaaS Founders:**
```json
{
  "keywords": ["founder", "saas", "startup", "bootstrapped", "indie hacker"]
}
```

**For Design Leaders:**
```json
{
  "keywords": ["design", "designer", "ux", "ui", "product design"]
}
```

**For AI Researchers:**
```json
{
  "keywords": ["ai", "artificial intelligence", "machine learning", "llm", "researcher"]
}
```

## View Results

```bash
# List generated files
ls results/

# View CSV in terminal (requires csvkit or similar)
cat results/substack_profiles_*.csv

# Or open in your favorite spreadsheet app
open results/substack_profiles_*.csv
```

## Common Issues

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "No URLs discovered"
- Check internet connection
- Try manual URLs: `python substack_finder.py --urls https://example.substack.com`

### Script is slow
- This is normal! Rate limiting prevents blocking
- Reduce `max_profiles` in config.json for faster tests
- Use specific URLs instead of auto-discovery

## Next Steps

1. Read the full [README_SUBSTACK_FINDER.md](README_SUBSTACK_FINDER.md)
2. Customize `config.json` for your needs
3. Build your own URL list for targeted searches
4. Export results and analyze in your favorite tool

## Example Output

```
============================================================
Substack Profile Finder
============================================================
Keywords: builder, founder, product, design, ai
Max profiles: 100
============================================================

Discovering profiles from Substack explore pages...
Discovered 45 unique profiles to scan.

Processing profiles...
✓ Found: Jane Doe (@janedoe) - Keywords: ['founder', 'product']
✓ Found: John Smith (@johnsmith) - Keywords: ['builder', 'ai']

============================================================
Results: Found 2 matching profiles
============================================================

✓ Exported to JSON: results/substack_profiles_20251027_120000.json
✓ Exported to CSV: results/substack_profiles_20251027_120000.csv
```

## Tips

1. **Start with test URLs** to verify everything works
2. **Adjust rate limiting** if you get errors (increase delay in config)
3. **Use specific keywords** for better targeting
4. **Check results folder** after each run
5. **Build URL lists** from existing discoveries

Happy discovering! 🚀
