import { Button } from '@mui/material';
import { ed25519 } from '@noble/curves/ed25519';
import { useWallet } from '@solana/wallet-adapter-react';
import bs58 from 'bs58';
import type { FC } from 'react';
import React, { useCallback } from 'react';
import { useNotify } from './notify';

interface SignMessageProps {
    defaultText: string;
}

export const SignMessage: FC<SignMessageProps> = ({ defaultText }) => {
    const { publicKey, signMessage } = useWallet();
    const notify = useNotify();

    const onClick = useCallback(async () => {
        try {
            if (!publicKey) throw new Error('Wallet not connected!');
            if (!signMessage) throw new Error('Wallet does not support message signing!');

            const message = new TextEncoder().encode(defaultText); 
            const signature = await signMessage(message);

            const response = await fetch(`${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/verify-signature`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    signature: bs58.encode(signature),
                    message: bs58.encode(message),
                    publicKey: bs58.encode(publicKey.toBytes()),
                    userId: defaultText
                }),
            });
            const data = await response.json();
            console.log(data)
            if (!data.valid) throw new Error('Message signature invalid!');
            notify('success', `Message signature: ${bs58.encode(signature)}`);
        } catch (error: any) {
            notify('error', `Sign Message failed: ${error?.message}`);
        }
    }, [publicKey, signMessage, notify, defaultText]);

    return (
        <div>
            <Button variant="contained" color="secondary" onClick={onClick} disabled={!publicKey || !signMessage}>
                Sign Message
            </Button>
        </div>
    );
};

export default SignMessage;