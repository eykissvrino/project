import type { Metadata } from 'next';
import '@/styles/globals.scss';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export const metadata: Metadata = {
  title: '시앤피컨설팅 직업능력컨설팅본부',
  description: 'HRM, HRD, AX 컨설팅 전문기관 - 시앤피컨설팅 직업능력컨설팅본부',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
