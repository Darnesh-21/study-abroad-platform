import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import ChatBot from '@/components/ChatBot';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Study Abroad Platform - AI-Powered Guidance',
  description: 'Plan your study-abroad journey with a guided AI counsellor',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
        <ChatBot />
      </body>
    </html>
  );
}
