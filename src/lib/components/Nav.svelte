<script lang="ts">
  import { page } from '$app/state';

  type Item = { href: string; label: string };
  const items: Item[] = [
    { href: '/', label: 'Home' },
    { href: '/cv', label: 'CV' },
    { href: '/lectures', label: 'Lectures' }
  ];

  const path = $derived(page.url?.pathname ?? '/');
  function active(href: string) {
    if (href === '/') return path === '/';
    if (href === '/cv') return path === '/cv' || path === '/cv-ko';
    return path === href || path.startsWith(href + '/');
  }
</script>

<nav class="no-print sticky top-0 z-30 bg-white border-b border-rule shadow-sm">
  <div class="max-w-[1180px] mx-auto px-6 md:px-10 flex items-center justify-between h-14">
    <a href="/" class="text-[14px] font-medium tracking-tight text-ink">
      Jeongbin Park
    </a>
    <ul class="flex items-center gap-4 md:gap-6">
      {#each items.slice(1) as item (item.href)}
        <li>
          <a
            href={item.href}
            class={[
              'text-[13px] transition-colors',
              active(item.href) ? 'text-mark font-medium' : 'text-faint hover:text-ink'
            ].join(' ')}
            aria-current={active(item.href) ? 'page' : undefined}
          >
            {item.label}
          </a>
        </li>
      {/each}
      <li>
        <a
          href="https://pnucolab.com"
          target="_blank"
          rel="noopener noreferrer"
          class="text-[13px] text-faint hover:text-ink transition-colors inline-flex items-center gap-1"
        >
          COLAB@PNU
          <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </a>
      </li>
    </ul>
  </div>
</nav>
