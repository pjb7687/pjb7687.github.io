from scholarly import scholarly
import os

CACHE_HEADERS = ["author_pub_id", "title", "author",
                 "journal", "conference", "volume", "number", "pages", "pub_year", "pub_url"]

def read_gs_cache(cache_path):
    bibs = {}
    if not os.path.exists(cache_path):
        with open(cache_path, "w", encoding='utf-8') as f:
            hj = '\t'.join(CACHE_HEADERS)
            f.write(f"#{hj}\n")
    with open(cache_path, encoding='utf-8') as f:
        f.readline()
        for line in f:
            entries = line.strip().split('\t')
            bib = {}
            for h, e in zip(CACHE_HEADERS[1:], entries[1:]):
                if len(e) > 0:
                    bib[h] = e
            bibs[entries[0]] = bib
    return bibs

def write_gs_cache(bibs, cache_path):
    def append_anyway(e, bib, entries):
        if e in bib:
            entries.append(str(bib[e]))
        else:
            entries.append("")
    with open(cache_path, "w", encoding='utf-8') as f:
        f.write('\t'.join(CACHE_HEADERS) + '\n')
        for author_pub_id, bib in bibs.items():
            entries = [author_pub_id, bib['title'], bib['author'], ]
            for hdr in CACHE_HEADERS[3:]:
                append_anyway(hdr, bib, entries)
            f.write('\t'.join(entries) + '\n')

def read_co_cache(cache_path):
    cocache = {}
    if not os.path.exists(cache_path):
        with open(cache_path, "w", encoding='utf-8') as f:
            f.write("#author_pub_id\tnum_cofirsts\tcorrespondence_indices\n")
    with open(cache_path, encoding='utf-8') as f:
        f.readline()
        for line in f:
            entries = line.strip().split('\t')
            cocache[entries[0]] = (int(entries[1]), [int(i) for i in ','.split(entries[2])], )
    return cocache

def write_co_cache(cocache, cache_path):
    with open(cache_path, "w", encoding='utf-8') as f:
        f.write("#author_pub_id\tnum_cofirsts\ncorrespondence_indices\n")
        for author_pub_id, c in cocache.items():
            f.write(f"{author_pub_id}\t{c[0]}\t{','.join([str(i) for i in c[1]])}\n")
    return cocache
  
def fetch_publications(author_id, gs_cache_path, co_cache_path, max_publications=0, verbose=True):
    if verbose:
        print("Fetching author profile...")

    author = scholarly.fill(scholarly.search_author_id(author_id))
    proceedings = []
    publications = []
    bibs = {}

    has_cofirst = False
    has_cocorrespondence = False

    gscache = read_gs_cache(gs_cache_path)
    cocache = read_co_cache(co_cache_path)
    for i, p in enumerate(author['publications']):
        if max_publications > 0 and i == max_publications:
            break
        bib = gscache.get(p['author_pub_id'], None)
        num_cofirsts = gscache.get(p['author_pub_id'], None)
        if bib is None or bib['title'] != p['bib']['title']:
            if verbose:
                print(f"Fetching publication '{p['bib']['title']}'...")
            scholarly.fill(p)
            p['bib']['num_cofirsts'], p['bib']['correspondence_indices'] = cocache.get(p['author_pub_id'], (1, []))
            bib = p['bib']
        bibs[p['author_pub_id']] = bib
        authors = list(bib['author'].split(' and '))
        cofirsts = int(bib['num_cofirsts'])
        correspondences = len(bib['correspondence_indices'])
        for i in range(len(authors)):
            if authors[i] == author['name']:
                authors[i] = ":underline:`" + authors[i] + "`"
        if cofirsts > 1:
            has_cofirst = True
            for i in range(cofirsts):
                authors[i] += '\\ :superscript:`†`'
        if correspondences > 1:
            has_cocorrespondence = True
            for i in bib['correspondence_indices']:
                authors[i] += '\\ :superscript:`*`'
        if 'journal' in bib:
            journal = bib['journal']
        else:
            journal = bib['conference']
        cit = f"{', '.join(authors)}, **\"{bib['title']}\"**, *{journal}*"
        if 'volume' in bib:
            cit += f" {bib['volume']}"
        if 'number' in bib:
            cit += f" ({bib['number']})"
        if 'pages' in bib:
            cit += f", {bib['pages']}"
        cit += f" ({bib['pub_year']})."
        if int(p['num_citations']) > 0:
            cit += f" [cited: {p['num_citations']}]"
        if 'journal' in bib:
            publications.append(cit, bib.get('pub_url', ""))
        else:
            proceedings.append(cit, bib.get('pub_url', ""))
    write_gs_cache(bibs, gs_cache_path)
    if verbose:
        print("Done!")
    return author, publications, proceedings, has_cofirst, has_cocorrespondence

def write_rst(author, publications, proceedings, has_cofirst, has_cocorrespondence, verbose=True):
    if verbose:
        print("Writing rst...")

    with open("source/publications.rst", "w", encoding="utf-8") as f:
        f.write(".. role:: underline\n")
        f.write("    :class: underline\n\n")
        f.write("CONFERENCE PROCEEDINGS\n")
        f.write("----------------------\n")
        f.write(".. container:: entries text-justify publications\n\n")
        for idx, (cit, pub_url) in enumerate(proceedings):
            if len(pub_url) > 0:
                f.write(f"    .. _proc{idx}: {pub_url}\n    .. |proc{idx}| replace:: {cit}\n    |proc{idx}|_\n\n")
            else:
                f.write(f"    {cit}\n\n")
        f.write("PUBLICATIONS\n")
        f.write("------------\n")
        f.write(".. container:: entries text-justify publications\n\n")
        for idx, (cit, pub_url) in enumerate(publications):
            if len(pub_url) > 0:
                f.write(f"    .. _pub{idx}: {pub_url}\n    .. |pub{idx}| replace:: {cit}\n    |pub{idx}|_\n\n")
            else:
                f.write(f"    {cit}\n\n")
        f.write(".. container:: text-right\n\n")
        f.write(f"    | Total Citations: {author['citedby']}, H-index: {author['hindex']}\n")
        f.write("    |\n\n")
        f.write(".. container:: entries text-left\n\n")
        if has_cofirst:
            f.write("    - †: Joint first authors.\n")
        if has_cocorrespondence:
            f.write("    - *: Co-corresponding authors.\n")
        f.write("    - The citation numbers were retrieved from Google Scholar.\n")

    if verbose:
        print("Done!")

if __name__ == "__main__":
    write_rst(*fetch_publications("XLVldUsAAAAJ", ".ci/gscache.txt",  ".ci/cofirsts_cocorrespondence_cache.txt", 0))
