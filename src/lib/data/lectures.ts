export type Lecture = {
  /** Korean title. Many slides are Korean-only -that's authentic. */
  title: string;
  /** External slide-deck URL (Google Slides / Drive). Undefined for unavailable lectures. */
  url?: string;
  /** Free-form note for items without a deck. */
  note?: string;
};

export type LectureSeries = {
  code: string;
  titleKo: string;
  titleEn: string;
  lectures: Lecture[];
  exam?: { label: string; url: string };
};

export const series: LectureSeries[] = [
  {
    code: 'BMI-101',
    titleKo: '의생명정보학개론',
    titleEn: 'Introduction to Biomedical Informatics',
    lectures: [
      {
        title: '오리엔테이션 (Orientation)',
        url: 'https://docs.google.com/presentation/d/1ZN-UxYrO9MvL-Z5ldtig_DOCzgtWXrRVLDHY8gvWrlY/edit?usp=sharing'
      },
      {
        title: '리눅스 계정 생성 및 실습',
        note: '서버 보안상 공개가 어려우니 양해 바랍니다.'
      },
      {
        title: '의생명정보학 개괄 (Overview of Biomedical Informatics)',
        url: 'https://docs.google.com/presentation/d/1cnqKZyUEkbq-pE3xZ1M5H_WMhms_xug_HpDEdiV0oCY/edit?usp=sharing'
      },
      {
        title: '생명정보학 (Bioinformatics)',
        url: 'https://docs.google.com/presentation/d/1Q8Lh7JZVG8Kgcs9SKauAWlLUAUJTkjl2_EHQ6y44Buc/edit?usp=sharing'
      },
      {
        title: '진화와 암 (Evolution and Cancer)',
        url: 'https://docs.google.com/presentation/d/1Wc0Zotv10s_WIBpthTrc2WJyzkKHzGfgMPOsMG-IVr0/edit#slide=id.g1dfc3155288_0_294'
      },
      {
        title: '유전질환과 GWAS, 약물 디자인, 인공지능',
        url: 'https://docs.google.com/presentation/d/1LJC-UEhoZxzu6tU-0mzj8ptL7RVtqEqfFieDoHRvPpU/edit?usp=sharing'
      },
      {
        title: '무작위대조시험과 멘델리안무작위분석, 역학, 데이터 보안, 원격의료',
        url: 'https://docs.google.com/presentation/d/1P0Nf6AMu-TIBewHqckBkdIS8yjqrGB5JBqwuyZXOseo/edit?usp=sharing'
      }
    ],
    exam: {
      label: '기말고사',
      url: 'https://drive.google.com/file/d/1rYlTTSCBhzFsauf-JxNGoG18bT1f0Lu6/view?usp=drive_link'
    }
  },
  {
    code: 'BIO-201',
    titleKo: '생명정보학',
    titleEn: 'Bioinformatics',
    lectures: [
      {
        title: '오리엔테이션 (Orientation), 리눅스 -이론',
        url: 'https://docs.google.com/presentation/d/1Bc9m8966uMQnEhzCPz7ro5B1owHjCjB0qsbA8quvCY0/edit?usp=sharing'
      },
      {
        title: '리눅스 -실습',
        url: 'https://docs.google.com/presentation/d/1xLQohcQvXO95HoCDHQNBsU9YroRH5Kjdjq67Y-xzax0/edit?usp=sharing'
      },
      {
        title: '유전체 분석 1 -이론',
        url: 'https://docs.google.com/presentation/d/1_irtxngX8C1MY6pZ83wQAqbOZzGauBdD3aKCgRiVQQ8/edit?usp=sharing'
      },
      {
        title: '유전체 분석 1 -실습',
        url: 'https://docs.google.com/presentation/d/1Nqtd227EQcHx-ds9arjcHhquo6NC1o1JmHiwXyn-1T4/edit?usp=sharing'
      },
      {
        title: '유전체 분석 2 -이론',
        url: 'https://docs.google.com/presentation/d/1UlG5dAQyv2Kz8AQxjbGyuacLLlo6mOKRkne7xZj8q6Y/edit?usp=sharing'
      },
      {
        title: '유전체 분석 2 -실습',
        url: 'https://docs.google.com/presentation/d/19LpNMIF6h1_XFKBlg241qfXz5x9yMVuywrTAGywSGk8/edit?usp=sharing'
      },
      {
        title: '유전체 분석 3 -이론',
        url: 'https://docs.google.com/presentation/d/1RhIU_mA_QUquTTR9hke6l47McqLzllCMkkEk9n2Yxvs/edit?usp=sharing'
      },
      {
        title: '유전체 분석 3 -실습',
        url: 'https://docs.google.com/presentation/d/1a7WkO_rKBlEgSsiN4okBcdzyMUaoIWlBoZmmCNdhkxQ/edit?usp=sharing'
      },
      {
        title: '유전체 분석 4 -이론 및 실습',
        url: 'https://docs.google.com/presentation/d/1hbgiUMoy1r8vi9euD-t-QNfRF3gOY1LZflJ6B0EuyDo/edit?usp=sharing'
      },
      {
        title: '유전체 분석 5 -이론 및 실습',
        url: 'https://docs.google.com/presentation/d/1krjq2MXzRDX06RaV627AnzAO5ratppcX8BOJv58MoVU/edit?usp=sharing'
      },
      {
        title: '유전체 분석 6 -실습',
        url: 'https://docs.google.com/presentation/d/19cew70qzAAbRnL71hdSXyJHlxxdTVbAuJU-P7yxDY64/edit?usp=sharing'
      },
      {
        title: '유전체 분석 7 -실습',
        url: 'https://docs.google.com/presentation/d/1RvkjSrVJGqKJrsRo8IRfpdI4KS-kc4fUX8Ybq5VBaxI/edit?usp=sharing'
      }
    ],
    exam: {
      label: '중간고사',
      url: 'https://docs.google.com/document/d/1lB-0GLVQnsgEyvfkzVG-WBfT_c_Qri0ljVeW7t2u4Ig/edit?usp=sharing'
    }
  }
];
