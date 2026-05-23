<script lang="ts">
  import Markdown from './Markdown.svelte';
  import AuthorList from './AuthorList.svelte';
  import { profile } from '$lib/data/profile';
  import { education, experience, service, teaching, notes } from '$lib/data/cv';
  import {
    publications,
    conferenceProceedings,
    stats,
    hasCofirst,
    hasCocorrespondence
  } from '$lib/data/publications';
  import type { Publication } from '$lib/data/publications';

  type Lang = 'en' | 'ko';
  let { initialLang = 'en' }: { initialLang?: Lang } = $props();
  let lang = $state<Lang>(initialLang);

  const L = {
    en: {
      lastUpdated: `last updated: ${profile.lastUpdated}`,
      print: 'Save as PDF',
      education: 'EDUCATION',
      experience: 'WORK EXPERIENCE',
      service: 'SERVICE',
      teaching: 'TEACHING',
      proceedings: 'CONFERENCE PROCEEDINGS',
      publications: 'PUBLICATIONS',
      totalCitations: 'Total Citations',
      hIndex: 'H-index',
    },
    ko: {
      lastUpdated: `마지막 갱신일: ${profile.lastUpdatedKo}`,
      print: 'PDF로 저장',
      education: 'EDUCATION',
      experience: 'WORK EXPERIENCE',
      service: 'SERVICE',
      teaching: 'TEACHING',
      proceedings: 'CONFERENCE PROCEEDINGS',
      publications: 'PUBLICATIONS',
      totalCitations: '총 인용수',
      hIndex: 'H-지수',
    }
  } as const;

  const t = $derived(L[lang]);
  const totalCitations = stats.citedby ?? profile.stats.totalCitations;
  const hIndex = stats.hindex ?? profile.stats.hIndex;

  function doPrint() {
    if (typeof window !== 'undefined') window.print();
  }

  function pubCitation(pub: Publication): string {
    let s = '';
    if (pub.volume) s += ' ' + pub.volume;
    if (pub.number) s += ' (' + pub.number + ')';
    if (pub.pages) s += ', ' + pub.pages;
    if (pub.year) s += ' (' + pub.year + ')';
    return s;
  }
</script>

<!-- Island menu bar above the paper -->
<div class="no-print flex items-center justify-center gap-3 py-3 sticky top-14 z-40">
  <div class="flex items-center gap-1 bg-white rounded-full shadow-md border border-rule px-1.5 py-1.5">
    <!-- Language toggle -->
    <button
      onclick={() => lang = 'en'}
      class={['px-3 py-1.5 rounded-full text-[13px] transition-colors cursor-pointer',
        lang === 'en' ? 'bg-ink text-white font-medium' : 'text-faint hover:text-ink'
      ].join(' ')}
    >
      English
    </button>
    <button
      onclick={() => lang = 'ko'}
      class={['px-3 py-1.5 rounded-full text-[13px] transition-colors cursor-pointer',
        lang === 'ko' ? 'bg-ink text-white font-medium' : 'text-faint hover:text-ink'
      ].join(' ')}
    >
      한국어
    </button>

    <!-- Divider -->
    <div class="w-px h-5 bg-rule mx-1"></div>

    <!-- Download PDF -->
    <button
      onclick={doPrint}
      class="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-[13px] text-faint hover:text-ink transition-colors cursor-pointer"
      title={t.print}
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
        <polyline points="14 2 14 8 20 8"></polyline>
        <line x1="12" y1="18" x2="12" y2="12"></line>
        <polyline points="9 15 12 18 15 15"></polyline>
      </svg>
      PDF
    </button>
  </div>
</div>

<article class="cv-print" style="position:relative; font-size:16px; font-family:'Roboto','Open Sans',sans-serif; width:250mm; max-width:100%; padding:20mm; margin:2mm auto 10mm auto; background:white; box-shadow:0 0 10px rgba(0,0,0,0.5);">

  <!-- HEADER -->
  <header class="text-center pb-4">
    <h1 style="font-size:32px; font-weight:bold; margin-bottom:4px;">Dr. Jeongbin Park</h1>
    <p style="font-size:14px;">({t.lastUpdated})</p>
  </header>

  <!-- CONTACT -->
  <div style="font-size:15px;" class="mb-6">
    <table class="mx-auto text-left">
      <tbody>
        <tr>
          <td class="text-right pr-5 align-top" style="padding-bottom:7px; width:35%;">{lang === 'en' ? 'Address:' : '주소:'}</td>
          <td class="align-top" style="padding-bottom:7px;">
            {#if lang === 'en'}
              <div>Room #413, Kyung-Ahm Engineering Building, Busandaehak-ro 49,</div>
              <div>Mulgeum-eup, Yangsan-si, 50612 Republic of Korea</div>
            {:else}
              {profile.address.ko}
            {/if}
          </td>
        </tr>
        <tr>
          <td class="text-right pr-5 align-top" style="padding-bottom:7px;">{lang === 'en' ? 'email:' : '이메일:'}</td>
          <td style="padding-bottom:7px;">{lang === 'en' ? profile.emailObfuscated : profile.email}</td>
        </tr>
        <tr>
          <td class="text-right pr-5 align-top" style="padding-bottom:7px;">{lang === 'en' ? 'Tel.:' : '전화:'}</td>
          <td style="padding-bottom:7px;">{lang === 'en' ? profile.tel : profile.telKo}</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- EDUCATION -->
  <section>
    <h2 style="font-size:19px; font-weight:bold; text-align:left; padding-top:12px; margin-bottom:0;">
      {t.education}
    </h2>
    <hr class="border-t border-black mb-4 mt-0.5">
    <table class="w-full" style="margin-left:10mm; padding-right:10mm;">
      <tbody>
        {#each education[lang] as entry, i (i)}
          <tr class="align-top">
            <td style="padding-bottom:14px; width:25%;">{entry.period}</td>
            <td style="padding-bottom:14px;">
              {#each entry.lines as line, j (j)}
                <div><Markdown source={line} /></div>
              {/each}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </section>

  <!-- WORK EXPERIENCE -->
  <section>
    <h2 style="font-size:19px; font-weight:bold; text-align:left; padding-top:12px; margin-bottom:0;">
      {t.experience}
    </h2>
    <hr class="border-t border-black mb-4 mt-0.5">
    <table class="w-full" style="margin-left:10mm; padding-right:10mm;">
      <tbody>
        {#each experience[lang] as entry, i (i)}
          <tr class="align-top">
            <td style="padding-bottom:14px; width:25%;">{entry.period}</td>
            <td style="padding-bottom:14px;">
              {#each entry.lines as line, j (j)}
                <div><Markdown source={line} /></div>
              {/each}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </section>

  <!-- SERVICE -->
  <section>
    <h2 style="font-size:19px; font-weight:bold; text-align:left; padding-top:12px; margin-bottom:0;">
      {t.service}
    </h2>
    <hr class="border-t border-black mb-4 mt-0.5">
    <div class="text-left" style="margin-left:10mm; padding-right:10mm;">
      {#each service[lang] as group, i (i)}
        <p class="font-bold mt-3 mb-1">{group.label}:</p>
        <ul style="list-style:disc outside; padding-left:10mm; margin-bottom:20px;">
          {#each group.items as item, j (j)}
            <li style="margin-bottom:10px;"><Markdown source={item} /></li>
          {/each}
        </ul>
      {/each}
    </div>
  </section>

  <!-- TEACHING -->
  <section>
    <h2 style="font-size:19px; font-weight:bold; text-align:left; padding-top:12px; margin-bottom:0;">
      {t.teaching}
    </h2>
    <hr class="border-t border-black mb-4 mt-0.5">
    <div class="text-left" style="margin-left:10mm; padding-right:10mm;">
      {#each teaching[lang] as group, i (i)}
        <p class="font-bold mt-3 mb-1">{group.label}:</p>
        <ul style="list-style:disc outside; padding-left:10mm; margin-bottom:20px;">
          {#each group.items as item, j (j)}
            <li style="margin-bottom:10px;"><Markdown source={item} /></li>
          {/each}
        </ul>
      {/each}
    </div>
  </section>

  <!-- CONFERENCE PROCEEDINGS -->
  {#if conferenceProceedings.length > 0}
    <section>
      <h2 style="font-size:19px; font-weight:bold; text-align:left; padding-top:12px; margin-bottom:0;">
        {t.proceedings}
      </h2>
      <hr class="border-t border-black mb-4 mt-0.5">
      <div class="text-justify" style="text-indent:-15mm; padding-left:25mm; padding-right:10mm;">
        {#each conferenceProceedings as pub (pub.id)}
          <p style="margin-bottom:0.5em; margin-top:0.8em;">
            {#if pub.url}<a href={pub.url} target="_blank" rel="noopener noreferrer" class="text-black no-underline"><AuthorList {pub} />, <strong>"{pub.title}"</strong>, <em>{pub.venue}</em>{pubCitation(pub)}.{#if pub.citations && pub.citations > 0}{' '}[cited: {pub.citations}]{/if}</a>{:else}<AuthorList {pub} />, <strong>"{pub.title}"</strong>, <em>{pub.venue}</em>{pubCitation(pub)}.{#if pub.citations && pub.citations > 0}{' '}[cited: {pub.citations}]{/if}{/if}
          </p>
        {/each}
      </div>
    </section>
  {/if}

  <!-- PUBLICATIONS -->
  <section>
    <h2 style="font-size:19px; font-weight:bold; text-align:left; padding-top:12px; margin-bottom:0;">
      {t.publications}
    </h2>
    <hr class="border-t border-black mb-4 mt-0.5">
    <div class="text-justify" style="text-indent:-15mm; padding-left:25mm; padding-right:10mm;">
      {#each publications as pub (pub.id)}
        <p style="margin-bottom:0.5em; margin-top:0.8em;" class="pub-entry">
          {#if pub.url}<a href={pub.url} target="_blank" rel="noopener noreferrer" class="text-black no-underline"><AuthorList {pub} />, <strong>"{pub.title}"</strong>, <em>{pub.venue}</em>{pubCitation(pub)}.{#if pub.citations && pub.citations > 0}{' '}[cited: {pub.citations}]{/if}</a>{:else}<AuthorList {pub} />, <strong>"{pub.title}"</strong>, <em>{pub.venue}</em>{pubCitation(pub)}.{#if pub.citations && pub.citations > 0}{' '}[cited: {pub.citations}]{/if}{/if}
        </p>
      {/each}
    </div>
  </section>

  <!-- TOTALS + NOTES -->
  <div class="text-right mt-4 mb-2">
    <p>{t.totalCitations}: {totalCitations.toLocaleString()}, {t.hIndex}: {hIndex}</p>
  </div>
  <div class="text-left mt-2" style="padding-left:10mm; padding-right:10mm;">
    <ul style="list-style:disc inside none; padding-left:0;">
      {#if hasCofirst}
        <li><Markdown source={notes[lang][0]} /></li>
      {/if}
      {#if hasCocorrespondence}
        <li><Markdown source={notes[lang][1]} /></li>
      {/if}
      <li><Markdown source={notes[lang][2]} /></li>
    </ul>
  </div>

</article>

<style>
  .no-underline {
    text-decoration: none !important;
  }
  .no-underline:hover {
    color: blue;
  }
</style>
