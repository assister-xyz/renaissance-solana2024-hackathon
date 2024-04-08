import React, { useState, ChangeEvent } from 'react';
import axios, { AxiosError } from 'axios'; // Import AxiosError for type declaration
import { SignTransaction } from "@/components/SignTransaction";
import { SignMessage } from "@/components/SignMessage";
import { SignIn } from "@/components/SignIn";
import dynamic from "next/dynamic";

const ReactConnectButton = dynamic(
  async () => (await import("@solana/wallet-adapter-react-ui")).WalletConnectButton,
  { ssr: false }
);
const ReactDisconnectButton = dynamic(
  async () => (await import("@solana/wallet-adapter-react-ui")).WalletDisconnectButton,
  { ssr: false }
);
const ReactDialogButton = dynamic(
  async () => (await import("@solana/wallet-adapter-react-ui")).WalletModalButton,
  { ssr: false }
);
const ReactMultiButton = dynamic(
  async () => (await import("@solana/wallet-adapter-react-ui")).WalletMultiButton,
  { ssr: false }
);

import './StackOverflowLinkVerifier.css';

interface StackOverflowLinkVerifierProps {}

const StackOverflowLinkVerifier: React.FC<StackOverflowLinkVerifierProps> = () => {
  const [link, setLink] = useState<string>('');
  const [isValid, setIsValid] = useState<boolean>(false);
  const [locked, setLocked] = useState<boolean>(false);
  const [code, setCode] = useState<string>('');
  const [verificationResult, setVerificationResult] = useState<string | null>(null);
  const [totalUpvotes, setTotalUpvotes] = useState<number | null>(null);
  const [signedMessage, setSignedMessage] = useState<string>('');

  const handleSignMessage = (message: string) => {
    setSignedMessage(message);
  };

  const isSolanaStackExchangeLink = (link: string): boolean => {
    const regex = /^https:\/\/solana\.stackexchange\.com\/users\/(\d+)(\/[-_a-zA-Z0-9]+)?$/;
    return regex.test(link);
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setLink(value);
    setIsValid(isSolanaStackExchangeLink(value));
  };

  const handleLock = () => {
    if (isValid) {
      setLocked(true);
      const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
      let result = '';
      for (let i = 0; i < 20; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
      }
      setCode(result);
    }
  };

  const handleUnlock = () => {
    setLocked(false);
    setCode('');
    setVerificationResult(null);
  };

  const handleVerifyStackOverflow = () => {
    const data = {
      link: link,
      code: code
    };

    fetch(`${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/verify-stackoverflow`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(result => {
        console.log('Response from server:', result);
        if (result.valid) {
          setVerificationResult('Success');
        } else {
          setVerificationResult('Failed to verify');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setVerificationResult('Failed to verify');
      });
  };

  const handleTotalUpvotes = () => {
    const data = {
      user_id: link
    };

    fetch(`${process.env.NEXT_PUBLIC_HOST}:${process.env.NEXT_PUBLIC_PORT}/total-upvotes`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(result => {
        console.log('Response from server:', result);
        if (result.total_upvotes !== undefined) {
          setTotalUpvotes(result.total_upvotes);
        } else {
          setVerificationResult('Failed to get total upvotes');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setVerificationResult('Failed to get total upvotes');
      });
  };



  return (
    <div className="container">
      <div className="input-container">
        <input
          className={`input-field ${isValid ? 'shrink' : ''}`}
          type="text"
          value={link}
          onChange={handleInputChange}
          placeholder="Enter Solana Stack Exchange Profile Link To Register"
          disabled={locked}
        />
        {isValid && !locked && (
          <button
            className="lock-button"
            onClick={handleLock}
          >
            Lock
          </button>
        )}
        {locked && (
          <button
            className="lock-button"
            disabled
          >
            Locked
          </button>
        )}
      </div>

      {locked && (
        <div className="locked-container">
          <div className="code-container">
            <p className="about-text">
              Please add the following text to your about section on your Solana Stack Exchange account
            </p>
            <div className="code-background">
              <code className="code">Code: {code}</code>
            </div>
            <button className="unlock-button" onClick={handleUnlock}>
              Unlock
            </button>
            <button className="verify-code-button" onClick={handleVerifyStackOverflow}>
              Verify Code
            </button>
            <button className="upvote-button" onClick={handleTotalUpvotes}>
              Total Upvotes
            </button>
            {totalUpvotes !== null && (
              <div className="upvotes-background">
                <p className="total-upvotes">Total Upvotes: {totalUpvotes}</p>
              </div>
            )}
            {verificationResult !== null && (
            <>
              <div className="verification-background">
                <p className={verificationResult === 'Success' ? 'success' : 'verification-result'}>
                  {verificationResult === 'Success' ? 'Success' : 'Failed to verify'}
                </p>
              </div>
              {verificationResult === 'Success' && (
                <div className="centered-buttons">
                  <ReactConnectButton />
                  <ReactDisconnectButton />
                  <ReactDialogButton />
                  <SignMessage defaultText={link}></SignMessage>
                </div>
              )}
            </>
          )}
          </div>
        </div>
      )}
    </div>
  );
};

export default StackOverflowLinkVerifier;
