# cv-based-tv-auto
This repo is intended to automate TV flows using Computer vision

### Sony LIV – Flow-Based Automation

Target Application: **Sony LIV**

![Image](https://blog.roboflow.com/content/images/2023/05/data-src-image-7b019a68-485b-4aef-be18-21388ec414ee.png)

---

## 1. Objective of This Repository

This repository defines a **Computer Vision–based automation framework** for Smart TV applications where native automation APIs are unavailable.

The primary objective is to **automate predefined user flows** in the Sony LIV TV application by:

* Observing the TV screen via **live video feed**
* Interpreting UI state using **computer vision**
* Driving navigation via **remote control inputs**
* Verifying behavior using **visual assertions**

This repository **does not execute automation by itself**.
It describes **what must be built and how the system should behave**, serving as:

* A **design contract**
* A **system specification**
* A **pre-instruction context for another AI model**

---

## 2. Scope

### In Scope

* Flow-based automation (deterministic, predefined)
* Live video perception (camera or capture card)
* Visual state detection
* Visual assertions
* Remote-driven navigation
* Black-box testing approach

### Out of Scope

* Free-form AI navigation
* Direct TV OS APIs
* Pixel-perfect UI testing
* Timing-based automation
* Autonomous decision-making

---

## 3. Core Philosophy

1. **The TV is a black box**
2. **Vision is the single source of truth**
3. **Actions are meaningless without assertions**
4. **Navigation is focus-based, not coordinate-based**
5. **Automation must behave like a human user**

---

## 4. High-Level System Design

```
Live Camera / Image
        ↓
Single Frame (image)
        ↓
LLM Vision Call
        ↓
Structured Focus Result (JSON)
        ↓
Deterministic Navigation Logic
```

The system is **closed-loop**:

* Every action is followed by visual verification
* The system never assumes success

---

## 5. Computer Vision Responsibilities

The CV layer is responsible for **interpreting what is visible on the TV screen**, not for decision-making.

### Visual Signals to be Extracted

* Current screen type (Home, Search, Playback, Error, Ad)
* App identity (Sony LIV detected or not)
* Focused UI element (highlighted tile or button)
* Visible text (titles, errors, labels)
* Playback state (motion vs static)
* Loading state (spinner or transition)
* Overlay presence (menus, popups)

These signals are converted into a **structured state representation**.

---

## 6. Assertions (Critical Concept)

Assertions define **truth conditions** based on what a real user would see.

Examples:

* Sony LIV home screen is visible
* Search option is focused
* Keyboard is displayed
* Playback has started
* Advertisement is playing
* Error message is shown

Assertions are:

* Visual
* Redundant (multiple signals)
* Time-bounded
* Deterministic

No flow step is considered complete without a passing assertion.

---

## 7. Flow-Based Automation Model

Automation is defined as **explicit flows**, not AI-driven exploration.

A flow is:

* A sequence of **expected user actions**
* Each action followed by a **visual assertion**

Flows represent:

* App launch
* Content search
* Content playback
* Ad handling
* Error handling

Flows are deterministic and repeatable.

---

## 8. Input Control Model

The system interacts with the TV using **remote-control inputs** (IR or equivalent).

Design rules:

* No absolute positioning
* No fixed key counts
* Navigation continues until **visual focus confirmation**
* Input is always validated visually

---

## 9. Failure Model

Failures are expected and informative.

Failure conditions include:

* Assertion timeout
* Unexpected screen
* UI layout change
* App crash
* Network error

On failure:

* Execution stops
* Visual evidence is captured
* Failure reason is recorded

---

## 10. Repository Structure (Conceptual)

```
Repository Root
│
├─ Vision Layer Definition
│   └─ What visual signals must be detected
│
├─ Assertion Definitions
│   └─ What conditions must be visually true
│
├─ Flow Definitions
│   └─ What user journeys must be automated
│
├─ Control Interface
│   └─ How actions are sent to the TV
│
├─ Execution Model
│   └─ How steps, retries, and failures are handled
│
└─ Documentation
    └─ Design, assumptions, and constraints
```

This structure exists to **communicate intent**, not implementation.

---

## 11. Intended Audience

* Automation engineers
* Computer vision engineers
* QA engineers
* AI models used for:

  * Code generation
  * Assertion logic generation
  * Failure analysis
  * Flow synthesis

---

## 12. How Another AI Model Should Use This Repository

This repository should be treated as:

* A **system specification**
* A **behavioral contract**
* A **constraint definition**

An AI model reading this repository should understand:

* What problem is being solved
* What must be detected visually
* What flows exist
* What constraints must not be violated
* What success and failure mean

---

## 13. Key Constraints (Non-Negotiable)

* No autonomy in navigation
* No assumptions without visual proof
* No reliance on internal app knowledge
* No hardcoded UI positions
* No timing-based waits

---

## 14. Summary

This project defines a **vision-driven, deterministic TV automation system** designed specifically for Sony LIV.

It prioritizes:

* Reliability over intelligence
* Observability over speed
* Determinism over flexibility

The repository exists to **guide implementation**, not to contain it.

---

If you want next, I can:

* Rewrite this for **even more AI-friendly language**
* Add a **“System Assumptions”** section
* Add a **“State Representation Contract”**
* Produce a **separate SYSTEM_PROMPT.md** for another model

Just tell me.
