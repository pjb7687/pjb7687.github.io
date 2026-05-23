// Build-time loader for Google Scholar cache produced by cache/get_citations.py.
//
// The cache lives outside src/ — these `?raw` imports are resolved by Vite at
// build time and inlined as plain strings, so no fs / network access is needed
// at runtime, which keeps the static adapter happy.

import gscacheRaw from '$cache/gscache.txt?raw';
import cocacheRaw from '$cache/cofirsts_cocorrespondence_cache.txt?raw';
import statsRaw from '$cache/stats.json?raw';

export type Publication = {
  id: string;
  /** Plain author list as a single string, e.g. "Foo and Bar and Baz". */
  authors: string[];
  /** Indices into `authors` that should be highlighted as the site owner. */
  selfIndices: number[];
  /** Number of joint-first authors (counted from index 0). */
  cofirstCount: number;
  /** Indices into `authors` flagged as co-corresponding. */
  correspondenceIndices: number[];
  title: string;
  venue: string;
  isJournal: boolean;
  volume?: string;
  number?: string;
  pages?: string;
  year?: number;
  url?: string;
  citations?: number;
};

export type AuthorStats = {
  name?: string;
  citedby?: number;
  hindex?: number;
  i10index?: number;
};

const SELF_NAMES = ['Jeongbin Park'];

/** Replace Unicode hyphens (U+2010–U+2015) and en/em-dashes with plain ASCII hyphen. */
function normalizeHyphens(s: string): string {
  return s.replace(/[\u2010\u2011\u2012\u2013\u2014\u2015]/g, '-');
}

function parseTSV(raw: string): Array<Record<string, string>> {
  const lines = normalizeHyphens(raw).split(/\r?\n/).filter((l) => l.length > 0);
  if (lines.length === 0) return [];
  const header = lines[0].replace(/^#/, '').split('\t');
  const out: Array<Record<string, string>> = [];
  for (let i = 1; i < lines.length; i++) {
    const cells = lines[i].split('\t');
    const row: Record<string, string> = {};
    for (let c = 0; c < header.length; c++) {
      row[header[c]] = cells[c] ?? '';
    }
    out.push(row);
  }
  return out;
}

type CoEntry = { num_cofirsts: number; correspondence_indices: number[] };
function parseCoCache(raw: string): Map<string, CoEntry> {
  const out = new Map<string, CoEntry>();
  const lines = raw.split(/\r?\n/).filter((l) => l.length > 0);
  for (let i = 1; i < lines.length; i++) {
    const cells = lines[i].split('\t');
    const id = cells[0];
    if (!id) continue;
    const num = parseInt(cells[1] || '1', 10) || 1;
    const idxRaw = cells[2] || '';
    const idx = idxRaw
      .split(',')
      .map((x) => x.trim())
      .filter((x) => x.length > 0)
      .map((x) => parseInt(x, 10))
      .filter((x) => !Number.isNaN(x));
    out.set(id, { num_cofirsts: num, correspondence_indices: idx });
  }
  return out;
}

function splitAuthors(s: string): string[] {
  if (!s) return [];
  return s
    .split(/\s+and\s+/)
    .map((a) => a.trim())
    .filter((a) => a.length > 0);
}

function findSelf(authors: string[]): number[] {
  const matches: number[] = [];
  authors.forEach((a, i) => {
    if (SELF_NAMES.some((n) => a === n || a.replace(/\s+/g, ' ') === n)) matches.push(i);
  });
  return matches;
}

function buildPublication(
  row: Record<string, string>,
  co: Map<string, CoEntry>
): Publication | null {
  const id = row.author_pub_id;
  const journal = row.journal?.trim() || '';
  const conference = row.conference?.trim() || '';
  const venue = journal || conference;
  if (!venue) return null;
  const authors = splitAuthors(row.author || '');
  const coEntry = co.get(id) ?? { num_cofirsts: 1, correspondence_indices: [] };
  return {
    id,
    authors,
    selfIndices: findSelf(authors),
    cofirstCount: coEntry.num_cofirsts,
    correspondenceIndices: coEntry.correspondence_indices,
    title: (row.title || '').replace(/\\"/g, '"'),
    venue,
    isJournal: journal.length > 0,
    volume: row.volume || undefined,
    number: row.number || undefined,
    pages: row.pages || undefined,
    year: row.pub_year ? parseInt(row.pub_year, 10) : undefined,
    url: row.pub_url || undefined,
    citations: row.num_citations ? parseInt(row.num_citations, 10) || undefined : undefined
  };
}

const co = parseCoCache(cocacheRaw);
const allRows = parseTSV(gscacheRaw);
const allPubs = allRows
  .map((r) => buildPublication(r, co))
  .filter((p): p is Publication => p !== null);

allPubs.sort((a, b) => (b.year ?? 0) - (a.year ?? 0));

export const publications: Publication[] = allPubs.filter((p) => p.isJournal);
export const conferenceProceedings: Publication[] = allPubs.filter((p) => !p.isJournal);

let parsedStats: AuthorStats = {};
try {
  parsedStats = JSON.parse(statsRaw);
} catch {
  parsedStats = {};
}
export const stats: AuthorStats = parsedStats;

/** True if any cached publication has a co-first / co-correspondence marker. */
export const hasCofirst = allPubs.some((p) => p.cofirstCount > 1);
export const hasCocorrespondence = allPubs.some(
  (p) => p.correspondenceIndices.length > 1
);
