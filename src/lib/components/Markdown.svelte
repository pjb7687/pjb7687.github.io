<script lang="ts" module>
  function escapeHtml(s: string) {
    return s
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  export function render(input: string): string {
    let out = escapeHtml(input);
    out = out.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    out = out.replace(/(?<![_\w])_([^_\n]+)_(?![_\w])/g, '<em>$1</em>');
    out = out.replace(/\\([#*])/g, '$1');
    // autolink bare URLs — use word-break so long URLs don't blow out layout
    out = out.replace(
      /(https?:\/\/[^\s<>")]+)/g,
      (url) =>
        `<a href="${url}" target="_blank" rel="noopener noreferrer" style="word-break:break-all">${url.replace(/^https?:\/\//, '')}</a>`
    );
    return out;
  }
</script>

<script lang="ts">
  let { source }: { source: string } = $props();
</script>

<!-- eslint-disable-next-line svelte/no-at-html-tags -->
<span>{@html render(source)}</span>
