#!/usr/bin/env python3

try:
    from .klippy import main
except ImportError:
    try:
        from klippy.klippy import main
    except ImportError:
        # Last resort fallback
        from klippy import main

if __name__ == "__main__":
    main()
