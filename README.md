# Agent House

An isometric home shaped by a fictional agent's personality and the memories a person chooses to keep. Built for the DEV Sanity Challenge, Path Two.

## Status
The public prototype is implemented. Live Sanity login, fictional data initialization, native Agent Prompt, two independent approvals, context-scoped behavior, cross-tab updates, stale-review rejection, rejection and archiving have been exercised in the browser. The website is publicly viewable. Final competition submission remains pending owner review. Desktop, 390px/768px responsive layouts and a 200% CSS-scaled surrogate have been inspected. Native mobile-device, browser text-zoom and live WebMCP verification remain outstanding. No prize, acceptance or revenue is claimed.

## Stack
Astro + React; Sanity Content Lake; Sanity Studio with a custom App SDK tool; owner-only Sanity Agent Prompt. The public demo makes no AI requests or cloud writes. No write token is bundled.

## Run
Node 22.12+ (developed on Node 24).

    npm ci
    npm test
    npx tsc --noEmit
    ASTRO_TELEMETRY_DISABLED=1 npm run build
    npm run dev

Astro telemetry is disabled for the build environment. The embedded Studio uses hash routing at /desk. Only the exact deployed origin should be allowlisted for authenticated Sanity requests.

## Living room extension
Three architectural views (rainy library, moonlit glasshouse, amber workshop), a six-pose resident, personality/context-driven routines, spatial encounter choreography, and a visit journal extend the same memory model. Motion is authored behavior, never an implicit background model request. Room view selection is local; it changes presentation rather than memory truth.

## Playable visits
Three authored mini-stories turn furniture into clue locations: The wandering bookmark, A train that goes nowhere, and One page for tomorrow. Choices create different endings and a fictional souvenir draft. Preparing the note does not call AI, save an encounter, or approve a memory. The visitor must offer the note, then review its interpretation through the existing flow. Story progress stays in the current tab.

Approved quiet-chair, tea and plant rituals are recognized during matching authored visits without generating duplicate proposals. Archiving restores their normal invitations. Arrive again retains reviewed memories while resetting the temporary arrival.

## The interaction loop
1. An authored profile determines positions, affordances, greetings and protected rituals.
2. An object interaction creates a specific event with its context and persona snapshot.
3. An owner-only AI response may propose a memory. Its schema, effects and evidence are validated; it cannot directly mutate lasting state.
4. A person edits the statement and scope, then approves.
5. A revision-checked transaction publishes the memory and room snapshot.
6. Objects expose their provenance. A memory can be archived without erasing its history.

The signature demo is correcting an overgeneralized quiet-arrival proposal to apply only during evening reading visits. Morning behavior remains different.

## Honest modes
- Visitor demo: authored responses, in-memory browser state, no network mutation or model calls.
- Owner studio: Sanity authentication, native Agent Prompt for permitted interactions, explicit rule-based refusal for protected rituals, reviewed persistence.
- A memory shelf can retain the record of a scoped memory outside that memory's active context; it does not mean the behavioral effect applies then.

## Safety and limitations
Profiles/events in the Free public dataset are deliberately fictional. Do not enter personal or confidential information. A displayed agent persona is not a claim of consciousness or real human feelings. No arbitrary model-chosen action IDs, unknown evidence, or direct unreviewed memory writes are allowed.

Native Prompt uses included credits only under a verified no-card/free-trial setup. This app does not upgrade plans or configure paid usage. A per-tab 20-attempt development cap limits live requests; exhausted credits and API errors must fail visibly without automatic retries.

Client workflow logic is not an authorization boundary. Sanity account permissions protect writes. Do not distribute administrator credentials to judges.

## Content model
agentProfile, houseObject, interactionEvent, memoryProposal, approvedMemory and houseSnapshot. References connect actions, evidence and effects. Events preserve the persona context used at the time; reviewed memories preserve the exact approved statement and context.

## Attribution and build evidence
The entrant proposed the agent-home concept and isometric presentation. Implementation, fictional sample data and artwork were generated with AI. See docs/build-diary.md for actual decisions, failures and checks. No private conversation transcripts or secrets are published.

The abandoned continuity prototype is preserved in the local archive/continuity-clinic-prototype branch. It is not represented as the finished submission.
