// Static CV content (everything that is NOT a publication - those come from
// cache/gscache.txt via src/lib/data/publications.ts).

export type CVEntry = {
  period: string;
  lines: string[];
};

export const education: { en: CVEntry[]; ko: CVEntry[] } = {
  en: [
    {
      period: '2016 -2020',
      lines: ['**Dr. rer. nat.** (Ph.D. equivalent) in Biology, Heidelberg University, Germany']
    },
    {
      period: '2012 -2014',
      lines: ['**M.Sc.** in Physics, Seoul National University, Korea']
    },
    {
      period: '2008 -2012',
      lines: ['**B.Sc.** in Physics, Pusan National University, Korea']
    }
  ],
  ko: [
    {
      period: '2016 -2020',
      lines: ['**이학박사 (Dr. rer. nat.)**, 생물학, 하이델베르크 대학교, 독일']
    },
    {
      period: '2012 -2014',
      lines: ['**이학석사 (M.Sc.)**, 물리학, 서울대학교, 대한민국']
    },
    {
      period: '2008 -2012',
      lines: ['**이학사 (B.Sc.)**, 물리학, 부산대학교, 대한민국']
    }
  ]
};

export const experience: { en: CVEntry[]; ko: CVEntry[] } = {
  en: [
    {
      period: '2026 -Present',
      lines: [
        'Associate Professor,',
        '**Department of Biomedical Informatics, School of Medicine, Pusan National University**'
      ]
    },
    {
      period: '2022 -2026',
      lines: [
        'Assistant/Associate Professor,',
        '**Department of Data Science, School of Biomedical Convergence Engineering, Pusan National University**'
      ]
    },
    {
      period: '2020 -2022',
      lines: [
        'Postdoctoral Researcher,',
        '**Division of Computational Genomics and System Genetics, German Cancer Research Center (DKFZ)**',
        '(Advisor: Prof. Oliver Stegle)'
      ]
    },
    {
      period: '2018 -2020',
      lines: [
        'Researcher (PhD student),',
        '**Digital Health Center, Berlin Institute of Health (BIH) / Charité**',
        '(Advisor: Prof. Roland Eils)'
      ]
    },
    {
      period: '2016 -2018',
      lines: [
        'Researcher (PhD student),',
        '**Division of Theoretical Bioinformatics, German Cancer Research Center (DKFZ)**',
        '(Advisor: Prof. Roland Eils)'
      ]
    },
    {
      period: '2015 -2016',
      lines: [
        'Research Collaboration,',
        '**Molecular Genome Engineering Laboratory, Hanyang University**',
        '(Research collaborator: Prof. Sangsu Bae)'
      ]
    },
    {
      period: '2014 -2015',
      lines: [
        'Research Collaboration,',
        '**Genome Engineering Laboratory, Seoul National University**',
        '(Research collaborator: Dr. Sangsu Bae)'
      ]
    },
    {
      period: '2012 -2014',
      lines: [
        'Researcher (MSc student),',
        '**Single Molecule Biophysics Laboratory, Seoul National University**',
        '(Advisor: Prof. Sungchul Hohng)'
      ]
    }
  ],
  ko: [
    {
      period: '2026 -현재',
      lines: ['**부교수**, 생명의료정보학교실, 의과대학, 부산대학교']
    },
    {
      period: '2022 -2026',
      lines: ['**조교수/부교수**, 데이터사이언스전공, 의생명융합공학부, 부산대학교']
    },
    {
      period: '2020 -2022',
      lines: [
        '**박사후 과정 연구원**, Division of Computational Genomics and System Genetics, 독일 암 연구소 (DKFZ)',
        '(지도교수: Prof. Oliver Stegle)'
      ]
    },
    {
      period: '2018 -2020',
      lines: [
        '**박사과정 연구원**, Digital Health Center, Berlin Institute of Health (BIH) 및 샤리테 (Charité) 대학병원',
        '(지도교수: Prof. Roland Eils)'
      ]
    },
    {
      period: '2016 -2018',
      lines: [
        '**박사과정 연구원**, Division of Theoretical Bioinformatics, 독일 암 연구소 (DKFZ)',
        '(지도교수: Prof. Roland Eils)'
      ]
    },
    {
      period: '2015 -2016',
      lines: ['**공동연구**, 분자유전공학연구실, 한양대학교', '(공동연구: 배상수 교수)']
    },
    {
      period: '2014 -2015',
      lines: [
        '**공동연구**, 유전체교정연구단, 서울대학교 및 기초과학연구원 (IBS)',
        '(공동연구: 배상수 박사)'
      ]
    },
    {
      period: '2012 -2014',
      lines: [
        '**석사과정 연구원**, 단분자생물물리연구실, 서울대학교',
        '(지도교수: 홍성철 교수)'
      ]
    }
  ]
};

export type ServiceGroup = { label: string; items: string[] };

export const service: { en: ServiceGroup[]; ko: ServiceGroup[] } = {
  en: [
    {
      label: 'Scientific Community',
      items: [
        'Korean Association for Applied Science Research (KASRA, https://kasra.kr), President, 2026-',
        'Korean Society for Bioinformatics (KSBI), Public Affairs Committee Member, 2023 / Academic Affairs Committee Member, 2024- / Computing Committee Member, 2025-',
        'Korea Genome Organization (KOGO), Information and Computing Committee Member, 2023-2024',
        'Single Cell & Spatial Omics Korea (SCSOK, co-founder), 2023-'
      ]
    },
    {
      label: 'Journal Editor',
      items: [
        'Genomics & Informatics, Associate Editor, 2025-'
      ]
    },
    {
      label: 'Ad-hoc Journal Reviewer',
      items: [
        'Bioinformatics, eLife, Communications Biology, NAR: Genomics and Bioinformatics, Scientific Reports, BMC Genomics, Journal of Open Source Software (JOSS)'
      ]
    },
    {
      label: 'Book Translation',
      items: [
        '**A Byte of Python (Korean Translation)** - An online Python guidebook originally written by Swaroop C H. Free access at https://github.com/pjb7687/byte_of_python/.'
      ]
    },
    {
      label: 'Open Source Contribution',
      items: [
        '**GNU Data Language (GDL)** - Ported GDL (https://github.com/gnudatalanguage/gdl/) on Windows (contributed mainly in 2014-2015). From 2021, serving as release manager of the project.'
      ]
    }
  ],
  ko: [
    {
      label: '대외 활동',
      items: [
        '응용과학연구협회 (KASRA, https://kasra.kr), 회장 (2026 -현재)',
        '한국유전체학회 정보전산위원 (2023 -현재)',
        '한국생명정보학회 대외위원 (2023), 학술위원 (2024 -현재), 전산위원 (2025 -현재)',
        'Single Cell & Spatial Omics Korea (창립멤버, 2023 -현재)'
      ]
    },
    {
      label: '학술지 편집',
      items: [
        'Genomics & Informatics, Associate Editor (2025 -현재)'
      ]
    },
    {
      label: 'Ad-hoc 저널 리뷰어',
      items: [
        'Bioinformatics, eLife, Communications Biology, NAR: Genomics and Bioinformatics, Scientific Reports, BMC Genomics, Journal of Open Source Software (JOSS)'
      ]
    },
    {
      label: '번역',
      items: [
        '**A Byte of Python (한국어 번역)** - 온라인 파이썬 가이드북 (원저자: Swaroop C H). 링크: https://github.com/pjb7687/byte_of_python/'
      ]
    },
    {
      label: '오픈소스 프로젝트',
      items: [
        '**GNU Data Language (GDL)** - GDL 프로젝트 (https://github.com/gnudatalanguage/gdl/) 윈도우 버전 포팅에 기여함 (2014 -2015년). 2021년부터 프로젝트 Release Manager로 기여하고 있음.'
      ]
    }
  ]
};

export const teaching: { en: ServiceGroup[]; ko: ServiceGroup[] } = {
  en: [
    {
      label: 'At PNU',
      items: [
        '**“Bioinformatics”**, **“UNIX Fundamentals”**, **“Introduction to Biomedical Informatics”**, **“Object-oriented Programming”**, **“Web Programming”**, School of Biomedical Convergence Engineering, Pusan National University',
        '**“Statistical Genomics”**, **“Clinical and Genomic Informatics”**, Graduate School of Genomic Data Science, Pusan National University'
      ]
    },
    {
      label: 'Before PNU',
      items: [
        'Invited lecture **“Spatial transcriptomics”** at “Single cell RNA-seq data analysis with R” (sponsored by the **ELIXIR EXCELERATE** project). CSC, Espoo, Finland. 29 May 2019.',
        'Student supervision, 3 student research interns (including 1 co-supervision), Division of Theoretical Bioinformatics, German Cancer Research Center (DKFZ), Germany. Jul 2016 -Feb 2018.',
        '**“Methoden der Bioinformatik -Python”** (lecture assistant), Faculty of Biosciences, Heidelberg University, WS 2016 and WS 2017.',
        '**“Physics Laboratory”** (teaching assistant), Department of Physics, Seoul National University, SS 2012.'
      ]
    }
  ],
  ko: [
    {
      label: '부산대학교',
      items: [
        '**“생명정보학”**, **“정보의학개론/의생명정보학개론”**, **“유닉스 기초”**, **“객체지향프로그래밍/고급프로그래밍”**, **“의생명과학프로그래밍”**, **“웹응용프로그래밍”**, 부산대학교 의생명융합공학부',
        '**“임상및유전체정보학”**, **“유전체통계학”**, **“바이오프로그래밍”**, 부산대학교 대학원 유전체데이터과학전공'
      ]
    },
    {
      label: '부산대학교 이전',
      items: [
        '초청강연 **“Spatial transcriptomics”**, lecture series “Single cell RNA-seq data analysis with R” (**ELIXIR EXCELERATE** 프로젝트). CSC, Espoo, 핀란드. 2019년 5월 29일.',
        '학생 지도, 연구 인턴 3인 지도 (공동지도 1인 포함), Division of Theoretical Bioinformatics, 독일 암 연구소 (DKFZ), 독일. 2016년 7월 -2018년 2월.',
        '**“Methoden der Bioinformatik -Python”** (강의보조), Faculty of Biosciences, 하이델베르크 대학교, WS 2016 및 WS 2017.',
        '**“물리학 실험”**, 물리학과, 서울대학교, SS 2012.'
      ]
    }
  ]
};

export const notes = {
  en: [
    '\\# Joint first authors.',
    '\\* Co-corresponding authors.',
    'Citation counts retrieved from Google Scholar.'
  ],
  ko: [
    '\\# 공동 제1저자.',
    '\\* 공동 교신저자.',
    '인용 수는 Google Scholar에서 가져온 값입니다.'
  ]
};
