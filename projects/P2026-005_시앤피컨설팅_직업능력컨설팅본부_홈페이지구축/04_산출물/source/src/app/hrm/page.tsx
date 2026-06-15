import Link from 'next/link';
import type { Metadata } from 'next';
import s from '@/styles/service.module.scss';

export const metadata: Metadata = {
  title: 'HRM 컨설팅 | 직무중심 인적자원관리 — CNP 직업능력컨설팅본부',
  description: '직무분석, 직무분류체계, 직무평가, 성과관리체계 구축 등 공공기관 직무중심 HRM 컨설팅',
};

const services = [
  { icon: '📊', title: '직무분석 및 직무분류체계 수립', desc: '조직의 미션·기능·업무를 체계적으로 분석하여 직무분류체계를 수립하고, 표준화된 직무기술서를 작성합니다.' },
  { icon: '📝', title: '직무기술서(JD) 작성', desc: '직무별 책임, 수행업무, 필요역량 등을 명확히 정의하여 채용·평가·보상의 기반이 되는 직무기술서를 작성합니다.' },
  { icon: '⚖️', title: '직무평가 및 직급체계 설계', desc: '직무의 상대적 가치를 객관적으로 평가하고, 이를 기반으로 합리적인 직급·보수체계를 설계합니다.' },
  { icon: '🎯', title: '성과관리체계 구축', desc: '조직 목표와 연계된 성과지표(KPI)를 설정하고, 공정하고 투명한 성과관리 프로세스를 구축합니다.' },
  { icon: '🏛️', title: '공공기관 경영평가 대응', desc: '인사 분야 경영평가 지표에 대한 체계적인 대응 전략을 수립하고 실행을 지원합니다.' },
  { icon: '📋', title: '정원산정 및 인력운영 진단', desc: '적정 인력 규모를 산정하고, 인력의 효율적 배치·운영 방안을 제시합니다.' },
];

const steps = [
  { num: 1, title: '현황진단', desc: '조직·인사 현황 분석' },
  { num: 2, title: '직무분석', desc: '기능·업무 체계 분석' },
  { num: 3, title: '체계설계', desc: '분류·직급체계 설계' },
  { num: 4, title: '평가구축', desc: '직무평가·성과관리' },
  { num: 5, title: '이행지원', desc: '제도 정착·교육' },
];

export default function HRMPage() {
  return (
    <>
      <section className={s.pageHero}>
        <div className={s.heroInner}>
          <div className={s.breadcrumb}><Link href="/">홈</Link> / <span>서비스</span> / <span>HRM</span></div>
          <span className={`${s.heroTag} ${s.heroTagBlue}`}>공공기관컨설팅팀</span>
          <h1 className={s.heroTitle}>직무중심 HRM 컨설팅</h1>
          <p className={s.heroDesc}>공공기관의 직무중심 인적자원관리체계를 체계적으로 수립하여, 조직의 효율성과 공정성을 높이는 맞춤형 HRM 솔루션을 제공합니다.</p>
        </div>
      </section>

      <section className={s.sectionDark}>
        <div className="container">
          <div className={s.secHeader}><span className={s.label}>Services</span><h2 className={s.secTitle}>주요 서비스</h2><p className={s.secDesc}>공공기관 인사관리 혁신을 위한 종합 HRM 컨설팅 서비스입니다.</p></div>
          <div className={s.grid3}>
            {services.map((svc) => (
              <div key={svc.title} className={s.card}>
                <div className={`${s.cardIcon} ${s.cardIconBlue}`}>{svc.icon}</div>
                <h3>{svc.title}</h3><p>{svc.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className={s.section}>
        <div className="container">
          <div className={s.secHeader}><span className={s.label}>Process</span><h2 className={s.secTitle}>컨설팅 수행 프로세스</h2></div>
          <div className={s.process}>
            {steps.map((step) => (
              <div key={step.num} className={s.processStep}>
                <div className={s.processNum}>{step.num}</div>
                <div className={s.processTitle}>{step.title}</div>
                <div className={s.processDesc}>{step.desc}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className={s.sectionDark}>
        <div className="container">
          <div className={s.secHeader}><span className={s.label}>Results</span><h2 className={s.secTitle}>주요 성과</h2></div>
          <div className={s.resultGrid}>
            {[{v:'300+',l:'공공기관 컨설팅'},{v:'150+',l:'직무분석 프로젝트'},{v:'100+',l:'성과관리체계 구축'},{v:'97%',l:'고객 재계약률'}].map(r=>(
              <div key={r.l} className={s.resultCard}><div className={s.resultValue}>{r.v}</div><div className={s.resultLabel}>{r.l}</div></div>
            ))}
          </div>
        </div>
      </section>

      <section className={s.cta}>
        <div className="container">
          <div className={s.ctaBox}>
            <h2>HRM 컨설팅이 필요하신가요?</h2>
            <p>직무분석, 직급체계, 성과관리 등 HRM 전 분야에 대한 상담을 제공합니다.</p>
            <Link href="/contact" className="btn btn-primary btn-lg">상담 문의하기</Link>
          </div>
        </div>
      </section>
    </>
  );
}
