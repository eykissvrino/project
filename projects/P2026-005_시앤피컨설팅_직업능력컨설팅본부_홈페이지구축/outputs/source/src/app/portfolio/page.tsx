'use client';

import { useState } from 'react';
import Link from 'next/link';
import styles from './page.module.scss';

const categories = ['전체', 'HRM', 'HRD', 'AX'];

const projects = [
  { cat: 'HRM', year: '2025', client: 'A 공공기관', title: '직무분석 및 직무분류체계 수립', desc: '전 직무 대상 직무분석 실시 및 직무분류체계·직무기술서 수립', status: '완료' },
  { cat: 'HRM', year: '2025', client: 'B 공기업', title: '성과관리체계 고도화 컨설팅', desc: '전략 연계형 BSC 기반 성과관리체계 재설계 및 KPI 체계 수립', status: '완료' },
  { cat: 'HRM', year: '2024', client: 'C 지방공기업', title: '직무급 보수체계 설계', desc: '직무평가 기반 직무등급 설정 및 직무급 보수체계 설계', status: '완료' },
  { cat: 'HRM', year: '2024', client: 'D 공공기관', title: '정원산정 및 인력운영 컨설팅', desc: '적정 인력 규모 산정 및 부서별 인력 재배치 방안 수립', status: '완료' },
  { cat: 'HRD', year: '2025', client: 'E 공공기관', title: '역량모델링 및 교육체계 수립', desc: '핵심·리더십·직무역량 모델링 및 직급·직무별 교육로드맵 수립', status: '완료' },
  { cat: 'HRD', year: '2024', client: 'F 공기업', title: 'NCS 기반 교육과정 개발', desc: 'NCS 활용 현장 중심 교육과정 10개 개발 및 학습모듈 설계', status: '완료' },
  { cat: 'HRD', year: '2024', client: 'G 민간기업', title: 'Skill 기반 인재개발 전략 수립', desc: '직무별 Skill Map 구축 및 개인 맞춤형 학습경로 설계', status: '완료' },
  { cat: 'HRD', year: '2025', client: 'H 공공기관', title: '교육효과성 분석 및 체계 개선', desc: 'Kirkpatrick 모형 기반 교육효과성 측정 및 개선 방안 도출', status: '진행중' },
  { cat: 'AX', year: '2025', client: 'I 공공기관', title: 'AX 진단 및 전략수립', desc: '조직 AI 성숙도 진단 및 단계별 AX 추진 로드맵 수립', status: '완료' },
  { cat: 'AX', year: '2025', client: 'J 공기업', title: 'AI 활용 워크플로우 재설계', desc: '주요 업무 프로세스 AI 관점 재설계 및 자동화 방안 도출', status: '진행중' },
  { cat: 'AX', year: '2024', client: 'K 지방공기업', title: 'AX Skill Set 구축 및 교육훈련', desc: '직무별 AI Skill Set 정의 및 맞춤형 AX 교육 프로그램 운영', status: '완료' },
  { cat: 'AX', year: '2025', client: 'L 민간기업', title: 'AI 리터러시 교육체계 설계', desc: '전사 대상 AI 리터러시 진단 및 수준별 교육체계 설계', status: '완료' },
];

const colorMap: Record<string, string> = { HRM: '#3B82F6', HRD: '#10B981', AX: '#8B5CF6' };

export default function PortfolioPage() {
  const [active, setActive] = useState('전체');
  const filtered = active === '전체' ? projects : projects.filter(p => p.cat === active);

  return (
    <>
      <section className={styles.hero}>
        <div className={styles.heroInner}>
          <div className={styles.bread}><Link href="/">홈</Link> / <span>포트폴리오</span></div>
          <h1>포트폴리오 &amp; 실적</h1>
          <p>시앤피컨설팅 직업능력컨설팅본부의 주요 프로젝트 수행 실적입니다.</p>
        </div>
      </section>

      <section className={styles.content}>
        <div className="container">
          <div className={styles.toolbar}>
            <div className={styles.filters}>
              {categories.map(cat => (
                <button key={cat} className={`${styles.filterBtn} ${active === cat ? styles.active : ''}`} onClick={() => setActive(cat)}>
                  {cat}
                  {cat !== '전체' && <span className={styles.count}>{projects.filter(p => p.cat === cat).length}</span>}
                </button>
              ))}
            </div>
            <span className={styles.total}>{filtered.length}건</span>
          </div>

          <div className={styles.grid}>
            {filtered.map((p, i) => (
              <div key={i} className={styles.card}>
                <div className={styles.cardHead}>
                  <span className={styles.badge} style={{ background: `${colorMap[p.cat]}12`, color: colorMap[p.cat] }}>{p.cat}</span>
                  <div className={styles.meta}>
                    {p.status === '진행중' && <span className={styles.statusLive}>진행중</span>}
                    <span className={styles.year}>{p.year}</span>
                  </div>
                </div>
                <h3>{p.title}</h3>
                <p className={styles.client}>{p.client}</p>
                <p className={styles.desc}>{p.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className={styles.cta}>
        <div className="container">
          <div className={styles.ctaBox}>
            <h2>유사한 프로젝트를 계획 중이신가요?</h2>
            <p>풍부한 경험을 바탕으로 최적의 솔루션을 제안해 드리겠습니다.</p>
            <Link href="/contact" className="btn btn-primary btn-lg">프로젝트 상담하기</Link>
          </div>
        </div>
      </section>
    </>
  );
}
