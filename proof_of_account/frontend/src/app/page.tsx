"use client";

import React from "react";
import { useState } from "react";
import dynamic from "next/dynamic";

import StackOverflowLinkVerifier from '../components/StackOverflowLinkVerifier';


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
    </>
  );

};

export default Try