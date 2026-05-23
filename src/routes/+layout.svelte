<script lang="ts">
  import './layout.css';
  import Nav from '$lib/components/Nav.svelte';
  import { profile } from '$lib/data/profile';

  let { children } = $props();
</script>

<svelte:head>
  <title>Jeongbin Park</title>
  <meta name="description" content="Personal website of Prof. Dr. Jeongbin Park, bioinformatician at Pusan National University." />
  <meta name="author" content="Jeongbin Park" />
  <meta name="theme-color" content="#ffffff" />
  <link rel="canonical" href="https://jeongbinpark.com/" />
</svelte:head>

<Nav />

<main class="max-w-[1180px] mx-auto px-6 md:px-10 pt-1 pb-24">
  {@render children()}
</main>

<footer class="no-print border-t border-rule bg-white">
  <div
    class="max-w-[1180px] mx-auto px-6 md:px-10 py-10 grid gap-6 sm:grid-cols-[1fr_auto] items-baseline text-[12px] text-faint"
  >
    <div class="space-y-1">
      <p>
        <span class="text-ink-2 font-medium">Jeongbin Park</span> · {profile.role}
      </p>
      <p>{profile.affiliation.en}</p>
    </div>
    <ul class="flex flex-wrap gap-x-5 gap-y-1 mono tracking-wider text-[10.5px] uppercase">
      <li>
        <a class="link-quiet hover:text-mark" href={profile.links.scholar} target="_blank" rel="noopener noreferrer"
          >Scholar</a
        >
      </li>
      <li>
        <a class="link-quiet hover:text-mark" href={profile.links.orcid} target="_blank" rel="noopener noreferrer"
          >ORCID</a
        >
      </li>
      <li>
        <a
          class="link-quiet hover:text-mark"
          href={profile.links.researchgate}
          target="_blank"
          rel="noopener noreferrer">ResearchGate</a
        >
      </li>
      <li>
        <a class="link-quiet hover:text-mark" href={profile.links.github} target="_blank" rel="noopener noreferrer"
          >GitHub</a
        >
      </li>
    </ul>
  </div>
</footer>
