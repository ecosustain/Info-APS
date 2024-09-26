'use client'
import React from "react";

import State from "./components/State"
import Charts from "./components/Charts";

import styles from "@/styles/page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <State />
        <Charts />
      </main>
    </div>
  );
}
