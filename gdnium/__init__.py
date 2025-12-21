"""
Gdnium - Undetectable Browser Automation Library

A self-contained stealth browser automation library with:
- CDP Direct communication (no WebDriver)
- Closed Shadow Root access
- Human-like behavior simulation
- Bot detection evasion
"""

from gdnium.core.browser import Browser
from gdnium.core.tab import Tab
from gdnium.core.element import Element

__version__ = "0.1.0"
__all__ = ["Browser", "Tab", "Element"]
