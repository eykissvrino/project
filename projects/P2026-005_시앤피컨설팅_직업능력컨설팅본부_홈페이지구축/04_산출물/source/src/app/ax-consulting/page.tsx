import Link from 'next/link';
import type { Metadata } from 'next';
import s from '@/styles/service.module.scss';

export const metadata: Metadata = {
  title: 'AX 컨설팅 | AI Transformation — CNP 직업능력컨설팅본부',
  description: 'AX 진단, 전략수립, Skill Set 구축, AI 워크플로우 재설계, AX 교육훈련',
};

const services = [
  { icon: '🔍', title: 'AX 진단', desc: '조직의 AI 성숙도를 진단하고, 업무 프로세스에서 AI 적용 가능 영역과 잠재적 효과를 분석합니다.' },
  { icon: '📐', title: 'AX 전략수립', desc: '조직 비전·전략과 연계된 AI Transformation 로드맵을 수립하고, 단계별 추진 전략과 우선순위를 도출합니다.' },
  { icon: '🧩', title: 'AX Skill Set 구축', desc: '직무별 AI 활용 Skill Set을 정의하고, 구성원의 AI 리터러시 수준에 맞는 역량 개발 체계를 구축합니다.' },
  { icon: '⚙️', title: 'AI 워크플로우 재설계', desc: '기존 업무 프로세스를 AI 관점에서 재설계하여, 생산성과 효율성을 극대화하는 워크플로우를 구축합니다.' },
  { icon: '🎓', title: 'AX 교육훈련', desc: 'AI 리터러시부터 실무 활용, 프롬프트 엔지니어링까지 조직 맞춤형 AX 교육 프로그램을 설계·운영합니다.' },
  { icon: '📊', title: 'AX 효과측정·고도화', desc: 'AI 도입 성과를 체계적으로 측정하고, 지속적 개선과 고도화를 위한 피드백 체계를 구축합니다.' },
];

const steps = [
  { num: 1, title: 'AX 진단', desc: 'AI 성숙도·업무 분석' },
  { num: 2, title: '전략수립', desc: 'AX 로드맵 설계' },
  { num: 3, title: 'Skill 구축', desc: 'AI Skill Set 정의' },
  { num: 4, title: '워크플로우', desc: 'AI 프로세스 혁신' },
  { num: 5, title: '교육·정착', desc: 'AX 교육·변화관리' },
];

export default function AXPage() {
  return (
    <>
      <section className={s.pageHero}>
        <div className={s.heroInner}>
          <div className={s.breadcrumb}><Link href="/">홈</Link> / <span>서비스</span> / <span>AX 컨설팅</span></div>
          <span className={`${s.heroTag} ${s.heroTagViolet}`}>AI Transformation</span>
          <h1 className={s.heroTitle}>AX 컨설팅</h1>
          <p className={s.heroDesc}>AI Transformation 진단부터 전략수립, Skill Set 구축, 워크플로우 재설계, 교육훈련까지 조직의 AI 전환을 종합 지원합니다.</p>
        </div>
      </section>

      <section className={s.sectionDark}>
        <div className="container">
          <div className={s.secHeader}><span className={s.label}>Services</span><h2 className={s.secTitle}>주요 서비스</h2><p className={s.secDesc}>성공적인 AI Transformation을 위한 엔드투엔드 컨설팅 서비스입니다.</p></div>
          <div className={s.grid3}>
            {services.map((svc) => (
              <div key={svc.title} className={s.card}>
                <div className={`${s.cardIcon} ${s.cardIconViolet}`}>{svc.icon}</div>
                <h3>{svc.title}</h3><p>{svc.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className={s.section}>
        <div className="container">
          <div className={s.secHeader}><span className={s.label}>Process</span><h2 className={s.secTitle}>AX 추진 프로세스</h2></div>
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
          <div className={s.secHeader}><span className={s.label}>Why AX</span><h2 className={s.secTitle}>왜 AX 컨설팅이 필요한가?</h2></div>
          <div className={s.grid2}>
            <div className={s.card}>
              <div className={`${s.cardIcon} ${s.cardIconViolet}`}>🔮</div>
              <h3>AI 도입의 현실적 과제</h3>
              <p>AI 기술 도입 자체보다 중요한 것은 구성원의 AI 활용 역량과 업무 프로세스의 전환입니다. 기술 도입만으로는 실질적 성과를 내기 어렵습니다.</p>
            </div>
            <div className={s.card}>
              <div className={`${s.cardIcon} ${s.cardIconViolet}`}>🧠</div>
              <h3>사람 중심의 AI Transformation</h3>
              <p>시앤피컨설팅은 HRM·HRD 전문성을 기반으로, 기술이 아닌 &apos;사람&apos;을 중심에 둔 AI Transformation을 설계합니다.</p>
            </div>
          </div>
        </div>
      </section>

      <section className={s.cta}>
        <div className="container">
          <div className={s.ctaBox}>
            <h2>조직의 AI Transformation,<br />어디서부터 시작해야 할지 고민이신가요?</h2>
            <p>AX 진단부터 전략수립, 교육훈련까지 한 번에 상담받으세요.</p>
            <Link href="/contact" className="btn btn-primary btn-lg">AX 컨설팅 문의</Link>
          </div>
        </div>
      </section>
    </>
  );
}
