# Substack Profile Finder - Real-World Usage Guide

## Important Note: Substack Bot Protection

Substack has implemented strong bot protection measures that block automated scraping requests (403 Forbidden errors). This is a security feature to protect their platform and users.

## How to Use This Tool Effectively

Since automated discovery is blocked, here are practical approaches:

### 1. Manual URL Collection + Automated Filtering (Recommended)

**Step 1: Manually collect Substack URLs**
- Browse Substack's website logged in
- Check your subscriptions and recommendations
- Follow links from social media (Twitter, LinkedIn)
- Ask for recommendations in communities
- Check "Top" and "Featured" lists on Substack

**Step 2: Save URLs to a file**

Create `my_substacks.txt`:
```
https://lenny.substack.com
https://every.to
https://digitalnative.substack.com
https://stratechery.com
... (add more)
```

**Step 3: Use the tool to filter by keywords**

This is where the tool adds value - filtering dozens or hundreds of manually collected URLs by keywords:

```bash
python3 substack_finder.py --urls-file my_substacks.txt
```

The tool will:
- Extract bios from each URL
- Match against your keywords
- Export only matching profiles
- Save time vs manually reading each bio

### 2. Use Demo Mode to Test

```bash
python3 demo_substack_finder.py
```

This demonstrates how the tool processes profiles and matches keywords using mock data.

### 3. Modify the Tool for API Access (Advanced)

If you have legitimate API access to Substack (e.g., through a partnership), you can modify the tool to use official APIs.

## Practical Workflows

### Workflow A: Building a Reading List

1. Export your email subscriptions to find Substack URLs
2. Add URLs shared in Slack/Discord communities
3. Create `urls.txt` with 50-100 URLs
4. Run: `python3 substack_finder.py --urls-file urls.txt`
5. Get filtered list of founders, builders, designers, etc.

### Workflow B: Research for a Specific Niche

1. Search Twitter for "substack.com + [your topic]"
2. Collect URLs from search results
3. Customize keywords in `config.json` for your niche
4. Run the tool to filter
5. Export to CSV for analysis

### Workflow C: Newsletter Recommendations

1. Browse Substack's web interface for categories
2. Copy URLs of interesting publications
3. Use tool to batch-check which ones match your interests
4. Save hours of manual bio reading

## Configuration for Best Results

Edit `config.json`:

```json
{
  "keywords": ["your", "specific", "keywords"],
  "rate_limit_delay": 3.0,
  "max_profiles": 200,
  "case_sensitive": false
}
```

**Increase `rate_limit_delay` to 3-5 seconds** if you're processing many URLs to avoid triggering additional protections.

## Alternative Approaches

### Use Substack's Official Features

- **Discover page**: Browse categories (Technology, Business, Culture)
- **Recommendations**: Check publications' recommendation sections
- **Leaderboard**: View top publications
- **Search**: Use Substack's built-in search

### Use Third-Party Directories

Some websites maintain curated lists of Substack newsletters:
- Newsletter directories
- Curated reading lists
- Community-maintained databases

Then use this tool to filter those lists by keywords.

## Value Proposition

Even with bot protection, this tool is valuable for:

1. **Batch Processing**: Filter 100+ manually collected URLs quickly
2. **Keyword Matching**: Auto-detect profiles matching your interests
3. **Data Export**: Get structured CSV/JSON for analysis
4. **Time Savings**: Avoid reading hundreds of bios manually
5. **Consistency**: Use same criteria across all profiles

## Example Use Case

Sarah wants to find product design newsletters:

1. **Manual Collection** (30 minutes):
   - Browse Substack's Design category
   - Check LinkedIn posts about Substack
   - Ask in Slack communities
   - Collect 75 URLs

2. **Automated Filtering** (2 minutes):
   ```bash
   # Save URLs to file
   python3 substack_finder.py --urls-file design_substacks.txt
   ```

3. **Result**:
   - Tool processes all 75 URLs
   - Finds 23 matching "product", "design", "builder"
   - Exports to CSV for review
   - **Saves ~1 hour** of manual bio reading

## Troubleshooting

### Still Getting 403 Errors?

This is expected. Solutions:

1. **Reduce rate**: Increase `rate_limit_delay` to 5-10 seconds
2. **Smaller batches**: Process 10-20 URLs at a time
3. **Manual mode**: Use the tool's filtering logic on data you already have
4. **Demo mode**: Test functionality without network requests

### No Matches Found?

1. Check your keywords are in English (or match bio language)
2. Try broader keywords
3. Verify URLs are valid Substack publications
4. Some profiles have minimal bios

## Future Improvements

If Substack releases an official API:
- Automated discovery would work
- Real-time filtering
- Subscription management
- More detailed metadata

Until then, this tool is best used for **filtering manually curated URL lists**.

## Legal & Ethical Notes

- This tool respects rate limits
- Use for personal research only
- Don't harass discovered authors
- Follow Substack's Terms of Service
- Consider supporting authors you discover

---

**Bottom Line**: Think of this as a "bulk bio checker" rather than a "profile crawler". Collect URLs manually, let the tool do the filtering.
