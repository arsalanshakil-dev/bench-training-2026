"""
countries.py — REST Countries API Wrapper
Usage:
    python countries.py get <country_name>
    python countries.py region <region_name>
    python countries.py compare <country1> <country2>
"""

import sys
import json
import urllib.request
import urllib.parse
import urllib.error

BASE_URL = "https://restcountries.com/v3.1"

# ─────────────────────────────────────────────
#  Internal helpers
# ─────────────────────────────────────────────

def _fetch(url: str) -> list[dict]:
    """Fetch JSON from a URL and return a list of country dicts."""
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(f"Not found: {url}") from e
        raise RuntimeError(f"HTTP {e.code}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e.reason}") from e


def _parse_country(data: dict) -> dict:
    """Extract a clean, flat dict from a raw REST Countries v3.1 entry."""
    name        = data.get("name", {})
    currencies  = data.get("currencies", {})
    languages   = data.get("languages", {})
    population  = data.get("population", 0)
    area        = data.get("area")
    capital     = data.get("capital", [])
    region      = data.get("region", "")
    subregion   = data.get("subregion", "")
    flag        = data.get("flag", "")
    tlds        = data.get("tld", [])
    timezones   = data.get("timezones", [])
    borders     = data.get("borders", [])

    currency_list = [
        f"{code} ({info.get('name', '')})"
        for code, info in currencies.items()
    ]
    language_list = list(languages.values())

    return {
        "name":        name.get("common", "Unknown"),
        "official":    name.get("official", ""),
        "capital":     ", ".join(capital) if capital else "N/A",
        "region":      region,
        "subregion":   subregion,
        "population":  population,
        "area_km2":    area,
        "languages":   language_list,
        "currencies":  currency_list,
        "tld":         tlds,
        "timezones":   timezones,
        "borders":     borders,
        "flag":        flag,
    }


# ─────────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────────

def get_country(name: str) -> dict:
    """
    Fetch a single country by name (common or official).

    Returns a clean dict with population, area, languages, currencies, etc.
    Raises ValueError if the country is not found.
    """
    encoded = urllib.parse.quote(name)
    url = f"{BASE_URL}/name/{encoded}?fullText=false"
    results = _fetch(url)
    lower = name.lower()
    for entry in results:
        common = entry.get("name", {}).get("common", "").lower()
        if common == lower:
            return _parse_country(entry)
    return _parse_country(results[0])


def get_region(region_name: str) -> list[dict]:
    """
    Fetch all countries in a geographic region.

    Recognised regions: Africa, Americas, Asia, Europe, Oceania.
    Returns a list of clean country dicts, sorted by population descending.
    """
    encoded = urllib.parse.quote(region_name)
    url = f"{BASE_URL}/region/{encoded}"
    results = _fetch(url)
    countries = [_parse_country(c) for c in results]
    countries.sort(key=lambda c: c["population"], reverse=True)
    return countries


def compare_countries(c1_name: str, c2_name: str) -> dict:
    """
    Compare two countries side-by-side.

    Returns a dict with keys 'country1', 'country2', and 'comparison'
    (a list of rows, each being a {'metric', 'c1', 'c2'} dict).
    """
    c1 = get_country(c1_name)
    c2 = get_country(c2_name)

    def fmt_pop(n: int) -> str:
        return f"{n:,}" if n is not None else "N/A"

    def fmt_area(n) -> str:
        return f"{n:,.0f} km²" if n is not None else "N/A"

    rows = [
        {
            "metric": "Official Name",
            "c1":     c1["official"],
            "c2":     c2["official"],
        },
        {
            "metric": "Capital",
            "c1":     c1["capital"],
            "c2":     c2["capital"],
        },
        {
            "metric": "Region / Subregion",
            "c1":     f"{c1['region']} / {c1['subregion']}",
            "c2":     f"{c2['region']} / {c2['subregion']}",
        },
        {
            "metric": "Population",
            "c1":     fmt_pop(c1["population"]),
            "c2":     fmt_pop(c2["population"]),
        },
        {
            "metric": "Area",
            "c1":     fmt_area(c1["area_km2"]),
            "c2":     fmt_area(c2["area_km2"]),
        },
        {
            "metric": "Languages",
            "c1":     ", ".join(c1["languages"]) or "N/A",
            "c2":     ", ".join(c2["languages"]) or "N/A",
        },
        {
            "metric": "Currencies",
            "c1":     ", ".join(c1["currencies"]) or "N/A",
            "c2":     ", ".join(c2["currencies"]) or "N/A",
        },
        {
            "metric": "Timezones",
            "c1":     ", ".join(c1["timezones"]),
            "c2":     ", ".join(c2["timezones"]),
        },
        {
            "metric": "Border Countries",
            "c1":     ", ".join(c1["borders"]) or "None",
            "c2":     ", ".join(c2["borders"]) or "None",
        },
    ]

    return {"country1": c1, "country2": c2, "comparison": rows}


# ─────────────────────────────────────────────
#  Pretty-print helpers
# ─────────────────────────────────────────────

def _print_country(c: dict) -> None:
    """Print a single country's details in a readable format."""
    print(f"\n{'─' * 50}")
    print(f"  {c['flag']}  {c['name']}")
    print(f"{'─' * 50}")
    fields = [
        ("Official Name",    c["official"]),
        ("Capital",          c["capital"]),
        ("Region",           f"{c['region']} › {c['subregion']}"),
        ("Population",       f"{c['population']:,}"),
        ("Area",             f"{c['area_km2']:,.0f} km²" if c["area_km2"] else "N/A"),
        ("Languages",        ", ".join(c["languages"]) or "N/A"),
        ("Currencies",       ", ".join(c["currencies"]) or "N/A"),
        ("Top-Level Domain", ", ".join(c["tld"]) or "N/A"),
        ("Timezones",        ", ".join(c["timezones"])),
        ("Borders",          ", ".join(c["borders"]) or "None"),
    ]
    for label, value in fields:
        print(f"  {label:<20} {value}")
    print()


def _print_region(countries: list[dict], region_name: str) -> None:
    """Print a summary table for all countries in a region."""
    print(f"\n  Region: {region_name}  ({len(countries)} countries)\n")
    header = f"  {'Country':<28} {'Population':>14} {'Area (km²)':>14}  Languages"
    print(header)
    print(f"  {'─' * (len(header) + 10)}")
    for c in countries:
        area = f"{c['area_km2']:>13,.0f}" if c["area_km2"] else "           N/A"
        langs = ", ".join(c["languages"][:2])
        if len(c["languages"]) > 2:
            langs += "…"
        print(f"  {c['name']:<28} {c['population']:>14,} {area}  {langs}")
    print()


def _print_comparison(result: dict) -> None:
    """Print a side-by-side comparison table."""
    c1  = result["country1"]
    c2  = result["country2"]
    rows = result["comparison"]

    n1 = f"{c1['flag']} {c1['name']}"
    n2 = f"{c2['flag']} {c2['name']}"

    col_metric = max(len(r["metric"]) for r in rows) + 2
    col_c1     = max(max(len(r["c1"]) for r in rows), len(n1)) + 2
    col_c2     = max(max(len(r["c2"]) for r in rows), len(n2)) + 2

    sep   = f"  ┼{'─' * col_metric}┼{'─' * col_c1}┼{'─' * col_c2}┼"
    def row_line(m, v1, v2):
        return f"  │ {m:<{col_metric - 2}} │ {v1:<{col_c1 - 2}} │ {v2:<{col_c2 - 2}} │"

    print(f"\n  {'COUNTRY COMPARISON':^{col_metric + col_c1 + col_c2 + 8}}")
    print(sep)
    print(row_line("Metric", n1, n2))
    print(sep)
    for r in rows:
        print(row_line(r["metric"], r["c1"], r["c2"]))
    print(sep)
    print()


# ─────────────────────────────────────────────
#  CLI entry-point
# ─────────────────────────────────────────────

def _usage():
    print(
        "\nUsage:\n"
        "  python countries.py get    <country_name>\n"
        "  python countries.py region <region_name>\n"
        "  python countries.py compare <country1> <country2>\n"
    )
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if not args:
        _usage()

    command = args[0].lower()

    try:
        if command == "get":
            if len(args) < 2:
                print("Error: provide a country name.")
                _usage()
            name = " ".join(args[1:])
            _print_country(get_country(name))

        elif command == "region":
            if len(args) < 2:
                print("Error: provide a region name.")
                _usage()
            region = " ".join(args[1:])
            countries = get_region(region)
            _print_region(countries, region.title())

        elif command == "compare":
            if len(args) < 3:
                print("Error: provide two country names.")
                _usage()
            c1, c2 = args[1], args[2]
            _print_comparison(compare_countries(c1, c2))

        else:
            print(f"Unknown command: '{command}'")
            _usage()

    except ValueError as e:
        print(f"\n  ✗  {e}\n")
        sys.exit(1)
    except RuntimeError as e:
        print(f"\n  ✗  {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()