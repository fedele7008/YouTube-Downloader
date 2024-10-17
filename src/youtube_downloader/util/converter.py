"""
Author: John Yoon
Email: fedelejohn7008@gmail.com
Version: 2.1.0

Copyright (c) 2024 John Yoon. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for more information.
"""

def byte_to_display(byte_size: int) -> str:
    """
    Convert a byte size to a human-readable string representation.

    This function takes a byte size as input and returns a string representation
    of the size in B, KB, MB, or GB, depending on the magnitude of the input.

    Args:
        byte_size (int): The size in bytes to be converted.

    Returns:
        str: A human-readable string representation of the byte size.
             The returned string includes the value (rounded to two decimal places
             for KB, MB, and GB) and the appropriate unit (B, KB, MB, or GB).

    Raises:
        ValueError: If the input byte_size is negative.

    Examples:
    ```
        >>> byte_to_display(500)
        '500 B'
        >>> byte_to_display(1500)
        '1.46 KB'
        >>> byte_to_display(1500000)
        '1.43 MB'
        >>> byte_to_display(1500000000)
        '1.40 GB'
    ```
    """
    if byte_size < 0:
        raise ValueError("Byte size cannot be negative")
    
    if byte_size < 1024:
        return f"{byte_size} B"
    elif byte_size < 1024**2:
        return f"{byte_size / 1024:.2f} KB"
    elif byte_size < 1024**3:
        return f"{byte_size / 1024**2:.2f} MB"
    else:
        return f"{byte_size / 1024**3:.2f} GB"

