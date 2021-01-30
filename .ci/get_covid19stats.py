#!env python
import urllib.request
import re
import os

import numpy as np
import pandas as pd

import pdfminer
from pdfminer.high_level import extract_pages

def extract_text(fn):
    found_elements = []
    for page_layout in extract_pages(fn, maxpages=1):
        for element in page_layout:
            if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                found_elements.append(element)
    found_elements.sort(key=lambda e: e.bbox[0])
    found_elements.sort(key=lambda e: e.bbox[1], reverse=True)
    return [e.get_text().strip() for e in found_elements]

def parse_numbers(idx, entries):
    return [float(e.strip('*').replace(',', '.').strip()) if ',' in e else int(e.strip('*').strip()) for e in entries[idx+1:idx+3]]

def calc_rolling_average(df):
    mask = df['Daily new'] == 0
    df.loc[mask, 'Daily new'] = df["Total"].diff()[mask]
    df['Daily new 7-day average'] = df['Daily new'].rolling(window=7).mean()
    return df

def fetch_stats(out_dir, verbose=True):
    urls = [
        "https://www.rhein-neckar-kreis.de/start/landratsamt/coronavirus+fallzahlen+03-07.html",
        "https://www.rhein-neckar-kreis.de/start/landratsamt/coronavirus+fallzahlen+08-09.html",
        "https://www.rhein-neckar-kreis.de/start/landratsamt/coronavirus+fallzahlen.html"
    ]
    p = re.compile('a href="(.+?Faktenblatt_Corona_RNK\.pdf)" title="" target="_blank">')

    if verbose:
        print("Checking updates...")

    pdf_urls = []
    for url in urls:
        with urllib.request.urlopen(url) as f:
            t = f.read().decode("utf-8")
            pdf_urls += list(p.findall(t))
    url_root = "https://www.rhein-neckar-kreis.de/"
    pdf_root = "pdfs/"
    if not os.path.exists(pdf_root):
        os.mkdir(pdf_root)

    df_headers = ["Total", "Recovered", "Deaths", "Quarantined", "7 Day Incidents", "Daily new"]
    if os.path.exists(os.path.join(out_dir, 'hd_stats.json')):
        hd_stats = pd.read_json(os.path.join(out_dir, 'hd_stats.json'), orient="split").T
        rnk_stats = pd.read_json(os.path.join(out_dir, 'rnk_stats.json'), orient="split").T
    else:
        hd_stats = pd.DataFrame(columns=df_headers)
        rnk_stats = pd.DataFrame(columns=df_headers)

    if len(pdf_urls) == 0:
        if verbose:
            print("No updates found!")
        return

    for pdf_url in pdf_urls:
        pdf_fn = pdf_url.split('/')[-1]

        date = pd.Timestamp("20%s-%s-%s"%(pdf_fn[:2], pdf_fn[2:4], pdf_fn[4:6]))
        if date in rnk_stats.index:
            continue
        
        if not os.path.exists(os.path.join(pdf_root, pdf_fn)):
            print("Downloading %s..."%pdf_fn)
            with urllib.request.urlopen(url_root + pdf_url) as f, open(os.path.join(pdf_root, pdf_fn), "wb") as fo:
                fo.write(f.read())

        print("Parsing %s..."%pdf_fn)
        covid_numbers = np.zeros([2, 6], dtype=float) # Rows: RNK, HD
                                                      # Cols: positive, recovered, deaths, quarantined, 7-day-incidences, difference yesterday
        covid_numbers[:, 4] = np.NaN
        entries = extract_text(os.path.join(pdf_root, pdf_fn))
        flags = np.zeros(5, dtype=bool)
        for idx, e in enumerate(entries):
            # RNK: idx == 0
            # HD: idx == 1
            if not flags[0] and ("Positive" in e or "Gesamtzahl" in e): # Positive
                covid_numbers[:, 0] = parse_numbers(idx, entries)
                flags[0] = True
            if not flags[1] and "Genesene" in e: # Recovered
                if 'Datenbank-Fehlers' in entries[-3] and 'Genesene Personen' in entries[-3]:
                    # Some numbers are not avilable due to database failure
                    covid_numbers[:, 1] = np.nan
                else:
                    covid_numbers[:, 1] = parse_numbers(idx, entries)
                flags[1] = True
            if not flags[2] and "Verstorbene" in e: # Deaths
                covid_numbers[:, 2] = parse_numbers(idx, entries)
                flags[2] = True
            if not flags[3] and "7-Tage-Inzidenz" in e: # 7-day-incidences
                covid_numbers[:, 4] = parse_numbers(idx, entries)
                flags[3] = True
            if not flags[4] and e == "Veränderung zum Vortag": # Daily new
                covid_numbers[:, 5] = parse_numbers(idx, entries)
                flags[4] = True
            if all(flags):
                # found all numbers
                break
        covid_numbers[:, 3] = covid_numbers[:, 0] - covid_numbers[:, 1] - covid_numbers[:, 2] # Calculate quarantined
        rnk_stats = rnk_stats.append(pd.DataFrame([covid_numbers[0]], columns=df_headers, index=[date]))
        hd_stats = hd_stats.append(pd.DataFrame([covid_numbers[1]], columns=df_headers, index=[date]))

    rnk_stats = rnk_stats.sort_index()
    hd_stats = hd_stats.sort_index()

    rnk_stats = calc_rolling_average(rnk_stats)
    rnk_stats.index = rnk_stats.index.strftime("%Y-%m-%d")
    rnk_stats.T.to_json(os.path.join(out_dir, "rnk_stats.json"), orient="split")

    hd_stats = calc_rolling_average(hd_stats)
    hd_stats.index = hd_stats.index.strftime("%Y-%m-%d")
    hd_stats.T.to_json(os.path.join(out_dir, "hd_stats.json"), orient="split")

    if verbose:
        print("Done!")

if __name__ == "__main__":
    fetch_stats("source/_static/")
