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

### Option 1: Demo Mode (Recommended First Test)

```bash
# Run with mock data to see how the tool works
python demo_substack_finder.py
```

Expected output:
- Processes 6 demo profiles
- Matches keywords in bios
- Shows results in terminal
- Exports to JSON and CSV in `results/` directory

This is the best way to understand the tool's functionality!

### Option 2: Use Your Own URL List

Create a file `my_urls.txt`:
```
https://example1.substack.com
https://example2.substack.com
```

Then run:
```bash
python substack_finder.py --urls-file my_urls.txt
```

**Note:** Due to Substack's bot protection, some URLs may return 403 errors. See [REAL_WORLD_USAGE.md](REAL_WORLD_USAGE.md) for strategies to work around this.

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
