from scholarly import scholarly
import os

CACHE_HEADERS = ["author_pub_id", "num_cofirsts", "num_colasts", "title", "author", "journal", "conference", "volume", "number", "pages", "pub_year"]

def read_cache(cache_path):
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

def write_cache(bibs, cache_path):
    def append_anyway(e, bib, entries):
        if e in bib:
            entries.append(str(bib[e]))
        else:
            entries.append("")
    with open(cache_path, "w", encoding='utf-8') as f:
        f.write('\t'.join(CACHE_HEADERS) + '\n')
        for author_pub_id, bib in bibs.items():
            entries = [author_pub_id, str(bib['num_cofirsts']), str(bib['num_colasts']), bib['title'], bib['author'], ]
            append_anyway('journal', bib, entries)
            append_anyway('conference', bib, entries)
            append_anyway('volume', bib, entries)
            append_anyway('number', bib, entries)
            append_anyway('pages', bib, entries)
            append_anyway('pub_year', bib, entries)
            f.write('\t'.join(entries) + '\n')

def fetch_publications(author_id, cache_path, max_publications=0, verbose=True):
    if verbose:
        print("Fetching author profile...")

    author = scholarly.fill(scholarly.search_author_id(author_id))
    proceedings = []
    publications = []
    bibs = {}

    has_cofirst = False
    has_colast = False

    gscache = read_cache(cache_path)
    for i, p in enumerate(author['publications']):
        if max_publications > 0 and i == max_publications:
            break
        bib = gscache.get(p['author_pub_id'], None)
        if  or bib['title'] != p['bib']['title']:
            if verbose:
                print(f"Fetching publication '{p['bib']['title']}'...")
            scholarly.fill(p)
            p['bib']['num_cofirsts'] = bib.get('num_cofirsts', 1)
            p['bib']['num_colasts'] = bib.get('num_colasts', 1)
            bib = p['bib']
        bibs[p['author_pub_id']] = bib
        authors = list(bib['author'].split(' and '))
        cofirsts = int(bib['num_cofirsts'])
        colasts = int(bib['num_colasts'])
        for i in range(len(authors)):
            if authors[i] == author['name']:
                authors[i] = ":underline:`" + authors[i] + "`"
        if cofirsts > 1:
            has_cofirst = True
            for i in range(cofirsts):
                authors[i] += '\\ :superscript:`†`'
        if colasts > 1:
            has_colast = True
            for i in range(len(authors)-1, len(authors)-colasts-1):
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
            publications.append(cit)
        else:
            proceedings.append(cit)
    write_cache(bibs, cache_path)
    if verbose:
        print("Done!")
    return author, publications, proceedings, has_cofirst, has_colast

def write_rst(author, publications, proceedings, has_cofirst, has_colast, verbose=True):
    if verbose:
        print("Writing rst...")

    with open("source/publications.rst", "w", encoding="utf-8") as f:
        f.write(".. role:: underline\n")
        f.write("    :class: underline\n\n")
        f.write("CONFERENCE PROCEEDINGS\n")
        f.write("----------------------\n")
        f.write(".. container:: entries text-justify\n\n")
        for cit in proceedings:
            f.write(f"    {cit}\n\n")
        f.write("PUBLICATIONS\n")
        f.write("------------\n")
        f.write(".. container:: entries text-justify\n\n")
        for cit in publications:
            f.write(f"    {cit}\n\n")
        f.write(".. container:: text-right\n\n")
        f.write(f"    | Total Citations: {author['citedby']}, H-index: {author['hindex']}\n")
        f.write("    |\n\n")
        f.write(".. container:: entries text-left\n\n")
        if has_cofirst:
            f.write("    - †: Joint first authors.\n")
        if has_colast:
            f.write("    - *: Co-corresponding authors.\n")
        f.write("    - The citation numbers were retrieved from Google Scholar.\n")

    if verbose:
        print("Done!")

if __name__ == "__main__":
    write_rst(*fetch_publications("XLVldUsAAAAJ", ".ci/gscache.txt", 0))
