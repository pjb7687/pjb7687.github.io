<script lang="ts">
  import type { Publication } from '$lib/data/publications';
  import AuthorList from './AuthorList.svelte';

  let { pub, index }: { pub: Publication; index: number } = $props();
</script>

<li class="pub-entry grid grid-cols-[2.25rem_1fr] gap-4 py-2.5 rule items-baseline">
  <span class="mono text-[10px] text-faint tabular pt-1 tracking-wider select-none">
    [{String(index).padStart(2, '0')}]
  </span>
  <div class="text-[13.5px] leading-relaxed text-ink-2">
    <AuthorList {pub} />
    {#if pub.url}
      , <a class="link font-medium text-ink" href={pub.url} target="_blank" rel="noopener noreferrer"
        >&ldquo;{pub.title}&rdquo;</a
      >
    {:else}
      , <span class="font-medium text-ink">&ldquo;{pub.title}&rdquo;</span>
    {/if},
    <em class="italic text-ink-2">{pub.venue}</em>{#if pub.volume}
      <span class="tabular"> {pub.volume}</span>
    {/if}{#if pub.number}
      <span class="tabular"> ({pub.number})</span>
    {/if}{#if pub.pages}
      <span class="tabular">, {pub.pages}</span>
    {/if}{#if pub.year}
      <span class="tabular"> ({pub.year})</span>
    {/if}.
    {#if pub.citations && pub.citations > 0}
      <span class="mono text-[10.5px] text-mark pl-1 tracking-wider"
        >cited {pub.citations}</span
      >
    {/if}
  </div>
</li>
