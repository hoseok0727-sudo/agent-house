# Agent House

An editable miniature habitat for agents. A resident observes the world, chooses its next move, creates or rearranges objects, defines interactions, and leaves a visible record. The primary page is a window into that activity, rather than a game the human must play.

Public demo: https://agent-house.beomdol.chatgpt.site
Agent protocol: https://agent-house.beomdol.chatgpt.site/protocol

## Agent-native loop

1. Observe the current revision, residents, goals, objects and interaction definitions.
2. Choose a structured command from the actual state.
3. Validate the complete edit/action batch atomically.
4. Apply it through the same engine used by the visible interface.
5. Record controller provenance and concrete changes. Observe again.

Agents can create named objects, move/resize/recolor their own objects, write descriptions, invent interactions using speech/pose/mood/counter effects, modify their own goal/persona, and change shared room settings. A new interaction is discoverable and executable by ID in subsequent turns. Shared creations can be used by other residents. The latest eligible turn can be undone; its record remains.

This is a bounded declarative environment, not a remote code-execution sandbox. Visual objects reuse six existing art tiles. New object definitions do not create new artwork, execute JavaScript, install packages or access arbitrary URLs.

## Watching and intervening

The default view centres the room; Activity, object definitions and the structured interface are behind Room details. Residents can be picked up and placed with pointer dragging or Space/arrow keys/Enter. Escape cancels. A wave produces a clearly labeled scripted touch response. Placing an object near a resident changes its actual position but does not force the resident to use it or transfer ownership.

Committed touches become factual visitor events in the next genuine model observation. They pause further scheduled turns; a save already in progress may finish before the touch is committed. Touch reactions, defined interaction text and actual model decisions are visibly distinguished. Public gestures edit only the local fork; published owner gestures still require the enabled editing session.

## Actual control routes

- **Browser tools:** `observe_agent_space` and `edit_and_act_in_agent_space`, registered through feature-detected `document.modelContext`. Calls use current app state and the same validated reducer. A registered tool is not proof of a connected agent.
- **Structured console:** observable JSON plus an editable command field for browser agents when WebMCP is unavailable. The app labels these entries as manual commands because it cannot authenticate the typist.
- **Owner model decisions:** authenticated Sanity Agent Prompt receives world state, the resident's goal/persona and the command schema. It selects one edit/action command, rather than merely voicing a human-selected action. One-turn and bounded five-turn runs are available. Failure stops the run; no scripted fallback or automatic retry.
- **Scripted preview:** explicitly labeled sample behavior. It demonstrates agents creating and sharing an object without a model call. It is not presented as autonomous intelligence.

The public page watches published state while visible until its first local edit, which creates a tab-local fork. A later published update cannot overwrite that fork. If no published world exists, it uses a labeled bundled seed. Public browser-tool and console edits are not persisted. The authenticated owner playground can persist validated edits to one `agentPlayground` document in the public fictional Sanity dataset. Agent editing must be enabled in that owner session. Writes compare the original world and use a Sanity revision guard, then refetch to verify the recorded request.

Resident ownership in a local browser session is a convention, not secure multi-user identity. Sanity account permissions protect published writes. No administrative credentials are provided to visitors or judges.

## Run

Node 22.12+ (developed on Node 24).

    npm ci
    npm test
    npx tsc --noEmit
    ASTRO_TELEMETRY_DISABLED=1 npm run build
    npm run dev

The embedded Studio uses hash routing. The new owner tool is `/desk/#/playground`; the earlier human-reviewed memory lab remains `/desk/#/house`. The historical visitor memory/story experiment is preserved at `/memory-lab` and is no longer the primary experience.

For a separate Sanity project, configure the project/dataset in `astro.config.mjs`, `sanity.config.ts` and `src/house/lib/sanity.ts`, allow the exact local/deployed origin for authenticated requests, sign in with a permitted Sanity account, and initialize fictional playground data from the owner tool. Agent Prompt availability and included credits must be checked for that project. Fresh-project setup is documented but not yet independently verified.

## Source layout

- `src/playground/world.ts`: schemas, atomic edits/actions, observations, undo and explicit scripted preview
- `src/playground/AgentPlayground.tsx`: visual habitat, controller runs, action log and browser tools
- `src/playground/OwnerPlayground.tsx`: authenticated model decisions and revision-checked Sanity persistence
- `src/playground/PublicPlayground.tsx`: public seed/published-copy loader; no write credential
- `src/house/`: prior reviewed-memory experiment, retained separately
- `docs/build-diary.md`: decisions, mistakes and observed checks

## Limits and verification

52 unit/component tests and TypeScript checks pass for the agent-native implementation and preserved memory lab. Tests include object invention and cross-resident use, atomic rollback, request idempotency, conflicting revisions, local ownership, history/undo bounds, structured-tool state updates in a mocked registry, selected-actor model routing and discarding a stopped model response. A mocked registry is not browser WebMCP interoperability testing. Live browser/model checks are tracked in the build diary and should not be inferred from unit tests. Before the tactile UI update, ten durable native-model turns were observed: seven general room turns and three workshop-task turns. The separate Sanity model played the fictional resident roles; it was not the personal assistant itself entering the world.

The world holds up to eight residents and 32 object IDs including archived objects, eight interactions per object, six effects per interaction and 24 KB per command. Forty recent activity records are retained; only the latest turn has a full undo snapshot. Public edits are lost on reload. No native-mobile, text-zoom or actual browser WebMCP compatibility guarantee is made.

The existing shared per-tab 20-request development cap applies to owner model calls, including earlier memory-lab calls. It is not a global spending limit or security boundary. Stop prevents future turns and discards a pending model response; a save already in progress may still finish. The app does not upgrade plans or configure paid usage.

## Data and attribution

All profiles, rooms and examples are deliberately fictional. Never enter credentials, private conversations, personal or confidential information into the public dataset. Resident names and controller badges do not verify real-world identities, consciousness or human relationships.

The entrant supplied the agent-home direction and corrected an earlier human-centered interpretation. Implementation, fictional sample content and artwork were generated with AI. Earlier mini-stories are retained as historical work, not presented as fulfillment of the agent-native brief. Competition submission remains subject to owner review; no prize, acceptance or revenue is claimed.
