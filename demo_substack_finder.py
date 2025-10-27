#!/usr/bin/env python3
"""
Demo mode for Substack Profile Finder
Simulates finding profiles with keywords to demonstrate functionality
"""

import json
import csv
import os
from datetime import datetime

# Mock data representing real Substack profiles
DEMO_PROFILES = [
    {
        "url": "https://lenny.substack.com",
        "handle": "lenny",
        "name": "Lenny's Newsletter",
        "bio": "A weekly advice column about product management, growth, working with humans, and anything else that's stressing you out about work. By Lenny Rachitsky, ex-Airbnb product lead.",
        "subscribers": "500000",
        "profile_image": "https://example.com/lenny.jpg",
        "discovered_at": datetime.now().isoformat()
    },
    {
        "url": "https://digitalnative.substack.com",
        "handle": "digitalnative",
        "name": "Not Boring",
        "bio": "Weekly essays on strategy, technology, and business. Written by Packy McCormick, founder and investor.",
        "subscribers": "150000",
        "profile_image": "https://example.com/packy.jpg",
        "discovered_at": datetime.now().isoformat()
    },
    {
        "url": "https://every.to",
        "handle": "every",
        "name": "Every",
        "bio": "A bundle of business-focused newsletters by founders, builders, and operators building tools powered by AI to help you do better work.",
        "subscribers": "75000",
        "profile_image": "https://example.com/every.jpg",
        "discovered_at": datetime.now().isoformat()
    },
    {
        "url": "https://future.com",
        "handle": "future",
        "name": "Future",
        "bio": "Essays about design, technology, and human-centered innovation. By a product designer at Google.",
        "subscribers": "25000",
        "profile_image": "https://example.com/future.jpg",
        "discovered_at": datetime.now().isoformat()
    },
    {
        "url": "https://aiexplained.substack.com",
        "handle": "aiexplained",
        "name": "AI Explained",
        "bio": "Breaking down the latest developments in artificial intelligence and machine learning for founders and builders in the AI space.",
        "subscribers": "50000",
        "profile_image": "https://example.com/ai.jpg",
        "discovered_at": datetime.now().isoformat()
    },
    {
        "url": "https://startup.substack.com",
        "handle": "startup",
        "name": "Startup Stories",
        "bio": "Weekly interviews and lessons from successful entrepreneurs, covering everything from first hire to IPO.",
        "subscribers": "30000",
        "profile_image": "https://example.com/startup.jpg",
        "discovered_at": datetime.now().isoformat()
    }
]

KEYWORDS = ["builder", "founder", "product", "design", "ai"]


def find_matches():
    """Find profiles matching keywords."""
    matches = []

    for profile in DEMO_PROFILES:
        matched_keywords = []
        bio_lower = profile['bio'].lower()

        for keyword in KEYWORDS:
            if keyword.lower() in bio_lower:
                matched_keywords.append(keyword)

        if matched_keywords:
            profile_copy = profile.copy()
            profile_copy['matched_keywords'] = matched_keywords
            matches.append(profile_copy)

    return matches


def export_demo_results():
    """Export demo results."""
    os.makedirs('results', exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    matches = find_matches()

    # Export to JSON
    json_path = f'results/demo_substack_profiles_{timestamp}.json'
    with open(json_path, 'w') as f:
        json.dump(matches, f, indent=2)
    print(f"\n✓ Demo results exported to JSON: {json_path}")

    # Export to CSV
    csv_path = f'results/demo_substack_profiles_{timestamp}.csv'
    if matches:
        keys = ['handle', 'name', 'bio', 'url', 'matched_keywords', 'subscribers', 'discovered_at']
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for profile in matches:
                row = profile.copy()
                row['matched_keywords'] = ', '.join(profile['matched_keywords'])
                writer.writerow({k: row.get(k, '') for k in keys})
        print(f"✓ Demo results exported to CSV: {csv_path}")

    return matches


def main():
    """Run demo."""
    print("=" * 60)
    print("Substack Profile Finder - DEMO MODE")
    print("=" * 60)
    print(f"Keywords: {', '.join(KEYWORDS)}")
    print(f"Demo profiles to scan: {len(DEMO_PROFILES)}")
    print("=" * 60)
    print("\nScanning demo profiles...\n")

    matches = export_demo_results()

    print("\n" + "=" * 60)
    print("Results:")
    print("=" * 60)

    for match in matches:
        print(f"\n✓ {match['name']} (@{match['handle']})")
        print(f"  Bio: {match['bio'][:80]}...")
        print(f"  Matched keywords: {', '.join(match['matched_keywords'])}")
        print(f"  URL: {match['url']}")

    print("\n" + "=" * 60)
    print(f"Total matches: {len(matches)} out of {len(DEMO_PROFILES)} profiles")
    print("=" * 60)


if __name__ == '__main__':
    main()
