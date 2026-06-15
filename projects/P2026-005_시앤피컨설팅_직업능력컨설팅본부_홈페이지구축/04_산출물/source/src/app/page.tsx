'use client';

import { useEffect, useRef } from 'react';
import Link from 'next/link';
import styles from './page.module.scss';

const services = [
  {
    tag: 'HRM',
    color: '#3B82F6',
    icon: '📋',
    title: '직무중심 HRM',
    team: '공공기관컨설팅팀',
    desc: '직무분석·직무분류체계·직무평가·성과관리체계 구축 등 공공기관의 직무중심 인적자원관리를 체계적으로 설계합니다.',
    highlights: ['직무분석 및 직무분류체계 수립', '직무평가 및 직급·보수체계 설계', '성과관리체계 구축', '경영평가 대응 컨설팅'],
    href: '/hrm',
  },
  {
    tag: 'HRD',
    color: '#10B981',
    icon: '🎯',
    title: '직무·역량·Skill 기반 HRD',
    team: 'HR솔루션팀',
    desc: '역량모델링, 교육체계 수립, NCS 기반 교육과정 개발, Skill 기반 인재개발 전략까지 맞춤형 HRD 솔루션을 제공합니다.',
    highlights: ['역량모델링 및 역량평가', '교육체계 수립·교육과정 개발', 'NCS 기반 과정 설계', 'Skill 기반 인재개발'],
    href: '/hrd',
  },
  {
    tag: 'AX',
    color: '#8B5CF6',
    icon: '⚡',
    title: 'AX 컨설팅',
    team: 'AI Transformation',
    desc: 'AI 성숙도 진단, AX 전략수립, Skill Set 구축, AI 워크플로우 재설계, AX 교육훈련까지 조직의 AI 전환을 종합 지원합니다.',
    highlights: ['AX 진단 및 전략수립', 'AX Skill Set 구축', 'AI 활용 워크플로우 재설계', 'AX 교육훈련 설계·운영'],
    href: '/ax-consulting',
  },
];

const stats = [
  { value: '500', suffix: '+', label: '프로젝트 수행' },
  { value: '200', suffix: '+', label: '공공기관 파트너' },
  { value: '15', suffix: 'yr+', label: '컨설팅 경력' },
  { value: '98', suffix: '%', label: '고객 만족도' },
];

const process = [
  { num: '01', title: '진단·분석', desc: '조직 현황 및 이슈 진단' },
  { num: '02', title: '전략 설계', desc: '맞춤형 솔루션 설계' },
  { num: '03', title: '구축·개발', desc: '체계 구축 및 도구 개발' },
  { num: '04', title: '실행·정착', desc: '이행 지원 및 변화관리' },
];

function useInView(ref: React.RefObject<HTMLElement | null>, threshold = 0.15) {
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          el.classList.add('visible');
          observer.disconnect();
        }
      },
      { threshold }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [ref, threshold]);
}

function Section({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  const ref = useRef<HTMLDivElement>(null);
  useInView(ref);
  return <section ref={ref} className={`${styles.section} ${className}`}>{children}</section>;
}

export default function Home() {
  return (
    <>
      {/* ===== HERO ===== */}
      <section className={styles.hero}>
        <div className={styles.heroBg}>
          <div className={styles.gridLines} />
          <div className={styles.orb1} />
          <div className={styles.orb2} />
          <div className={styles.orb3} />
        </div>

        <div className={styles.heroContent}>
          <div className={styles.heroBadge}>
            <span className={styles.badgeDot} />
            Competency & Performance
          </div>

          <h1 className={styles.heroTitle}>
            <span className={styles.heroLine1}>조직과 구성원의</span>
            <span className={styles.heroLine2}>성장을 설계합니다</span>
          </h1>

          <p className={styles.heroDesc}>
            HRM · HRD · AX 컨설팅 전문기관<br />
            시앤피컨설팅 직업능력컨설팅본부
          </p>

          <div className={styles.heroActions}>
            <Link href="/contact" className="btn btn-primary btn-lg">
              상담 문의하기
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
            <Link href="/portfolio" className="btn btn-outline-light btn-lg">
              포트폴리오
            </Link>
          </div>

          <div className={styles.heroStats}>
            {stats.map((s) => (
              <div key={s.label} className={styles.heroStat}>
                <span className={styles.heroStatVal}>{s.value}<span>{s.suffix}</span></span>
                <span className={styles.heroStatLabel}>{s.label}</span>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.heroScroll}>
          <span>Scroll</span>
          <div className={styles.scrollLine} />
        </div>
      </section>

      {/* ===== ABOUT ===== */}
      <Section className={styles.about}>
        <div className="container" id="about">
          <div className={styles.aboutGrid}>
            <div className={styles.aboutLeft}>
              <span className={styles.label}>About</span>
              <h2 className={styles.h2}>
                직업능력컨설팅본부를<br />소개합니다
              </h2>
            </div>
            <div className={styles.aboutRight}>
              <p className={styles.aboutLead}>
                시앤피컨설팅 직업능력컨설팅본부는 공공기관 및 민간기업의
                인적자원관리(HRM), 인적자원개발(HRD), 그리고 AI Transformation(AX) 분야에서
                체계적인 방법론과 풍부한 현장 경험을 바탕으로 맞춤형 솔루션을 제공하는 전문기관입니다.
              </p>
              <p className={styles.aboutBody}>
                경영학 박사, 공인노무사, 경영지도사 등 각 분야 전문가로 구성된 컨설팅 그룹으로,
                직무분석·역량모델링·교육체계 수립·AI 전환 전략까지 조직 성장의 전 과정을 지원합니다.
              </p>
              <div className={styles.aboutFeatures}>
                <div className={styles.aboutFeature}>
                  <div className={styles.featureIcon}>🏛️</div>
                  <div>
                    <strong>공공기관 특화</strong>
                    <span>경영평가 대응 및 공공부문 HRM/HRD 전문</span>
                  </div>
                </div>
                <div className={styles.aboutFeature}>
                  <div className={styles.featureIcon}>🔬</div>
                  <div>
                    <strong>방법론 기반</strong>
                    <span>체계적인 컨설팅 프레임워크와 검증된 도구 활용</span>
                  </div>
                </div>
                <div className={styles.aboutFeature}>
                  <div className={styles.featureIcon}>🤖</div>
                  <div>
                    <strong>AX 선도</strong>
                    <span>HR 전문성 기반 AI Transformation 컨설팅</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </Section>

      {/* ===== SERVICES ===== */}
      <Section className={styles.servicesSec}>
        <div className="container">
          <div className={styles.secHeader}>
            <span className={styles.label}>Services</span>
            <h2 className={styles.h2}>핵심 서비스 영역</h2>
            <p className={styles.secDesc}>
              세 가지 핵심 영역에서 조직의 지속가능한 성장을 설계합니다
            </p>
          </div>

          <div className={styles.serviceGrid}>
            {services.map((svc, i) => (
              <Link href={svc.href} key={svc.tag} className={styles.serviceCard} style={{ '--accent': svc.color, animationDelay: `${i * 0.1}s` } as React.CSSProperties}>
                <div className={styles.cardTop}>
                  <span className={styles.cardIcon}>{svc.icon}</span>
                  <span className={styles.cardTag} style={{ background: `${svc.color}15`, color: svc.color }}>{svc.tag}</span>
                </div>
                <h3 className={styles.cardTitle}>{svc.title}</h3>
                <p className={styles.cardTeam}>{svc.team}</p>
                <p className={styles.cardDesc}>{svc.desc}</p>
                <ul className={styles.cardList}>
                  {svc.highlights.map((h) => (
                    <li key={h}>
                      <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M2.5 7L5.5 10L11.5 4" stroke={svc.color} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
                      {h}
                    </li>
                  ))}
                </ul>
                <div className={styles.cardAction}>
                  자세히 보기
                  <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><path d="M3 8H13M13 8L9 4M13 8L9 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/></svg>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </Section>

      {/* ===== PROCESS ===== */}
      <Section className={styles.processSec}>
        <div className="container">
          <div className={styles.secHeader}>
            <span className={styles.label}>Process</span>
            <h2 className={styles.h2}>컨설팅 수행 프로세스</h2>
          </div>
          <div className={styles.processGrid}>
            {process.map((p, i) => (
              <div key={p.num} className={styles.processCard} style={{ animationDelay: `${i * 0.1}s` }}>
                <span className={styles.processNum}>{p.num}</span>
                <h3>{p.title}</h3>
                <p>{p.desc}</p>
                {i < process.length - 1 && <div className={styles.processArrow}>→</div>}
              </div>
            ))}
          </div>
        </div>
      </Section>

      {/* ===== CTA ===== */}
      <Section className={styles.ctaSec}>
        <div className="container">
          <div className={styles.ctaBox}>
            <div className={styles.ctaOrb} />
            <span className={styles.label}>Get Started</span>
            <h2>프로젝트에 대해<br />상담을 원하시나요?</h2>
            <p>
              HRM · HRD · AX 컨설팅에 대한 문의사항이 있으시면 언제든 연락주세요.<br />
              전문 컨설턴트가 맞춤 상담을 제공합니다.
            </p>
            <div className={styles.ctaActions}>
              <Link href="/contact" className="btn btn-primary btn-lg">무료 상담 신청</Link>
              <a href="tel:02-0000-0000" className="btn btn-outline-light btn-lg">
                📞 02-0000-0000
              </a>
            </div>
          </div>
        </div>
      </Section>
    </>
  );
}
