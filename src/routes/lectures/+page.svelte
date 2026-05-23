<script lang="ts">
  import { series } from '$lib/data/lectures';
</script>

<svelte:head>
  <title>Lectures · Prof. Dr. Jeongbin Park</title>
  <meta name="description" content="강의자료 — Bioinformatics, Biomedical Informatics, and related courses at PNU." />
</svelte:head>

<header class="pt-4 pb-10 grid grid-cols-12 gap-6 items-end">
  <div class="col-span-12 md:col-span-3 space-y-2">
    <div class="mono text-[10px] text-faint tracking-[0.15em] uppercase">Lectures</div>
    <p class="text-[12.5px] text-faint">의생명융합공학부, 부산대학교</p>
  </div>
  <div class="col-span-12 md:col-span-9">
    <h1 class="text-[clamp(28px,4vw,40px)] font-bold tracking-[-0.01em] leading-tight">
      Lecture Materials
    </h1>
    <p class="text-[14px] text-ink-2 max-w-[52ch] mt-3 leading-relaxed">
      Course slides for undergraduate and graduate classes taught at Pusan National University.
    </p>
  </div>
</header>

{#each series as s, si (s.code)}
  <section class="grid grid-cols-12 gap-6 py-12 rule-top">
    <header class="col-span-12 md:col-span-3 space-y-2 md:sticky md:top-24 self-start">
      <!-- code removed -->
      <h2 class="text-[18px] font-medium leading-tight">{s.titleKo}</h2>
      <p class="text-[12px] text-faint italic">{s.titleEn}</p>
    </header>

    <ol class="col-span-12 md:col-span-9">
      {#each s.lectures as l, li (li)}
        {#if l.url}
          <li>
            <a
              href={l.url}
              target="_blank"
              rel="noopener noreferrer"
              class="group grid grid-cols-[3rem_1fr_auto] gap-4 items-baseline py-4 rule hover:bg-paper-tint/60 transition-colors px-1"
            >
              <span class="mono text-[10.5px] text-faint tabular tracking-wider"
                >{String(li + 1).padStart(2, '0')}</span
              >
              <span class="text-[15px] text-ink-2 group-hover:text-mark transition-colors">
                {l.title}
              </span>
              <span class="mono text-[10px] text-faint tracking-wider uppercase whitespace-nowrap"
                >slides ↗</span
              >
            </a>
          </li>
        {:else}
          <li
            class="grid grid-cols-[3rem_1fr_auto] gap-4 items-baseline py-4 rule px-1 text-faint"
          >
            <span class="mono text-[10.5px] tabular tracking-wider"
              >{String(li + 1).padStart(2, '0')}</span
            >
            <div>
              <div class="text-[15px]">{l.title}</div>
              {#if l.note}
                <div class="text-[12px] mt-0.5 italic">{l.note}</div>
              {/if}
            </div>
            <span class="mono text-[10px] tracking-wider uppercase whitespace-nowrap">non-public</span>
          </li>
        {/if}
      {/each}
      {#if s.exam}
        <li class="grid grid-cols-[3rem_1fr_auto] gap-4 items-baseline py-4 rule px-1">
          <span class="mono text-[10.5px] text-mark tabular tracking-wider">EX</span>
          <a
            href={s.exam.url}
            target="_blank"
            rel="noopener noreferrer"
            class="link text-[14.5px] text-ink-2 hover:text-mark"
          >
            {s.exam.label} · {s.exam.url.replace(/^https?:\/\//, '').slice(0, 60)}…
          </a>
          <span class="mono text-[10px] text-faint tracking-wider uppercase whitespace-nowrap"
            >exam ↗</span
          >
        </li>
      {/if}
    </ol>
  </section>
{/each}
