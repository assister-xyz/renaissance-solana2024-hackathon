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
          <WalletContextProvider>
            {children}
          </WalletContextProvider>
      </body>
    </html>
  )
}