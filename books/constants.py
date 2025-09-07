"""
Constants for ISBN validation patterns.
"""

# ISBN validation patterns
ISBN_10_PATTERN = r'[\dX]{10}'
ISBN_13_PATTERN = r'\d{13}'
ISBN_COMBINED_PATTERN = rf'{ISBN_10_PATTERN}|{ISBN_13_PATTERN}'
