<script lang="ts">
  import type { Publication } from '$lib/data/publications';
  let { pub }: { pub: Publication } = $props();

  type Token = { author: string; isSelf: boolean; markers: string };

  const tokens = $derived.by<Token[]>(() =>
    pub.authors.map((author, i) => {
      let markers = '';
      if (pub.cofirstCount > 1 && i < pub.cofirstCount) markers += '#';
      if (pub.correspondenceIndices.length > 1 && pub.correspondenceIndices.includes(i))
        markers += '*';
      return { author, isSelf: pub.selfIndices.includes(i), markers };
    })
  );
</script>

<span>{#each tokens as t, i (i)}{#if t.isSelf}<span class="author-self">{t.author}</span>{:else}{t.author}{/if}{#if t.markers}<sup class="mono text-[0.65em] align-super tracking-tight">{t.markers}</sup>{/if}{#if i < tokens.length - 1}{', '}{/if}{/each}</span>
