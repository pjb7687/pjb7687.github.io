<script lang="ts">
  import CVPage from '$lib/components/CVPage.svelte';
  import { onMount } from 'svelte';

  onMount(() => {
    document.body.style.background = '#ddd';
    return () => { document.body.style.background = ''; };
  });
</script>

<svelte:head>
  <title>이력서 · Prof. Dr. Jeongbin Park</title>
  <meta name="description" content="박정빈 박사 (Prof. Dr. Jeongbin Park) 학력·경력·논문 이력서" />
  <link rel="canonical" href="https://jeongbinpark.com/cv" />
</svelte:head>

<CVPage initialLang="ko" />
