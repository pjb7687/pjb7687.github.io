<script lang="ts">
  import { profile } from '$lib/data/profile';
  import { publications, stats, conferenceProceedings } from '$lib/data/publications';

  const hasCitations = publications.some((p) => (p.citations ?? 0) > 0);
  const featured = (
    hasCitations
      ? [...publications].sort((a, b) => (b.citations ?? 0) - (a.citations ?? 0))
      : [...publications].sort((a, b) => (b.year ?? 0) - (a.year ?? 0))
  ).slice(0, 4);

  const totalCitations = stats.citedby ?? profile.stats.totalCitations;
  const hIndex = stats.hindex ?? profile.stats.hIndex;
  const pubCount = publications.length + conferenceProceedings.length;
</script>

<svelte:head>
  <title>Dr. Jeongbin Park · Bioinformatician · Pusan National University</title>
</svelte:head>

<!-- HERO -->
<section class="pt-16 pb-16 max-w-[720px] mx-auto text-center">
  <p class="text-[13px] text-faint uppercase tracking-wide mb-4">{profile.role}</p>
  <h1 class="text-[clamp(36px,5vw,56px)] font-bold leading-tight tracking-[-0.02em] text-ink mb-6">
    Dr. Jeongbin Park
  </h1>
  <p class="text-[15px] leading-relaxed text-ink-2 mb-4">
    A bioinformatician building tools for
    CRISPR design, spatial transcriptomics, and single-cell genomics &mdash;
    currently teaching and running a lab at
    <a class="link" href={profile.affiliation.url} target="_blank" rel="noopener noreferrer">{profile.affiliation.en}</a>.
  </p>
  <p class="text-[13px] leading-relaxed text-faint max-w-[560px] mx-auto">
    Trained in physics (Pusan National University &middot; Seoul National University) and biology (Heidelberg University),
    with postdoctoral research at DKFZ Heidelberg. Returned to Korea in 2022
    to establish the
    <a class="link" href={profile.links.lab} target="_blank" rel="noopener noreferrer">Computational Omics Laboratory (COLab)</a>.
  </p>

  <!-- Social icons -->
  <div class="flex justify-center items-center gap-4 mt-8" style="font-size:28px; line-height:1;">
    <a href={profile.links.scholar} target="_blank" rel="noopener noreferrer" title="Google Scholar" style="color:#4285f4;">
      <i class="ai ai-google-scholar"></i>
    </a>
    <a href={profile.links.orcid} target="_blank" rel="noopener noreferrer" title="ORCID" style="color:#b2c046;">
      <i class="ai ai-orcid"></i>
    </a>
    <a href={profile.links.researchgate} target="_blank" rel="noopener noreferrer" title="ResearchGate" style="color:#00ccbb;">
      <i class="ai ai-researchgate"></i>
    </a>
    <a href={profile.links.github} target="_blank" rel="noopener noreferrer" title="GitHub" style="color:#181717;">
      <i class="bi bi-github"></i>
    </a>
  </div>
</section>

<!-- STATS -->
<section class="py-6 border-t border-rule">
  <div class="flex justify-center gap-12 text-center">
    <div>
      <div class="text-[11px] text-faint uppercase tracking-wide">Publications</div>
      <div class="text-[24px] font-medium tabular text-ink mt-1">{pubCount}</div>
    </div>
    <div>
      <div class="text-[11px] text-faint uppercase tracking-wide">Citations</div>
      <div class="text-[24px] font-medium tabular text-ink mt-1">
        {totalCitations.toLocaleString()}
      </div>
    </div>
    <div>
      <div class="text-[11px] text-faint uppercase tracking-wide">h-index</div>
      <div class="text-[24px] font-medium tabular text-ink mt-1">{hIndex}</div>
    </div>
  </div>
</section>

<!-- RESEARCH INTERESTS -->
<section class="grid grid-cols-12 gap-x-6 gap-y-8 py-12 border-t border-rule">
  <div class="col-span-12 md:col-span-3 space-y-2">
    <div class="text-[12px] text-faint uppercase tracking-wide">Research Interests</div>
  </div>
  <div class="col-span-12 md:col-span-9 space-y-8">
    {#each [
      {
        title: 'AI + Biology',
        desc: 'Machine learning for omics and biomedical data analysis',
        papers: publications.filter(p => /READRetro/i.test(p.title)).slice(0, 4)
      },
      {
        title: 'Spatial Omics',
        desc: 'Spatial transcriptomics, single-cell analysis, and cell-type inference',
        papers: (() => {
          const all = publications.filter(p => /spatial|in situ|SSAM|cell type|segmentation|SpaceTx|pheno-seq/i.test(p.title) && !/Correction/i.test(p.title) && !/PloS/i.test(p.venue));
          const ssam = all.filter(p => /segmentation-free/i.test(p.title));
          const rest = all.filter(p => !/segmentation-free/i.test(p.title));
          return [...ssam, ...rest].slice(0, 4);
        })()
      },
      {
        title: 'CRISPR',
        desc: 'Genome editing tool design, off-target analysis, and guide RNA databases',
        papers: publications.filter(p => /CRISPR|Cas9|Cas-OFF|Cas-Des|Cas-ana|Cpf1|Digenome|base editing|off-target|gene knockout/i.test(p.title)).slice(0, 4)
      }
    ] as area (area.title)}
      <div>
        <div class="text-[16px] sm:text-[18px] font-medium text-ink">{area.title}</div>
        <div class="text-[12px] text-faint mt-0.5 mb-3">{area.desc}</div>
        <ul class="space-y-1.5 text-[13px]">
          {#each area.papers as pub (pub.id)}
            <li class="leading-relaxed">
              {#if pub.url}
                <a href={pub.url} target="_blank" rel="noopener noreferrer" class="underline text-ink-2 hover:text-ink">{pub.title}</a>
              {:else}
                <span class="text-ink-2">{pub.title}</span>
              {/if}
              <span class="text-faint"> - <em>{pub.venue}</em>{#if pub.year}{' '}({pub.year}){/if}{#if pub.citations && pub.citations > 0}{' '}[cited: {pub.citations}]{/if}</span>
            </li>
          {/each}
        </ul>
      </div>
    {/each}
  </div>
</section>

<!-- CONTACT -->
<section class="grid grid-cols-12 gap-x-6 gap-y-6 py-14 border-t border-rule">
  <div class="col-span-12 md:col-span-3">
    <div class="text-[12px] text-faint uppercase tracking-wide">Contact</div>
  </div>
  <div class="col-span-12 md:col-span-9 grid sm:grid-cols-2 gap-8 text-[13px] text-ink-2">
    <div>
      <div class="text-[11px] text-faint uppercase tracking-wide mb-1">Email</div>
      <a class="link" href="mailto:{profile.email}">{profile.email}</a>
    </div>
    <div>
      <div class="text-[11px] text-faint uppercase tracking-wide mb-1">Office</div>
      <div class="leading-relaxed">{profile.address.en}</div>
      <div class="text-[11px] text-faint mt-1 tabular">{profile.tel}</div>
    </div>
  </div>
</section>
