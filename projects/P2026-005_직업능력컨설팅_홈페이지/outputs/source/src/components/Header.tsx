'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import styles from './Header.module.scss';

const navItems = [
  { label: '본부소개', href: '/#about' },
  {
    label: '서비스',
    children: [
      { label: 'HRM 컨설팅', desc: '직무중심 인적자원관리', href: '/hrm', icon: '📋' },
      { label: 'HRD 컨설팅', desc: '직무·역량·Skill 기반 인재개발', href: '/hrd', icon: '🎯' },
      { label: 'AX 컨설팅', desc: 'AI Transformation', href: '/ax-consulting', icon: '⚡' },
    ],
  },
  { label: '포트폴리오', href: '/portfolio' },
  { label: '문의하기', href: '/contact' },
];

export default function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [dropOpen, setDropOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', onScroll);
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? 'hidden' : '';
    return () => { document.body.style.overflow = ''; };
  }, [mobileOpen]);

  return (
    <header className={`${styles.header} ${scrolled ? styles.scrolled : ''}`}>
      <div className={styles.inner}>
        <Link href="/" className={styles.logo} onClick={() => setMobileOpen(false)}>
          <div className={styles.logoMark}>C&amp;P</div>
          <div className={styles.logoText}>
            <span className={styles.logoSub}>CNP CONSULTING</span>
            <span className={styles.logoMain}>직업능력컨설팅본부</span>
          </div>
        </Link>

        <nav className={`${styles.nav} ${mobileOpen ? styles.open : ''}`}>
          {navItems.map((item) =>
            item.children ? (
              <div
                key={item.label}
                className={styles.dropdown}
                onMouseEnter={() => setDropOpen(true)}
                onMouseLeave={() => setDropOpen(false)}
              >
                <button className={styles.navLink} onClick={() => setDropOpen(!dropOpen)}>
                  {item.label}
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none" className={`${styles.chevron} ${dropOpen ? styles.chevronOpen : ''}`}>
                    <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </button>
                <div className={`${styles.mega} ${dropOpen ? styles.megaOpen : ''}`}>
                  <div className={styles.megaInner}>
                    <div className={styles.megaLabel}>서비스 영역</div>
                    <div className={styles.megaGrid}>
                      {item.children.map((child) => (
                        <Link
                          key={child.href}
                          href={child.href}
                          className={styles.megaCard}
                          onClick={() => { setMobileOpen(false); setDropOpen(false); }}
                        >
                          <span className={styles.megaIcon}>{child.icon}</span>
                          <div>
                            <strong>{child.label}</strong>
                            <span>{child.desc}</span>
                          </div>
                          <svg className={styles.megaArrow} width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <path d="M6 4L10 8L6 12" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                          </svg>
                        </Link>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <Link
                key={item.label}
                href={item.href!}
                className={styles.navLink}
                onClick={() => setMobileOpen(false)}
              >
                {item.label}
              </Link>
            )
          )}
          <Link href="/contact" className={styles.cta} onClick={() => setMobileOpen(false)}>
            상담 문의
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M3 7H11M11 7L7.5 3.5M11 7L7.5 10.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
        </nav>

        <button
          className={`${styles.burger} ${mobileOpen ? styles.burgerOpen : ''}`}
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="메뉴"
        >
          <span /><span /><span />
        </button>
      </div>
    </header>
  );
}
