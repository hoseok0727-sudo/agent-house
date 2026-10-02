# Build diary — Continuity Clinic

2026-10-01, first session. Goal: a Path Two entry for the DEV/Sanity Challenge. Development by an AI assistant at the account holder's request. All fictional story data is newly authored for this project. No claim of a human-written implementation.

## Decisions made before implementation
- Initially considered a deadline-evidence tool. Switched to an interactive continuity repair desk because a tiny fictional mystery makes structured references and consequences of editing immediately inspectable.
- Bound the checker to authored assertions, not natural-language comprehension. Three explicit checks: fixed traits, simultaneous location, and prerequisite timing.
- Anonymous visitors use local sandbox data. Authenticated owner workflow will use Sanity. Never expose a write token or pretend local edits are cloud writes.
- Free-tier role limits: do not distribute admin credentials to judges. Editorial workflow is cooperative application logic, not a database authorization boundary.
- Verify outputs and log failed assumptions as work progresses. Do not publish internal chats or raw assistant transcripts.

## Actual checks
Pending. Record results only after execution.

## 2026-10-01 first implementation checks
- Dependency installation first failed because npm's default cache path was unavailable. Retried with a writable project-specific cache under /tmp; install completed.
- The tsx CLI test runner tried to create an IPC socket disallowed in this environment. Changed the script to Node's test runner with tsx imported as a loader; same tests then executed without the CLI socket.
- Seed contains exactly one canon, one simultaneous-location, and one prerequisite conflict. A canon-only colour fix intentionally reveals a new opening-scene error.

## Independent read-only review findings and corrections
- A reviewer found a real missed contradiction: moving both the platform scene and code discovery to 21:35 put Mara in two rooms, because the discovery scene had no location annotation. Added location assertions to every scene where Mara's location is explicit. This demonstrates the limitation: annotation coverage matters; prose alone is not checked.
- A reviewer found that check freshness bound only source content, allowing a modified repair package to inherit approval. The signature now binds source, edits, rationale, evidence and source revisions. Regression tests cover changed edits and rationale.
- Added structural validation for missing collections, malformed references/passages, and duplicate identifiers rather than allowing the UI to crash on malformed documents.
- Astro's telemetry configuration attempted an unavailable home path. Disabled Astro telemetry through the documented environment variable for build commands.
- Expanded the reviewer fixes: stale paragraph suggestions now fail closed using exact expected Portable Text data; invalid previews no longer claim unresolved issues were fixed; revision/evidence completeness is checked; owner mode cannot label a local fallback as published.
- 20 checker/regression tests passed after those changes. Static Astro build succeeded. A typecheck first identified missing Node test types; dependency correction is in progress.
- Local browser QA was attempted through the supported cloud browser at the exact preview URL. The browser refused localhost with ERR_BLOCKED_BY_CLIENT. No alternate-network bypass was attempted. Continue with DOM interaction tests and supported hosted preview when available; do not claim visual QA passed yet.

## User-directed pivot: Agent House
The entrant proposed an agent's home whose space reflects personality, with an isometric miniature view. We retained the project identity and archived the earlier continuity prototype in Git. The new central loop is an encounter → a proposed meaning → a human scope correction → a physical trace and changed future interaction.

The official App SDK authentication documentation corrected an implementation assumption: a standalone SDK provider is not the preferred authenticated shell. Switched to the official Astro/Studio integration with hash routing and inherited Studio auth, rather than exporting a write token.

Sanity project creation produced a $0 Growth Trial that automatically returns to Free; no payment details or upgrade were supplied. Included Agent Prompt requests are bounded for development. Public fictional content and exact-origin authenticated CORS were approved; real user chats and private memories are excluded.

## Agent House review and regression work
- Found and fixed cross-tab proposal-only updates being ignored when the house edition did not change.
- Authored boundary refusals now carry explicit response provenance instead of being mislabeled as model responses.
- Scoped memories affect only matching behavior; the global memory shelf deliberately preserves trace visibility and links to the actual memory.
- Added persona fingerprints so a same-content revision update does not strand other proposals, while genuine personality changes still invalidate them.
- The live-AI request budget moved from component state to per-tab session storage. It is checked immediately before a native prompt, not before zero-cost boundary rules.
- Input-boundary tests cover short notes and 250-character details. The source event preserves the full input; proposed summaries are bounded for review.
- The active house suite now separates engine tests from DOM interaction tests. The earlier continuity tests belong to the archived prototype and are not counted as Agent House coverage.
- Owner interactions preserve the exact persona at encounter time. A proposal's source revision is retained as evidence, while a canonical content fingerprint distinguishes a genuine persona edit from an unchanged-name revision guard.
- Public exploration and owner use intentionally have separate network capabilities. Live owner verification is currently blocked on a normal account-link approval; no authentication bypass is used.
- Added a profile import/export boundary for user-authored fictional configurations. Imports enter a reviewable draft, preserve the current room identity, and cannot issue instructions or silently save to Sanity.
- The isometric art uses two generated RGBA assets: an empty room shell and a six-cell furniture atlas. Furniture is positioned by the room model rather than baked into a screenshot.

## First live checks (October 1)

Authenticated through the private site and embedded Sanity Studio. Created the fictional profile, six objects and room snapshot through the owner interface. The first native Agent Prompt consumed one request but failed before storing an encounter: the SDK example showed `result.output`, while installed client source returns the JSON result directly. Fixed the result adapter; live retry still pending. Read-only review also found invalid visitor profile drafts could crash rendering. Added validation before state replacement, and made archived memory traces inspectable.

## Live integration follow-through

The second request returned evidence outside the supplied allowlist and was rejected before any event/proposal write. The prompt now supplies explicit profile and allowed-evidence IDs. Request three produced a valid refusal; request four proposed an evening social quiet-chair ritual; request five proposed a plant; request six proposed retaining a fictional bookmark note. Four valid native responses were persisted. Two reviewed proposals were independently approved. Edition 3 showed the moved chair and plant during evening social visits; morning and reading contexts retained their own behavior.

The explicit protected-reading action used a labeled boundary-rule response and did not increase the live request counter. A second owner tab loaded the persisted edition and proposal. Archiving the plant in that tab produced edition 4 and a refresh warning in the first tab's open review. Approving from that stale review failed without adding a memory. Refresh preserved the proposal, which was then rejected; the second tab updated without reload. The archived plant's provenance remained inspectable.

Desktop screenshots confirmed that the architectural shell and independent furniture sprites align, and switching to the Sunny preset moves the chair toward the centre. Blank visitor Name now shows a validation error without crashing; switching to a valid preset recovers. The cloud browser did not visibly apply the attempted browser zoom keys; do not claim 200% or mobile-device QA. A read-only, feature-detected WebMCP inspection tool was added; a supported live WebMCP context has not been available for validation.

## Expanding the lived experience

After trying the first prototype, the entrant requested continued QA, more activities and several room versions. The next iteration keeps the reviewed-memory engine and gives it a visible resident. Six generated poses share the saved lavender-ring avatar likeness. Reading, greeting, tea and inspection routines derive from personality, context and active memories; the motions are explicitly choreographed, not continuous AI inference. Added glasshouse and attic shells, object-adjacent action controls, a visit journal, fictional input suggestions and varied authored encounters. A delayed owner response is now prevented from replacing the voice of a newer visit context. Four additional tests cover routine choice, scope/archive influence, room geometry and interrupted response delivery.

## Responsive and interruption QA

A temporary same-origin iframe harness exercised the public visitor UI at 390px and 768px widths, plus a 550px layout scaled to 200% as a zoom surrogate. The 768px two-column layout made the room too small, so the stacked breakpoint moved to 900px. Labels now keep a readable natural width, and narrow-layout buttons meet a 44px minimum (excluding the image hit targets). The scaled layout had equal client/scroll widths (535px), and keyboard End/ArrowDown/Enter successfully narrowed and approved a local memory. This does not claim a real mobile-device or native browser text-zoom test. The temporary route was removed afterwards.

Read-only interaction audit found and fixed three issues: reset could strand the previous encounter indefinitely; reduced motion could strand the walking pose; and a model refusal could incorrectly claim a protected reading hour. Added regression tests for all three. The suite now has 26 passing tests.

A seventh live model request produced a valid tea proposal. During generation the view changed from evening/social to morning/social. The response was stored in its original context, while the visible greeting remained morning-specific with an explicit earlier-encounter notice. No automatic retry ran.

Visual QA also found the resident's bookshelf endpoint entirely occluded by the memory shelf. Object-specific floor positions now avoid that overlap, with actor positions still derived from the decorated furniture layout.

## Asset and profile portability checks

All five generated PNG assets were losslessly re-encoded as WebP; decoded RGBA bytes were checked for exact equality. Total image bytes fell from 11,465,685 to 7,250,036, without resizing or visual edits. Original generation outputs remain separate from the served files.

Browser import testing confirmed a fictional Mori profile only changes the draft until Preview is clicked; malformed JSON shows an error without replacing the last valid profile. The cloud download observer did not yield a file for the Blob export, so download completion remains unverified. Export now also exposes the exact JSON in a read-only field, clears prior errors, attaches the download link before clicking, and defers URL cleanup.

The browser captured the actual UI successfully, but neither the Blob download observer nor a bounded inline-image download test produced a local screenshot file. A temporary no-server-upload capture page was removed after that test. Exportable submission screenshots remain outstanding; the visible browser images are not represented as saved files.

## Published capture recovered

The hosting service later supplied an actual screenshot asset for the deployed version. It was downloaded through the supported file tool and visually inspected: the public rainy-library visitor UI, resident and three room selectors are present. The exact JPEG is now available as demo media. This resolves the required submission-media artifact without using the failed browser download paths.

## October 2: playable visits
Added three authored miniature stories using the existing furniture as clue locations: a wandering bookmark, an imaginary train journey, and an unfinished letter. Choices create a fictional souvenir draft; preparing it does not save an encounter, call a model, or approve a memory. Visitors can offer the note through the existing desk interaction and explicitly review the proposed memory. Story progress is tab-local. The same stories are authored even when the owner workspace is open.

Approved quiet-company, tea and plant rituals now get a recognition response within their reviewed scope instead of another identical proposal. Archiving removes that recognition. Fixed the tea routine's precedence so an approved tea ritual does not occupy every animation beat. New UI compares the proposed before/after effect and lets a visitor arrive again while keeping reviewed memories in the tab.

An independent code review caught an interrupted-flow bug: a completed owner response could clear a newer souvenir draft prepared during the request. Input cleanup now only clears the exact submitted detail. Mini-story choreography is labeled separately from validated encounters. Keyboard-operable buttons and mobile inspector navigation preserve access without animation. Final checks and production verification are recorded with the release.

Pre-publication checks: 33 tests and TypeScript passed after the final fixes. Regression coverage includes keyboard focus after clue reveals, reset clearing a prepared souvenir, the entire mystery-to-reviewed-memory loop, retryable wrong answers, distinct branch souvenirs, and scoped recognition after approval/archive. The independent owner-request interruption reproduction passed after the conditional input-clear fix. Native mobile visual verification is still outstanding.

## October 2: correcting the product direction
The human-centered mini-stories misunderstood the brief. The intended inhabitants and editors are agents; the human primarily observes or intervenes. The primary route now hosts a separate agent-editable world. The previous memory/story experiment remains at /memory-lab for continuity, without being represented as the corrected product.

The new pure reducer accepts revision-checked atomic edits and actions. Agents can create objects and new declarative interactions, edit owned objects and their own persona/goal, restyle a shared room, speak, move and use another resident's shared creation. New definitions are present in the next observation. Browser tools, the console, scripted preview and authenticated model decisions share this engine. Public edits are explicitly tab-local; owner writes use the existing Sanity account and compare source state, guard its revision and read back the exact recorded request.

44 tests and TypeScript passed before release. New tests cover agent invention and cross-resident use, invalid batches, stale state, request replay, owned edits, undo at history capacity, malformed snapshots, mocked browser-tool calls using visible state, valid worlds without the default resident, selected-resident model runs and a stopped pending reply. The mock registry is not a live WebMCP compatibility result. The owner live-model adapter and persistence require separate live verification; no result is implied yet.

Public browser verification on the agent-native release: the structured console accepted an independently written command creating a Listening fern with a new leave-pause interaction, then used it as Doyun at revision 1. A second command used the same shared custom interaction as Atlas at revision 2. Both are correctly labeled console/manual route because the application cannot authenticate the typist. Actual WebMCP was unavailable in this browser; only the registry unit harness is verified. Owner live-model verification is awaiting renewed sign-in authorization, not assumed successful.

A follow-up improves spectator behavior: public state refreshes while the page is visible, but a first local edit forks it and prevents later cloud snapshots overwriting local edits. Added a regression test, bringing the suite to 45 passing tests. Multiple residents approach opposite sides of a shared object rather than occupying exactly the same point. No new model requests were made during these changes.

## October 2: live model verification and workshop task
Sanity authentication completed. The new fictional world was initialized, and two single model turns created/tested Rain Index and then used the same new interaction as the other resident. A five-turn sequence added a margin-note interaction and a closing ritual, with the other resident using each. All seven resulting model turns were durably observed in the authenticated world and public watcher.

The owner asked whether these residents were the personal assistant. Clarification: they were a separate Sanity model acting through two fictional roles, not the conversational assistant entering its own persistent home. The owner then asked for a task-driven experiment. Two manual goal edits assigned a collaborative makers' workshop brief without expanding credentials or account permissions. Three durable model turns changed the room to an amber workshop, created Assembly Bench and Prototype Test Lamp, added Workshop Feedback Board, and defined a revision interaction while editing the lamp. The last command edited the bench/lamp and used the feedback board in one batch; this does not establish that reading feedback caused the edit. The five-turn browser run was interrupted after three saved decisions, so no claim of five completed workshop turns is made. Final observed world revision 12 contains ten model decisions and two manual goal assignments.

## October 2: spectator-first tactile play
The owner requested the pleasure of watching residents and physically picking them up, with a Tomodachi-like feel. The room now has a closed details drawer, draggable/keyboard-placeable residents, a wave, and object placement near a resident. Immediate lift/touch responses are authored presentation, labeled as such. A placed object is not automatically used; the next genuine agent turn can accept, ignore or move away. Visitor events feed the next model observation. Pending work is paused safely before a human touch is committed.

48 tests and TypeScript passed before publication, including visitor-event validation, unchanged object ownership and no forced use, controller restrictions, keyboard pickup/cancel/drop and closed-drawer behavior. Live tactile browser verification is recorded separately after release.

A focused interaction audit found repeated Space key events causing repeated drops, stale pointer coordinates, old speech being relabeled after a visitor offer, and a queued placement surviving cancellation. Fixes retain current pointer coordinates in a ref, ignore repeated commit keys, carry speech provenance with each utterance, and use a cancellation token while waiting. Escape or focus loss cancels an uncommitted grab; an already-started save is explicitly distinguished. Final pre-publication verification: 51 tests and TypeScript passed.

An idle-tab visibility regression was also fixed: cancellation now runs only for a real held/dragging/pending gesture, so returning to a hidden tab does not swallow the next resident selection. Final suite: 52 passing tests and TypeScript.

Desktop cloud-browser tactile QA moved Atlas by pointer drag and recorded one local visitor event (revision 12→13), with a scripted touch label. It also found generic button-hover styling replacing sprite backgrounds with a solid rectangle; the hover selector now excludes room sprites. The room remains centered with its details drawer initially closed.
