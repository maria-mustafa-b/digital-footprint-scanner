<div align="center">

# 🔍 Digital Footprint Scanner

**An open-source OSINT tool that builds a full digital identity report from a username or email address.**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active%20Development-orange?style=flat-square)]()

[Features](#features) · [Architecture](#architecture) · [Getting Started](#getting-started) · [API Reference](#api-reference) · [Roadmap](#roadmap) · [Ethics](#ethics--legal)

</div>

---

## Overview

Digital Footprint Scanner is a portfolio-grade OSINT (Open Source Intelligence) tool that accepts a username or email address and produces a comprehensive public identity report. It fans out across dozens of public data sources in parallel, aggregates the results, identifies cross-platform patterns, and outputs an interactive dashboard, a PDF cyber report, and a graph-based identity map.

> **Intended use:** Self-assessment, security research, and educational purposes only. See [Ethics & Legal](#ethics--legal) before using.

---

## Features

### Core scanning
- **Username footprint search** — checks 300+ platforms via Sherlock/WhatsMyName
- **Email breach detection** — queries HaveIBeenPwned and similar breach databases
- **Cross-platform identity mapping** — links accounts by shared email, username variants, bio cross-references, and profile photo hashing
- **Search engine dorking** — automated Google/Bing queries to surface indexed mentions

### Intelligence layer
- **Risk scoring engine** — weighted 0–100 exposure score based on breach severity, platform count, data type exposed, and username reuse patterns
- **Identity clustering** — graph-based algorithm that groups accounts likely belonging to the same person using NetworkX connected components
- **Pattern detection** — flags username reuse, credential reuse across breaches, and linked bios

### Output
- **Interactive React dashboard** — live scan progress, filterable results table, risk gauge
- **PDF cyber report** — exportable one-page summary with exposure score, platform list, and recommendations
- **D3.js identity graph** — force-directed visualization of account relationships and signal edges
- **JSON export** — machine-readable output for use with other security tools

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                          │
│            Username  ·  Email  ·  Phone (optional)          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                    Input normalizer
                            │
         ┌──────────────────┼──────────────────┐
         ▼                  ▼                  ▼
  ┌─────────────┐   ┌──────────────┐   ┌─────────────────┐
  │  Username   │   │   Breach     │   │  Social mapper  │
  │  checker    │   │   scanner    │   │  + dork engine  │
  │ (Sherlock)  │   │   (HIBP)     │   │  (platform APIs)│
  └──────┬──────┘   └──────┬───────┘   └────────┬────────┘
         └──────────────── ▼ ───────────────────┘
                   Data aggregator
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   Risk scorer     Identity clusterer    Pattern detector
         └─────────────────┼─────────────────┘
                    Report builder
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
    Dashboard           PDF report      Identity graph
```

The backend is fully async — all collectors run concurrently via `asyncio` and `aiohttp`, keeping scan time under 30 seconds for most targets.

---
