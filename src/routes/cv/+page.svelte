<script lang="ts">
  import CVPage from '$lib/components/CVPage.svelte';
  import { onMount } from 'svelte';

  onMount(() => {
    document.body.style.background = '#ddd';
    return () => { document.body.style.background = ''; };
  });
</script>

<svelte:head>
  <title>Curriculum Vitae · Dr. Jeongbin Park</title>
  <meta name="description" content="Academic CV of Dr. Jeongbin Park - education, work experience, publications, and teaching." />
  <link rel="canonical" href="https://jeongbinpark.com/cv" />
</svelte:head>

<CVPage initialLang="en" />
