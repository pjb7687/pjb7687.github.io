<script lang="ts">
  import Markdown from './Markdown.svelte';
  type Props = { period: string; lines: string[] };
  let { period, lines }: Props = $props();
</script>

<div class="entry-row grid grid-cols-[7.5rem_1fr] gap-x-6 py-3 rule items-baseline">
  <span class="mono text-[11px] text-faint tabular tracking-wider pt-1 select-none">
    {period}
  </span>
  <div class="text-[14px] leading-relaxed text-ink-2 space-y-0.5">
    {#each lines as line, i (i)}
      <div><Markdown source={line} /></div>
    {/each}
  </div>
</div>
