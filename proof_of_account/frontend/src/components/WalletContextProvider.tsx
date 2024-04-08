"use client";

import { FC, ReactNode } from "react";
import dynamic from "next/dynamic";

import { SnackbarProvider } from "notistack";
import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react'
import { WalletModalProvider as AntDesignWalletModalProvider } from '@solana/wallet-adapter-ant-design';
import { WalletModalProvider as ReactUIWalletModalProvider } from '@solana/wallet-adapter-react-ui';
const MaterialUIWalletDialogProvider = dynamic(
    async () => (await import("@solana/wallet-adapter-material-ui")).WalletDialogProvider,
    { ssr: false }
  );


import * as web3 from '@solana/web3.js'
import * as wallet from '@solana/wallet-adapter-wallets';
require('@solana/wallet-adapter-react-ui/styles.css')
require('@solana/wallet-adapter-ant-design/styles.css')


const WalletContextProvider: FC<{ children: ReactNode }> = ({ children }) => {

    const wallets = [
        new wallet.AlphaWalletAdapter(),
        new wallet.AvanaWalletAdapter(),
        //new wallet.BitKeepWalletAdapter(),
        new wallet.BitpieWalletAdapter(),
        //new wallet.CensoWalletAdapter(),
        new wallet.CloverWalletAdapter(),
        new wallet.Coin98WalletAdapter(),
        new wallet.CoinbaseWalletAdapter(),
        new wallet.CoinhubWalletAdapter(),
        new wallet.FractalWalletAdapter(),
        new wallet.HuobiWalletAdapter(),
        new wallet.HyperPayWalletAdapter(),
        new wallet.KeystoneWalletAdapter(),
        new wallet.KrystalWalletAdapter(),
        new wallet.LedgerWalletAdapter(),
        new wallet.MathWalletAdapter(),
        new wallet.NekoWalletAdapter(),
        new wallet.NightlyWalletAdapter(),
        new wallet.NufiWalletAdapter(),
        new wallet.OntoWalletAdapter(),
        new wallet.ParticleAdapter(),
        new wallet.PhantomWalletAdapter(),
        new wallet.SafePalWalletAdapter(),
        new wallet.SaifuWalletAdapter(),
        new wallet.SalmonWalletAdapter(),
        new wallet.SkyWalletAdapter(),
        new wallet.SolflareWalletAdapter(),
        new wallet.SolongWalletAdapter(),
        new wallet.SpotWalletAdapter(),
        new wallet.TokenPocketWalletAdapter(),
        new wallet.TokenaryWalletAdapter(),
        new wallet.TorusWalletAdapter(),
        new wallet.TrustWalletAdapter(),
        // new wallet.UnsafeBurnerWalletAdapter(),
        // new wallet.WalletConnectWalletAdapter(),
        new wallet.XDEFIWalletAdapter()
    ]

    const endpoint = web3.clusterApiUrl('devnet')

    return (
        <SnackbarProvider autoHideDuration={3000}>
            <ConnectionProvider endpoint={endpoint}>
                <WalletProvider wallets={wallets}>
                    <MaterialUIWalletDialogProvider>
                        <AntDesignWalletModalProvider>
                            <ReactUIWalletModalProvider>
                                {children}
                            </ReactUIWalletModalProvider>
                        </AntDesignWalletModalProvider>
                    </MaterialUIWalletDialogProvider>
                </WalletProvider>
            </ConnectionProvider>
        </SnackbarProvider>
    )
}

export default WalletContextProvider