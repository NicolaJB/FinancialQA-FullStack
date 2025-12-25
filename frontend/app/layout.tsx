import './globals.css';
import { ReactNode } from 'react';

export const metadata = {
  title: 'Financial QA',
  description: 'Ask questions about financial documents',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main className="container mx-auto p-4">{children}</main>
      </body>
    </html>
  );
}
