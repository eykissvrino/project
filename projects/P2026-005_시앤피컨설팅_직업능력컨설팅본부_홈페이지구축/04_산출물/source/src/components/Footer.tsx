import Link from 'next/link';
import styles from './Footer.module.scss';

const footerLinks = {
  services: [
    { label: 'HRM 컨설팅', href: '/hrm' },
    { label: 'HRD 컨설팅', href: '/hrd' },
    { label: 'AX 컨설팅', href: '/ax-consulting' },
  ],
  company: [
    { label: '본부 소개', href: '/#about' },
    { label: '포트폴리오', href: '/portfolio' },
    { label: '문의하기', href: '/contact' },
  ],
};

export default function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        {/* Top */}
        <div className={styles.top}>
          <div className={styles.brand}>
            <Link href="/" className={styles.logo}>
              <div className={styles.logoMark}>C&amp;P</div>
              <div>
                <span className={styles.logoSub}>CNP CONSULTING</span>
                <span className={styles.logoMain}>직업능력컨설팅본부</span>
              </div>
            </Link>
            <p className={styles.tagline}>
              Competency &amp; Performance — HRM · HRD · AX 컨설팅 전문기관으로서
              조직과 구성원의 성장을 함께 설계합니다.
            </p>
          </div>

          <div className={styles.links}>
            <div className={styles.col}>
              <h4>서비스</h4>
              {footerLinks.services.map((link) => (
                <Link key={link.href} href={link.href}>{link.label}</Link>
              ))}
            </div>
            <div className={styles.col}>
              <h4>바로가기</h4>
              {footerLinks.company.map((link) => (
                <Link key={link.href} href={link.href}>{link.label}</Link>
              ))}
              <a href="https://www.cnp.re.kr" target="_blank" rel="noopener noreferrer">시앤피컨설팅 그룹 →</a>
            </div>
            <div className={styles.col}>
              <h4>연락처</h4>
              <span>서울특별시 (추후 업데이트)</span>
              <span>Tel. 02-0000-0000</span>
              <span>info@cnpconsulting.co.kr</span>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className={styles.bottom}>
          <p>© 2026 시앤피컨설팅 직업능력컨설팅본부. All rights reserved.</p>
          <div className={styles.bottomLinks}>
            <a href="#">개인정보처리방침</a>
            <a href="#">이용약관</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
