# My-Projects
## My Projects: Building in Public

### StackShelf
- [StackShelf.app (Repo)](https://github.com/karozi/StackShelf.app/blob/main/README.md)
- [StackShelf.app (Website)](www.stackshelf.app)

### Substack Profile Finder
Python tool to filter Substack profiles by keywords (builder, founder, product, design, AI) in their bios.

**Key Features:**
- Batch process and filter URL lists by keywords
- Extract profile metadata (bio, name, subscribers)
- Export matches to JSON and CSV
- Demo mode to test functionality
- Rate limiting and ethical scraping

**Quick Start:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run demo to see how it works
python demo_substack_finder.py

# Filter your own URL list
python substack_finder.py --urls-file my_substacks.txt
```

**Documentation:**
- [Real-World Usage Guide](REAL_WORLD_USAGE.md) ⭐ Start here!
- [Full Documentation](README_SUBSTACK_FINDER.md)
- [Quick Start Guide](QUICKSTART.md)

**Note:** Due to Substack's bot protection, this tool works best for filtering manually collected URL lists rather than automated discovery.
