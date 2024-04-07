"use client";

import React from "react";
import { useState } from "react";
import dynamic from "next/dynamic";

import { SignTransaction } from "@/components/SignTransaction";
import { SignMessage } from "@/components/SignMessage";
import { SignIn } from "@/components/SignIn";
//import { StackOverflowLinkVerifier } from "@components/StackOverflowLinkVerifier";
import StackOverflowLinkVerifier from '../components/StackOverflowLinkVerifier';

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




const Try = () => {

  const [reactToggle, setReactToggle] = useState(true);
  function toggleReact() {
    setReactToggle(!reactToggle);
  }

  const [muiToggle, setMuiToggle] = useState(false);
  function toggleMui() {
    setMuiToggle(!muiToggle);
  }

  const [antToggle, setAntToggle] = useState(false);
  function toggleAnt() {
    setAntToggle(!antToggle);
  }

  const [connectToggle, setConnectToggle] = useState(true);
  function toggleConnect() {
    setConnectToggle(!connectToggle);
  }

  const [disconnectToggle, setDisconnectToggle] = useState(true);
  function toggleDisconnect() {
    setDisconnectToggle(!disconnectToggle);
  }

  const [dialogToggle, setDialogToggle] = useState(true);
  function toggleDialog() {
    setDialogToggle(!dialogToggle);
  }

  const [multiToggle, setMultiToggle] = useState(true);
  function toggleMulti() {
    setMultiToggle(!multiToggle);
  }

  const [signInToggle, setSignInToggle] = useState(true);
  function toggleSignIn() {
    setSignInToggle(!signInToggle);
  }

  const [signMessageToggle, setSignMessageToggle] = useState(true);
  function toggleSignMessage() {
    setSignMessageToggle(!signMessageToggle);
  }

  const [signTransactionToggle, setSignTransactionToggle] = useState(true);
  function toggleSignTransaction() {
    setSignTransactionToggle(!signTransactionToggle);
  }



  return (
    <>
      <StackOverflowLinkVerifier></StackOverflowLinkVerifier>
      {connectToggle && <div className='flex flex-col h-1/5 items-center justify-center'>
        <ReactConnectButton />
      </div>}
      {disconnectToggle && <div className='flex flex-col h-1/5 items-center justify-center'>
        <ReactDisconnectButton />
      </div>}
      {dialogToggle && <div className='flex flex-col h-1/5 items-center justify-center'>
        <ReactDialogButton />
      </div>}
    </>
  );

};

export default Try