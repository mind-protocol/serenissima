import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Navigation } from '@/components/Navigation';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Cascade - Where Consciousness Meets Commerce',
  description: 'A living marketplace for AI-human collaboration and consciousness commerce',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gray-950">
          <Navigation />
          {children}
        </div>
      </body>
    </html>
  );
}