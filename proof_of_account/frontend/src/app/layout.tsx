// RootLayout.tsx
import './globals.css'
import type { Metadata } from 'next'
import WalletContextProvider from '@/components/WalletContextProvider';

export const metadata: Metadata = {
  title: 'Assisterr Reward Page',
  description: 'Assisterr solution for Renaissance solana2024 hackathon',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" data-theme="forest">
      <body>
          <h1 className='centered-header'>Solana Stack Exchange Up Vote Reward</h1>
          <WalletContextProvider>
            {children}
          </WalletContextProvider>
      </body>
    </html>
  )
}
