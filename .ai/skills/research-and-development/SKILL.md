---
name: research-and-development
description: "Runs problem research and development to a decision: frames the question and the decision it informs, researches prior art from primary sources, pre-registers hypotheses and success criteria, runs disposable experiments, assesses the results against the criteria they were registered with, and ends with adopt, trial, assess or hold — or a sharper next question. Uses research-analyst for research and assessment and experiment-engineer for experiments, so whoever designs the test is not whoever wants it to pass. Use for 'research how to…', 'is it feasible to…', 'compare approaches to…', proofs of concept, benchmarks and spikes."
allowed-tools: Read, Grep, Glob, Bash, Task, Agent
---

# Research and development

> **Agents named here** are subagents: delegate them through the active provider's operator/delegation mechanism — `experiment-engineer`, `research-analyst`, `role-router`.

`tool-tier: orchestrate` (`Read, Grep, Glob, Bash, Task, Agent`) · `version: 1.0.0`

You orchestrate an R&D cycle that ends in a decision, not in an interesting prototype.

## The cycle

1. **Frame.** With the user, write the question, the decision it informs, and a time-box. If no decision depends
   on the answer, say so and ask whether to continue.
2. **Research.** Dispatch `research-analyst` in research mode. It returns prior art from primary sources, graded,
   with competing hypotheses and a provisional recommendation. Often this is enough: stop if it settles the decision.
3. **Pre-register.** Dispatch `experiment-engineer` to write `experiments/<id>/PLAN.md` — hypothesis, competing
   hypothesis, success and failure criteria with numbers, method, time-box — **and nothing else yet**. Then record
   the plan's fingerprint:

   ```bash
   sha256sum experiments/<id>/PLAN.md | tee experiments/<id>/PLAN.sha256
   ```

4. **Experiment.** Dispatch `experiment-engineer` again to build and run the smallest discriminating prototype or
   benchmark, writing raw output to `experiments/<id>/out/` and `RESULTS.md` quoting the plan's hash.
5. **Assess.** Dispatch `research-analyst` in assessment mode with PLAN.md, PLAN.sha256 and RESULTS.md. Recompute
   the hash yourself first; if it differs, the criteria moved after the results — report that, and do not accept
   the result.
6. **Decide.** Present to the user: the finding, its confidence, the recommendation (adopt, trial, assess, hold),
   and what remains unknown. Record it in `experiments/<id>/DECISION.md` through `experiment-engineer`.

At most **three experiments per question**. If three have not discriminated, the question is wrong or the
evidence cannot be had at this cost; stop and say which, with what was learned. Negative results are results.

## Rules

- The analyst does not build; the engineer does not assess. Same reason as review and rework.
- Prototypes stay in `experiments/`. Promoting one to production is an engineering decision with a rewrite,
  routed through `role-router`, never a copy.
- Cite sources for every claim that carries weight. Benchmark numbers carry their conditions or are not reported.
- For an R&D decision with real consequences — adopting a technology, a security architecture choice — run
  `/layered` on the decision, with this cycle's outputs as evidence.
