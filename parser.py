"""
Parses country codes from the HTML file into a clean text format,
then lets you look up any country by name.

Usage:
    python parse_country_codes.py                  # interactive lookup
    python parse_country_codes.py --dump           # print all countries
    python parse_country_codes.py --country Iraq   # lookup from command line
"""

import re
import sys
import os

HTML_FILE = "codes"


def parse_countries(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    # Match each row: country name, dial code, ISO codes (e.g. "IQ / IRQ")
    pattern = re.compile(
        r'<a href="[^"]*">([^<]+)</a>'          # country name
        r'.*?<span class="row_space">([^<]+)</span>'  # dial code
        r'.*?<td class="iso-col"[^>]*>([^<]+)</td>',  # ISO codes
        re.DOTALL
    )

    countries = {}
    for match in pattern.finditer(html):
        name = match.group(1).strip()
        dial = match.group(2).strip()
        iso_raw = match.group(3).strip()           # e.g. "IQ / IRQ"
        iso2, iso3 = [x.strip() for x in iso_raw.split("/")]
        countries[name.lower()] = {
            "name": name,
            "dial": dial,
            "iso2": iso2,
            "iso3": iso3,
        }

    return countries


def format_country(entry):
    return (
        f"{entry['name']}: codes: {entry['dial']} "
        f"{entry['iso2']} {entry['iso3']}"
    )


def lookup(countries, query):
    key = query.strip().lower()
    if key in countries:
        return format_country(countries[key])
    # Partial match fallback
    matches = [v for k, v in countries.items() if key in k]
    if matches:
        return "\n".join(format_country(m) for m in matches)
    return f'No country found for "{query}".'


def dump_all(countries):
    for entry in countries.values():
        print(format_country(entry))


def export_json(countries, output_path="country_codes.json"):
    import json
    # Use country name as the key for easy lookups
    data = {entry["name"]: {"dial": entry["dial"],
                            "iso2": entry["iso2"],
                            "iso3": entry["iso3"]} for entry in countries.values()}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Exported {len(data)} countries to '{output_path}'.")


if __name__ == "__main__":
    # Resolve the HTML file relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, HTML_FILE)

    if not os.path.exists(filepath):
        print(f"Error: could not find '{filepath}'")
        print("Make sure the 'codes' HTML file is in the same folder as this script.")
        sys.exit(1)

    countries = parse_countries(filepath)

    if "--json" in sys.argv:
        out = "country_codes.json"
        idx = sys.argv.index("--json")
        if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("--"):
            out = sys.argv[idx + 1]
        export_json(countries, os.path.join(script_dir, out))
    elif "--dump" in sys.argv:
        dump_all(countries)
    elif "--country" in sys.argv:
        idx = sys.argv.index("--country")
        if idx + 1 < len(sys.argv):
            query = " ".join(sys.argv[idx + 1:])
            print(lookup(countries, query))
        else:
            print("Please provide a country name after --country.")
    else:
        print(f"Loaded {len(countries)} countries. Type a name to look it up (or 'quit' to exit).\n")
        while True:
            query = input("Country: ").strip()
            if query.lower() in ("quit", "exit", "q"):
                break
            if query:
                print(lookup(countries, query))
