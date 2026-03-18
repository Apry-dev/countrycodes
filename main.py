"""
main.py
Entry point. Reads country_codes.json, generates new 3-letter codes,
resolves collisions, and writes new_country_codes.json.
"""

import json
from codegenerator import make_code
from collision import resolve_collisions
from collections import defaultdict

INPUT_FILE = "list.json"
OUTPUT_FILE = "new_country_codes.json"



def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        countries = json.load(f)


    raw_codes = {name: make_code(name) for name in countries}

    clashes = defaultdict(list)
    for name, code in raw_codes.items():
        clashes[code].append(name)

    for code, names in clashes.items():
        if len(names) > 1:
            print(f"{code}: {names}")

    final_codes = resolve_collisions(raw_codes)
    for name, code in final_codes.items():
        print(f"{name}: {code}  (was {countries[name]['iso3']})")
    # Merge new code into existing country data
    output = {
        name: {**data, "new_code": final_codes[name]}
        for name, data in countries.items()
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Generated codes for {len(output)} countries --> '{OUTPUT_FILE}'\n")


if __name__ == "__main__":
    main()
