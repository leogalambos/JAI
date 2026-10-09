# Discovery meeting — ACME Pay s.r.o., 1 October 2026

Present: CTO (Jana Horak), Head of Partnerships (Petr Novak), our team.

## Goals
ACME Pay wants to double partner revenue in 2027 by opening its payments API to around 40 partner payment
service providers (PSPs) across the EU.

## Concerns
Last year a partner's breach exposed card tokens issued by ACME Pay. Partners now ask for contractual proof of
security controls before they sign. The CTO is worried about who can change partner routing configuration:
today three platform engineers share one administrator account.

## Constraints
Small platform team (3 engineers). Everything runs in AWS (eu-central-1). Go-live target: Q2 2027.
Budget for new tooling is limited; managed AWS services are preferred over self-hosted products.
