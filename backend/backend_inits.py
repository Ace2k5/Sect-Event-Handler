"""
Initialization constants and configuration for Sect-Event-Handler.

This module defines global constants used throughout the application,
including website configurations for scraping and file paths.
"""

from pathlib import Path

# List of (table_css_class, url) tuples for each game's wiki
SITES = [
    # Arknights: CSS class for event tables and wiki URL
    ("mrfz-wtable flex-table", "https://arknights.wiki.gg/wiki/Event"),
    # Limbus Company: CSS class for event tables and wiki URL
    ("lcbtable2", "https://limbuscompany.wiki.gg/wiki/Events"),
    ("wikitable evt-list-tbl sortable jquery-tablesorter", "https://azurlane.koumakan.jp/wiki/Evens")
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# Path to user configuration file (relative to backend directory)
LOCAL_USER = Path("local_user.json")
LOCAL_COOKIES = Path("local_cookies.json")