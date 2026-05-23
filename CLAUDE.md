# CLAUDE.md

Personal academic website for **Dr. Jeongbin Park** — bioinformatician at the School of Biomedical Convergence Engineering, Pusan National University. Served at https://jeongbinpark.com.

## Stack

- SvelteKit 2 with Svelte 5 (runes mode, see `svelte.config.js`)
- TypeScript (strict)
- Tailwind CSS v4 (via `@tailwindcss/vite`) with `@tailwindcss/typography` plugin
- `@sveltejs/adapter-static` — fully static, deployed to GitHub Pages branch `gh-pages` with custom domain
- pnpm (host) / uv (Python script) / Docker (scheduled builds)

## Layout

```
src/
  app.html
  routes/
    +layout.svelte          # global shell (nav, container, footer)
    +layout.ts              # `prerender = true`
    layout.css              # Tailwind + design tokens + print stylesheet
    +page.svelte            # home (/)
    cv/+page.svelte         # English CV (uses CVPage with lang="en")
    cv-ko/+page.svelte      # Korean CV (uses CVPage with lang="ko")
    lectures/+page.svelte
  lib/
    data/
      profile.ts            # name, contact, social links
      cv.ts                 # education, work, service, teaching, notes (en + ko)
      lectures.ts           # course/slide listing
      publications.ts       # parses cache/*.txt at build time (?raw imports)
    components/
      CVPage.svelte         # the print-ready CV layout, shared by /cv and /cv-ko
      PublicationEntry.svelte
      AuthorList.svelte     # underlines self + appends # / * markers from co-cache
      Section.svelte
      EntryRow.svelte       # year/period + content row
      Markdown.svelte       # tiny **bold**/_italic_/autolink renderer
      Nav.svelte
cache/                      # Google Scholar cache (single source of truth for pubs)
  gscache.txt               # TSV — author, title, venue, year, num_citations, ...
  cofirsts_cocorrespondence_cache.txt  # TSV — # / * markers per pub
  stats.json                # totals (citedby, hindex)
  get_citations.py          # uv script; PEP-723 inline deps; updates the TSVs
static/
  CNAME                     # jeongbinpark.com
  .nojekyll
Dockerfile                  # node + uv + pnpm
entrypoint.sh               # build | scheduler
build.sh                    # refresh cache, install, build
compose.yml                 # scheduled service (Wed 03:00 KST, restart: always)
```

## How publications get into the build

Publications are **never hardcoded** in TypeScript. The flow is:

1. `cache/get_citations.py` runs via `uv run cache/get_citations.py` (PEP-723 inline metadata pulls `scholarly` from the `pjb7687/scholarly@sortbydate` fork).
2. The script writes / updates:
   - `cache/gscache.txt` — one row per publication (TSV), with `num_citations` now part of the schema so the SvelteKit build doesn't need network or Python.
   - `cache/cofirsts_cocorrespondence_cache.txt` — manual annotations for joint-first / co-corresponding authors.
   - `cache/stats.json` — total citations + h-index.
3. `src/lib/data/publications.ts` imports the cache files via Vite `?raw` (`$cache/gscache.txt?raw`) and parses them at build time. The `$cache` alias is set in `svelte.config.js`.
4. The CV pages render whatever is in the cache; `index.html` surfaces the top 4 by citations (or by year if citation data is empty).

**Do not** copy publication data out of the cache into TS. The cache is canonical and is what gets re-fetched periodically.

## Build

Local:
```
pnpm install
./build.sh                 # = uv run cache/get_citations.py + pnpm build
# or, without refreshing citations:
pnpm build                 # uses whatever is in cache/
```

Docker (one-off):
```
docker compose run --rm web build
```

Docker (scheduled — every Wednesday at 03:00 KST, restart always):
```
docker compose up -d
docker compose logs -f web
```

The scheduler is a tiny shell loop in `entrypoint.sh` (not cron) so all build output lands directly on the container's stdout, which `docker compose logs` streams.

## Design constraints

- **White background. Sans-serif (Pretendard Variable + JetBrains Mono).** No dark backgrounds, no serif body. Academic but distinctive — not Bootstrap.
- **Print PDF in classic academic format.** The CV pages have a Save-as-PDF button that triggers `window.print()`. Print styles live in `src/routes/layout.css` under `@media print` and produce single-column, hairline-ruled output at A4 with margins and tight academic typography. The nav, footer, and print button are hidden in print.
- **Author highlight.** The self-author (Jeongbin Park) gets a soft yellow `author-self` highlight on screen and a plain underline in print. Co-first / co-corresponding markers (`#`, `*`) come from the co-cache.

## Content

- Home: name + role + intro, stats ticker (publication count, citations, h-index), navigation tiles, featured publications, contact.
- /cv: full academic CV in English (education, work, service, teaching, conference proceedings, publications, notes). Cache-driven.
- /cv-ko: same structure in Korean. Cache-driven (publications are language-agnostic).
- /lectures: course list with Google Slides links (mostly Korean — that's authentic).

The **COVID-19 dashboard** page (`covid19hd.html`) from the old Sphinx site is dead and is intentionally NOT ported.

## Conventions

- Svelte 5 runes only (`$state`, `$derived`, `$props`). Runes mode is enforced in `svelte.config.js`.
- No Bootstrap, no jQuery, no SCSS — those are remnants of the Sphinx era and have been removed.
- All publication data flows from `cache/*.txt` through `src/lib/data/publications.ts`. To change the publication list, run `uv run cache/get_citations.py`, then rebuild.
- Korean and English CVs share a single component (`CVPage.svelte` with a `lang` prop) so they never drift apart structurally.
