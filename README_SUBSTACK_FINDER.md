# Substack Profile Finder

A Python tool to discover Substack profiles with specific keywords (builder, founder, product, design, AI) in their bios.

## Features

- **Multiple Discovery Methods**
  - Explore Substack's category pages (technology, business, design, startup, etc.)
  - Scan Substack's leaderboard
  - Process custom URL lists

- **Smart Keyword Matching**
  - Case-insensitive search by default
  - Searches both profile bios and names
  - Tracks which keywords matched each profile

- **Data Extraction**
  - Profile handle and name
  - Bio/description text
  - Profile URL
  - Profile image URL
  - Subscriber count (when visible)
  - Discovery timestamp

- **Export Options**
  - JSON format (structured data)
  - CSV format (spreadsheet-friendly)
  - Results saved with timestamps

- **Ethical Scraping**
  - Rate limiting (2 second delay by default)
  - Respects website structure
  - Error handling for failed requests

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Verify installation:**
```bash
python substack_finder.py --help
```

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "keywords": ["builder", "founder", "product", "design", "ai"],
  "rate_limit_delay": 2.0,
  "max_profiles": 100,
  "output_dir": "results",
  "discovery_sources": {
    "explore_page": true,
    "recommendations": true,
    "leaderboard": true
  },
  "case_sensitive": false,
  "export_formats": ["json", "csv"]
}
```

### Configuration Options

- `keywords`: List of keywords to search for in bios
- `rate_limit_delay`: Seconds to wait between requests (default: 2.0)
- `max_profiles`: Maximum matching profiles to find (default: 100)
- `output_dir`: Directory to save results (default: "results")
- `case_sensitive`: Whether keyword matching is case-sensitive (default: false)
- `export_formats`: Output formats - "json", "csv", or both

## Usage

### Method 1: Auto-Discovery (Recommended for exploring)

Automatically discover profiles from Substack's explore and leaderboard pages:

```bash
python substack_finder.py
```

This will:
1. Scan Substack's category pages (tech, business, design, etc.)
2. Check the leaderboard for top publications
3. Extract bios and match against keywords
4. Export results to `results/` directory

### Method 2: Custom URL List

Check specific Substack publications:

```bash
# Single URLs
python substack_finder.py --urls https://example.substack.com https://another.substack.com

# From a file (one URL per line)
python substack_finder.py --urls-file urls.txt
```

### Method 3: Custom Configuration

Use a different config file:

```bash
python substack_finder.py --config my_config.json
```

## Example URLs File

Create a file `urls.txt` with Substack URLs (one per line):

```
https://paulg.substack.com
https://lenny.substack.com
https://digitalnative.substack.com
https://caseyjaccoma.substack.com
https://every.to
```

Then run:
```bash
python substack_finder.py --urls-file urls.txt
```

## Output Format

### JSON Output
```json
[
  {
    "url": "https://example.substack.com",
    "handle": "example",
    "name": "Jane Doe",
    "bio": "Product designer and founder building tools for creators",
    "subscribers": "5000",
    "profile_image": "https://...",
    "discovered_at": "2025-10-27T12:00:00",
    "matched_keywords": ["product", "designer", "founder"]
  }
]
```

### CSV Output
Spreadsheet with columns:
- handle
- name
- bio
- url
- matched_keywords
- subscribers
- discovered_at

## How It Works

1. **Discovery Phase**
   - Fetches Substack category and leaderboard pages
   - Extracts publication URLs from these pages
   - Deduplicates URLs

2. **Extraction Phase**
   - Visits each publication URL
   - Extracts metadata (name, bio, image, etc.) from HTML meta tags
   - Applies rate limiting between requests

3. **Matching Phase**
   - Searches bio and name text for keywords
   - Records which keywords matched
   - Collects matching profiles

4. **Export Phase**
   - Saves results to JSON and/or CSV
   - Timestamps output files
   - Creates results directory if needed

## Tips for Best Results

1. **Start Small**: Test with a few URLs first to verify it works
2. **Adjust Rate Limiting**: Increase `rate_limit_delay` if you get rate limited
3. **Customize Keywords**: Add specific terms relevant to your search
4. **Use URL Lists**: For targeted searches, curate your own list of URLs
5. **Monitor Progress**: The script shows progress bars and real-time matches

## Common Use Cases

### Finding Tech Founders
```json
{
  "keywords": ["founder", "ceo", "co-founder", "entrepreneur", "startup"]
}
```

### Finding Product Designers
```json
{
  "keywords": ["product", "design", "designer", "ux", "ui"]
}
```

### Finding AI Builders
```json
{
  "keywords": ["ai", "machine learning", "ml", "gpt", "builder"]
}
```

## Limitations

- Substack doesn't have an official API, so this uses web scraping
- Rate limiting is important to avoid being blocked
- Some profiles may have minimal bios or custom domains
- Subscriber counts are only visible when made public by authors
- Discovery is limited to pages accessible without authentication

## Ethical Considerations

This tool is designed for:
- Research and discovery
- Finding writers in specific niches
- Building curated reading lists
- Academic or journalistic research

Please use responsibly:
- Respect rate limits
- Don't spam or harass discovered profiles
- Follow Substack's Terms of Service
- Only use public information

## Troubleshooting

### "No URLs discovered to scan"
- Check your internet connection
- Substack's page structure may have changed
- Try providing custom URLs with `--urls` or `--urls-file`

### "Error extracting profile"
- Some URLs may be invalid or private
- The script will continue with other URLs
- Check rate limiting if many errors occur

### Results are empty
- Keywords might be too specific - try broader terms
- Adjust `max_profiles` to scan more
- Try different discovery sources in config

## Example Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit config.json with your keywords
nano config.json

# 3. Run the finder
python substack_finder.py

# 4. Check results
ls results/
cat results/substack_profiles_*.csv
```

## Contributing

Suggestions for improvement:
- Add more discovery sources
- Improve bio extraction accuracy
- Add filtering by subscriber count
- Support for custom domains
- Parallel processing for faster scanning

## License

This tool is for educational and research purposes. Use responsibly and in accordance with Substack's Terms of Service.

---

**Note**: This tool uses web scraping and is not officially affiliated with or endorsed by Substack. The unofficial nature means it may break if Substack changes their website structure.
