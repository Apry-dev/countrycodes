"""
collision.py
Resolves duplicate generated codes across a set of countries.
"""


def resolve_collisions(raw_codes):
    """
    Given a dict of {country_name: code}, ensures all codes are unique.
    The first country to claim a code keeps it clean.
    Duplicates get their last character replaced with 2, 3, 4 ...

    Returns a new dict of {country_name: resolved_code}.
    """
    seen = {}
    final = {}

    for country, code in raw_codes.items():
        if code not in seen:
            seen[code] = country
            final[country] = code
        else:

            for suffix in range(2, 10):
                candidate = code[:2] + str(suffix)
                if candidate not in seen:
                    seen[candidate] = country
                    final[country] = candidate
                    break
            else:
                # Extremely unlikely fallback — just keep the duplicate
                final[country] = code

    return final
