'use client';

import { useState } from 'react';
import Link from 'next/link';
import styles from './page.module.scss';

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <>
      <section className={styles.hero}>
        <div className={styles.heroInner}>
          <div className={styles.bread}><Link href="/">홈</Link> / <span>문의하기</span></div>
          <h1>문의하기</h1>
          <p>HRM · HRD · AX 컨설팅에 대한 문의사항이 있으시면 언제든 연락해 주세요.</p>
        </div>
      </section>

      <section className={styles.content}>
        <div className="container">
          <div className={styles.grid}>
            {/* Form */}
            <div className={styles.formWrap}>
              <h2>상담 신청</h2>
              <p className={styles.formDesc}>양식을 작성해 주시면, 담당 컨설턴트가 빠르게 연락드리겠습니다.</p>

              {submitted ? (
                <div className={styles.success}>
                  <div className={styles.successIcon}>
                    <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><path d="M8 16L14 22L24 10" stroke="#10B981" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/></svg>
                  </div>
                  <h3>문의가 접수되었습니다</h3>
                  <p>빠른 시일 내에 담당 컨설턴트가 연락드리겠습니다.</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className={styles.form}>
                  <div className={styles.row}>
                    <div className={styles.field}>
                      <label htmlFor="name">성함 <span>*</span></label>
                      <input type="text" id="name" required placeholder="홍길동" />
                    </div>
                    <div className={styles.field}>
                      <label htmlFor="org">소속기관/기업 <span>*</span></label>
                      <input type="text" id="org" required placeholder="소속기관 또는 기업명" />
                    </div>
                  </div>
                  <div className={styles.row}>
                    <div className={styles.field}>
                      <label htmlFor="email">이메일 <span>*</span></label>
                      <input type="email" id="email" required placeholder="example@email.com" />
                    </div>
                    <div className={styles.field}>
                      <label htmlFor="phone">연락처 <span>*</span></label>
                      <input type="tel" id="phone" required placeholder="010-0000-0000" />
                    </div>
                  </div>
                  <div className={styles.field}>
                    <label htmlFor="service">관심 서비스</label>
                    <select id="service" defaultValue="">
                      <option value="" disabled>선택해주세요</option>
                      <option value="hrm">HRM 컨설팅 (직무중심 인적자원관리)</option>
                      <option value="hrd">HRD 컨설팅 (직무·역량·Skill 기반)</option>
                      <option value="ax">AX 컨설팅 (AI Transformation)</option>
                      <option value="multi">복수 서비스</option>
                      <option value="other">기타</option>
                    </select>
                  </div>
                  <div className={styles.field}>
                    <label htmlFor="budget">예상 예산 규모</label>
                    <select id="budget" defaultValue="">
                      <option value="" disabled>선택해주세요</option>
                      <option value="~5000">5,000만원 미만</option>
                      <option value="5000~1억">5,000만원 ~ 1억원</option>
                      <option value="1억~3억">1억원 ~ 3억원</option>
                      <option value="3억+">3억원 이상</option>
                      <option value="undecided">미정</option>
                    </select>
                  </div>
                  <div className={styles.field}>
                    <label htmlFor="msg">문의 내용 <span>*</span></label>
                    <textarea id="msg" rows={5} required placeholder="프로젝트 개요, 기대 일정, 문의사항 등을 자유롭게 작성해주세요" />
                  </div>
                  <button type="submit" className="btn btn-primary btn-lg" style={{ width: '100%' }}>문의 접수하기</button>
                </form>
              )}
            </div>

            {/* Info */}
            <div className={styles.infoWrap}>
              <div className={styles.infoCard}>
                <h3>연락처 정보</h3>
                <div className={styles.infoList}>
                  {[
                    { icon: '📍', label: '주소', value: '서울특별시 (추후 업데이트)' },
                    { icon: '📞', label: '전화', value: '02-0000-0000' },
                    { icon: '✉️', label: '이메일', value: 'info@cnpconsulting.co.kr' },
                    { icon: '🕐', label: '업무시간', value: '월~금 09:00 - 18:00' },
                  ].map(item => (
                    <div key={item.label} className={styles.infoItem}>
                      <div className={styles.infoIcon}>{item.icon}</div>
                      <div>
                        <strong>{item.label}</strong>
                        <p>{item.value}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className={styles.infoCard}>
                <h3>빠른 상담이 필요하신가요?</h3>
                <p className={styles.quickP}>
                  급한 문의는 전화 또는 이메일로 직접 연락해 주세요. 평일 업무시간 내 빠른 응대가 가능합니다.
                </p>
                <a href="tel:02-0000-0000" className="btn btn-dark" style={{ width: '100%' }}>
                  📞 전화 상담하기
                </a>
              </div>

              <div className={styles.trustCard}>
                <div className={styles.trustItem}>
                  <strong>500+</strong>
                  <span>프로젝트 수행</span>
                </div>
                <div className={styles.trustItem}>
                  <strong>98%</strong>
                  <span>고객 만족도</span>
                </div>
                <div className={styles.trustItem}>
                  <strong>15yr+</strong>
                  <span>컨설팅 경력</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
