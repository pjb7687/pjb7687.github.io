"""
Fetch publication metadata + Google-Scholar citation counts.

Run from project root:
    uv run cache/get_citations.py

Writes:
    cache/gscache.txt                          (TSV — bib + num_citations)
    cache/cofirsts_cocorrespondence_cache.txt  (TSV — co-first / co-corresponding markers)
    cache/stats.json                           (author totals: citedby, hindex)

The SvelteKit build reads these files at compile time; no Python is needed during
the SvelteKit build itself.
"""

# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "scholarly @ git+https://github.com/pjb7687/scholarly.git@sortbydate",
# ]
# ///

from scholarly import scholarly as s
import json
import os
import sys

CACHE_DIR = os.path.dirname(os.path.abspath(__file__))
GS_CACHE = os.path.join(CACHE_DIR, "gscache.txt")
CO_CACHE = os.path.join(CACHE_DIR, "cofirsts_cocorrespondence_cache.txt")
STATS_JSON = os.path.join(CACHE_DIR, "stats.json")

AUTHOR_ID = "XLVldUsAAAAJ"

CACHE_HEADERS = [
    "author_pub_id",
    "title",
    "author",
    "journal",
    "conference",
    "volume",
    "number",
    "pages",
    "pub_year",
    "pub_url",
    "num_citations",
]


def read_gs_cache(cache_path):
    bibs = {}
    if not os.path.exists(cache_path):
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write("#" + "\t".join(CACHE_HEADERS) + "\n")
        return bibs
    with open(cache_path, encoding="utf-8") as f:
        header = f.readline().lstrip("#").strip().split("\t")
        for line in f:
            entries = line.rstrip("\r\n").split("\t")
            bib = {}
            for h, e in zip(header[1:], entries[1:]):
                if len(e) > 0:
                    bib[h] = e
            if entries:
                bibs[entries[0]] = bib
    return bibs


def write_gs_cache(bibs, cache_path):
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write("#" + "\t".join(CACHE_HEADERS) + "\n")
        for author_pub_id, bib in bibs.items():
            row = [author_pub_id]
            for hdr in CACHE_HEADERS[1:]:
                row.append(str(bib.get(hdr, "")))
            f.write("\t".join(row) + "\n")


def read_co_cache(cache_path):
    cocache = {}
    if not os.path.exists(cache_path):
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write("#author_pub_id\tnum_cofirsts\tcorrespondence_indices\n")
        return cocache
    with open(cache_path, encoding="utf-8") as f:
        f.readline()
        for line in f:
            entries = line.rstrip("\r\n").split("\t")
            if not entries[0]:
                continue
            indices = []
            if len(entries) > 2 and entries[2]:
                indices = [int(i) for i in entries[2].split(",")]
            cocache[entries[0]] = (int(entries[1]), indices)
    return cocache


def write_co_cache(cocache, cache_path):
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write("#author_pub_id\tnum_cofirsts\tcorrespondence_indices\n")
        for author_pub_id, c in cocache.items():
            f.write(f"{author_pub_id}\t{c[0]}\t{','.join(str(i) for i in c[1])}\n")


def fetch_publications(author_id, gs_cache_path, co_cache_path, max_publications=0, verbose=True):
    if verbose:
        print(f"Fetching author profile for {author_id}…", file=sys.stderr)
    author = s.fill(s.search_author_id(author_id))

    old_bibs = read_gs_cache(gs_cache_path)
    old_cocache = read_co_cache(co_cache_path)

    # Build fresh dicts — only publications still on Scholar are kept.
    bibs = {}
    cocache = {}

    for i, p in enumerate(author["publications"]):
        if max_publications and i == max_publications:
            break
        pub_id = p["author_pub_id"]
        bib = old_bibs.get(pub_id, None)
        if bib is None or bib.get("title") != p["bib"]["title"]:
            if verbose:
                print(f"  fetching '{p['bib']['title']}'…", file=sys.stderr)
            s.fill(p)
            bib = dict(p["bib"])
            bib["pub_url"] = p.get("pub_url", "")
        # always refresh num_citations — it changes over time
        bib["num_citations"] = str(int(p.get("num_citations", 0) or 0))
        bibs[pub_id] = bib

        cocache[pub_id] = old_cocache.get(pub_id, (1, []))

    removed = set(old_bibs) - set(bibs)
    if removed and verbose:
        for r in removed:
            print(f"  removed '{old_bibs[r].get('title', r)}'", file=sys.stderr)

    write_gs_cache(bibs, gs_cache_path)
    write_co_cache(cocache, co_cache_path)

    return {
        "name": author.get("name", ""),
        "citedby": int(author.get("citedby", 0) or 0),
        "hindex": int(author.get("hindex", 0) or 0),
        "i10index": int(author.get("i10index", 0) or 0),
    }


if __name__ == "__main__":
    stats = fetch_publications(AUTHOR_ID, GS_CACHE, CO_CACHE)
    with open(STATS_JSON, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    print(f"\nDone. citedby={stats['citedby']}, hindex={stats['hindex']}", file=sys.stderr)
