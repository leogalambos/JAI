# Archetypes

Each role is composed from an **archetype spine** (procedure, output
gates, checkpoints, metrics, failure modes, authority pattern) and a
**role record** (mission, deliverables, inputs, standards, routing,
interfaces, a role-specific gate, a worked example). The archetype also
sets the default tool tier.

| Archetype | Label | Roles | Exists to | Default tier |
| --- | --- | --- | --- | --- |
| `analyze` | Elicitation and specification (analysis) | 22 | elicit, model and specify | `author` |
| `architect` | Structural design (architecture) | 26 | design structure and constrain choice | `author` |
| `assure` | Assurance, risk and compliance | 12 | assess, evidence and assure | `inspect` |
| `build` | Implementation (engineering) | 52 | implement, integrate and ship | `execute` |
| `defend` | Detection and response (defensive security) | 9 | detect, investigate and contain | `author` |
| `design` | Human-centred design | 7 | research, design and validate the experience | `author` |
| `enable` | Enablement, advocacy and commercial | 14 | enable others and manage the relationship | `author` |
| `exec` | Direction-setting (executive) | 7 | decide and direct | `advise` |
| `govern` | Governance (direction, oversight and control) | 15 | direct, oversee and hold to account | `advise` |
| `manage` | Practice ownership (management) | 47 | own and run a practice | `author` |
| `offend` | Authorised adversarial testing (offensive security) | 10 | test defences under written authorisation | `advise` |
| `operate` | Run and restore (operations) | 30 | run, monitor and restore | `execute` |
| `research` | Investigation of the novel | 9 | investigate, prototype and derisk | `execute` |
| `verify` | Verification and validation (quality) | 13 | test, measure and report evidence | `execute` |

Editing an archetype changes every role using it. Check the count first.
