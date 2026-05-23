<script lang="ts">
  type Props = {
    number: string;
    label: string;
    title?: string;
    children: import('svelte').Snippet;
  };
  let { number, label, title, children }: Props = $props();
</script>

<section class="grid grid-cols-1 md:grid-cols-[10rem_1fr] gap-x-12 gap-y-4 py-10 rule-top">
  <header class="md:sticky md:top-24 self-start space-y-1">
    <div class="mono text-[10px] text-faint tracking-[0.2em] uppercase">§ {number}</div>
    <h2 class="small-caps text-[12px] text-ink font-semibold">{label}</h2>
    {#if title}
      <p class="text-[13px] text-faint leading-snug max-w-[10rem]">{title}</p>
    {/if}
  </header>
  <div class="min-w-0">
    {@render children()}
  </div>
</section>
