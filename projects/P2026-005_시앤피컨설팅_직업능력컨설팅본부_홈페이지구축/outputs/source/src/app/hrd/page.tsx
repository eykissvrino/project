import Link from 'next/link';
import type { Metadata } from 'next';
import s from '@/styles/service.module.scss';

export const metadata: Metadata = {
  title: 'HRD 컨설팅 | 직무·역량·Skill 기반 인재개발 — CNP 직업능력컨설팅본부',
  description: '역량모델링, 교육체계 수립, NCS 기반 교육과정 개발, Skill 기반 인재개발 전략',
};

const services = [
  { icon: '🎯', title: '역량모델링 및 역량평가', desc: '핵심·리더십·직무역량을 체계적으로 도출하고, 역량 진단·평가 도구를 개발하여 인재개발의 기반을 마련합니다.' },
  { icon: '📚', title: '교육체계 수립', desc: '조직 전략과 연계된 교육비전·목표를 설정하고, 직급·직무·역량별 맞춤형 교육 로드맵을 수립합니다.' },
  { icon: '📘', title: 'NCS 기반 교육과정 개발', desc: '국가직무능력표준(NCS)을 활용하여 현장 중심 교육과정을 체계적으로 개발하고, 학습모듈 및 평가도구를 설계합니다.' },
  { icon: '💡', title: 'Skill 기반 인재개발', desc: '직무별 Skill을 정의하고, Skill Gap 분석을 통해 개인 맞춤형 학습 경로를 설계하는 차세대 인재개발 전략을 수립합니다.' },
  { icon: '📊', title: '교육효과성 분석', desc: 'Kirkpatrick 4단계 모형 등을 활용하여 교육훈련의 효과성을 체계적으로 측정하고 개선 방안을 도출합니다.' },
  { icon: '🔄', title: '학습경험 설계(LXD)', desc: '학습자 중심의 경험 설계 방법론을 적용하여, 몰입도 높은 교육 프로그램을 설계·개발합니다.' },
];

const steps = [
  { num: 1, title: '요구분석', desc: '조직·직무·학습자 분석' },
  { num: 2, title: '역량도출', desc: '역량모델링·Skill 맵핑' },
  { num: 3, title: '체계설계', desc: '교육체계·로드맵 수립' },
  { num: 4, title: '과정개발', desc: '교육과정·콘텐츠 개발' },
  { num: 5, title: '실행지원', desc: '운영·평가·피드백' },
];

export default function HRDPage() {
  return (
    <>
      <section className={s.pageHero}>
        <div className={s.heroInner}>
          <div className={s.breadcrumb}><Link href="/">홈</Link> / <span>서비스</span> / <span>HRD</span></div>
          <span className={`${s.heroTag} ${s.heroTagGreen}`}>HR솔루션팀</span>
          <h1 className={s.heroTitle}>직무·역량·Skill 기반<br />HRD 컨설팅</h1>
          <p className={s.heroDesc}>역량모델링, 교육체계 수립, NCS 기반 교육과정 개발부터 Skill 기반 인재개발 전략까지, 조직 맞춤형 HRD 솔루션을 제공합니다.</p>
        </div>
      </section>

      <section className={s.sectionDark}>
        <div className="container">
          <div className={s.secHeader}><span className={s.label}>Services</span><h2 className={s.secTitle}>주요 서비스</h2><p className={s.secDesc}>조직의 인재개발 역량을 한 단계 높이는 종합 HRD 컨설팅 서비스입니다.</p></div>
          <div className={s.grid3}>
            {services.map((svc) => (
              <div key={svc.title} className={s.card}>
                <div className={`${s.cardIcon} ${s.cardIconGreen}`}>{svc.icon}</div>
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
            {[{v:'200+',l:'교육체계 수립'},{v:'500+',l:'교육과정 개발'},{v:'100+',l:'역량모델링 수행'},{v:'95%',l:'교육 만족도'}].map(r=>(
              <div key={r.l} className={s.resultCard}><div className={s.resultValue}>{r.v}</div><div className={s.resultLabel}>{r.l}</div></div>
            ))}
          </div>
        </div>
      </section>

      <section className={s.cta}>
        <div className="container">
          <div className={s.ctaBox}>
            <h2>HRD 컨설팅이 필요하신가요?</h2>
            <p>역량모델링, 교육체계, Skill 기반 인재개발 등에 대한 상담을 제공합니다.</p>
            <Link href="/contact" className="btn btn-primary btn-lg">상담 문의하기</Link>
          </div>
        </div>
      </section>
    </>
  );
}
