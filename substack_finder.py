#!/usr/bin/env python3
"""
Substack Profile Finder
Discovers Substack profiles with specific keywords in their bios.
"""

import json
import csv
import time
import os
import re
from datetime import datetime
from typing import List, Dict, Set, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class SubstackProfileFinder:
    """Find Substack profiles matching keyword criteria."""

    def __init__(self, config_path: str = "config.json"):
        """Initialize the finder with configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        self.keywords = self.config['keywords']
        self.rate_limit = self.config['rate_limit_delay']
        self.max_profiles = self.config['max_profiles']
        self.case_sensitive = self.config['case_sensitive']
        self.output_dir = self.config['output_dir']

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        # Track discovered profiles to avoid duplicates
        self.discovered_profiles: Set[str] = set()
        self.matched_profiles: List[Dict] = []

        # Session for requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })

    def _rate_limit_sleep(self):
        """Sleep to respect rate limits."""
        time.sleep(self.rate_limit)

    def _contains_keywords(self, text: str) -> List[str]:
        """Check if text contains any keywords and return matched ones."""
        if not text:
            return []

        search_text = text if self.case_sensitive else text.lower()
        matched = []

        for keyword in self.keywords:
            search_keyword = keyword if self.case_sensitive else keyword.lower()
            if search_keyword in search_text:
                matched.append(keyword)

        return matched

    def _extract_profile_data(self, url: str, max_retries: int = 3) -> Optional[Dict]:
        """Extract profile data from a Substack publication URL."""
        last_error = None

        for attempt in range(max_retries):
            try:
                self._rate_limit_sleep()

                # Add random delay for retries
                if attempt > 0:
                    retry_delay = 2 ** attempt  # Exponential backoff
                    time.sleep(retry_delay)

                response = self.session.get(url, timeout=15, allow_redirects=True)
                response.raise_for_status()

                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract various data points
                profile_data = {
                    'url': url,
                    'handle': self._extract_handle(url),
                    'name': None,
                    'bio': None,
                    'subscribers': None,
                    'profile_image': None,
                    'discovered_at': datetime.now().isoformat(),
                    'matched_keywords': []
                }

                # Try to find author name
                name_elem = soup.find('meta', property='og:site_name')
                if name_elem:
                    profile_data['name'] = name_elem.get('content', '').strip()

                # Try to find description/bio
                desc_elem = soup.find('meta', property='og:description')
                if desc_elem:
                    profile_data['bio'] = desc_elem.get('content', '').strip()

                # Also check for meta description
                if not profile_data['bio']:
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    if meta_desc:
                        profile_data['bio'] = meta_desc.get('content', '').strip()

                # Try to find profile image
                image_elem = soup.find('meta', property='og:image')
                if image_elem:
                    profile_data['profile_image'] = image_elem.get('content', '')

                # Look for subscriber count (if visible)
                # This varies by Substack's HTML structure
                subscriber_text = soup.find(string=re.compile(r'subscribers?', re.I))
                if subscriber_text:
                    numbers = re.findall(r'\d+[,\d]*', subscriber_text)
                    if numbers:
                        profile_data['subscribers'] = numbers[0].replace(',', '')

                return profile_data  # Success

            except Exception as e:
                last_error = e
                if attempt == max_retries - 1:
                    # Last attempt failed
                    print(f"Error extracting profile from {url} after {max_retries} attempts: {e}")
                # Continue to next retry

        return None  # All retries failed

    def _extract_handle(self, url: str) -> str:
        """Extract handle from Substack URL."""
        parsed = urlparse(url)
        hostname = parsed.hostname or ''

        # Handle both custom domains and substack.com subdomains
        if '.substack.com' in hostname:
            return hostname.replace('.substack.com', '')
        return hostname

    def discover_from_explore_page(self, limit: int = 50) -> List[str]:
        """Discover profiles from Substack's explore/discover pages."""
        print("Discovering profiles from Substack explore pages...")
        discovered_urls = []

        # Try different category pages
        categories = [
            'technology',
            'business',
            'design',
            'startup',
            'culture',
            'top'
        ]

        for category in categories:
            try:
                url = f"https://substack.com/discover/category/{category}"
                self._rate_limit_sleep()

                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Find links to Substack publications
                    links = soup.find_all('a', href=True)
                    for link in links:
                        href = link['href']
                        if '.substack.com' in href and href not in discovered_urls:
                            # Normalize URL
                            if not href.startswith('http'):
                                href = 'https://' + href.lstrip('/')
                            discovered_urls.append(href)

                            if len(discovered_urls) >= limit:
                                return discovered_urls

            except Exception as e:
                print(f"Error fetching category {category}: {e}")
                continue

        return discovered_urls

    def discover_from_leaderboard(self) -> List[str]:
        """Discover profiles from Substack's leaderboard."""
        print("Discovering profiles from Substack leaderboard...")
        discovered_urls = []

        try:
            url = "https://substack.com/discover/leaderboard"
            self._rate_limit_sleep()

            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find publication links
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if '.substack.com' in href:
                        if not href.startswith('http'):
                            href = 'https://' + href.lstrip('/')
                        if href not in discovered_urls:
                            discovered_urls.append(href)

        except Exception as e:
            print(f"Error fetching leaderboard: {e}")

        return discovered_urls

    def discover_from_url_list(self, url_list: List[str]) -> List[str]:
        """Accept a manual list of Substack URLs to check."""
        print(f"Processing {len(url_list)} provided URLs...")
        return url_list

    def find_matching_profiles(self, urls: List[str]) -> List[Dict]:
        """Process URLs and find profiles matching keywords."""
        print(f"\nProcessing {len(urls)} profiles...")

        for url in tqdm(urls, desc="Scanning profiles"):
            # Skip if already processed
            if url in self.discovered_profiles:
                continue

            self.discovered_profiles.add(url)

            # Extract profile data
            profile = self._extract_profile_data(url)

            if profile and profile['bio']:
                # Check for keyword matches
                matched_keywords = self._contains_keywords(profile['bio'])

                # Also check name for keywords
                if profile['name']:
                    matched_keywords.extend(self._contains_keywords(profile['name']))

                # Remove duplicates
                matched_keywords = list(set(matched_keywords))

                if matched_keywords:
                    profile['matched_keywords'] = matched_keywords
                    self.matched_profiles.append(profile)
                    print(f"\n✓ Found: {profile['name']} (@{profile['handle']}) - Keywords: {matched_keywords}")

            # Stop if we've reached max
            if len(self.matched_profiles) >= self.max_profiles:
                print(f"\nReached maximum of {self.max_profiles} profiles.")
                break

        return self.matched_profiles

    def export_results(self):
        """Export results to JSON and CSV."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Export to JSON
        if 'json' in self.config['export_formats']:
            json_path = os.path.join(self.output_dir, f'substack_profiles_{timestamp}.json')
            with open(json_path, 'w') as f:
                json.dump(self.matched_profiles, f, indent=2)
            print(f"\n✓ Exported to JSON: {json_path}")

        # Export to CSV
        if 'csv' in self.config['export_formats']:
            csv_path = os.path.join(self.output_dir, f'substack_profiles_{timestamp}.csv')
            if self.matched_profiles:
                keys = ['handle', 'name', 'bio', 'url', 'matched_keywords', 'subscribers', 'discovered_at']
                with open(csv_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    writer.writeheader()
                    for profile in self.matched_profiles:
                        # Convert list to string for CSV
                        row = profile.copy()
                        row['matched_keywords'] = ', '.join(profile['matched_keywords'])
                        writer.writerow({k: row.get(k, '') for k in keys})
                print(f"✓ Exported to CSV: {csv_path}")

    def run(self, custom_urls: Optional[List[str]] = None):
        """Run the complete profile discovery and matching workflow."""
        print("=" * 60)
        print("Substack Profile Finder")
        print("=" * 60)
        print(f"Keywords: {', '.join(self.keywords)}")
        print(f"Max profiles: {self.max_profiles}")
        print("=" * 60)

        all_urls = []

        # Use custom URLs if provided
        if custom_urls:
            all_urls.extend(custom_urls)
        else:
            # Discover from various sources
            if self.config['discovery_sources'].get('explore_page', True):
                all_urls.extend(self.discover_from_explore_page())

            if self.config['discovery_sources'].get('leaderboard', True):
                all_urls.extend(self.discover_from_leaderboard())

        # Remove duplicates
        all_urls = list(set(all_urls))

        print(f"\nDiscovered {len(all_urls)} unique profiles to scan.")

        # Find matching profiles
        if all_urls:
            self.find_matching_profiles(all_urls)

            print("\n" + "=" * 60)
            print(f"Results: Found {len(self.matched_profiles)} matching profiles")
            print("=" * 60)

            # Export results
            if self.matched_profiles:
                self.export_results()
            else:
                print("\nNo matching profiles found.")
        else:
            print("\nNo URLs discovered to scan.")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Find Substack profiles by keywords in bio')
    parser.add_argument('--config', default='config.json', help='Path to config file')
    parser.add_argument('--urls', nargs='+', help='Specific URLs to check')
    parser.add_argument('--urls-file', help='File containing URLs (one per line)')

    args = parser.parse_args()

    # Initialize finder
    finder = SubstackProfileFinder(config_path=args.config)

    # Prepare URLs
    custom_urls = []
    if args.urls:
        custom_urls.extend(args.urls)

    if args.urls_file:
        with open(args.urls_file, 'r') as f:
            custom_urls.extend([line.strip() for line in f if line.strip()])

    # Run the finder
    finder.run(custom_urls=custom_urls if custom_urls else None)


if __name__ == '__main__':
    main()
