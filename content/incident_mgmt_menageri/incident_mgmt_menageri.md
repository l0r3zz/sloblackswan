## Incident Management for the Menagerie: When the Animals Attack

![][Eugene_F_Kranz_at_his_console_at_the_NASA_Mission_Control_Center]

### The Origins: From Emergency Rooms to War Rooms

Here's a dirty secret about incident management: we didn't invent it. We borrowed it from people who deal with actual emergencies, the kind where buildings collapse, chemicals spill, and helicopters need to land in the right place at the right time.

In the 1970s, California's emergency responders had a problem. When multiple agencies showed up to the same disaster: fire departments, police, hazmat teams, EMS, chaos ensued. Everyone had their own radio frequency. Everyone had their own chain of command. Everyone thought they were in charge. Coordination wasn't just difficult; it was nearly impossible.

The solution was the Incident Command System (ICS), developed through FIRESCOPE (Firefighting Resources of California Organized for Potential Emergencies). The insight was elegant: the problem wasn't firefighting or hazmat response or search and rescue. The problem was *human coordination under stress*. Different agencies, different expertise, different vocabularies, and somehow they all had to work together when everything was on fire (sometimes literally).

ICS gave them common terminology, clear authority structures, and scalable organization. It worked so well that by the 1990s it became the national standard for emergency response. FEMA adopted it. The military studied it. Hospital emergency rooms implemented versions of it.

And then, sometime around the late 1990s, IT folks started having the same realization.

Remember what incident response looked like in the early days of internet infrastructure? Your database crashes at 2 AM. Whoever answers the pager becomes the de facto "incident commander," not because they're qualified, but because they picked up the phone. Information scatters across email threads, IRC channels, and voicemails. Three different people make conflicting decisions about whether to failover. Recovery takes four hours instead of forty minutes because nobody knows who's doing what.

The parallels to pre-ICS emergency response were obvious.
Outtages in major service providers, while lives may not be at stake, significant revenue and perhapse the future of the enterprise may be. Both were high-stress environments where minutes matter. Teams werfe dealing with unclear situations  requiring rapid sense-making. There is a need for clear authority assignment without bureaucratic delay and the actions of multiple specialist teams have to be efficiently coordinated. It's easy for personel to experience information overload so the filtering and prioritization is necessary.

ITIL tried to codify this for enterprise IT in the 1980s. The DevOps movement brought it to software teams in the 2000s. But the real transformation happened when Ben Treynor Sloss built something new at Google.

In 2003, Treynor founded what would become Site Reliability Engineering, famously described as "what happens when you ask a software engineer to design an operations team." His team didn't just adopt ICS; they reimagined it for distributed systems and software engineers. They took principles designed for coordinating fire trucks and helicopters and adapted them for coordinating microservices and on-call rotations. The result became the foundation for modern tech incident management, codified in the 2016 Google SRE book that changed the industry [Beyer et al., 2016].
{::pagebreak /}
### The Google Model: SRE and the Incident Management Revolution

Google's Site Reliability Engineering organization didn't just adapt ICS, they transformed it for the reality of distributed systems operated by software engineers, not emergency responders.

The key insights:

**Incidents are Learning Opportunities, Not Failures**

Traditional IT incident management treated incidents as aberrations to be prevented. Google's SRE approach treats them as inevitable in complex systems and therefore valuable sources of learning.
This isn't semantic. It's fundamental. If incidents are failures, you hide them. If incidents are learning, you study them.

**Blamelessness as Infrastructure**

Google formalized what the best emergency responders already knew: blame destroys information flow.
As I've written elsewhere, the Unwritten Laws of Information Flow apply brutally during incidents [White, 2025]:

- **First Law**: Information flows to where it's safe. If engineers fear blame, they hide problems during the incident ("I thought it might be my deploy, but I didn't want to say...") and lie in retrospectives.
- **Second Law**: Information flows through trust networks. During incidents, you need information from the person who knows, not the person who's senior. Hierarchy kills speed.
- **Third Law**: Information degrades crossing boundaries. Every "escalation" loses context. Direct communication between domain experts is faster and more accurate.

Google's blameless postmortem culture isn't kindness. It's engineering for information flow.

**Runbooks as Code, Not Compliance Documents**

Google treats runbooks like software: versioned, tested, reviewed, and continuously improved. A runbook that hasn't been tested is fan fiction.

This matters because most IT organizations have runbooks that are written once during a calm period, tested only when the incident happens, and never updated until after an incident has been resloved... maybe. 

Google's approach: if you haven't practiced the runbook in a game day, you don't have a runbook.

**Chaos Engineering as Incident Prevention**

Google (and Netflix, and Amazon) discovered something counterintuitive: the best way to get better at incidents is to cause more incidents.

Controlled chaos, deliberately breaking things in production, serves multiple purposes. You can  tests your runbooks under realistic conditions. You can provide low stakes incident response training for your teams. And you may uncover hidden fragilities before they manifest as customer-impacting outages

This is antifragility in action: getting stronger through stress.


**Severity Levels That Match Impact**

Google's severity definitions are customer-impact-focused:

- **P0/SEV-1**: Customer-facing service completely down or severely degraded
- **P1/SEV-2**: Significant degradation of service functionality
- **P2/SEV-3**: Minor loss of functionality, workarounds available
- **P3/SEV-4**: Cosmetic issues, minimal customer impact

Note what's missing: server metrics. An incident isn't P0 because CPU is at 100%. It's P0 because customers can't use the service.

This distinction matters for our bestiary:

- A Black Swan might register as P0 within minutes
- A Grey Rhino might never trip a severity threshold until it finally fails catastrophically
- An Elephant in the Room creates chronic P3s that never escalate but destroy morale
- A Black Jellyfish cascade can go from P3 to P0 in under five minutes
![][incident-severity]
{::pagebreak /}
### The Incident Command System: A Foundation, Not a Straitjacket
#### **Physical ICS incidents vs. IT incidents:**

ICS assumes:

- Geographically bounded incidents (a fire, a building collapse)
- Physical response teams
- Clear roles based on agency (fire department, police, EMS)

IT incidents are:

- Geographically distributed (global services, remote teams)
- Virtual teams assembled ad-hoc
- Role boundaries based on technical domain, not organizational chart

Good incident management adapts ICS principles to IT reality rather than forcing IT reality into ICS structure.

#### **The Incident Command Team**

![][incident-response-team]

ICS provides a structure for coordinating complex responses. For IT incident management, we modify them a little to reflect a structure more relevant to SRE teams:
{::pagebreak /}
| Role | Primary Responsibility | Why It Matters |
|------|----------------------|----------------|
| **Incident Commander (IC)** | Overall incident management, strategic decisions | Single point of authority prevents chaos |
| **Communications Lead (Comms)** |Internal and external messaging | Manages information flow to stakeholders|
| **Scribe** | Documentation, prediction, resource tracking | Ensures organizational memory and future planning |
| **Technical Lead** | Manages and directs technical resolution effort | Focus on problem resolution, not politics |
| **Subject Matter Expert (SME)** | In the weeds of the effort| Bringing to bear technical expertise to the situation |

For small incidents, one person might wear multiple hats. For large incidents (especially Black Swans or stampedes), you need the full structure. Let's go into more detail on each role.

**The Incident Commander Role**

When things go sideways, the natural state of an org is chaos. Everyone starts "helping" in parallel. Three people declare three different root causes. Someone pings the CEO. Someone else starts a war in the status page comments. The Incident Commander exists to impose order on that mess.

The IC is not the hero debugger. The IC is the air traffic controller. They run the room, keep information flowing, make decisions when the data is incomplete, and protect the responders from becoming a stakeholder-driven improv troupe. At Google, this role got formalized because scaling systems without scaling coordination is just chaos at a higher QPS.

So what does an IC actually do? First, they declare the incident and take command early. The handoff has to be explicit - you announce "I'm IC" in the war room so everyone knows who's making decisions. There's no subtle assumption of leadership here. When the building's on fire, you need to know who's running the evacuation.

Then you set priorities, and the priority order matters: stabilize first, understand second, optimize later. Too many ICs try to solve the root cause while customers are still experiencing an outage. Stop the bleeding before you figure out why you're bleeding.

The IC maintains situational awareness across all workstreams. That means tracking what we know, what we don't know, and what we're trying next. It means making calls under uncertainty and keeping decision latency low. Waiting for perfect information means the incident lasts twice as long, and perfect information doesn't exist during a crisis anyway.

Part of that coordination is keeping roles clear. The Technical Lead drives technical strategy. SMEs investigate and execute. Communications handles updates. The Scribe captures reality as it unfolds. When roles blur, chaos returns. The IC's job is to prevent that blur.

Most importantly, the IC shields responders from external pressure. Every VP has an idea. Every customer success manager has a theory about what's wrong. Every executive who just discovered the Slack channel thinks "any update?" counts as helping. The IC filters that noise and lets the responders focus. You're the bouncer at the door of the war room, and most people don't get in.

Finally, the IC decides when to close the incident and transition cleanly into learning mode. That last part matters - incidents don't end when service is restored. They end when you've documented what happened, captured what you learned, and committed to the action items that prevent recurrence.

The most common failure mode? The IC grabs a keyboard. They stop running the room and start debugging. And the incident immediately reverts to an unmoderated group chat with better uptime graphs. Don't be that IC. Your job is coordination, not code. If you're typing grep commands, you're not doing your job.

**The Communications Lead Role**

During an incident, your engineers are trying to hold a complicated system in their heads while it actively betrays them. Now imagine also asking them to provide real-time updates to executives, customer support, and that one VP who just discovered the Slack channel and thinks "any update?" is a contribution. That's why the Communications Lead exists.

The Comms Lead is the pressure relief valve. They take messy, half-true technical reality and translate it into accurate, calm updates for humans. Done right, this role keeps the IC and Technical Lead focused, keeps stakeholders informed, and keeps the incident from turning into a second incident made of rumors. Tooling helps here - FireHydrant, Blameless, or whatever your org uses - because the best comms are consistent, timestamped, and boring in the most reassuring way possible.

The first thing a Comms Lead does is establish an update cadence and stick to it. Every 15 minutes, every 30 minutes, whatever fits the incident severity. And here's the critical part: you update even when there's nothing new to report. "No new ETA yet, still investigating" is a valid update. Silence makes stakeholders assume the worst. Regular boring updates keep them calm.

Then you translate technical status into stakeholder language without lying or speculating. The engineers are debugging packet loss in the service mesh. Stakeholders need to know "we're investigating network connectivity issues, estimated resolution within 2 hours." You're not dumbing it down. You're contextualizing it for people who need to make business decisions, not technical ones.

You coordinate with Support, Customer Success, PR, Legal, and executives on what gets said and when. Each of these groups needs slightly different information at different times. Support needs customer-facing language. Legal needs to know if there's a compliance impact. PR needs to know if this hits the news. Executives need strategic context. You're the conductor making sure everyone's playing from the same score.

Most importantly, you maintain a single source of truth - usually a status page plus an internal summary document. Without this, Slack becomes folklore. Someone posts speculation, it gets quoted as fact, and suddenly you're fighting rumors while trying to fix the actual problem. The single source of truth prevents that. Point everyone at the canonical document and update only that.

And like the IC, you protect responders from drive-by questions and context-free escalations. When someone asks "have we tried restarting it?" for the fifth time, you answer them so the engineers don't have to break focus. You're the shield between chaos and the people solving the problem.

The common failure modes are opposites: either the Comms Lead goes silent (stakeholders panic), or they overshare raw hypotheses (stakeholders panic faster). Silence creates a vacuum that fills with speculation. Oversharing turns tentative debugging into perceived commitments. The balance: frequent, calm, accurate updates that communicate what we know without promising what we don't.

**The Scribe Role**

If you don't write it down during the incident, you will rewrite history afterward. Not intentionally. Your brain will do it for you. Stress makes memory unreliable, and incidents are basically a live demo of that fact.

The Scribe is your external hard drive. They capture the timeline, decisions, hypotheses, and outcomes while everyone else is heads-down. Modern platforms like FireHydrant and others, can auto-capture a bunch of this, but automation isn't the job. The job is building a coherent narrative in real time: what we knew, when we knew it, what we tried, and why.

Start with the timeline. Maintain it in real time with timestamps. Not vibes ("around lunchtime"), not approximations ("mid-morning"), actual timestamps. "2024-01-15 14:23:17 UTC: Error rate spiked to 12%, customer reports increased." Precision matters because post-incident, you'll correlate this timeline with deploy logs, monitoring data, and customer impact. Fuzzy timestamps make that correlation impossible.

Record decisions and the rationale behind them. "We rolled back deploy #3421 because p99 latency doubled from 200ms to 450ms after it shipped, and the error rate correlation was .94." Not just "we rolled back." Capturing why you decided helps future incidents and prevents second-guessing during postmortems. When decisions are made under uncertainty - which is most decisions - document what information you had at decision time.

Track action items and owners during the incident. Not the cleanup items for later. The right-now items. "SME database investigating connection pool exhaustion, SME network checking for packet loss, TL coordinating both workstreams." This tracking keeps the IC from asking "wait, who's looking at the cache layer?" six times. Everyone can glance at the doc and see who owns what.

Capture key artifacts. Links to dashboards, log queries, config changes, runbook pages, graphs someone screenshots, anything that helps tell the story. These artifacts disappear fast - dashboards auto-refresh, logs age out, screenshots get lost in Slack. The Scribe grabs them and pins them to the incident document before they evaporate.

And periodically - every 15-20 minutes - summarize for the IC so the room stays aligned. "Current state: Error rate 8%, down from 12% peak. Database team found connection pool exhaustion, applied mitigation. Network team ruled out packet loss. Next step: validate mitigation is working." This summary keeps everyone operating from the same mental model of reality.

The common failure mode: the Scribe becomes a stenographer for Slack spam instead of a curator of signal. They copy-paste every message from the war room channel into the doc. The result is a 400-line document of noise with the actual signal buried somewhere around line 247. Don't transcribe Slack. Curate the narrative. Your job is building a story that makes sense, not creating a logfile.

**The Technical Lead Role**

The Incident Commander runs the room. The Technical Lead runs the work. That separation is the whole point. The IC is optimizing for coordination and decision-making under uncertainty. The Technical Lead is optimizing for "how do we stop the bleeding without making it worse?"

The Technical Lead manages the technical strategy: containment, mitigation, recovery, and validation. They direct the SMEs, choose which hypotheses to pursue, and keep the team from turning twelve unrelated fixes into performance art. They also do something subtle but critical: they keep the response shaped like a funnel - wide exploration early, narrow focus once evidence shows up.

So what does that look like in practice? The Technical Lead starts by leading technical triage. They form hypotheses about what's wrong, design tests for those hypotheses, and converge on likely causes. Not "I think it's the database" as speculation, but "if it's the database, we'd see X metric behaving Y way, and we'd expect Z symptom in the logs." Form testable hypotheses, then test them.

Then they direct the SMEs and split workstreams cleanly. One SME investigates the database. Another checks network connectivity. A third looks at the cache layer. The split is clean - no overlap, no duplicate effort, no random heroics where someone decides to debug three unrelated things simultaneously. Parallel investigation with clear ownership.

As evidence comes in, the Technical Lead proposes mitigation steps to the IC with risk framing. Not "let's restart the service," but "we can restart the service - that's reversible if it doesn't work, low risk. Or we can failover to the backup region - that's high impact but irreversible in the short term, higher risk." The IC makes the call, but they need that risk context to make it intelligently.

After the IC approves action, the Technical Lead validates recovery. Service restored isn't enough. Are error rates actually stable? Is p99 latency back to normal? Are we seeing any hidden second-order failures - did fixing the database overload something downstream? Validation prevents declaring victory while the system smolders.

And throughout the incident, the Technical Lead calls out when the situation has shifted domains. You started in Complicated - investigating with experts. But twenty minutes in, you realize this is actually Complex - no amount of analysis is revealing the answer, you need to start probing. That domain shift changes the strategy, and the Technical Lead needs to announce it so everyone adapts their approach.

The most common failure mode? The Technical Lead tries to be the best debugger in the room instead of the person coordinating the debuggers. They grab a terminal and start running queries instead of directing the SME who owns that subsystem. They solve one piece of the problem personally while three other pieces stay uncoordinated. Your job is orchestration, not implementation. Even though the temptation is great to jump into the fight, stay one level above the weeds.

**The Subject Matter Expert (SME) Role**

SMEs are the ones in the weeds. They know the service, the dependency graph, the failure modes, and which "simple restart" will actually detonate the remaining working parts. They are the reason your incident response isn't just confident guessing.

An SME's job is not to "own the incident." It's to own a slice of the technical problem space and report back with evidence. The best SMEs stay brutally factual under pressure: what they're seeing, what they tried, what changed, and what they recommend next. They don't need to be loud. They need to be right.

The SME investigates a specific subsystem or domain. The database SME investigates the database. The network SME checks network connectivity. The auth SME looks at authentication flows. The storage SME examines disk and cache behavior. You own your domain, and you go deep - not broad. No database SME should be debugging the web tier unless the Technical Lead explicitly redirects them.

And the updates you provide to the Technical Lead need to be evidence-based, not just theories. Not "I think it might be connection pool exhaustion" but "Connection pool is at 98% capacity for the last 15 minutes, correlates with error rate spike at 14:23 UTC. Pool exhaustion is confirmed, not speculated." Evidence changes how the Technical Lead prioritizes your findings.

When it comes time to execute mitigations, SMEs do it safely - with rollbacks and guardrails when possible. You're not cowboy-fixing things in production. If you're increasing a connection pool size, you test on staging first if time permits. If you're restarting a service, you verify the dependency chain won't cascade. If you're pushing a config change, you push to one instance before rolling to the fleet. Safe execution matters because making the incident worse is worse than taking another five minutes to do it right.

And you identify hidden dependencies and second-order effects before they bite you. "If we flush this cache, it'll spike database load by 300% until the cache rewarms." "If we restart this service, it'll reconnect to all downstream services simultaneously and create a thundering herd." You know your subsystem deeply enough to predict the ripple effects, and you surface those predictions before the Technical Lead commits to a plan.

After the incident, you contribute to post-incident learning with precise technical context. Not "the database was slow" but "Connection pool exhaustion due to increased query load from the new recommendation engine, pool size hadn't been scaled since March, recommendation engine went to 100% traffic on January 10th." That precision helps the postmortem generate useful action items instead of vague "improve database monitoring."

The common failure mode: SMEs chase the most interesting problem, not the most incident-relevant one. You're a database expert, and you notice an interesting query optimization opportunity while investigating. The optimization isn't causing the outage, but it's technically fascinating, so you go down that rabbit hole while the actual problem stays unfixed. Stay disciplined. Solve the incident-relevant problem first. Log the interesting tangent for later.


{::pagebreak /}
#### **The ICS Principles That Matter for IT:**

1. **Unity of Command**: Every person reports to one person. No conflicting orders.

2. **Manageable Span of Control**: ICs should manage 3-7 direct reports. Beyond that, delegate.

3. **Common Terminology**: No acronyms that aren't shared. No jargon that creates confusion.

4. **Integrated Communications**: Everyone shares the same information environment. (This is where Slack, Zoom war rooms, and shared docs become critical infrastructure.)

5. **Establishment of Command**: The IC is declared early and clearly. "I'm taking IC" is an explicit handoff.

![][ICS-4-IT]
{::pagebreak /}

### Anatomy of an Incident
![][anatomy-of-an-incident]

Before moving further, let's get closure on some important traditional  terms around incidents. 

| Acronym | Name | Definition |
|--------|------|------------|
| **MTTF** | Mean Time To Failure | Duration of normal operation before an incident occurs. Represents system stability leading up to a failure. |
| **TTD** | Time To Diagnose | Time from the moment the incident begins until the underlying problem is identified, when responders understand what is failing and why. |
| **TIA** | Time To Action | Time from incident start (or investigation start) to the first meaningful corrective action. Covers human response and system triage before mitigation begins. |
| **ETRS** | Estimated Time to Restore Service | Time from incident start until service is restored to a functional, customer-usable state. Restoration does not necessarily imply full resolution. |
| **ETTR** | Estimated Time to Resolution | Time from incident start until the underlying issue is fully remediated and the system is back in normal operation (restore → fix → verify → monitor). |
| **MTBF** | Mean Time Between Failure | Full cycle time between the end of one incident and the beginning of the next: MTTF → (TTD + TIA + ETRS + ETTR) → next MTTF. |


This is the traditional view of the time line of an incident. You may see these things defined differently in other documents or by other authors. To a certain extent, these definitions have become sort of a religious thing in the incident management community.  But we're going to assert that this model is somewhat outdated. They measure internal process efficiency, but not customer impact.

#### The Traditional KPIs (And Why They're Incomplete)

The incident management community has standardized on four KPIs: MTTD (Mean Time to Detect), MTTA (Mean Time to Acknowledge), MTTR (Mean Time to Resolve), and Incident Frequency. These became "sort of a religious thing" because they're measurable, trackable, and make pretty dashboards. But they measure internal process efficiency, not customer pain or organizational learning.

Take MTTD. It measures time from incident start to detection, which matters because faster detection means faster response. Straightforward enough. But it assumes all incidents are equally detectable. Black Swans by definition can't be detected before they happen - you're measuring a capability that doesn't apply. Grey Rhinos were detected months ago, so detection time is irrelevant when the problem is organizational unwillingness to act. The metric optimizes for a capability that doesn't apply uniformly across the bestiary.

MTTA measures time from alert to human acknowledgment. It's supposed to measure on-call responsiveness, and it does - sort of. But acknowledging an alert doesn't equal understanding the incident. You can acknowledge instantly and still be confused for hours. Your MTTA looks great on the dashboard while your customers are screaming. It measures process compliance, not incident comprehension.

MTTR measures time from detection to resolution, which directly correlates with customer pain duration. This one matters more than the others because it tracks something customers actually experience. But "resolution" is often gamed. Did you fix the root cause or apply a band-aid? Did you learn anything or just restore service? MTTR rewards speed over learning, which means organizations optimize for closing the ticket rather than understanding the problem. Fix it fast, learn nothing, repeat the same incident next month. Great MTTR, terrible organizational learning.

MTBF is the average amount of time you can expect to go before another incident occurs , but the metric is completely context-free. One Black Swan matters more than ten minor incidents. Frequency without severity context is noise. You can have low incident frequency and still be fragile - you're just lucky you haven't been tested yet. Or you can have high incident frequency because you're practicing chaos engineering and deliberately breaking things to learn. The number alone tells you nothing.
{::pagebreak /}
#### The KPIs That Actually Matter

Here are a set of KPI's that align with what customers experience and what organizations learn:

| KPI | Definition | Why It Matters | Measurement Challenge |
|-----|-----------|----------------|----------------------|
| **Customer-Impacting Downtime** | Total minutes of degraded or unavailable service, weighted by users affected | Directly measures customer pain | Requires honest assessment, not gaming |
| **Time to Understanding** | Duration from incident start to comprehending what's wrong | Understanding precedes fixing | Subjective, requires honest incident timeline |
| **Decision Latency Under Uncertainty** | Time from "we need to decide" to action when information is incomplete | Tests organizational adaptability | Hard to measure, critical for Black Swans |
| **Information Flow Velocity** | Time for critical context to reach decision-makers | Tests org structure and culture | Requires tracing communication paths |
| **Postmortem Quality Score** | Depth of learning, actionability of items, honesty of analysis | Indicates whether org is learning | Requires qualitative assessment |
| **Action Item Completion Rate** | Percentage of postmortem action items actually completed | Tests whether learning translates to improvement | Easy to measure, often embarrassing |
| **Repeat Incident Rate** | Percentage of incidents that are similar to previous ones | Indicates failure to learn | Requires classification and memory |
| **Cross-Team Coordination Efficiency** | Quality of coordination when incident spans multiple teams | Tests org structure and communication | Qualitative, based on participant feedback |
| **Psychological Safety Index** | Willingness of team to surface uncomfortable truths in retrospectives | Foundation for all learning | Measured via surveys and retrospective quality |
{::pagebreak /}
#### KPI Relevance by Animal Type

Different animals make different KPIs relevant:

| KPI | Black Swan | Grey Swan | Grey Rhino | Elephant | Black Jellyfish |
|-----|-----------|-----------|-----------|----------|----------------|
| **MTTD** | Low relevance (undetectable) | High relevance (should catch early) | Low relevance (already detected) | Low relevance (everyone knows) | Medium relevance (cascade detection) |
| **MTTR** | High relevance (speed of adaptation) | High relevance | Medium relevance (knew the fix) | Low relevance (org issue) | High relevance (cascade containment) |
| **Time to Understanding** | **Critical** (novel situation) | High relevance | Low relevance (understood already) | Medium relevance | High relevance (complex cascade) |
| **Decision Latency** | **Critical** (rapid decisions needed) | High relevance | Medium relevance | Low relevance | **Critical** (speed matters) |
| **Information Flow Velocity** | **Critical** (need all context) | High relevance | Medium relevance | **Critical** (if elephant revealed) | High relevance |
| **Postmortem Quality** | **Critical** (learning from unprecedented) | High relevance | Medium relevance | **Critical** (cultural issues) | High relevance |
| **Action Item Completion** | High relevance | High relevance | **Critical** (finally fixing it) | **Critical** (cultural change) | High relevance |
| **Repeat Incident Rate** | Low relevance (swans don't repeat) | Medium relevance | **Critical** (did we fix it?) | **Critical** (pattern of avoidance) | Medium relevance |
| **Cross-Team Coordination** | **Critical** (novel requires diverse expertise) | High relevance | Low relevance | Medium relevance | **Critical** (cascade crosses boundaries) |
| **Psychological Safety** | High relevance | Medium relevance | High relevance | **Critical** (root cause) | Medium relevance |

**Key Insight**: Black Swans and Black Jellyfish demand the highest performance on organizational adaptability KPIs (decision latency, information flow, coordination). Grey Rhinos and Elephants demand the highest performance on organizational honesty KPIs (action item completion, psychological safety, repeat incidents).

The animals reveal what your organization is actually good at. If you handle Black Swans well but have high repeat incident rates, you're good at crisis adaptation but bad at learning and follow-through. If you have low repeat incidents but terrible decision latency, you're good at process but bad at speed.

Use KPIs diagnostically to understand organizational strengths and weaknesses across the bestiary.
{::pagebreak /}
#### Practical Measurement Methods for Qualitative KPIs

The traditional KPIs (MTTD, MTTR) are easy to measure - they're numbers. The KPIs that actually matter (decision latency, information flow velocity, postmortem quality) require qualitative assessment. Here's how to measure them.

**Decision Latency Under Uncertainty**

**What it measures:** Time from "we need to decide" to action when information is incomplete.

**Measurement Method**

**1. Timeline Analysis:**

- Review incident timeline
- Identify decision points: "Should we failover?" "Should we roll back?" "Should we escalate?"
- Measure time from decision point identification to action taken
- Note information available at decision time (percentage complete)

**2 .Decision Point Identification:**

- During incident: Scribe captures decision points in real-time
- Tag each decision: "Decision needed: [what], Information available: [%], Time to decide: [duration]"
- Post-incident: Analyze decision latency for each point

**3. Qualitative Assessment:**

- Decision made in <15 minutes with <30% information = Low latency (good for Black Swans)
- Decision made in >60 minutes with >70% information = High latency (may be appropriate for Complicated, bad for Chaotic)
- Pattern: Consistently high latency in Chaotic domains = organizational problem

**Example:**
 "Decision to failover: Identified at T+12, decided at T+28, executed at T+30. Information available: 25%. Decision latency: 16 minutes."
{::pagebreak /}
**Information Flow Velocity**

**What it measures:** Time for critical context to reach decision-makers.

**Measurement Method:**

**1. Communication Path Tracing:**

- During incident: Scribe tracks information flow
- Identify critical information: "Engineer A noticed anomaly X"
- Trace path: A → B → C → IC
- Measure time at each hop: A noticed at T+5, told B at T+8, B told C at T+12, C told IC at T+18
- Total latency: 13 minutes (from T+5 to T+18)

**2. Path Comparison:**

- Compare actual path (trust networks) vs org chart path
- Measure latency difference
- Identify bottlenecks (which hops take longest?)

**3. Post-Incident Review:**

- Ask: "Who knew what when?"
- Map information flow diagram
- Identify: Where did information get stuck? Why?

**Example:** 
"Critical info: DNS anomaly. Path: Junior engineer (T+0) → Trusted teammate (T+3) → Senior engineer (T+7) → IC (T+12). Org chart would have been: Junior engineer → Manager → Director → VP → IC (estimated T+45). Trust network was 3.75x faster."
{::pagebreak /}
**Postmortem Quality Score**

**What it measures:** Depth of learning, actionability of items, honesty of analysis.

**Measurement Method: Qualitative Rubric**

**Rate each postmortem on 1-5 scale:**

**1. Honesty (Are people telling the truth?)**

- 5: Multiple people admit mistakes, confusion, disagreements
- 4: Some people admit mistakes
- 3: Mistakes mentioned but not attributed
- 2: Only "system" or "process" failures, no human errors
- 1: Narrative is too clean, no one admits anything

**2. Depth of Analysis (Do we understand root causes?)**

- 5: Systemic root causes identified (organizational, cultural, technical)
- 4: Technical root cause with contributing factors
- 3: Technical root cause identified
- 2: Symptom identified, not root cause
- 1: No analysis, just "incident happened, we fixed it"

**3. Actionability (Are action items specific and trackable?)**

- 5: Action items are specific, measurable, owned, with timelines
- 4: Action items are specific and owned
- 3: Action items exist but vague
- 2: Generic "improve monitoring" without specifics
- 1: No action items, or items impossible to complete

**4. Learning Transfer (Will this help future incidents?)**

- 5: Postmortem teaches reusable patterns, principles, frameworks
- 4: Postmortem teaches lessons applicable to similar incidents
- 3: Postmortem documents what happened
- 2: Postmortem describes incident but no lessons
- 1: Postmortem is just a timeline, no learning

**Scoring:**

- 18-20 points: Excellent postmortem
- 14-17 points: Good postmortem
- 10-13 points: Adequate postmortem
- 6-9 points: Poor postmortem (needs improvement)
- 1-5 points: Theater (not real learning)
{::pagebreak /}
**Psychological Safety Index**

**What it measures:** Willingness of team to surface uncomfortable truths.

**Measurement Method:**

**1. Postmortem Survey (Anonymous):**

- "Did you feel safe admitting mistakes during this postmortem?"
- "Did you hold back information because you feared consequences?"
- "Did you disagree with decisions made during the incident but not speak up?"
- Rate each 1-5 (1=strongly disagree, 5=strongly agree)
- Aggregate scores across team

**2. Retrospective Observation:**

- Observe postmortem behavior:
- Do people admit mistakes?
- Do junior people speak up?
- Do people disagree with senior people?
- Do people ask questions without fear?

**3. Pattern Analysis:**

- Track psychological safety across multiple postmortems
- Identify trends: improving or degrading?
- Correlate with incident outcomes: Does psychological safety correlate with faster resolution?

**Example Survey Questions:**

- "I felt comfortable admitting I made a mistake" (1-5)
- "I felt comfortable disagreeing with senior people" (1-5)
- "I held back information because I feared consequences" (reverse scored)
- "I felt safe asking questions without looking stupid" (1-5)

**Aggregate Index:** Average of all responses. Track over time to measure improvement.
{::pagebreak /}
**Cross-Team Coordination Efficiency**

**What it measures:** Quality of coordination when incident spans multiple teams.

**Measurement Method: Qualitative Assessment**

**Post-Incident Survey to Participants:**

**1. Communication Effectiveness:**

- "Information flowed smoothly between teams" (1-5)
- "We had clear channels for cross-team communication" (1-5)
- "Conflicts between teams were resolved quickly" (1-5)

**2. Role Clarity:**

- "Each team knew their responsibilities" (1-5)
- "We avoided duplicate work across teams" (1-5)
- "Decision-making authority was clear" (1-5)

**3. Coordination Quality:**

- "Team coordination enabled faster resolution" (1-5)
- "We synthesized information effectively across teams" (1-5)
- "IC coordinated teams without micromanaging" (1-5)

**Aggregate Score:** Average across all questions. Higher = better coordination.

**Qualitative Indicators:**

- Low score + fast resolution = Teams worked independently (may indicate good isolation)
- Low score + slow resolution = Coordination problems hurt response
- High score + fast resolution = Good coordination helped response
- High score + slow resolution = Coordination good but other factors slowed response

**Implementation Tips:**

- Start with one KPI at a time (don't try to measure everything at once)
- Use existing incident data (timelines, postmortems) rather than adding new processes
- Make measurement lightweight (don't create bureaucracy)
- Focus on trends over time, not individual incident scores
- Share results with teams to drive improvement (not punishment)

**Remember:** These are qualitative measures. They require judgment. The goal isn't perfect measurement - it's identifying patterns and trends that reveal organizational strengths and weaknesses.
{::pagebreak /}
### Culture as Incident Management Infrastructure

Before we dive into animal-specific incident management, we need to address the foundation that makes everything else possible: culture.


#### The Unwritten Laws in Practice

As described in my earlier work on information flow [White, 2025], these laws manifest during incidents:

**First Law: Information Flows to Where It's Safe**

During incidents, you need information from people who might have made a mistake that contributed to the incident, from junior engineers who are afraid to speak up, from people working in different organizations with different incentives, and from anyone with context that contradicts what leadership believes. If these people fear punishment, they stay silent. You operate with incomplete information. You make worse decisions. The incident lasts longer and causes more damage.

Blamelessness isn't about protecting feelings. It's about getting the information you need to fix the problem.

**Second Law: Information Flows Through Trust Networks, Not Reporting Lines**

Your org chart is a comforting fiction. Real information during incidents flows like this:

```
Actual information flow during incident:
Engineer A (noticed anomaly) 
  → Engineer B (A's trusted former teammate, now different team)
    → Senior Engineer C (B's mentor)
      → IC (C knows them from previous incident)

Org chart says information should flow:
Engineer A 
  → A's manager 
    → Director 
      → VP 
        → IC
```

By the time information traverses the org chart, the incident is over or the context is destroyed.

Good incident management creates direct channels between domain experts and decision-makers, regardless of hierarchy. War rooms, Slack channels, and Zoom bridges exist to short-circuit the org chart.
{::pagebreak /}
**Third Law: Information Degrades Crossing Boundaries**

Every hop in the communication chain loses fidelity. Technical precision becomes "there's a database problem." Urgency calibration fails - what's P0 for them becomes P3 for us. Nuance dies - "just restart it" gets passed along when restart will actually make it worse.

Good incident management minimizes hops by bringing domain experts into the war room directly, using shared documents everyone can edit, preferring synchronous communication (call over Slack over email), and recording decisions and context in real-time.

#### Building the Culture That Makes Incident Management Work

**Blameless Postmortems as Practice, Not Policy**

Every organization claims to have blameless postmortems. Few actually do.

The test: In your last postmortem, did anyone admit they:

- Made a mistake that contributed to the incident?
- Didn't understand something they should have?
- Were confused during the incident and afraid to ask?
- Disagreed with a decision but didn't speak up?

If no one admitted any of these things, your postmortem was theater. Real incidents involve human error, confusion, and miscommunication. If your postmortem doesn't reflect that, people are hiding the truth.

**Psychological Safety as Technical Requirement**

Google's Project Aristotle found psychological safety was the #1 predictor of team effectiveness [Duhigg, 2016]. For incident management, it's not just important, it's foundational.

Psychological safety means:

- You can admit you don't know something
- You can disagree with senior people
- You can surface bad news without fear
- You can make mistakes and learn from them

Without psychological safety, your incident management degrades in predictable ways. People hide problems, which means late detection. They won't speak up with critical context, which slows understanding. They won't admit mistakes, which produces poor postmortems. They won't take reasonable risks, which creates slow decision-making under uncertainty. Every failure mode traces back to fear of consequences for telling the truth.

Build psychological safety deliberately. Leaders model vulnerability - they admit mistakes, say "I don't know," and show that uncertainty is acceptable. When someone brings bad news or dissents from the prevailing theory, thank them explicitly. Make it visible that surfacing problems is valued, not punished. Never punish someone for being wrong, but do punish hiding information. That distinction matters: errors are learning opportunities, concealment is organizational poison. Celebrate learning, not perfection, because incidents are inherently imperfect situations and learning requires honest examination of what went wrong.

And critically: follow through. If someone shares uncomfortable truth and then faces retaliation, you've destroyed psychological safety permanently. Protection has to be real, not performative.

**Documentation as Time-Shifted Information Flow**

The Unwritten Laws [White, 2025] apply to documentation:

Information flows to where it's safe: If postmortems are used for performance reviews, they'll be sanitized fiction.

Information flows through trust: The best postmortems are written by the people who lived through the incident, not by a "documentation specialist" three levels removed.

Information degrades crossing boundaries: Document while the incident is fresh (within 48 hours). Wait two weeks and the nuance is gone.

Good postmortem culture:

- Written by responders, not observers
- Shared widely (information wants to be free)
- Focused on learning, not compliance
- Action items tracked to completion
- Revisited after time to see what predictions were right

Now, with foundation established, let's examine how incident management differs across our bestiary.

But before we can do that, we need one more tool: a way to think about how to think about incidents. Culture provides the foundation, but different types of problems require different types of thinking. That's where the Cynefin Framework comes in.

---
{::pagebreak /}
### The Cynefin Framework for Incident Response

Before we dive into animal-specific incident management, we need one more tool: a way to think about how to think about incidents.

ICS gives us structure. Google SRE gives us practices. But none of them answer the fundamental question: **How should we think about this problem?**

That's where the Cynefin Framework comes in. Developed by Dave Snowden in the late 1990s, Cynefin (pronounced "kuh-NEV-in") is a sense-making framework that categorizes situations based on the relationship between cause and effect [Snowden & Boone, 2007]. The name is Welsh for "the place of your multiple belongings," representing the multiple factors in our environment that influence us in ways we can never fully understand.

For incident response, Cynefin provides something critical: **Different types of problems require different types of thinking.** Using the wrong approach wastes time, makes things worse, or both.
![][cynefin-framework]
{::pagebreak /}
#### Why SREs Need This

Modern distributed systems are inherently complex. Incidents don't follow predictable patterns. The framework gives you a mental model for:

1. **Classifying the incident** - What kind of problem is this?
2. **Choosing the right response strategy** - How should we think about this?
3. **Avoiding common mistakes** - What not to do in this situation
4. **Transitioning between states** - How incidents evolve and how to guide that evolution

The key insight: **ordered domains** (right side of the framework) have discoverable cause-and-effect relationships. **Unordered domains** (left side) have relationships that can only be understood in hindsight or not at all.

#### The Five Domains

The framework divides all situations into five domains arranged around a central area:

#### Domain 1: Clear (Simple/Obvious) - "The Recipe Domain"

Start with the easy stuff. The Clear domain is where cause and effect are obvious to any reasonable person. You see the problem, you know what it is, you know how to fix it. Best practices exist and are well-established. The solution is known and repeatable. Following procedures produces predictable results. This is your runbook territory.

The decision heuristic for Clear domains is Sense → Categorize → Respond. You sense the situation: the service is down, alerts are firing, you can see exactly what failed. You categorize it: this matches the database connection pool exhaustion pattern you've seen twelve times before. You respond: apply the standard solution from runbook #23, increase the pool size, restart the service. Done. Incident resolved in 15 minutes because you've done this exact thing before and documented it.

What does this look like during an actual incident? Service restart following documented procedure. Applying a known patch for a recently disclosed vulnerability. Following a runbook for that database issue that happens every Tuesday when batch processing runs. Standard deployment rollback when you catch a bad deploy during canary testing. These are the problems where experience compounds - you've seen it before, you fixed it before, you wrote down how to fix it, now you just execute.

What works in Clear domains: runbooks, playbooks, standard operating procedures, best practices, automation, scripts. Everything that converts "we know how to do this" into "we've automated doing this." This is where the investment in documentation pays off. Good runbooks in Clear domains mean junior engineers can resolve incidents without escalating, which means your senior engineers sleep through the night instead of fixing database connection pools at 2 AM.

What doesn't work: overthinking simple problems. Calling in experts when a runbook exists. Experimenting when a solution is known. Ignoring established procedures because you want to try something clever. Clear domain incidents reward following the recipe, not improvising.

But here's the danger - what I call the cliff edge. Clear domains have a sharp boundary with Chaotic. If you're following a recipe and something fundamental changes, you can suddenly find yourself in chaos. Your standard database restart procedure works 99% of the time. But when the underlying storage system fails, following that same procedure makes things worse - the database comes up, can't reach storage, cascades errors to every connected service, and now you've amplified the problem. You thought you were in Clear, applying best practices. You were actually in Chaotic, and your best practices became accelerant.

For incident management: Most routine incidents - your P3s and P4s - live in the Clear domain. They're the "known knowns." We know what they are, we know how to fix them, we've documented the fix. The danger is when teams treat Complex or Chaotic incidents as Clear, applying runbooks that don't fit. That's not efficiency. That's denial. If your runbook doesn't match what you're seeing, you're not in Clear anymore. Stop following the recipe and reassess.

#### Domain 2: Complicated - "The Expert Domain"

One level up from Clear: the Complicated domain. Here, cause and effect relationships exist, but they're not obvious. You need expertise to find them. Multiple valid solutions may exist. The answer is discoverable through investigation - you can figure it out, but not by following a runbook. You need experts with diagnostic tools and systematic methods.

The decision heuristic shifts: Sense → Analyze → Respond. You sense the situation - gather information, collect metrics, pull logs, get the shape of the problem. Then you analyze using expert knowledge, tools, and investigation to understand cause and effect. Only after analysis do you respond with the solution. The key difference from Clear: you have to discover the answer through investigation. It's not in a runbook yet.

Let's get concrete. Database performance degradation requiring query analysis. You see high latency, but it's not the standard connection pool exhaustion pattern. An expert database engineer has to pull query logs, analyze execution plans, identify the pathological query that's causing the spike, and recommend an optimization. That's Complicated. Network routing issues requiring packet capture and analysis. Memory leak investigation requiring profiling tools to find where the heap's bleeding out. Security incident requiring forensic analysis to trace the attack path. Root cause analysis of a production bug where the symptoms don't immediately reveal the cause.

What works in Complicated domains: expert consultation, systematic investigation, data collection and analysis, multiple perspectives from different experts, diagnostic tools and techniques, formal analysis processes. You're bringing expertise and methodology to bear on a problem that yields to systematic investigation. This is where your principal engineers and specialists earn their keep.

What doesn't work: rushing to action without analysis. You'll fix the wrong thing. Ignoring expert advice because you want to move fast. Applying simple solutions to complicated problems - restarting services when you need to rewrite queries. Analysis paralysis, where experts disagree indefinitely about the best approach and no one makes a decision. And treating the problem as simple when expertise is genuinely needed - that causes junior engineers to waste hours applying runbooks that don't fit.

Here's the expert trap, and it's insidious: in Complicated domains, experts can become entrenched in their viewpoints. Multiple valid solutions exist, and experts will argue indefinitely about which is "best." The database expert wants to optimize queries. The infrastructure expert wants to scale hardware. The application expert wants to refactor code. All three solutions might work, but while they're debating architectural philosophy, the incident continues.

This is where the IC's job becomes critical. Gather expert opinions. Listen to the options. Then make a decision when experts disagree. You're not picking the "best" solution - you're picking a good-enough solution that stops the customer pain. Avoid analysis paralysis. And critically, recognize when the situation has moved from Complicated to Complex - when no amount of analysis will reveal the answer because the system behavior is emergent, not deterministic.

For incident management: Grey Swans often start in the Complicated domain. We know something is wrong, we can investigate, but the answer isn't immediately obvious. The weak signals were there, but connecting them requires expert analysis. Grey Rhinos that finally charge often require Complicated-domain analysis afterward to understand why they were ignored and how to prevent recurrence. You're not dealing with novel phenomena. You're dealing with phenomena that require expertise to decode.

#### Domain 3: Complex - "The Experimentation Domain"

Here's where it gets uncomfortable for engineers: the Complex domain is where cause and effect only become clear after the fact. You can analyze all you want - gather logs, examine metrics, interview witnesses - but the system won't yield its secrets through investigation alone. The situation is emergent. Patterns appear over time through interaction of multiple factors, and your mental models - all those hard-won heuristics from solving Complicated problems - don't apply here.

This is the domain of distributed systems failures you've never seen before, cascading outages where the root cause isn't a single component but an interaction pattern, and Black Swan incidents where your existing understanding actively misleads you. Multiple factors interact in ways you can't predict upfront. No amount of analysis will reveal the answer because the answer doesn't exist yet - it emerges from the system's behavior. The only way forward is experimentation.

The decision heuristic for Complex domains is Probe → Sense → Respond. That means you run safe-to-fail experiments to explore the problem space. You're not testing a hypothesis like "I think it's the database." You're probing the system to see what emerges. Then you observe what actually happens - not what you expect to happen. And then you adapt based on what you learned and probe again. It's iterative, it's uncomfortable, and it's the only approach that works when cause-and-effect is emergent rather than deterministic.

Let's be concrete about what this looks like during an incident. You're seeing a novel system failure - something that doesn't match any known precedent. Instead of gathering more diagnostic data (that's Complicated-domain thinking, and it won't help), you might route 10% of traffic to a different region to see if the issue is regional. That's a safe-to-fail probe: if you're wrong, you've only affected 10% of traffic, and you can revert immediately. But if you're right, you've learned something about the problem space. You observe what emerges from that experiment, then design your next probe based on what you learned.

This feels wrong to engineers trained on deterministic systems. You want to understand before you act. But in Complex domains, understanding comes through action, not analysis. The pattern reveals itself through experimentation, and trying to analyze your way to an answer just wastes time while the incident continues. Your intuition - your pattern-matching capability built from years of experience - actively works against you here because the patterns don't match anything you've seen before.

So what works in Complex domains? Safe-to-fail experiments. Multiple parallel probes. Observing emergent patterns. Iterative adaptation. Learning from small failures. Building understanding over time. You're not solving the problem immediately. You're discovering what the problem is through experimentation, and then solving it.

What doesn't work: trying to analyze your way to an answer. Waiting for perfect information before acting - perfect information won't arrive. Applying expert solutions without testing - expert solutions are based on past patterns, and Complex means the patterns are novel. Command-and-control management - you can't command your way out of emergent complexity. Expecting immediate results - Complex problems don't resolve quickly. And treating the situation as Complicated when it's truly Complex - that burns time applying analytical methods to a system that won't yield to analysis.

The key technique here is safe-to-fail probes. These are experiments designed so failure is acceptable - the experiment won't make things worse. Learning is guaranteed - even if the experiment fails, you learn something. Cost is low - the experiment doesn't consume critical resources. And there's reversibility - you can undo the experiment if needed.

Examples during incident response: Route 10% of traffic to a different region to test if it's regional. Disable a specific feature to test if that feature is triggering the problem. Manually trip a circuit breaker to see if it breaks a cascade. Gradually reduce load to find the breaking point. Temporarily disable a dependency to test its impact. None of these are solutions. They're probes that teach you about the system's behavior without making things worse.

The goal: move from Complex to Complicated. As you run probes and learn, patterns emerge. The situation should transition from Complex (unknown unknowns) to Complicated (known unknowns). Once you're in Complicated territory, you can apply expert analysis. The key is patience. Complex problems don't resolve quickly, and trying to force speed just makes you thrash.

For incident management: Black Swans almost always start in Complex or Chaotic domains. Grey Swans often transition from Complicated to Complex as you realize the problem is more emergent than analyzable - those weak signals existed, but their interaction creates unpredictable outcomes. The framework provides a structured way to handle these situations without panicking or applying strategies that don't fit. You're not failing to solve the problem. You're appropriately matching your response to the problem's nature.

#### Domain 4: Chaotic - "The Crisis Domain"

Now we're in the deep end: the Chaotic domain. Cause and effect relationships are constantly shifting. No visible patterns exist. Immediate action is required to stabilize. The system is in crisis, and there's no time for analysis or experimentation. Your only goal is to establish order. Stop the bleeding. Prevent the cascade. Keep the failure contained before it metastasizes into something worse.

The decision heuristic flips: Act → Sense → Respond. Not "understand then act" but "act immediately, then understand what happened." You act to stabilize the situation - failover, rollback, shed load, whatever stops the crisis from spreading. Once stabilized, you sense - assess what's happening now that things aren't actively burning. Then you respond - make strategic decisions based on what you've learned. Understanding comes after stabilization, not before.

What does Chaotic look like? Complete system outage affecting all users. Active security breach in progress. Data center failure. Cascading failure spreading rapidly across services. Black Swan incident in early stages. Any P0 incident where the system is actively degrading and every second of delay makes it worse. This is where hesitation kills.

What works in Chaotic domains: immediate action to stop the bleeding. Failover procedures - route traffic away from failing systems. Load shedding - reduce load to prevent cascade. Emergency rollbacks - revert to last known good state. Kill switches - disable problematic services or features. IC taking control immediately. Rapid decision-making with minimal information. Stabilization first, understanding second. Always.

What doesn't work: analysis before action. You'll analyze while the system burns. Waiting for perfect information - perfect information doesn't exist in Chaotic situations, and waiting means the problem spreads. Experimentation - there's no time for safe-to-fail probes when the system is in crisis. Consensus-building - too slow, too many stakeholders, too much talking while the incident cascades. Tentative responses - if you're going to act, act decisively. And trying to understand before stabilizing - understanding is a luxury you can't afford until the crisis is contained.

The goal in Chaotic domains: move the situation to a more manageable domain, usually Complex or Complicated. You don't need to understand everything. You don't need to fix the root cause. You need to stop the crisis from getting worse. Containment first, comprehension later.

Common actions during Chaotic incidents: Failover - route traffic away from failing systems to systems that work. Load shedding - reduce load to prevent cascade, even if that means some customers can't access some features. Kill switches - disable problematic services or features entirely, accept the feature loss to prevent total system loss. Emergency rollback - revert to last known good state even if you're not sure that's the issue. Isolation - isolate affected systems to prevent spread to healthy systems. None of these are elegant. All of them buy you time.

Once you've stabilized (Act), you can assess (Sense), and then make strategic decisions (Respond). The situation typically transitions from Chaotic → Complex → Complicated as understanding increases. You contain the crisis, which gets you to Complex where you can start probing. The probes reveal patterns, which gets you to Complicated where you can analyze. The analysis finds the root cause, which gets you to Clear where you can permanently fix it. But all of that starts with acting immediately to stabilize.

For incident management: Black Swans often start in Chaotic. The system fails in a way you've never seen, cascades rapidly, and your first response has to be "stop the spread" not "understand the cause." The framework provides permission - no, provides a mandate - to act without full understanding. That's critical for Black Swan response because waiting to understand means you're analyzing during catastrophe. Many teams waste precious minutes trying to understand a Chaotic situation when they should be stabilizing first. Those minutes turn P0 incidents into existential incidents.

#### Domain 5: Confusion (Disorder) - "The Unknown Domain"

The fifth domain is different: Confusion, sometimes called Disorder. This is where you don't know which of the other four domains applies. It's unclear what type of problem you're facing. The situation has elements of multiple domains. Team members disagree about what's happening. No clear decision-making strategy is apparent. You're confused about which framework to use.

This is more common than anyone wants to admit. The incident starts, alerts are firing, teams are scrambling, and someone asks "What kind of problem is this?" Half the team thinks it's Clear - just follow the runbook. The other half thinks it's Chaotic - we need to act immediately. The database expert thinks it's Complicated and wants to analyze. The SRE on call thinks it's Complex and wants to probe. Everyone's operating from a different mental model, and coordination breaks down because you can't coordinate when you don't agree on what you're coordinating.

The decision heuristic for Confusion: Break Down → Classify → Apply Appropriate Strategy. You decompose the situation into constituent parts. You classify each part into the appropriate domain. And you apply the right strategy for each part. The incident isn't one monolithic thing. It's multiple components, and each component might be in a different domain.

What does this look like in practice? An incident where some aspects are clear - you know the payment service is down, that's straightforward. But other aspects are chaotic - cascading effects are spreading to other services in unpredictable ways. You don't treat the whole incident as one domain. You treat the payment service as Clear (follow the recovery runbook), and you treat the cascade as Chaotic (act immediately to contain).

Or a multi-service outage where different services require different approaches. Service A is clearly down due to a known issue - that's Clear. Service B is exhibiting novel failure modes no one's seen before - that's Complex. Service C is degraded but experts can diagnose it - that's Complicated. Three services, three different domains, three different response strategies running in parallel.

What works in Confusion: breaking the problem into components, assigning different strategies to different parts, acknowledging uncertainty explicitly ("we're not sure what domain this is yet, so we're going to probe while we investigate"), discussing which domain applies rather than assuming everyone agrees, and revisiting classification as understanding improves. Confusion is a temporary state. Your job is to move out of it by classifying the situation.

What doesn't work: treating the whole situation as one domain when it clearly isn't. Ignoring the confusion and hoping everyone converges on the same strategy. Forcing a single approach when the problem demands multiple approaches. Operating in "firefighting mode" without classification - that's just thrashing.

Here's the danger: When in Confusion, people default to their preferred domain. Engineers default to Complicated - let's analyze and gather more data. Managers default to Clear - follow the process and apply best practices. Operators default to Chaotic - act immediately and fix it fast. These defaults are cognitive biases, and they prevent the team from accurately classifying the situation. You end up with engineers analyzing while the system burns, or operators acting randomly while they should be investigating.

The IC's job in Confusion: explicitly classify the situation. Don't let people work from different assumptions. Call it out: "We're in Confusion right now. Let's break this down. The primary outage is Chaotic - we need to act. The secondary effects are Complex - we need to probe. Let's assign roles based on that classification." Make the classification explicit, get agreement, and then move forward with appropriate strategies.

For incident management: Many incidents start in Confusion. You get paged, you join the war room, and it's not immediately clear what's happening. The framework provides a way out: break it down, classify the parts, apply appropriate strategies to each part. This is especially important for stampedes where multiple animals are attacking simultaneously. You might have a Black Swan (Complex/Chaotic) happening at the same time as an Elephant (cultural dysfunction) and a Grey Rhino (known issue finally failing). Three different animals, three different domains, three different response strategies. Don't force them into one approach. Classify, split workstreams, and coordinate multiple strategies in parallel.
{::pagebreak /}
### How ICS Roles Adapt to Cynefin Domains

ICS provides structure, but how you execute that structure depends on which Cynefin domain your incident occupies. The same role requires different approaches in Chaotic vs Complicated vs Complex situations. Understanding these adaptations makes your incident response more effective.

#### ICS Role Adaptations by Cynefin Domain

| Role | Clear Domain | Complicated Domain | Complex Domain | Chaotic Domain |
|------|-------------|-------------------|----------------|----------------|
| **Incident Commander (IC)** | Ensure runbook is followed correctly; verify solution worked | Coordinate expert analysis; prevent analysis paralysis; make decision when experts disagree | Coordinate experimentation; maintain multiple parallel probes; synthesize learning | Act immediately; stabilize first; shield responders from external pressure; make rapid decisions with minimal information |
| **Technical Lead** | Verify runbook steps are executed properly | Direct experts; choose which hypotheses to pursue; manage systematic investigation | Design safe-to-fail probes; coordinate parallel experiments; observe emergent patterns | Execute immediate stabilization actions; break feedback loops; prioritize stopping the bleeding |
| **Subject Matter Expert (SME)** | Execute runbook procedures in their domain | Perform systematic investigation using expert tools; provide evidence-based analysis | Run experiments in their domain; observe and report emergent behavior; test hypotheses | Execute immediate fixes; provide quick technical assessments; identify critical paths |
| **Communications Lead** | Standard status update templates; routine stakeholder notifications | Technical status updates as experts converge on cause; ETA based on investigation timeline | Updates on experimentation progress; communicate uncertainty honestly; "still learning" updates | Immediate crisis communication; honest about uncertainty; frequent updates during stabilization |
| **Scribe** | Document runbook execution; note any deviations | Capture expert analysis; document evidence gathering; record decision rationale | Capture experiment results; document emergent patterns; track what was learned | Real-time timeline of actions taken; capture decisions under pressure; document stabilization steps |

#### Key Insights: Why Role Adaptation Matters

**The IC in Different Domains:**

In **Clear** domains, the IC ensures the runbook is executed correctly - a quality assurance role. In **Complicated** domains, the IC prevents analysis paralysis by making decisions when experts disagree. In **Complex** domains, the IC coordinates experimentation and synthesizes learning. In **Chaotic** domains, the IC acts immediately, prioritizing stabilization over understanding.

The mistake many ICs make: applying Clear-domain management (follow procedures) to Complex problems (need experimentation) or Chaotic situations (need immediate action).

**The Technical Lead in Different Domains:**

In **Clear** domains, the Technical Lead verifies runbook execution. In **Complicated** domains, they direct expert investigation. In **Complex** domains, they design and coordinate experiments. In **Chaotic** domains, they execute stabilization actions directly.

The mistake: Technical Leads often try to analyze their way through Complex problems (should experiment) or Chaotic situations (should act first).

**The SME in Different Domains:**

In **Clear** domains, SMEs execute procedures. In **Complicated** domains, they investigate systematically. In **Complex** domains, they experiment and observe. In **Chaotic** domains, they execute immediate fixes.

The mistake: SMEs often try to investigate Complex problems systematically (should experiment) or analyze Chaotic situations (should act first).

**The Communications Lead in Different Domains:**

In **Clear** domains, standard templates work. In **Complicated** domains, technical updates as analysis progresses. In **Complex** domains, honest communication about uncertainty. In **Chaotic** domains, frequent crisis updates.

The mistake: Communicating certainty in Complex domains (creates false expectations) or staying silent in Chaotic domains (stakeholders panic).

#### Practical Example: Same Incident, Different Domains

**Scenario:** Database performance degradation affecting customer transactions.

**If Classified as Clear:**

- IC: "This matches runbook #23 for database connection pool exhaustion. Follow procedure."
- Technical Lead: "Execute steps 1-3 from runbook #23, verify pool size increase worked."
- SME (Database): "Running standard connection pool increase procedure."
- Communications: "Standard maintenance procedure in progress, expected resolution in 15 minutes."
- Scribe: "Following runbook #23, standard procedure."

**If Classified as Complicated:**

- IC: "Database team, analyze query patterns. Network team, check latency. Report back with evidence."
- Technical Lead: "We need expert analysis to identify the root cause. Coordinate investigations."
- SME (Database): "Analyzing slow query log, examining index usage, reviewing connection patterns."
- Communications: "Database performance issue under investigation. Experts analyzing root cause. ETA based on investigation progress."
- Scribe: "Multiple expert investigations in progress: database queries, network latency, connection pooling."

**If Classified as Complex:**

- IC: "This doesn't match any known pattern. Let's run safe-to-fail experiments to learn what's happening."
- Technical Lead: "Design three parallel probes: test query performance in isolation, test network path, test connection pool behavior under load. Observe patterns."
- SME (Database): "Running isolated query performance test. Observing behavior as load increases. Testing different query patterns."
- Communications: "Investigating novel performance issue. Running experiments to understand root cause. Will update as we learn."
- Scribe: "Experiments in progress: isolated query test, network path test, connection pool load test. Observing emergent patterns."

**If Classified as Chaotic:**

- IC: "Database is degrading rapidly. Act immediately: failover to standby, shed load, isolate affected queries. Understand later."
- Technical Lead: "Execute failover immediately. Break feedback loops. Stop the bleeding."
- SME (Database): "Executing emergency failover. Shedding non-critical load. Isolating problem queries."
- Communications: "Database performance issue affecting customers. Executing emergency procedures to stabilize. Updates every 5 minutes."
- Scribe: "T+0: Emergency failover initiated. T+2: Load shedding applied. T+5: Problem queries isolated."

**The Same Incident, Different Approaches:**

Notice how the same technical problem (database performance) requires completely different role execution depending on domain classification. The IC's job changes from quality assurance (Clear) to decision-making under expert disagreement (Complicated) to coordination of experimentation (Complex) to immediate action (Chaotic).

This is why Cynefin classification matters: it tells you not just how to think about the problem, but how to structure your response team's work.

#### Recognizing When Role Adaptation Is Needed

**Warning Signs You're Using the Wrong Approach:**

- IC is insisting on following procedures when the situation is novel (Clear thinking in Complex domain)
- Technical Lead is trying to analyze when immediate action is needed (Complicated thinking in Chaotic domain)
- SMEs are investigating systematically when they should be experimenting (Complicated thinking in Complex domain)
- Communications is promising ETAs when the situation is uncertain (Clear/Complicated thinking in Complex/Chaotic domain)

**The Fix:**

Explicitly classify the Cynefin domain, then adjust role expectations accordingly. Announce to the team: "We're in Complex domain, so Technical Lead is coordinating experiments, not directing expert analysis."

{::pagebreak /}
### Applying Cynefin to Incident Response: Practical Framework

#### Step 1: Classify the Incident

**Questions to Ask:**

1. **Is the cause obvious?** → Clear
2. **Can experts figure it out?** → Complicated
3. **Do we need to experiment to learn?** → Complex
4. **Do we need to act immediately?** → Chaotic
5. **Are we unsure which applies?** → Confusion

**Classification Exercise:**

- **Clear:** "This matches runbook #47 for database connection pool exhaustion"
- **Complicated:** "We need to analyze the query patterns to understand the performance degradation"
- **Complex:** "We've never seen this failure mode before, and it's affecting multiple services in ways we don't understand"
- **Chaotic:** "The entire system is down and we're losing customers by the second"
- **Confusion:** "Some parts of this look like a known issue, but other parts are completely novel"

#### Step 2: Apply the Appropriate Strategy

**Clear Domain Response:**

- Follow the runbook
- Execute standard procedures
- Don't overthink it
- Verify the solution worked

In this domain, speed comes from recognition and execution. The problem matches a known pattern, the solution is documented, and your job is to apply it without second-guessing. Resist the temptation to innovate when the recipe works.

**Complicated Domain Response:**

- Assemble experts
- Gather diagnostic data
- Analyze systematically
- Choose a solution based on analysis
- Avoid analysis paralysis

Here, expertise and investigation reveal the answer. The problem is solvable through systematic analysis, but you need the right people with the right tools examining the right data. The key is balancing thoroughness with urgency - analyze enough to make good decisions, but not so much that the incident drags on while you pursue perfect understanding.

**Complex Domain Response:**

- Design safe-to-fail probes
- Run experiments in parallel
- Observe emergent patterns
- Adapt based on learning
- Be patient - solutions emerge over time

This domain requires accepting that you can't think your way to the answer - you have to discover it through action. Each probe teaches you something about the system's behavior, patterns emerge from experimentation, and understanding builds iteratively. Your instinct will be to analyze more, but the system won't yield to analysis because the relationships are emergent rather than discoverable.

**Chaotic Domain Response:**

- Act immediately to stabilize
- Don't wait for understanding
- Use failover, load shedding, isolation
- Once stable, assess the situation
- Transition to Complex or Complicated as understanding improves

In crisis, hesitation is expensive. You act to contain the damage first, understand what happened second. The goal isn't solving the problem perfectly - it's preventing it from getting worse while you buy yourself time to figure out what's actually going on. Analysis comes after stabilization, never during.

**Confusion Domain Response:**

- Break the incident into components
- Classify each component
- Apply appropriate strategy to each
- Revisit classification as situation evolves

When you're uncertain which domain applies, decomposition creates clarity. By breaking the incident into smaller pieces, you can classify each piece independently and apply the right strategy to each. This prevents the paralysis that comes from trying to apply a single approach to a situation that doesn't fit any single domain.

#### Step 3: Recognize Domain Transitions

**Natural Progression (Clockwise):**
Chaotic → Complex → Complicated → Clear

This represents increasing understanding:

- **Chaotic:** Act to stabilize
- **Complex:** Experiment to learn
- **Complicated:** Analyze to understand
- **Clear:** Apply known solution

As you gain understanding during an incident, you should move clockwise through these domains. What starts as crisis requiring immediate action becomes emergent behavior requiring experimentation, which reveals patterns requiring analysis, which eventually becomes a known solution you can document. This progression is natural and expected - forcing the wrong domain wastes time.

**Dangerous Transitions:**

- **Clear → Chaotic:** The "cliff edge" - following a recipe when context has fundamentally changed
- **Complicated → Chaotic:** Analysis paralysis during a crisis
- **Ordered → Complex:** Trying to analyze or follow procedures when the situation is emergent

These transitions happen when your approach doesn't match the reality. Following a runbook when context has fundamentally changed can make things worse fast. Analyzing when you should be acting lets the crisis spread. Trying to understand through investigation when the system is genuinely emergent burns time without generating insight.

**During an Incident:**

- Monitor which domain you're in
- Adjust strategy as the situation evolves
- Don't get stuck in one domain when you should transition
- Explicitly discuss transitions with the team

Domain awareness is a real-time activity, not a one-time classification. As your understanding changes, your strategy should change. The IC's job includes calling out transitions explicitly so the team stays aligned on which type of thinking is appropriate right now, not five minutes ago.

{::pagebreak /}
### Quick Classification Guide: Real-Time Decision Tree

During an incident, you need to classify the domain quickly, not perfectly. This guide helps you make that call in real-time when every minute matters.

#### The Classification Questions (Ask in Order)

**1. Do we need to act immediately to prevent catastrophe?**

   - YES → **Chaotic** (Go to Chaotic response immediately)
   - NO → Continue to question 2

**2. Do we have a runbook or procedure for this exact scenario?**

   - YES → **Clear** (Follow the runbook)
   - NO → Continue to question 3

**3. Can domain experts analyze their way to an answer using existing tools and knowledge?**

   - YES → **Complicated** (Assemble experts, gather data, analyze)
   - NO → Continue to question 4

**4. Do we need to experiment to learn what's happening?**

   - YES → **Complex** (Design safe-to-fail probes, observe patterns)
   - NO → Continue to question 5

**5. Are we unsure which of the above applies, or do different parts require different approaches?**
   - YES → **Confusion** (Break down into components, classify each part)

#### Quick Recognition Signals

**Clear Domain Signals:**

- "This matches runbook #47"
- "We've seen this before, standard procedure is..."
- Clear cause-effect relationship visible
- Solution is known and repeatable

**Complicated Domain Signals:**

- "We need the database team to analyze the query patterns"
- "This requires network packet capture analysis"
- Multiple valid solutions exist, experts need to choose
- Answer is discoverable through investigation

**Complex Domain Signals:**

- "We've never seen this failure mode before"
- "Multiple services are failing in ways we don't understand"
- Cause-effect only clear in hindsight
- Need to experiment to learn

**Chaotic Domain Signals:**

- "The entire system is down right now"
- "We're losing customers by the second"
- No visible patterns, immediate action required
- Stabilize first, understand later

**Confusion Domain Signals:**

- "Some parts look like a known issue, but others are completely new"
- Team members disagree about what type of problem this is
- Different parts require different strategies
- Unclear which domain applies

#### How to Communicate Classification to the Team

**For Chaotic:**
"I'm classifying this as Chaotic. We're acting immediately to stabilize. Focus on: [failover/load shedding/isolation]. No analysis yet. We'll reassess once stable."

**For Complex:**
"I'm classifying this as Complex. We need to experiment to learn. Let's design safe-to-fail probes: [specific experiments]. Observe patterns as they emerge."

**For Complicated:**
"I'm classifying this as Complicated. [Expert A], analyze [specific area]. [Expert B], investigate [specific component]. Report back with evidence, not theories."

**For Clear:**
"I'm classifying this as Clear. Follow runbook #[number]. [Person], execute steps 1-3. [Person], verify solution worked."

**For Confusion:**
"We're in Confusion - parts need different approaches. Breaking it down: Component A is [domain], Component B is [domain]. [Person] handles A using [strategy], [Person] handles B using [strategy]."

#### Recognizing Domain Transitions

**Signals You've Moved from Chaotic → Complex:**

- System is stable (not getting worse)
- Immediate danger passed
- Now time to understand what happened
- Can run experiments safely

**Signals You've Moved from Complex → Complicated:**

- Patterns have emerged from experiments
- Cause-effect relationship now visible
- Experts can analyze with existing tools
- No longer need to experiment to learn

**Signals You've Moved from Complicated → Clear:**

- Root cause identified
- Solution is known and repeatable
- Can create runbook for next time
- Following procedure will work

**Signals You've Moved from Clear → Chaotic:**

- Following the runbook made things worse
- Context fundamentally changed
- "This time is different"
- Need immediate action to stop the bleeding

**Communicating Transitions:**
"I'm reclassifying from [old domain] to [new domain]. Evidence: [specific observation]. Strategy change: [new approach]."

#### War Room Template: Cynefin Classification

**Incident:** [Name/ID]  
**Initial Classification:** [Domain]  
**Classification Time:** [Timestamp]  
**Who Classified:** [IC Name]  
**Rationale:** [Brief reason]

**Current Domain:** [Domain]  
**Last Updated:** [Timestamp]  
**Evidence of Classification:** [What signals you're seeing]

**Domain Transitions:**
- [Time] - [Old Domain] → [New Domain] - [Reason]

**Strategy Being Applied:** [Current approach based on domain]

---

Use this guide during incidents. Print it, put it on the war room wall, reference it when uncertainty strikes. The goal isn't perfect classification - it's using the right thinking for the problem you're facing.

{::pagebreak /}
### Common Mistakes made in Incidents and How to Avoid Them

The most common mistake? Treating a Complex problem like it's Clear. You're facing a novel failure mode - something you've never seen before - and someone's insisting you follow the runbook. The runbook doesn't apply. The runbook was written for Known Problem X, and you're dealing with Unprecedented Problem Y. But there's a human tendency to force novelty into familiar patterns because familiar patterns are comfortable. This is expensive during incidents. You waste time following procedures that don't fit while customers experience the outage. Explicitly classify the incident before you respond. Ask yourself and your team directly: "Is this a known problem with a known solution, or are we in uncharted territory?" If you can't answer confidently, you're probably in Complex, and runbooks won't save you.

The second mistake is analysis paralysis in crisis. You're in a Chaotic situation - the system is actively degrading, cascades are spreading, customers are screaming - and the team is trying to analyze before acting. "Let's gather more logs." "Let's examine the metrics." "Let's bring in the database expert." Meanwhile the incident spreads because you're analyzing while the building burns. Chaotic domains demand action first, understanding second. Recognize when you're in Chaotic. Give yourself permission to act without full understanding. Stabilize the bleeding before you figure out why you're bleeding. You can analyze all you want after you've contained the crisis.

The third mistake is command-and-control in Complex situations. You're facing genuinely emergent behavior - a distributed systems failure with interaction patterns you don't understand - and an expert is imposing solutions without testing them. "I've seen this before, we need to do X." But Complex means you haven't seen this before. Expert solutions are based on past patterns, and Complex means the patterns are novel. Recognize Complex domains and design safe-to-fail experiments instead. Learn through iteration. Probe, sense, respond. The pattern reveals itself through experimentation, not through expert assertion.

Related to that: treating Complex as Complicated. You're bringing in more experts, gathering more data, analyzing harder - when the problem requires experimentation. This is particularly insidious because it feels productive. "We're doing something. We're analyzing. We have three senior engineers looking at it." But if the situation is truly Complex, no amount of analysis will reveal the answer because the answer only emerges through the system's behavior. Ask yourself: "Can we analyze our way to an answer, or do we need to experiment to learn?" If the latter, you're in Complex. Stop gathering data and start running safe-to-fail probes.

The final mistake is complacency in Clear domains. You're following best practices without recognizing when context has changed. Your standard database restart procedure works 99% of the time. But this time the underlying storage system failed, and following that same procedure makes things worse - the database comes up, can't reach storage, cascades errors to every connected service, and now you've amplified the problem. You thought you were in Clear, applying best practices. You were actually in Chaotic, and your best practices became accelerant. Periodically challenge best practices. Monitor for context shifts. Recognize when "this time is different." The cliff edge between Clear and Chaotic is sharp, and the fall is expensive.

Now that we understand Cynefin, let's see how it applies to each animal in our bestiary. The framework provides the decision-making strategy; the animals provide the context. Together, they tell you not just how to think about an incident, but what type of risk you're actually facing.
{::pagebreak /}
### Incident Management by Animal Type
Each animal that may show up has a particular strategy that needs to be implemented in order to appropriately deal with it. A skilled Incident Commander will also realize that there may be more than one animal involved. There may be a stampede or there may be some hybrid animal. Bear in mind that these animal classifications are really just a mnemonic in order for you to bring some structure to a chaotic thought process that you might be embedded in at the time. Read through these incident management scenarios, and use them to formulate your own plan when confronted with individual animals or with a combination of them.


#### Black Swan Incidents: When the Unprecedented Strikes

**Cynefin Domain Classification**

Black Swans almost always start in **Chaotic** or **Complex** domains:

**Initial State: Chaotic**

- Unprecedented event
- Mental models breaking
- Need immediate stabilization
- Act first, understand later

**After Stabilization: Complex**

- No known solution exists
- Must experiment to learn
- Safe-to-fail probes essential
- Patterns emerge over time

**Key Insight:** 

Black Swans require you to abandon runbooks and expert analysis. You're in uncharted territory. The framework gives you permission to experiment and learn rather than pretending you can analyze your way to a solution.

**Characteristics During the Incident**

**What You Know:**

- Something catastrophic is happening
- It doesn't match any pattern you've seen before
- Your runbooks don't apply
- Your mental models are breaking

**What You Don't Know:**

- Root cause
- Scope of impact
- What will work to fix it
- When it will end
- What other systems might be affected

**The Psychological Challenge:**

Black Swan incidents create cognitive dissonance. Your brain wants to fit this into a known pattern. "This is like that database incident last year." But it isn't. Forcing it into an existing mental model delays understanding and leads to wrong decisions.

The IC's job is to maintain this tension: move fast despite uncertainty while resisting the urge to pretend you understand what's happening.

**Scenario 1: The AWS S3 Outage (February 28, 2017)**

**The Trigger:**
An engineer debugging the S3 billing system needed to remove a few servers. They typed a command with parameters to remove servers. They made a typo. Instead of removing a few servers, the command removed a large number of servers including the index subsystem and placement subsystem.

**The Black Swan Moment:**
No one had considered "what if someone accidentally removes critical S3 subsystems?" The scenario wasn't in any runbook. The blast radius was unprecedented. Even the AWS status dashboard was hosted on S3 and went down, preventing AWS from communicating about the outage.

**What Made It a Black Swan:**

- This category of operator error hadn't occurred before at this scale
- The tooling was assumed to have safeguards (it didn't)
- The dependency of the status page on S3 wasn't appreciated
- The cascading effect on thousands of services was unpredicted

**The Incident Management Response:**

**T+0 to T+15 minutes: Confusion Phase (Chaotic Domain)**

- Multiple teams getting alerts simultaneously
- Initial hypothesis: network partition (wrong)
- Standard S3 recovery procedures attempted (didn't work)
- Growing realization this is unprecedented
- **Cynefin Action:** Act immediately to stabilize, don't wait for understanding

**T+15 to T+60 minutes: Adaptation Phase (Transitioning to Complex)**

- IC declared by senior SRE leadership
- Assembled cross-functional team (storage, networking, control plane)
- Abandoned standard procedures
- Focus shifted to "how do we restart these subsystems from zero?"
- Problem: subsystems designed to never be fully offline, restart procedures untested
- **Cynefin Action:** Recognize we're in Complex domain, need to experiment

**T+60 to T+240 minutes: Novel Solution Phase (Complex Domain)**

- Engineering team had to develop restart sequence in real-time
- Subsystems had circular dependencies (A needs B to start, B needs A)
- Required breaking assumptions about how systems boot
- Communication challenge: telling customers we don't know when recovery will complete
- **Cynefin Action:** Safe-to-fail probes to understand restart sequence

**Key Decisions Under Uncertainty:**

**1. Decision - Attempt full subsystem restart vs. partial recovery:**+

   - **Context**: Partial recovery might be faster but risk corruption
   - **Information available**: ~30%
   - **Time to decide**: 15 minutes
   - **Outcome**: Full restart chosen, added time but ensured data integrity
   - **Cynefin Note:** This was a Complex-domain decision - no expert analysis could determine the answer, required experimentation

**2. Decision - Public communication about lack of ETA:**

   - **Context:** Customers demanding timeline, but genuinely unknown
   - **Information available**: ~20%
   - **Time to decide**: 30 minutes
   - **Outcome**: Honest communication about uncertainty, preserved trust
   - **Cynefin Note:** Accepting uncertainty is key to Complex-domain thinking

**Postmortem Learning:**

**What was genuinely unpredictable:**

- This specific failure mode
- Cascading effects through internet infrastructure
- Circular dependency problem in restart

**What could have been better:**

- Safeguards on administrative commands (Grey Rhino that became visible)
- Status page hosted independently of S3 (architecture assumption now revealed)
- Tested restart procedures (Black Swan revealed lack of testing)

**The Meta-Learning:**
This Black Swan revealed multiple Grey Rhinos (known risks that had been deprioritized):

- Admin tooling lacked safeguards
- DR testing hadn't included "full subsystem restart"
- Status page dependency was known but accepted

This is common: Black Swans often reveal a herd of other animals.

**Scenario 2: The COVID-19 Digital Transformation Shock**

**The Context:**
In March 2020, entire organizations shifted to remote work within days. For IT infrastructure, this created unprecedented load patterns that couldn't have been predicted from historical data.

**What Made It a Black Swan (or Swan-Adjacent):**

The pandemic itself was a Grey Rhino (WHO had warned for years). But the specific digital infrastructure impacts bordered on Black Swan because:

- No historical precedent for simultaneous global shift
- Scale (100x normal remote work, not 2x)
- Duration (sustained for years, not weeks)
- Behavioral changes (Zoom fatigue, asynchronous work patterns)

**The Incident Management Challenge:**

This wasn't a discrete incident; it was a permanent shift masquerading as a temporary surge.

**Week 1: Crisis Response (Chaotic Domain)**

- VPN infrastructure designed for 5% remote hitting 95% remote
- Video conferencing services seeing 30x normal load
- Home internet infrastructure becoming critical path
- Traditional incident response: scale up capacity
- **Cynefin Action:** Act immediately to stabilize (failover, load shedding)

**Week 2-4: Sustained Crisis (Transitioning to Complex)**

- Realizing this isn't a "spike" to be weathered
- Supply chain constraints (can't order servers fast enough)
- Architectural limitations revealed (VPN doesn't scale to 100%)
- Shift from incident response to architectural transformation
- **Cynefin Action:** Recognize this is Complex - need to experiment with new architectures

**Month 2-6: Permanent Adaptation (Complex Domain)**

- Abandoning VPN model for zero-trust architecture
- Rethinking capacity planning (new baseline, not anomaly)
- Accepting that historical data is useless for forecasting
- Building for new normal, not recovering to old normal
- **Cynefin Action:** Experimentation with new models, learning what works

**Key IC Decisions:**

**1. Declaring this is not a normal incident (Week 2)**

   - Recognition that incident response framework doesn't fit
   - Shift from "restore service" to "transform architecture"
   - Communication to stakeholders: this is permanent change
   - **Cynefin Note:** Recognizing domain transition from Chaotic to Complex

**2. Abandoning historical capacity models (Week 3)**

   - Traditional approach: forecast from past data
   - Black Swan approach: assume past is irrelevant
   - Build based on current reality, not historical trends
   - **Cynefin Note:** Complex domain thinking - past patterns don't apply

**3. Prioritizing architectural change over stability (Month 2)**

   - Normally: don't change architecture during crisis
   - Black Swan: current architecture can't handle new reality
   - Risk trade-off: short-term instability for long-term viability
   - **Cynefin Note:** Complex domain requires experimentation, even during crisis

**Postmortem Insights:**

**Organizational adaptability was the differentiating factor:**

- Companies with high psychological safety adapted faster (could admit "our VPN strategy is wrong")
- Companies with operational slack (extra capacity, financial reserves) survived better
- Companies with cross-functional teams (engineering + product + business) made better decisions
- Companies with blame culture struggled (people hid problems, delayed escalation)

**The animals revealed:**

- **Grey Rhino**: Inadequate remote work infrastructure (known, ignored)
- **Elephant**: "We don't really trust remote work" (cultural resistance)
- **Black Jellyfish**: VPN failure cascaded to collaboration tools, to home networks
- **Grey Swan**: Pandemic was predictable; specific digital impact was complex
{::pagebreak /}

**Black Swan Incident Management Principles**

**1. Recognize You're in Unprecedented Territory (Cynefin: Classify as Chaotic or Complex)**

The first principle of Black Swan incident management: You need to accept you're in unprecedented territory. Not "kind of like that time" or "similar to when" - actually unprecedented. Your mental models don't apply here. That's not a failure of preparation. That's the definition of a Black Swan.

You'll know you're facing one when your runbooks fail to match the situation. When domain experts - the people who usually have confident answers - look confused or keep revising their theories. When teams are debating multiple hypotheses without convergence, and no one can eliminate alternatives through evidence. When the scope keeps expanding in ways you didn't predict, revealing dependencies and failure modes you didn't know existed.

Here's what the Incident Commander needs to do: Declare it explicitly. Say out loud, to the team and to stakeholders: "This is unprecedented. We're adapting in real-time." That declaration does two critical things. First, it gives the team permission to abandon standard procedures that don't fit. Second, it sets expectations with stakeholders that you're operating under uncertainty - there won't be confident ETAs, and the story will evolve as you learn.

Then classify the Cynefin domain: Are we in Chaotic (act immediately to stabilize) or Complex (experiment to learn)? That classification drives your next moves. Chaotic means you act first and understand later. Complex means you probe, sense, and respond. Getting this wrong wastes time: treating Chaotic as Complex means you're experimenting while the building burns. Treating Complex as Chaotic means you're making panicked changes without learning.

Assemble diverse expertise - not just your usual responders, but people from adjacent domains who might see patterns you're missing. And communicate uncertainty to stakeholders honestly. No one trusts confident predictions during unprecedented events. They trust transparency about what you know, what you don't, and what you're doing to learn.

What you cannot do: Force-fit this into known patterns. Your brain desperately wants to categorize this as "just like that database incident last year," but it isn't. The pattern-matching instinct that usually serves you well becomes a liability here. You can't wait for certainty before acting - certainty won't arrive until after you're done. Don't follow standard procedures if they clearly don't apply - that's denial, not discipline. Don't pretend you know more than you do - stakeholders can smell false confidence, and it destroys trust. And critically, if you're in Complex domain, you cannot analyze your way to a solution. Analysis assumes discoverable cause-and-effect relationships. Complex means those relationships only emerge through experimentation. Trying to analyze longer just burns time without generating understanding.

**2. Optimize for Information Flow, Not Chain of Command**

Black Swans require rapid adaptation, and hierarchical communication is too slow. In unprecedented situations, information needs to flow from whoever has it to whoever needs it, regardless of org chart position. Your normal escalation paths - engineer to manager to director to VP to decision-maker - take minutes or hours. You have seconds or minutes.

Create direct channels immediately. War room with domain experts, regardless of seniority. If the junior engineer who deployed the change has context, they're in the room. If the database expert is an IC3 and not a staff engineer, they're still in the room. Expertise and context matter. Titles don't. Set up shared documents everyone can edit simultaneously - Google Docs, Notion, whatever your org uses. The IC updates strategy, the Scribe updates timeline, SMEs update investigation findings, all in the same document in real-time. Everyone has the same view of reality.

Document decisions in real-time with rationale. Not "we decided to failover" but "we decided to failover because error rate was 45% and rising, customer impact was total, and the risk of failover (30 seconds of additional downtime) was lower than risk of not failing over (continued 45% error rate indefinitely)." That contemporaneous documentation helps the next IC understand why you made that choice.

And skip normal escalation paths. If you need executive approval for something, bring the executive into the war room. Don't send a Slack message up the chain and wait for a response. Bring them into the context, explain the situation, get the approval, continue. Black Swans don't wait for email threads.

The IC's role in this information chaos: Synthesize information from diverse sources. You're getting updates from six SMEs, each investigating a different subsystem. Your job is to build the coherent picture from those fragments. Make calls when consensus isn't possible - experts will disagree, and someone has to decide. Shield responders from external pressure - every executive has questions, every customer success manager wants updates, your job is to filter that so responders can focus. And maintain a coherent narrative despite chaos - the situation is confusing, but your explanation of it shouldn't be. Clarity in communication even when the situation itself is unclear.

**3. Make Reversible Decisions Rapidly, Irreversible Decisions Carefully (Cynefin: Safe-to-Fail Probes)**

During Black Swan incidents, you'll need to make decisions with 20-30% of the information you'd like to have. That's uncomfortable. Engineers are trained to gather data, analyze, then decide. But Black Swans don't give you that luxury. Use decision reversibility as your guide for how fast to move.

Reversible decisions get made quickly. Trying a potential fix you can roll back in 30 seconds? Do it. Routing traffic differently in a way you can revert immediately? Do it. Adding capacity you can remove? Do it. Opening circuit breakers you can close? Do it. These are safe-to-fail probes in Complex domain thinking - if you're wrong, you can undo it quickly, and even being wrong teaches you something about the system's behavior. The cost of trying is low. The cost of not trying is continued customer impact.

In Cynefin terms, these reversible decisions are your probes. You're not committing to a solution. You're testing hypotheses about what might help. Probe → sense → respond. Try something, observe what emerges, adapt. This is how you navigate unprecedented situations - through experimentation with low-cost reversibility.

Irreversible decisions take more time, even during a Black Swan. Deleting data you can't recover? Slow down, make sure. Declaring to customers that their data is permanently lost? Don't say that until you're certain. Major architectural changes that can't be rolled back during the incident? Defer if possible. Publicly committing to timelines you're not confident about? Don't. Irreversible decisions have high cost if wrong, so you need higher confidence before making them.

The key distinction: reversible decisions test hypotheses and generate learning even when wrong. Irreversible decisions are one-way doors. Move fast through the two-way doors. Move carefully through the one-way doors. And when you're uncertain which kind of door you're facing, treat it as irreversible until you know for sure.

**4. Document Everything in Real-Time**

Your future self - and your organization - needs to understand what happened and why. Black Swans are learning opportunities, but only if you capture what you learned while it's still fresh. Document everything in real-time because memory is unreliable under stress, and waiting until after the incident means you'll rewrite history without meaning to.

What to document: Start with the timeline of events. Automated where possible - system metrics, log entries, deploy events - but also manual annotations about human decisions and observations. When did we first notice the problem? When did we realize it wasn't matching known patterns? When did we make each significant decision?

Capture hypotheses considered and why they were rejected. "We thought it might be database connection pool exhaustion (ruled out: pool at 45% capacity). We thought it might be a network issue (ruled out: packet loss normal). We thought it might be the recent deploy (validated: rolled back, error rate dropped from 40% to 5%)." That hypothesis trail shows your reasoning and helps future incidents when someone proposes a hypothesis you already tested.

Document decisions and the reasoning you had with incomplete information. This is critical. "We decided to failover to backup region at T+45 with only 25% confidence in root cause because customer impact was total and risk of failover was lower than risk of continued outage." That captures your decision context. In the postmortem, people will have perfect information and may question your choices. The real-time doc shows what information you actually had at decision time.

Track who knew what when. This matters for understanding information flow. "IC learned about anomalous API behavior at T+12, 15 minutes after junior engineer first observed it." Why the 15-minute delay? Was it fear of escalating? Wrong comm channel? That's organizational learning waiting to happen.

Capture surprising findings - anything that contradicted your mental models. "We assumed service B didn't depend on service A, but during incident discovered A failure cascaded to B through shared cache." That's a dependency you didn't know about, and documenting it prevents the same surprise next time.

And critically: document Cynefin domain classification and transitions. "Started classified as Complex, attempted safe-to-fail probes. At T+30 realized situation was Chaotic, shifted to immediate stabilization actions. At T+60 after stabilization, moved to Complicated where expert analysis could help." That domain awareness helps you learn whether you matched strategy to problem type.

Why this matters: Black Swans are learning opportunities, but real-time documentation captures context that disappears. Write it while the incident is happening. Wait until the postmortem and the nuance is gone - you'll remember what you did but not why you did it. Postmortem quality depends on contemporaneous notes. And while future Black Swans may be different, decision-making principles under uncertainty apply across incidents. Documenting how you decided helps others learn to decide when facing their own unprecedented situations.

**5. Plan for Extended Duration**

Black Swans often last longer than expected because you're learning as you go. You can't follow a runbook to resolution when there's no runbook. You're discovering the solution through experimentation, and that takes time. Plan accordingly.

Rotation planning matters. The IC should rotate every 6-8 hours maximum. Decision fatigue is real, and an exhausted IC makes worse decisions. You need someone fresh to synthesize the situation and make calls. Responders need breaks too - burnout helps no one, and an engineer who's been debugging for 14 hours straight will miss things a fresh engineer would catch. Maintain situation awareness through handoffs by having the outgoing IC brief the incoming IC while they overlap. Walk through what you know, what you've tried, what you're currently testing, and what you're unsure about.

Document decision rationale so the next IC can continue your strategy. If you decided to focus on database investigation over network investigation, write down why. The next IC needs to understand your reasoning or they'll restart analysis you already completed. That handoff documentation prevents rework.

Communication cadence: Regular updates even if there's no progress. "Still working on it" is information - it tells stakeholders you're engaged and making effort, which prevents panic. Be honest about uncertainty in timelines. Don't say "we'll have this fixed in 2 hours" when you're 30% confident. Say "we're investigating multiple hypotheses, expect updates every 30 minutes, timeline unclear given unprecedented nature." Stakeholders can handle uncertainty if you're transparent about it. What they can't handle is false confidence followed by blown estimates.

Escalate to executives early. You might think you're protecting them by not raising the alarm until you're sure. You're actually preventing them from providing air cover. If this is a Black Swan, executives need to know so they can handle customer escalations, board communications, press inquiries, and executive-level decisions. Bring them in early - "This is unprecedented, we're adapting, expect extended duration, I'll update you every hour" - so they're prepared to support you rather than surprised when it goes long.

**6. Transition from Response to Learning**

The incident isn't over when service is restored. It's over when you've learned from it. Black Swans are the highest-value learning opportunities your organization will encounter because they expose assumptions you didn't know you were making and fragilities you didn't know existed. Don't waste that learning.

Conduct a comprehensive postmortem, and make it genuinely comprehensive. Start with: What was genuinely unprecedented? Not "the database failed" (databases fail all the time) but "the database failed in this specific way that we'd never seen, triggering a cascade through a dependency we didn't know about, amplified by a feedback loop we didn't expect." Specificity matters.

What assumptions were broken? "We assumed services A and B were independent - they're not, they share a cache. We assumed failover would be automatic - it wasn't, the automation depended on a service that failed. We assumed experts would converge on root cause quickly - they didn't, the failure mode was novel." Broken assumptions are gold. They show you where your mental models don't match reality.

What other risks did this reveal? Black Swans often travel with friends - look for the stampede. If one assumption broke, what other assumptions might be equally fragile? If one dependency was hidden, what other dependencies might be undocumented? If one automation failed, what other automations have similar failure modes? Mine the incident for insights about risk you didn't know you were carrying.

How did the organization adapt? What worked well during the incident? What slowed you down? Who made the critical observations? Where did information flow smoothly and where did it get stuck? This organizational learning is as important as the technical learning - Black Swans test your adaptability, and understanding how you adapted helps you get better at it.

What would help next time? You can't predict the specific Black Swan that comes next - that's why they're Black Swans. But you can improve adaptability. Better monitoring for unexpected correlations. Better war room practices for rapid information synthesis. Better frameworks for decision-making under uncertainty. Better rotation planning for extended incidents. Focus action items on improving your capability to handle the unprecedented, not on preventing this specific incident from recurring.

And critically: What Cynefin domain were we in, and did we use the right strategy? If you were in Complex domain but kept trying to analyze your way to an answer, that's a strategy mismatch worth learning from. If you were in Chaotic but spent time debating before acting, that's a learning opportunity. The framework helps you assess whether you matched your response to the problem type.

Focus action items on: Building antifragility - systems that benefit from stress, that get stronger when tested. Improving adaptability - people and processes that can handle novelty without breaking. Reducing fragility - single points of failure, brittle assumptions, hidden dependencies, cascades waiting to happen. Black Swans expose fragility. Use that exposure to become more robust.

---
{::pagebreak /}
#### Grey Swan Incidents: The Complex and Monitorable
**Cynefin Domain Classification**

Grey Swans often start in **Complicated** or **Complex** domains:

**Initial State: Complicated**

- Known but underestimated risk
- Weak signals exist
- Expert analysis can help
- But complexity may be higher than expected

**May Transition to Complex:**

- As you investigate, you realize the problem is more emergent
- Multiple interacting factors
- Need experimentation, not just analysis

**Key Insight:** Grey Swans often start as Complicated (we can analyze this) but reveal themselves as Complex (we need to experiment). The framework helps you recognize when to switch strategies.

**Characteristics During the Incident**

**What You Know:**

- This is complicated but not unprecedented
- Similar events have happened (to you or others)
- Early warning signals existed if you were watching
- Root cause will be complex interaction of factors

**What You Don't Know:**

- Exact interaction effects causing this manifestation
- Full scope of impact
- Which intervention will work best

**The Psychological Challenge:**

Grey Swans create false confidence. "We've seen something like this before" can lead to applying the wrong solution to a similar-looking-but-different problem. The complexity is genuine; pattern matching without deep understanding fails.

**Scenario 1: The Knight Capital Trading Disaster (August 1, 2012)**

**The Context:**
Knight Capital Group was a major market maker, executing billions in trades daily. They were deploying new trading software to comply with NYSE's Retail Liquidity Program.

**The Incident:**

**T-minus 1 day: Deployment**

- New software deployed to 7 of 8 servers
- Old code flagged for deletion but left on one server
- Deployment verification incomplete

**T+0 (Market Open): Cascade Begins**

- New software activated
- One server still running old code
- Old code was a repurposed test algorithm never meant for production
- Algorithm started executing: buy high, sell low, repeat rapidly

**T+0 to T+45 minutes: Uncontrolled Execution**

- Algorithm executing millions of unintended trades
- Each trade losing money
- Positive feedback loop: more trades → bigger losses → more frantic trading
- 4 million trades in 154 stocks
- $7 billion in erroneous positions

**T+45 minutes: Recognition and Shutdown**

- Traders notice bizarre market movements
- Knight realizes the algorithm is theirs
- Kill switch activated
- Damage assessment begins: $440 million loss
- Knight Capital nearly bankrupt

**Why This Was a Grey Swan:**

**Complexity factors that made it monitorable:**

- Deployment risk: known (software deployments can fail)
- Configuration drift: known (servers getting out of sync)
- Algorithm validation: known requirement
- Test code in production: known antipattern

**Why it manifested as catastrophic:**

- Specific interaction: old code + new trigger condition
- Speed of execution: 45 minutes from normal to catastrophic
- Positive feedback: algorithm design amplified losses
- Market impact: trades moved markets, worsening losses

**Cynefin Analysis:**

**Initial State: Complicated Domain**

- Known risk factors (deployment, configuration)
- Expert analysis could have identified the problem
- Systematic investigation would have revealed the issue

**Why it became catastrophic:**

- No one was analyzing (assumed deployment was fine)
- No monitoring for the specific interaction
- System moved to Chaotic domain before anyone noticed

**What monitoring could have caught:**

**1. Pre-deployment:** It seems like very little vetting or "second eyes" were done for the deployment plan

   - Configuration drift detection (1 of 8 servers different)
   - Pre-production validation (test algorithm still present)
   - Deployment verification (all servers updated)

**2. During incident:** If there was a "kill switch", staff were hesitant to flip it.

   - Anomaly detection (trading volume 100x normal)
   - Position monitoring (accumulating huge positions)
   - Loss tracking (money hemorrhaging)

**The Incident Management Failure:**

**Detection lag:**

- Anomalous trading began immediately
- Detection took 30+ minutes
- No automated circuit breakers for algorithmic trading

**Understanding lag:**

- Even after detection, determining cause took time
- "Is this a bug, a hack, or deliberate?"
- Complex system made diagnosis difficult

**Response coordination:**

- Multiple teams involved (trading, technology, risk)
- No clear incident commander
- Decision to shut down took too long (cost increased exponentially with time)

**Postmortem Learning:**

**This was preventable with better practices:**

- Deployment verification (all servers updated)
- Configuration management (detect drift)
- Automated position limits (circuit breakers)
- Rapid kill switches (faster shutdown)

**The Grey Swan lesson:**
Known risk factors (deployment, configuration, algorithm testing) combined in a way that was predictable but not predicted. Better instrumentation and monitoring would have caught this.

**Cynefin Lesson:**
This started as a Complicated-domain problem (could have been analyzed and prevented) but moved to Chaotic (crisis requiring immediate action) because no one was watching. The framework helps recognize that Complicated problems need expert attention, not assumption.

**Grey Swan Incident Management Principles**

**1. Instrument for Weak Signals (Cynefin: Recognize Complicated Domain Needs Monitoring)**

Grey Swans give early warnings if you're watching for them. That's the whole point - these aren't unpredictable Black Swans. They're complex but monitorable. The challenge is distinguishing signal from noise, and the key is knowing what kind of signal matters.

Monitor rate of change, not just absolute values. Error rate at 2% doesn't alarm you. Error rate increasing 20% per minute does - that's a cascade starting, not a steady state. Latency at 500ms might be acceptable. Latency growing exponentially from 200ms to 500ms to 1250ms over ten minutes means saturation is approaching and you're about to fall off a cliff. Resource consumption at 60% is fine. Resource consumption accelerating from 40% to 60% to 75% in five minutes means you have a leak or an attack, and extrapolation says you hit 100% in another five minutes.

Look for correlation across systems. One service showing elevated errors might be that service's problem. Multiple services showing issues simultaneously means something upstream failed or a shared dependency is degrading. Watch for problems spreading through the dependency graph - if service A fails and then service B starts failing 2 minutes later, that's not coincidence. Look for temporal correlation where multiple unrelated things started around the same time - that points to a common cause like a deploy or a configuration change.

Monitor distribution shape changes, not just averages. Tail behavior shifting - p99 latency growing faster than p50 - means your worst-case performance is degrading, which often precedes total failure. Bimodal distributions appearing means you have two distinct failure modes operating simultaneously, which suggests partial degradation cascading. Outliers becoming more frequent means your system is approaching instability - exceptions are becoming rules.

Watch for interaction anomalies. Normal components behaving abnormally together. Service A works fine standalone, service B works fine standalone, but when they interact under specific load patterns something breaks. Unexpected traffic patterns - sudden spikes at unusual times, unusual geographic distribution, unusual API call sequences. Circular dependencies activating - A depends on B, B depends on C, and it turns out C depends on A under specific conditions you've never hit before. These interaction anomalies are Grey Swan territory - they're detectable if you're watching for the right patterns.

**2. Recognize Complexity, Don't Oversimplify (Cynefin: Don't Force Complex into Complicated)**

Grey Swans are inherently complex, and forcing them into simple mental models delays understanding. The human brain wants simple stories - single root causes, clear villains, straightforward fixes. But Grey Swans don't work that way. They emerge from interactions, and oversimplifying them means you'll miss the actual dynamics.

Warning signs you're oversimplifying: Someone says "It's just a database issue" when you're actually seeing an interaction of database performance plus cache invalidation patterns plus load balancer timeout settings. Someone says "This is like that other incident" when it's similar on the surface but different in the underlying dynamics. Single root cause fixation when there are multiple contributing factors that only cause failure when they interact in specific ways.

Better approach: Map the full interaction space. Don't just identify the component that failed - identify all the components involved and how they interacted to produce the failure. Draw the interaction diagram. Show the feedback loops. A calls B, B calls C, C's response time affects A's retry logic, retries amplify B's load, amplified load degrades C's performance further. That's a feedback loop, and it matters more than identifying which component "failed first."

Identify all contributing factors. The deploy that introduced the bug. The monitoring gap that delayed detection. The cache warming pattern that created load spikes. The retry logic that amplified the problem. The timeout setting that made things worse. None of these alone caused the incident. They combined to cause the incident. The "root cause" isn't one of these factors. The root cause is the complex interaction of these five factors.

Understand the feedback loops - where actions amplified themselves. Negative feedback loops stabilize systems. Positive feedback loops destabilize them. Grey Swans often involve positive feedback that wasn't anticipated. Identifying those loops helps you understand why the incident escalated so quickly and where to break the cycle next time.

Accept that "root cause" might genuinely be "complex interaction of 5 factors." That's not satisfying. It doesn't give you one thing to fix. But it's accurate. And accurately modeling the complexity helps you see similar interaction patterns in other parts of your system. Recognize when you're in Complex domain, not Complicated. If expert analysis isn't converging on a clear answer, you're probably in Complex. Shift to probe-sense-respond instead of trying to analyze longer.

**3. Comprehensive Postmortem for Complex Events**

Grey Swan postmortems are more valuable than simple failure postmortems because they teach systems thinking. A simple failure teaches you "don't do X." A Grey Swan teaches you how complex systems behave, how interactions create emergent failure, and how to think about complexity. Don't waste that learning opportunity.

Document the interaction diagram. Show all components involved - not just the one that "failed" but all the ones that participated in creating the failure. Map how they interacted to produce the failure - service A called service B which updated cache C which triggered behavior in service D. Show the feedback loops that amplified it - more retries led to higher load which led to slower responses which led to more retries. Explain why this interaction wasn't anticipated - we knew about each component's behavior independently, but we didn't model their interaction under these specific conditions.

Document the weak signals. What early warnings existed? Was there a performance regression three weeks ago that went uninvestigated? Was there a gradual increase in error rate that stayed below alert thresholds? Was there a deploy that correlated temporally with the first subtle signs of trouble? Why were these signals missed or dismissed? Were thresholds set too loosely? Was the monitoring not capturing the right metrics? Were people too busy to investigate marginal degradation? What monitoring would have caught this earlier? That's your action item - add the monitoring that would have given you 30 minutes of warning instead of 30 seconds.

Document the decision tree during the incident. What hypotheses did you consider? "Maybe it's database connection pool exhaustion. Maybe it's network issues. Maybe it's cache thrashing. Maybe it's the recent deploy." Why were some eliminated? "Connection pool at 40% capacity, rules out that hypothesis. Network packet loss normal, rules out network. Cache hit rate dropped from 95% to 12%, validates cache hypothesis." What data drove convergence? When did you have enough evidence to commit to a mitigation strategy? What was your decision latency and why? Did you take 10 minutes to decide because you were still gathering data, or because the team couldn't agree on the hypothesis, or because the IC was uncertain?

Do Cynefin reflection. What domain were you in at different stages? Did you start in Complicated and transition to Complex as you realized analysis wasn't converging? Did you use the right strategy for each domain? If you were in Complex but kept trying to analyze instead of probe, that's a learning opportunity. When did you transition between domains? As you ran probes and learned, did you move from Complex to Complicated? Could you have recognized the domain earlier and shifted strategy faster? That's organizational learning about how you classify and adapt.

---
{::pagebreak /}
#### Grey Rhino Incidents: When Ignorance Ends Abruptly

**Cynefin Domain Classification**

Grey Rhinos are usually **Complicated** domain problems:

**State: Complicated**

- The problem is known
- Experts can analyze it
- Solutions exist but aren't being applied
- Organizational psychology, not technical complexity

**Key Insight:** 

Grey Rhinos are usually Complicated-domain problems that organizations treat as Clear (ignore) or Complex (too hard to solve). The framework helps recognize that expert analysis and decision-making can address them - the barrier is organizational, not technical.

**Characteristics During the Incident**

**What You Know:**

- This was entirely predictable
- You've known about it for months (or years)
- The fix is probably straightforward
- You're here because you ignored it

**The Psychological Challenge:**

Grey Rhino incidents create cognitive dissonance and organizational shame. Everyone knew this could happen. Now it has happened. The temptation is to pretend it was unpredictable (save face) rather than admit it was ignored (learn the lesson).

**Scenario: The Equifax Data Breach (2017)**

Equifax had a known vulnerability in Apache Struts (CVE-2017-5638) for which a patch existed. The vulnerability was:

- Publicly disclosed: March 7, 2017
- Patch available: March 7, 2017 (same day)
- Exploited against Equifax: Mid-May 2017
- Detected by Equifax: July 29, 2017

**Timeline of Ignoring:**

**March 7: Vulnerability disclosed**

- Apache Struts announces critical remote code execution vulnerability
- Patch available immediately
- Security community warns: patch this now

**March 8-9: Initial response**

- Equifax security team sends notification to patch
- Notification goes to IT teams
- Some systems patched, some not

**March 10 - May 13: The Gap**

- Vulnerability sits unpatched on critical systems
- No systematic verification that all systems patched
- No vulnerability scanning to detect unpatched systems
- Security team assumes patching complete

**Mid-May: Breach Begins**

- Attackers exploit unpatched Apache Struts vulnerability
- Gain access to sensitive data
- 143 million Americans' personal information compromised
- Breach continues undetected for 76 days

**Why This Was a Grey Rhino:**

**High probability:**

- Known vulnerability with active exploits in the wild
- Apache Struts widely targeted
- Patch available (fixing was straightforward)

**High visibility:**

- Security advisories everywhere
- Industry warnings about this specific vulnerability
- Internal security team flagged it

**Actively ignored:**

- Patching notification sent but not verified
- No systematic check for unpatched systems
- Vulnerability scanners not run or not acted upon
- Weeks and months passed without action

**Consequences:**

- $1.4 billion in costs (settlement, remediation, regulatory fines)
- Reputation destruction
- Executive departures
- Regulatory changes across industry

**The Lesson:**
This was entirely preventable. The rhino was visible for months. The cost of fixing it (applying a patch) was trivial. The cost of ignoring it was catastrophic.

**Cynefin Analysis:**

**This was a Complicated-domain problem:**

- Known vulnerability (experts could analyze)
- Known solution (apply patch)
- Known process (patch management)
- The barrier was organizational, not technical

**Why it was ignored:**

- Treated as Clear ("we have a patching process") when process wasn't working
- Or treated as Complex ("too hard to fix all systems") when it was actually straightforward
- Never properly analyzed as Complicated ("what's preventing us from patching?")

**The framework helps:**

- Recognize this is Complicated (expert analysis can solve it)
- Identify the organizational barriers
- Apply systematic solutions

**Grey Rhino Incident Management Principles**

**1. Acknowledge the Rhino Immediately (Cynefin: Classify as Complicated, Not Complex)**

The first step in Grey Rhino incident management is admitting this was preventable. Don't waste time pretending it wasn't. The temptation during a Grey Rhino incident is to perform organizational face-saving: "This was unpredictable! A perfect storm! Who could have known?" Everyone could have known. You did know. You chose not to act. Acknowledge that immediately.

During the incident, the IC needs to state it explicitly: "We knew about this risk. We're responding now." Not as blame assignment - you're not looking for whose fault it is mid-incident - but as factual acknowledgment that prevents the team from operating under false pretenses. Acknowledge it to stakeholders too. Don't hide that this was preventable. Stakeholders can handle "we knew this was a risk and now we're addressing it" better than they can handle "this was completely unpredictable" followed by later revelations that no, you knew.

Classify this as Complicated domain. Expert analysis can solve this. That's the whole point - you ignored it not because it was technically intractable but because organizational factors prevented action. Now that the incident has forced action, bring in the experts. Let them analyze and recommend the fix. The technical problem is usually straightforward. The organizational problem - why you ignored it - is what's complex, but that's for the postmortem, not the incident response.

Focus on resolution, not blame assignment. You're fixing the problem now. Save the organizational reckoning for after service is restored. But do document what was known and when. "This issue was first raised in Q3 2023. It was raised again in Q1 2024 with increased severity. Engineering proposed a fix with 3-week timeline. Fix was deprioritized for feature work. Incident occurred Q2 2024." That timeline goes in the incident doc contemporaneously because memories will get hazy afterward, and the postmortem needs that factual foundation.

**2. Look for the Herd**

Grey Rhinos travel in groups. If you ignored one, you probably ignored others. And if one rhino just charged, the others might be close behind. During the incident response, do a quick scan for related rhinos.

Ask explicitly: "What else have we been ignoring that's similar to this?" If this Grey Rhino was database capacity, what other capacity limits are you approaching? If this was security patching, what other unpatched vulnerabilities exist? If this was technical debt, what other deferred maintenance is waiting to fail? The organizational factors that let you ignore this rhino - schedule pressure, competing priorities, normalized risk - those same factors probably let you ignore similar rhinos.

Prioritize other charging rhinos for immediate action. You don't want to fix this incident only to have a related incident hit tomorrow because you ignored the herd. If you're already mobilized, if executives are already paying attention, if the organization is already facing the pain of ignoring risk, use that moment to address the related risks too. "We're fixing the database capacity issue. We're also addressing the cache capacity issue and the storage capacity issue because they're all the same pattern of deferred scaling." Bundle the rhino management.

**3. Conduct a "Why Did We Ignore This?" Postmortem (Cynefin: Analyze Organizational Barriers)**

Grey Rhino postmortems are different from other types because the technical failure is usually simple. The interesting question - the valuable question - is organizational. Why did you ignore this when you knew it was coming?

Start with the easy question: What happened? Database ran out of capacity, queries timed out, service degraded. That's straightforward. Now the hard question: We knew this could happen. We had the data. We had capacity trend graphs showing we'd hit the limit in June. It's June. Why didn't we fix it?

This is where the postmortem gets uncomfortable and valuable. What organizational factors led to ignoring this? Was it competing priorities - feature work always won against infrastructure work? Was it resource constraints - not enough engineers to do everything? Was it misaligned incentives - nobody got promoted for preventing incidents, but people got promoted for shipping features? Was it optimism bias - "we'll probably be fine, the trend might level off"? Was it diffusion of responsibility - everyone thought someone else was handling it?

What incentives or disincentives exist in the organization? What gets rewarded? What gets punished? If an engineer raises a Grey Rhino risk and proposes fixing it, what happens? Do they get praised for foresight or criticized for being a blocker? If they don't raise it and it fails, what happens? Do they get blamed for not speaking up or does everyone shrug and say "how could we have known?" Those incentive structures shape which risks get addressed and which get ignored.

What other rhinos are we currently ignoring? This is the most valuable question. Don't just fix this one rhino. Use this incident to surface the full herd. Go through your backlog, your tech debt list, your "things we should do someday" document. Which of those are actually Grey Rhinos - risks you're actively ignoring that will eventually charge? Bring them into visibility. Prioritize them honestly.

How do we change our prioritization process? This is the action item that matters. If your current process let you ignore an obvious risk until it became an incident, your process is broken. Fix the process. Maybe it's dedicating 20% of engineering capacity to reliability work that can't be deprioritized. Maybe it's having a quarterly "rhino review" where you explicitly discuss known risks and decide which to address. Maybe it's changing how you measure engineering success to include prevented incidents, not just shipped features.

Do Cynefin reflection: Why did we treat this as Clear (ignore it) or Complex (too hard to solve) instead of Complicated (expert analysis can solve it)? Grey Rhinos are usually Complicated-domain problems. Expert analysis would have shown: "Here's the trend, here's when we hit the limit, here's the fix, here's the timeline." The barrier wasn't technical complexity. It was organizational inertia. What expert analysis would have revealed the organizational barriers? And how do we ensure Complicated-domain problems get expert attention in the future instead of being ignored until they charge?

---
{::pagebreak /}
#### Elephant in the Room Incidents: When Silence Breaks

**Cynefin Domain Classification**

Elephants in the Room often create **Confusion** or **Complicated** domains:

**State: Often Confusion**

- Unclear what the real problem is
- Cultural/psychological factors mixed with technical
- Requires breaking down into components

**Key Insight:** 
Elephants often create Confusion because the technical problem is Clear or Complicated, but the organizational problem (naming the elephant) is Complex. The framework helps separate these.

**Characteristics During the Incident**

**What You Know:**

- Everyone has known about this problem
- Nobody has been willing to discuss it openly
- The incident has finally forced the conversation
- This is as much cultural as technical

**The Psychological Challenge:**

Elephant incidents are fundamentally different because they're organizational dysfunctions manifesting as technical failures. The IC must navigate both technical response and cultural exposure.

**Scenario: The Boeing 737 MAX Crisis**

**The Elephant:**

Boeing had a cultural problem that everyone inside the company knew about but wouldn't openly discuss: increasing pressure to cut costs and accelerate schedules, compromising engineering rigor and safety culture.

**The Elephants (Widely Known Internally):**

**1. Schedule pressure over safety rigor**
Intense pressure to ship

   - Engineers felt rushed
   - Testing compressed
   - Concerns about MCAS design raised but minimized

**2. MCAS single-point-of-failure design**
Lack of strong, insistent technical oversight

   - Relied on single sensor (AOA sensor)
   - No redundancy
   - Engineers knew this was risky
   - Business case won over safety case

**October 29, 2018: Lion Air Flight 610**

- 737 MAX crashes shortly after takeoff
- 189 people killed
- Investigation finds MCAS activated due to faulty AOA sensor

**March 10, 2019: Ethiopian Airlines Flight 302**

- Another 737 MAX crashes
- 157 people killed
- Same failure mode
- Now undeniable: this is design problem, not pilot error

**Consequences:**

- 346 deaths
- 20-month grounding
- $20+ billion in costs
- Criminal charges
- CEO resignation

**The Meta-Lesson:**

The elephants were:

1. **Culture that prioritized schedule/cost over safety** (everyone knew)
2. **MCAS design flaws** (engineers knew)
3. **Retaliation against safety concerns** (employees knew)

The crashes didn't reveal new information to insiders. They forced public acknowledgment of what was already known internally.

**Cynefin Analysis:**

**This was a Confusion-domain problem:**

- Technical problem: Complicated (expert analysis could identify MCAS design flaws)
- Organizational problem: Complex (cultural change requires experimentation)
- Mixed together: Confusion (unclear which domain applies)

**The framework helps:**

- Break down into components
- Technical issue: Complicated (analyze and fix)
- Cultural issue: Complex (experiment with organizational change)
- Apply appropriate strategy to each
**Elephant Incident Management Principles**

**1. Recognize You're Dealing with a Cultural Problem (Cynefin: Break Down Confusion)**

When the incident reveals an elephant, traditional incident management is insufficient. You're not just dealing with a technical failure. You're dealing with an organizational dysfunction that manifested as a technical failure. The system didn't break because of bad code or infrastructure limits. It broke because something everyone knew about was

 never addressed, and now the silence has been broken by catastrophe.

Recognize immediately that you're in Confusion domain. The incident has two components mixed together, and they require different strategies. Break it down: The technical component is usually Clear or Complicated. The database failed, the service went down, the patch wasn't applied. Expert analysis can solve that part. Fix the database, restore the service, apply the patch. That's straightforward incident response.

The organizational component is usually Complex. Why did everyone know about this risk and nobody act? That's emergent from organizational culture, incentive structures, power dynamics, and psychological safety (or lack thereof). You can't analyze your way to a cultural fix. Cultural change requires experimentation - safe-to-fail probes in how you operate, how you communicate, how you reward and punish behavior.

Apply the appropriate Cynefin strategy to each component. Technical problem: bring in experts, analyze, execute the fix. Organizational problem: recognize it's Complex, plan safe-to-fail experiments for after the incident is resolved, don't try to solve organizational dysfunction during the crisis. But do acknowledge that both components exist. Don't pretend this was purely technical when everyone in the room knows it wasn't.

**2. Create Psychological Safety for Truth-Telling**

The incident is forcing the elephant into visibility. People who have been living with this dysfunction, who have been afraid to name it, are now watching it play out as a crisis. If you want the truth - and you need the truth to understand what actually happened - you have to make it safe to tell.

The IC needs to state this explicitly, out loud, to the entire incident response team and to stakeholders: "We need to understand the full scope of this problem. That means hearing uncomfortable truths about how we got here. Nobody will be punished for honestly sharing what they know about this situation, including things that were known before this became an incident."

That declaration creates permission. People who knew about the elephant but were afraid to name it need to hear that it's safe now. People who raised concerns that were ignored need to hear that those concerns are valued, not career-limiting. People who have context about why the organization didn't act need to hear that sharing that context won't make them the scapegoat.

And critically: follow through on that promise. If someone shares uncomfortable truth during the incident or postmortem and then faces retaliation afterward, you've destroyed psychological safety permanently. The IC can make the promise, but leadership has to honor it. Make that explicit to executives too: "We need honest assessment of organizational factors, which means protecting people who provide it."

**3. Postmortem Must Address Organizational Root Causes (Cynefin: Complex Domain for Cultural Change)**

Elephant postmortems are different from other postmortems. Technical root cause is often simple - the thing failed because it wasn't fixed, patched, scaled, or addressed. That's obvious. The valuable postmortem question - the uncomfortable postmortem question - is organizational. Why wasn't it fixed?

Ask elephant-specific questions: Who knew about this problem before it became an incident? Not "was this knowable" but "who actually knew"? Names and dates. Be specific. When did they know? How did they know? Did they raise it? If they raised it, what happened to that concern? If they didn't raise it, why not?

Why wasn't it addressed earlier? This is where you excavate organizational dysfunction. Was it resource constraints - not enough engineers to do everything? Was it competing priorities - other work always won? Was it political - someone senior didn't want to hear about it? Was it diffusion of responsibility - everyone thought someone else was handling it? Was it fear - raising it would be career-limiting?

What organizational factors prevented action? Look at incentive structures. What gets rewarded? What gets punished? What gets ignored? If someone had pushed hard to fix this before it became an incident, would they have been praised or perceived as a troublemaker? If they didn't push and it failed, are they being blamed now? Those incentives shape which elephants get named and which stay hidden.

What happens to people who raise uncomfortable issues? This is about organizational psychological safety. Can junior engineers challenge senior decisions? Can anyone say "I think we're making a dangerous mistake" without fear? Or does raising concerns make you the problem? If your organization punishes messengers, you'll keep having Elephant incidents because people learn to stay silent.

What incentives created or sustained this problem? Sometimes the incentive to ignore the elephant is explicit - "ship features, not reliability work." Sometimes it's implicit - promotions go to feature builders, not problem preventers. Sometimes it's structural - teams don't own their own long-term reliability, so no one has skin in the game. Identify the incentives because changing them is how you prevent future elephants.

What other elephants exist in the organization? Use this incident to surface the rest of the herd. In a psychologically safe postmortem, ask: "What else does everyone know about but nobody talks about?" You'll get a list. Prioritize that list. Start addressing the elephants systematically instead of waiting for them to cause incidents.

Do Cynefin reflection: How do we address the Complex-domain organizational problem? Cultural change is Complex. You can't mandate it. You experiment. What safe-to-fail experiments can we run for cultural change? Maybe it's anonymous surveys about organizational health. Maybe it's rotating incident command to give more people exposure to systemic issues. Maybe it's changing how you measure engineering success to include reliability. Run small experiments, observe what emerges, adapt.

How do we prevent Confusion from paralyzing us? Elephant incidents create Confusion - technical + organizational mixed together. The framework helps: break it down, classify each part, apply appropriate strategies. Don't let the organizational complexity prevent you from fixing the technical problem. And don't let the technical fix make you think you've addressed the organizational dysfunction.

---
{::pagebreak /}
#### Black Jellyfish Incidents: When Cascades Bloom

**Cynefin Domain Classification**

Black Jellyfish (cascades) start in **Chaotic** or **Complex** domains:

**Initial State: Chaotic**

- Cascade spreading rapidly
- Immediate action needed
- Break the feedback loop

**After Breaking Loop: Complex**

- Understanding why the cascade happened
- Experimenting with prevention
- Emergent behavior from dependencies

**Key Insight:** 

Cascades require immediate Chaotic-domain action (break the loop), then Complex-domain learning (understand the system interactions that caused it).

**Characteristics During the Incident**

**What You Know:**

- Something is spreading rapidly
- Multiple systems are failing
- Error rates are accelerating
- Dependencies are cascading

**The Psychological Challenge:**

Black Jellyfish incidents create urgency and confusion. Everything is happening fast. Multiple teams are paging. The scope keeps expanding. The temptation is to fix everything at once, which makes coordination impossible.

**Scenario: The 2017 Amazon S3 US-EAST-1 Outage (Cascade Analysis)**

**The Jellyfish Bloom:**

**T+5 to T+15 minutes: First-Order Cascade**

**Services directly depending on S3 fail:**

- Static websites hosted on S3: Down
- CloudFront CDN serving S3 content: Degraded
- S3-backed applications: Failing

**Unexpected first-order failures:**

- EC2 instance metadata service: Uses S3 for storage → failing
- Lambda: Code stored in S3 → new function invocations failing

**T+15 to T+30 minutes: Second-Order Cascade**

**Services depending on first-order failures cascade:**

- Auto Scaling Groups can't launch instances (need metadata)
- API Gateway endpoints backed by Lambda: Failing
- CloudWatch metrics ingestion degraded

**T+30 to T+60 minutes: Third-Order Cascade**

**The infamous status page problem:**

- AWS Status Dashboard: Hosted on S3 → unavailable
- Can't even communicate about the outage

**Why This Was a Black Jellyfish:**

**Known components:**

- S3 dependencies were documented (mostly)
- Cascade risk in distributed systems is known

**Unpredictable cascade:**

- Speed: 15 minutes from trigger to massive blast radius
- Hidden dependencies: Status page on S3, metadata on S3
- Positive feedback: Retry storms amplifying the problem

**Cynefin Analysis:**

**Initial State: Chaotic Domain**

- Cascade spreading rapidly
- Immediate action required
- No time for analysis or experimentation
- **Action:** Break the feedback loop immediately

**After Stabilization: Complex Domain**

- Understanding cascade mechanics
- Experimenting with prevention strategies
- Learning about dependency interactions
- **Action:** Safe-to-fail probes to understand system behavior

**Black Jellyfish Incident Management Principles**

**1. Stop the Amplification First (Cynefin: Chaotic Domain Action)**

Jellyfish cascades accelerate. That's what makes them dangerous - they amplify themselves through positive feedback loops. Your first priority isn't understanding what went wrong. Your first priority is breaking the amplification so the cascade stops spreading.

Break the loops immediately. Disable retries - if a service is failing, retrying just amplifies the load on it. Shed load aggressively - drop requests, reject connections, fail fast instead of queueing. Isolate spreading failures - if service A is cascading to service B, break that connection. Circuit breakers, kill switches, manual isolation, whatever stops the spread. Stop making it worse - every action you take should reduce amplification, not increase it.

This is Chaotic-domain thinking: act first, understand later. You don't have time to analyze the full cascade path while it's spreading. You need to stop the bleeding. Trip circuit breakers. Shed load. Isolate failing components. Make the system stable even if degraded. Once you've broken the positive feedback loops and the cascade has stopped spreading, then you can move to Complex domain and start understanding why it happened. But stabilization comes first.

**2. Recover in Dependency Order**

After you've stopped the cascade, recovery needs to happen in dependency order. Fix dependencies first, not the biggest problem first. This is counterintuitive because your instinct is to fix whatever's causing the most customer pain, but that instinct will fail you during cascades.

Wrong approach: "API Gateway is down affecting the most customers, fix it first." You restart API Gateway. It comes up, tries to connect to Lambda, Lambda is still failing, API Gateway's health checks fail, it goes back down. You've burned five minutes accomplishing nothing.

Right approach: "S3 → Lambda → API Gateway. Fix in that order." S3 is the root dependency. Fix S3 first. Then fix Lambda, which depends on S3. Then fix API Gateway, which depends on Lambda. Each service comes up in an environment where its dependencies are already healthy. Recovery succeeds instead of thrashing.

Map the dependency graph before you start recovery. It doesn't have to be perfect - approximate is fine. But understand what depends on what. Then recover from the bottom up, from dependencies to dependents. Root services first, then services that depend on those, then services that depend on those. This prevents the painful cycle of restarting something only to have it fail because its dependencies aren't ready yet.

**3. Identify and Break Circular Dependencies**

The nightmare scenario during cascade recovery: circular dependencies. Service A depends on Service B. Service B depends on Service A. Both are down. Neither can start because each is waiting for the other. You're stuck in deadlock, and recovery-in-dependency-order doesn't help because there is no proper ordering.

Common patterns: Service A uses Service B for health checks. Service B uses Service A for configuration. Both services are down. Service A can't start because its health check fails when B is unavailable. Service B can't start because it can't fetch config from A. Both services stay down, waiting for each other.

Breaking strategies: Manual bootstrap. You manually start one service in degraded mode, bypassing its dependency. Once it's up, you start the dependent service, then you bring the first service back to normal mode. This requires having a degraded/bypass mode built into your services. Temporary mocks. You spin up a mock of service A that service B can talk to, start B, then replace the mock with real A. Dependency injection for critical paths. Build your services so they can start without all dependencies being healthy - they degrade gracefully rather than refusing to start. Cold start procedures that document how to manually break circular dependencies because you will encounter them during cascades and you don't want to figure out the procedure while everything's on fire.

**4. Post-Jellyfish Postmortem: Focus on Cascade Mechanics (Cynefin: Complex Domain Learning)**

Black Jellyfish postmortems need to focus on cascade mechanics, not just the initial failure. The root cause might be "S3 had an outage," but that's not the learning. The learning is "S3 outage cascaded through Lambda, API Gateway, and our authentication service because of retry amplification and hidden dependencies." Document the mechanics because that's what helps you prevent future cascades.

Document the full cascade path. Draw the dependency graph - all the services involved, all the connections between them. Show how failure propagated - S3 went down, Lambda started failing health checks, API Gateway started retrying, retries amplified load on Lambda, Lambda degraded further, authentication service depended on API Gateway. Track the cascade through the system step by step. Identify the amplification mechanisms - what made it worse? Retries? Timeouts that were too long? Missing circuit breakers? Cache stampedes when things started recovering? Note surprising dependencies - the connections you didn't know existed until the cascade revealed them.

Organize action items by category: Dependency reduction. Can you remove dependencies? Can you make services more independent? Can you add local caching so temporary upstream failures don't cascade? Cascade resistance. Circuit breakers to prevent retry storms. Bulkheads to contain failures to specific components. Rate limiting to prevent amplification. Monitoring improvements. How do you detect cascades early? Watch for correlation of errors across services. Watch for exponential growth in retry rates. Watch for domino patterns in service health. Recovery procedures. Document how to recover from cascades in dependency order. Document how to break circular dependencies. Document your kill switches and when to use them. Architecture changes. Sometimes cascades reveal that your architecture is fundamentally fragile. What needs restructuring?

Do Cynefin reflection: How do we design systems to resist cascades? This is Complex domain - cascades are emergent from system interactions, not reducible to simple rules. What safe-to-fail experiments can we run to test cascade resistance? Run chaos engineering exercises. Deliberately fail components and observe cascade behavior. Test your circuit breakers under realistic load. Practice your recovery procedures. How do we move from Complex (emergent cascade behavior we don't understand) to Complicated (understood patterns we can design around)? By documenting cascades when they happen, identifying common patterns, and building resistance to those patterns into the architecture.

---
{::pagebreak /}
#### Hybrid Animals and Stampedes: When Multiple Animals Attack

**Cynefin Domain Classification for Stampedes**

Stampedes almost always start in **Confusion** or **Chaotic** domains:

**Initial State: Confusion or Chaotic**

- Multiple risk types interacting
- Unclear which animal is primary
- Different parts require different strategies
- Immediate action needed but unclear what to do

**Key Insight:** 

Stampedes require breaking down into components, classifying each part, and applying appropriate Cynefin strategies to each. This is the framework's strength: handling situations that don't fit neatly into one domain.

**The Stampede Pattern**

Sometimes a single risk event, often a Black Swan, doesn't just cause direct damage. It stresses the system in ways that reveal all the other animals that were hiding in the shadows.

Think of it like a stampede in the wild: one lion (Black Swan) appears, and suddenly you realize the savannah is full of animals you didn't know were there. Grey Rhinos that were grazing peacefully start charging. Elephants in the Room become impossible to ignore. Black Jellyfish that were floating dormant suddenly bloom and sting everything.

The system was always full of these risks. The Black Swan just revealed them.

**Cynefin Framework for Managing Stampedes**

**Step 1: Break Down the Stampede**

When multiple animals attack simultaneously, you're in Confusion domain. The first step is decomposition: identify each animal. What Black Swan triggered this? What Grey Rhinos are now charging? What Elephants are now visible? What Black Jellyfish cascades are blooming? Then classify each component. Black Swan components are Chaotic or Complex. Grey Rhino components are Complicated. Elephant components exist in Confusion or Complex. Black Jellyfish components are Chaotic or Complex.

**Step 2: Apply Appropriate Strategy to Each Component**

For Black Swan components in Chaotic or Complex domains, act immediately to stabilize (Chaotic phase), then experiment to learn (Complex phase). Don't try to analyze your way to a solution - the novelty requires action-based learning. For Grey Rhino components in Complicated domain, expert analysis can solve this. The barrier is organizational, not technical. Apply systematic solutions that address the known risk. For Elephant components in Confusion or Complex domains, break down further into technical versus organizational aspects. The technical side is usually Complicated. The organizational side is usually Complex and requires experimentation. Create psychological safety for truth-telling about what everyone already knows. For Black Jellyfish components in Chaotic or Complex domains, break feedback loops immediately (Chaotic response), then understand cascade mechanics (Complex investigation), and recover in dependency order.

**Step 3: Coordinate Multiple Strategies**

The IC's challenge is that different components need different thinking. You can't apply one strategy to everything, and you must coordinate without creating confusion. The coordination principles: explicitly discuss which domain each component is in so everyone understands the thinking required. Assign different responders to different components based on their ability to work in that domain. Use different communication channels for different strategies - don't mix Chaotic-domain rapid action updates with Complex-domain experimentation discussions. Document which strategy is being applied where so the team maintains coherent awareness across parallel workstreams.

**Step 4: Recognize Domain Transitions**

As you address components, they transition through domains. The natural progression runs Chaotic → Complex → Complicated → Clear for technical problems, and Confusion → Components classified → Appropriate strategies applied for the overall incident. Watch for components moving between domains as your understanding increases. Watch for new components appearing - more animals revealed as you understand the system better. Watch for interactions between components creating new domains - what started as two separate Complicated problems might interact to create Complex emergent behavior.

**Example 1: The AWS DynamoDB Outage (October 20, 2025) as a Stampede**

**The Trigger:**
At 12:11 AM PDT (07:11 UTC) on October 20, 2025, AWS engineers detected a rise in error rates and latency across multiple services in the US-EAST-1 region. By 1:26 AM (08:26 UTC), the problem had escalated into full DynamoDB endpoint failures. The root cause was traced to a DNS resolution error affecting DynamoDB's control layer, a misconfigured DNS propagation update that triggered recursive health checks and retry storms.

**The Stampede Breakdown:**

This incident revealed a classic stampede: multiple animals attacking simultaneously [White, 2025b].

The Black Jellyfish Component operated in Chaotic then Complex domains. A minor DNS misconfiguration rippled across opaque dependencies in unpredictable ways. DynamoDB's centrality in AWS's transaction and state management layers caused cascading dependency failures. The disruption was nonlinear, hidden, and widely felt by users unaware of their reliance on DynamoDB. The Cynefin action required breaking feedback loops immediately (Chaotic response), then understanding cascade mechanics (Complex investigation).

The Grey Rhino Component existed in Complicated domain. The risks from talent loss and interdependencies were visible for years. Industry voices had warned that attrition was undermining cloud stability. Between 2022 and 2025, Amazon laid off over 27,000 employees, with attrition reaching 81% in key teams. Expert analysis could have solved this - the barrier was organizational, not technical.

The Elephant in the Room Component moved from Confusion to Complex domains. Inside Amazon, discussions around staff loss and burnout were politically radioactive. The cultural silence prevented action, even as warning signs mounted. Institutional memory, often invisible and untracked, evaporated. Without that folklore, detection time ballooned to 75 minutes.
- **Cynefin Action:** Break down into technical (Complicated) and organizational (Complex) components. Create psychological safety for truth-telling.

**Detailed Timeline (UTC):**

- **06:45** - Early anomaly detection
- **07:00** - DNS propagation failures begin
- **07:11** - Cross-region impact initiates
- **07:25** - First customer alerts (Reddit, Coinbase)
- **07:45** - Retry amplification across EC2 and DNS
- **08:10** - AWS status page acknowledges degradation
- **08:26** - Full DynamoDB endpoint failures
- **09:20** - Major global customer impact (Snapchat, Venmo, TikTok, Fortnite, Alexa)
- **10:30** - Mitigation escalated
- **11:15** - Cross-regional failover attempted
- **12:00** - Partial restoration of DynamoDB
- **14:00** - Stabilization phase begins
- **16:30** - AWS publishes Health Dashboard update
- **18:45** - Major customer backlog clearance
- **22:00** - AWS declares incident resolved

**Observed Impact:**

- Duration: ~15 hours from onset to declared resolution
- Scope: 113 AWS services across multiple regions
- Notable Customers Affected: Reddit, Coinbase, Snapchat, Venmo, TikTok, Fortnite, Alexa
- User Symptoms: Latency above 5s, authentication errors, session failures
- Data Consequences: Delayed queue processing, minor corruption mitigated by replay

**Why This Was a Stampede:**

The incident wasn't just a technical failure; it was a crisis of forgotten knowledge. A generation of dashboards had nobody left who could interpret them under stress. The outage exposed a deeper form of technical debt: epistemic debt. When memory leaves, the system's ability to self-repair dies quietly.

**The Coordination Challenge:**

The IC had to simultaneously:

- Break cascade loops (Chaotic action for Black Jellyfish)
- Address infrastructure capacity issues (Complicated analysis for Grey Rhino)
- Navigate organizational silence about talent loss (Complex experimentation for Elephant)

All while coordinating across 113 affected services and multiple regions. This is why stampedes are so dangerous; they require multiple types of thinking at once, and the organizational context (the Elephant) makes technical response more difficult.

**Cynefin Analysis:**

The initial state was Chaotic domain. The cascade was spreading rapidly through DynamoDB dependencies. Immediate action was required to break retry storms with no time for analysis or experimentation. The action: break the feedback loop immediately.

After stabilization, the situation moved to Complex domain. Teams needed to understand cascade mechanics across 113 services, experiment with prevention strategies, and learn about dependency interactions. The action: safe-to-fail probes to understand system behavior.

The Grey Rhino Component existed in Complicated domain. Known risks from talent loss and interdependencies could have been addressed through expert analysis identifying the organizational barriers. The barrier was organizational, not technical. The action: systematic solutions for knowledge retention and redundancy.

The Elephant Component progressed from Confusion to Complex. The technical problem (DNS misconfiguration) was Complicated. The organizational problem (cultural silence preventing action) was Complex. Mixed together, they created Confusion where it was unclear which domain applied. The action: break down into components and apply appropriate strategy to each.

The postmortem revealed what was genuinely unpredictable: the specific interaction between DNS misconfiguration and DynamoDB's control layer, the speed and scope of cascade across 113 services, and the extent of hidden dependencies. What could have been better: institutional memory retention (Grey Rhino that became visible), cultural safety to discuss talent loss risks (Elephant that became visible), and dependency mapping and cascade resistance (Black Jellyfish prevention).

**The Meta-Learning:**
This stampede revealed all three animals simultaneously. The DNS misconfiguration (Black Jellyfish trigger) exposed the Grey Rhino (known but ignored talent loss risks) and forced acknowledgment of the Elephant (cultural silence about organizational issues). The incident demonstrates that when multiple animals attack, you can't address them sequentially; you must coordinate multiple response strategies simultaneously.

**Lessons for SREs:**

- Institutional memory is part of your reliability stack
- People need redundancy too; losing senior staff isn't just a headcount issue, it's a hazard amplifier
- Observe the topology, not just the service; map secondary dependencies
- Measure resilience by adaptability, not just uptime
- Evolve incident protocols; local fixes don't work in globally entangled systems

**Example 2: The October 10, 2025 Crypto Crash as a Stampede**

**The Trigger:**
President Trump's tweet about tariffs triggered a market crash that revealed multiple animals.

**The Stampede Breakdown:**

The Black Swan Component operated in Chaotic then Complex domains. The timing of the tweet was unpredictable, and the market reaction was unprecedented in scale. The Cynefin action: act immediately to stabilize markets, then experiment to understand new patterns.

The Grey Rhino Component existed in Complicated domain. Exchange capacity issues had been known for months, and infrastructure limitations were visible but ignored. The Cynefin action: expert analysis can solve this - apply systematic capacity fixes.

The Black Jellyfish Component moved through Chaotic to Complex domains. The cascade rippled through exchanges with positive feedback loops amplifying losses. The Cynefin action: break feedback loops immediately, then understand cascade mechanics.

The Elephant Component progressed from Confusion to Complex. The leverage culture was widely known but unspoken, with organizational dysfunction preventing honest discussion. The Cynefin action: break down into technical (Complicated) and organizational (Complex) components.

The coordination challenge was severe. The IC had to stabilize markets (Chaotic action for Black Swan), fix exchange capacity (Complicated analysis for Grey Rhino), break cascade loops (Chaotic action for Black Jellyfish), and address leverage culture (Complex experimentation for Elephant) - all simultaneously. This is why stampedes are so dangerous. They require multiple types of thinking at once.

**Stampede Incident Management Principles**

**1. Break Down, Don't Simplify (Cynefin: Handle Confusion by Decomposition)**

Stampedes are Confusion-domain problems by definition - multiple animals attacking simultaneously, each requiring different approaches. The wrong instinct is to simplify: "Let's treat this as one big problem and apply one strategy." That instinct will fail because you're trying to force heterogeneous components into a single framework.

Break it down instead. Identify each animal in the stampede. Is that a Black Swan (unprecedented)? Is that a Grey Rhino (ignored risk)? Is that a Black Jellyfish (cascade)? Is that an Elephant (cultural dysfunction)? Name each component explicitly. Don't blur them together into "everything's broken." Distinguish them.

Then classify each component's Cynefin domain. The Black Swan might be Complex. The Grey Rhino might be Complicated. The cascade might be Chaotic. The Elephant might create Confusion because it mixes cultural and technical. Each component gets its own domain classification, and that classification drives strategy.

Apply the appropriate strategy to each component. The Chaotic cascade gets immediate action - break the feedback loops. The Complicated Grey Rhino gets expert analysis. The Complex Black Swan gets safe-to-fail probes. The Confusion Elephant gets broken down into technical (Complicated) and cultural (Complex) components. You're running multiple strategies in parallel, each matched to its domain.

And critically: coordinate without creating more confusion. This is hard. You're managing multiple workstreams using different approaches. The IC's job is synthesis - maintaining a coherent picture of the stampede while enabling parallel execution. More on that in principle 2.

What not to do: Treat the whole stampede as one type of problem. "This is a crisis, we're in Chaotic domain, everyone act immediately." But some components need analysis, not action. Some need probes, not decisions. Forcing everything into one domain wastes effort on components that need different thinking. Don't apply one strategy to everything. Don't ignore the complexity by pretending it's simpler than it is. And don't simplify when you should decompose - decomposition is the tool for handling Confusion.

**2. Coordinate Multiple Strategies**

Different components need different thinking, and the IC must coordinate multiple parallel strategies without creating chaos. This is the hard part of stampede management - not the technical work, but the coordination work. You're running Chaotic-domain immediate action, Complicated-domain expert analysis, and Complex-domain experimentation simultaneously. Each needs different people, different decision-making approaches, different communication styles. The IC synthesizes without homogenizing.

Use explicit domain classification for each component. Don't just track "components A, B, and C." Track "Component A (Black Jellyfish - Chaotic), Component B (Grey Rhino - Complicated), Component C (Elephant - Confusion)." The domain label tells everyone what strategy applies to that component. It creates shared understanding without lengthy explanations.

Set up separate workstreams for different domains. One workstream handles the Chaotic cascade - they're breaking feedback loops, opening circuit breakers, stabilizing immediately. Another workstream handles the Complicated analysis - they're investigating the Grey Rhino, bringing in experts, forming hypotheses. A third workstream handles the Confusion breakdown - they're separating technical from cultural components. Each workstream operates independently with its own Technical Lead, using the approach appropriate for its domain.

Use different communication channels for different strategies. The Chaotic workstream needs rapid updates - every 5-10 minutes, "here's what we just did, here's what we're doing next." The Complicated workstream needs analysis updates - every 30 minutes, "here's what we've learned, here's our hypothesis, here's our next investigation." The Complex workstream needs learning updates - every hour, "here's what emerged from our probes, here's what we're adapting." Don't force them all into the same cadence.

And critically: regular synthesis of all workstreams. The IC isn't solving problems. The IC is maintaining situational awareness across all workstreams, identifying interactions between components, making strategic decisions about priorities and resources. Every 30 minutes, the IC synthesizes: "Here's where we are across all components, here are the interactions we've identified, here's what we're prioritizing and why." That synthesis keeps everyone operating from the same big-picture understanding even while executing different strategies.

**Stampede Coordination Playbook: Practical Implementation**

When multiple animals attack simultaneously, standard incident response breaks down. You need a playbook that enables parallel coordination without chaos. Here's how to structure it.

**War Room Structure for Stampedes**

**Physical/Virtual Organization:**

**1. Main War Room (IC + Scribes + Communications)**

   - Central coordination hub
   - Single source of truth (incident timeline, status board)
   - IC synthesizes information from all workstreams
   - Communications Lead manages all external messaging

**2. Workstream Rooms (One per Animal/Domain)**

   - Separate physical/virtual spaces for each component
   - Each workstream has its own Technical Lead
   - Each workstream operates independently using appropriate strategy
   - Workstream leads report to Main War Room IC at regular intervals

**3. Cross-Stream Coordination Channel**

   - Shared document/chat for information that affects multiple workstreams
   - IC monitors for interactions between components
   - Technical Leads use this to coordinate dependencies

**Communication Protocols for Multiple Workstreams**

**Regular Cadence:**

- Every 15 minutes: Workstream leads provide status update to Main War Room
- Every 30 minutes: IC synthesizes all workstreams into unified status
- On-demand: Workstream can escalate to IC if blocked or if component interactions discovered

**Update Format from Workstream to IC:**
```
Workstream: [Animal Type - Domain]
Status: [Chaotic/Complex/Complicated/Clear]
Progress: [What we've done]
Findings: [What we've learned]
Next Actions: [What we're trying next]
Blockers: [What's preventing progress]
Interactions: [How this affects other workstreams]
```

**IC Synthesis Template:**
```
Incident Status: [Overall]
Components: [List all animals/domains active]
Interactions: [How components are affecting each other]
Priority: [Which component needs most attention]
Decisions Needed: [Where IC input required]
```

**Information Synthesis Techniques for IC**

**The IC's Role in Stampedes:**

The IC doesn't solve technical problems. The IC synthesizes information from multiple parallel workstreams and makes strategic decisions.

**Synthesis Method 1: The Funnel**

Start wide (all components, all possibilities), then narrow as understanding emerges:

**1. Wide Phase (First 30 minutes):**

   - Identify all animals present
   - Classify each component's domain
   - Assign workstreams
   - Don't try to understand interactions yet

**2. Convergence Phase (Next 1-2 hours):**

   - Workstreams report findings
   - IC identifies component interactions
   - Adjust priorities based on interactions
   - Make strategic decisions about resource allocation

**3. Focus Phase (Once patterns emerge):**

   - IC directs coordination of critical interactions
   - Prioritize workstreams that unblock others
   - Make decisions about trade-offs between components

**Synthesis Method 2: Dependency Mapping**

Map how components affect each other:

- Component A (Black Jellyfish cascade) is blocking Component B (Grey Rhino fix)
- Solution: Break cascade first (Component A), then address underlying issue (Component B)
- Component C (Elephant cultural issue) is preventing honest communication about Component D (Black Swan)
- Solution: Create psychological safety (Component C) to enable accurate assessment (Component D)

**Synthesis Method 3: Time-Based Prioritization**

Different components have different time pressures:

- Component requiring immediate action (Chaotic) gets priority over Component requiring analysis (Complicated)
- But: Component that unblocks others gets priority over isolated Component

**Decision-Making Framework When Conflicts Arise**

**Conflict Type 1: Resource Conflicts**

"Two workstreams need the same expert/same system access"

**Resolution:**

- IC assigns priority based on: which component blocks others, which has highest customer impact, which has shortest time window
- Communicate decision clearly: "Expert goes to Workstream A for next 30 minutes, then B. Here's why."

**Conflict Type 2: Strategy Conflicts**

"Workstream A says stabilize, Workstream B says investigate"

**Resolution:**

- IC decides based on Cynefin domain classification
- Chaotic components: stabilize first
- Complicated components: investigate first
- If genuine conflict, components might need different approaches (that's the point of stampedes)

**Conflict Type 3: Communication Conflicts**

"Workstream A wants to communicate X, Workstream B wants to communicate Y, they conflict"

**Resolution:**

- Communications Lead (not workstream leads) owns all external messaging
- Communications Lead synthesizes workstream updates into unified message
- If workstreams have conflicting information, IC makes call: which is most accurate, which gets communicated

**Example: Coordinating Multiple Strategies Simultaneously**

**Scenario:** DNS misconfiguration (Black Jellyfish) cascading while talent loss (Grey Rhino) prevents quick diagnosis, and cultural silence (Elephant) blocks honest assessment.

**T+0 to T+30 minutes: Initial Classification**

- IC: "This is a stampede. Breaking down: Component A (Black Jellyfish cascade) = Chaotic, Component B (Talent loss impact) = Complicated, Component C (Cultural silence) = Confusion."
- IC assigns:
  - Workstream A: Break cascade loops (Chaotic action)
  - Workstream B: Analyze talent loss impact (Complicated analysis)
  - Workstream C: Address cultural barriers (Confusion breakdown)

**T+30 to T+90 minutes: Parallel Execution**

- Workstream A: Breaking retry storms, opening circuit breakers, shedding load
- Workstream B: Analyzing which missing expertise is blocking diagnosis
- Workstream C: Creating psychological safety for honest assessment

**T+90 minutes: IC Synthesis**

- IC receives updates from all three workstreams
- IC identifies interaction: Workstream C's psychological safety work enables Workstream B to accurately assess talent gaps, which helps Workstream A understand why diagnosis is slow
- IC decision: Prioritize Workstream C (cultural work) because it unblocks others

**T+90 to T+180 minutes: Coordinated Response**

- Workstream C establishes psychological safety
- Workstream B now accurately assesses: "Missing DNS expertise is blocking diagnosis"
- Workstream A adjusts: "Focusing on breaking cascade while DNS experts from other teams are brought in"

**Key Insight:** 
The IC doesn't solve any component. The IC synthesizes information, identifies interactions, and coordinates parallel strategies.

**Warning Signs You're Not Coordinating Well:**

- Workstreams are duplicating effort
- Workstreams are conflicting with each other
- IC is trying to solve technical problems instead of coordinating
- Information from workstreams isn't being synthesized
- Decisions are being made in isolation without considering interactions

**The Fix:** Explicit synthesis cadence, clear communication protocols, IC focused on coordination not execution.

**3. Watch for Interactions**

Components in a stampede don't exist in isolation - they interact. A Grey Rhino charging can trigger a Black Jellyfish cascade. An Elephant being named can reveal more Rhinos you didn't know existed. Understanding these interactions is critical because they change your priorities and strategies.

Monitor for components triggering other components. You're fixing the Grey Rhino database capacity issue, and that fix triggers a Black Jellyfish cascade because all your services try to reconnect simultaneously and overload the database. You weren't expecting that interaction, but now you need to address it. Or you're breaking a Black Jellyfish feedback loop, and that reveals a Grey Rhino - turns out the cascade was masking an underlying capacity problem that's been growing for months.

Watch for domain transitions as you address components. You start treating something as Complicated - bring in experts, analyze systematically. But as you investigate, you realize it's actually Complex - no amount of analysis is revealing the pattern because it's emergent. That domain transition means you need to shift strategy from analysis to probes. Or you stabilize a Chaotic cascade, and once stable it moves to Complex where you can start experimenting to understand why it happened.

Look for new components appearing - more animals revealed. You're responding to what you thought was a Black Swan. Then someone finally feels safe enough to admit this was actually a known risk (Grey Rhino). Then you discover the reason it was ignored was cultural dysfunction (Elephant). What started as one animal becomes a stampede as the investigation reveals more. Don't resist that revelation - adjust your response to match reality.

And watch for interactions creating new domains. Two Complicated-domain problems can interact to create a Complex-domain problem. Two independent components that each make sense individually combine in ways that create emergent behavior you can't predict. When interactions create complexity, acknowledge it and shift your strategy accordingly.

**4. Post-Stampede Postmortem: The Full Picture**

Stampede postmortems are the most complex because you're not analyzing one incident - you're analyzing multiple incidents that happened simultaneously and interacted. Don't simplify the postmortem to match what you wish had happened. Document what actually happened in its full complexity.

Address each animal individually first. The Grey Rhino that charged: what was it, when was it first identified as a risk, why wasn't it addressed? The Black Jellyfish cascade: what triggered it, how did it propagate, what feedback loops amplified it? The Elephant that got revealed: what was everyone afraid to name, why was there silence, what changed when it got named? Treat each component as its own incident with its own root cause analysis.

Then address how they interacted. This is the unique value of stampede postmortems. The Grey Rhino charging triggered the Black Jellyfish cascade. The Black Jellyfish cascade forced the Elephant into visibility because the crisis made silence untenable. The Elephant being named revealed more Grey Rhinos. Map these interactions explicitly because they reveal system dynamics you can't see by analyzing components in isolation.

Document which Cynefin domains were involved for each component. The Grey Rhino was Complicated - we knew about it, experts could have analyzed and fixed it. The Black Jellyfish was Chaotic during the cascade, then transitioned to Complex for understanding why. The Elephant created Confusion because it mixed technical and cultural. That domain mapping helps you understand whether you used appropriate strategies.

Assess whether appropriate strategies were used. Did you treat the Chaotic cascade with immediate action or did you waste time analyzing? Did you treat the Complicated Grey Rhino with expert analysis or did you guess? Did you break down the Confusion Elephant or did you try to force it into one domain? Strategy mismatches are learning opportunities.

Evaluate how coordination worked (or didn't). Did the IC successfully synthesize across workstreams? Did workstreams duplicate effort or conflict? Did information flow effectively? Were strategic decisions made with awareness of component interactions? Coordination during stampedes is hard, and honest assessment of what worked and what didn't helps you improve.

Do Cynefin reflection: Did we properly classify each component into its domain? Classification drives strategy, so misclassification causes strategy mismatches. Did we use the right strategy for each domain? If you used Complicated-domain analysis on a Complex problem, that's a mismatch worth learning from. How did we coordinate multiple strategies? What worked about our coordination approach? What created confusion? And what would help next time? Not "how do we prevent this specific stampede" but "how do we get better at handling multiple animals simultaneously?"

---
{::pagebreak /}
### Universal Incident Management Principles Across the Bestiary

#### 1. Information Flow Is Everything

Look back at every scenario in this chapter. The AWS S3 outage where engineers couldn't communicate about the incident because the status page was hosted on S3. The Knight Capital disaster where recognition of the problem took 30 minutes because monitoring wasn't configured for the specific failure mode. The Equifax breach where a patch notification went to IT teams but systematic verification that all systems were patched never happened. The Boeing 737 MAX where safety concerns were raised but never reached decision-makers with enough urgency to change course.

Every one of these failures - Black Swans, Grey Swans, Grey Rhinos, Elephants, cascades, stampedes - every single one has information flow failure at its core. The information existed. Someone knew, or the monitoring showed it, or the weak signals were present. But that information didn't flow to where it was needed, when it was needed, with enough fidelity to act on it.

This is why the Unwritten Laws of Information Flow aren't abstract theory - they're operational requirements. Information flows to where it's safe: if people fear punishment, they hide problems during incidents. You operate with incomplete information. You make worse decisions. The incident lasts longer and causes more damage. Information flows through trust networks, not reporting lines: org charts don't match reality during crises. Direct channels between domain experts and decision-makers matter more than hierarchical escalation. Information degrades crossing boundaries: every hop in the communication chain loses context and urgency. The engineer who noticed the anomaly knows it's critical. By the time it traverses manager → director → VP → IC, it's been downgraded to "something to look at when we have time."

Your incident response structure has to be designed for information flow first. That's why ICS puts the Incident Commander in direct contact with subject matter experts, not buried under five layers of management. That's why war rooms exist - to short-circuit organizational boundaries and create direct communication channels. That's why the Scribe role matters - real-time documentation prevents information loss as the incident evolves. That's why blameless postmortems are foundational - psychological safety enables honest information sharing, and without honest information you can't learn.

When you're designing incident response procedures, optimizing monitoring strategies, or building postmortem culture, ask yourself: Does this improve information flow, or does it create barriers? Because across all animal types, all Cynefin domains, all scales of crisis, incident management success depends on getting the right information to the right people at the right time. Everything else is commentary.

#### 2. Psychological Safety Is Infrastructure

You cannot effectively manage incidents in a blame culture. Period. Not "it's harder" or "it's suboptimal." You cannot do it. Blame destroys information flow, and information flow is everything.

Think about the Elephant scenarios in this chapter. Boeing 737 MAX, where engineers knew about MCAS risks but didn't push back hard enough against schedule pressure. The countless Grey Rhinos where people knew about risks but were afraid to be the one who kept raising the alarm. Every incident where someone in the postmortem says "I thought it might be my deploy, but I didn't want to say..." because admitting mistakes feels career-limiting.

Psychological safety isn't a nice-to-have for team happiness. It's a technical requirement for incident response. You need people to admit mistakes immediately so you can investigate the right hypothesis. You need junior engineers to speak up when they notice something wrong, even if it contradicts what senior people think. You need honest assessment of organizational dysfunction in Elephant postmortems. None of that happens if people fear consequences for telling the truth.

Google's Project Aristotle found psychological safety was the #1 predictor of team effectiveness, ahead of individual talent, team composition, or any other factor. For incident management, it's even more critical. Incidents are high-stress, time-pressured situations where the truth is uncomfortable and mistakes are inevitable. If your culture punishes honesty during those situations, you get silence and hidden information.

Build psychological safety deliberately. Leaders model vulnerability - admit mistakes, say "I don't know," show that uncertainty is acceptable. Thank people for bad news and dissent - make it clear that surfacing problems is valued. Never punish someone for being wrong - punish hiding information, not making errors. Celebrate learning, not perfection - incidents are learning opportunities, and learning requires honest examination of what went wrong. Make it explicit in incident response and postmortems: "Nobody will be punished for honestly sharing what they know."

And critically: follow through. If someone shares uncomfortable truth and then faces retaliation, you've destroyed psychological safety permanently. Protection has to be real, not performative. Make that clear to executives: we need honest assessment, which means protecting people who provide it.

#### 3. Documentation Is Time-Shifted Information Flow

Real-time documentation during incidents isn't bureaucracy. It's information flow across time. The Scribe captures what's happening now so that people in the future - including your future self two hours from now - can understand what happened and why.

This serves multiple critical purposes. It maintains a coherent narrative during the incident itself. When the IC rotates after six hours, the incoming IC reads the timeline and understands the current state without requiring a 30-minute handoff. When stakeholders ask "what's happening," the Comms Lead pulls from the documented timeline instead of relying on fragmented Slack threads and fading memory.

It enables high-quality postmortems. Two weeks after the incident, your memory will have rewritten the story. Decisions that were uncertain at the time will seem obvious in retrospect. Hypotheses that were seriously considered and then rejected will be forgotten. Real-time documentation captures your actual reasoning with incomplete information, not the cleaned-up story you tell yourself afterward. The postmortem quality depends entirely on the contemporaneous notes.

It teaches future responders. When the next incident happens - and there will be a next incident - responders read previous incident docs to understand patterns, learn decision-making frameworks, and see how others handled uncertainty. Well-documented incidents become training material for handling future uncertainty.

It builds organizational memory. Without documentation, every incident response team reinvents practices from scratch. With documentation, you accumulate knowledge about your system's failure modes, your organization's response capabilities, and the effectiveness of different strategies. That accumulated knowledge makes you collectively smarter.

And critically: it documents Cynefin domain classification and transitions. "Started classified as Complex, attempted safe-to-fail probes. At T+30 realized situation was Chaotic, shifted to immediate stabilization actions. At T+60 after stabilization, moved to Complicated where expert analysis helped." That domain awareness captures not just what you did but why you did it, and helps you learn whether you matched strategy to problem type. Future incidents benefit from that reflected learning.

#### 4. Decision-Making Under Uncertainty Is A Core Skill

During incidents, you will make decisions with 20-30% of the information you'd like to have. That's not a failure of preparation. That's the nature of incident response. Learning to decide under uncertainty is a core skill, and the framework for it is simpler than you think: categorize decisions by reversibility.

Reversible decisions get made fast. Can this be undone if you're wrong? Then do it quickly. Routing traffic differently - you can revert immediately. Opening a circuit breaker - you can close it. Adding capacity - you can remove it. Trying a potential fix you can roll back in 30 seconds - do it. The cost of trying is low, the cost of not trying is continued customer impact, and even being wrong teaches you something about the system's behavior. These reversible decisions are safe-to-fail probes in Complex domain thinking - you're not committing to a solution, you're testing hypotheses.

Irreversible decisions take more time, even during incidents. Can't be undone easily? Slow down and make sure. Data deletion you can't recover from. Public commitments to customers that you'll be held to. Major architectural changes that can't be rolled back mid-incident. These are one-way doors. You need higher confidence before walking through them, and that means taking time to gather more information or consult more expertise.

Use Cynefin classification to guide your decision-making approach. In Chaotic domain: act immediately, preferring reversible actions that stabilize without locking you into specific paths. In Complex domain: run safe-to-fail experiments that are reversible by design - you're learning through action, and reversibility means failed experiments don't make things worse. In Complicated domain: analyze then decide - you might be committing to irreversible fixes, but expert analysis gives you confidence. In Clear domain: follow established procedures, which are usually reversible because they've been tested many times.

The meta-skill isn't making perfect decisions with incomplete information. The meta-skill is recognizing which decisions are reversible (make them quickly) versus irreversible (take appropriate time), and matching your decision-making approach to the Cynefin domain you're operating in.

#### 5. Postmortems Are Organizational Learning

Incidents are expensive. The cost isn't just downtime and customer impact - it's also the opportunity cost of every engineer who responded, every meeting that got rescheduled, every feature that didn't ship. The only way that cost generates value is if you learn from it. Postmortems are how organizations learn.

Good postmortems have recognizable patterns. People admit mistakes and confusion - "I thought it might be my deploy, but I waited 15 minutes before saying anything because I wasn't sure." "I didn't understand the dependency between services A and B." "We debated for 20 minutes about whether to failover because we couldn't agree on the risk." That honesty signals psychological safety and enables real learning. Root causes include organizational factors, not just technical - "The database ran out of capacity" is incomplete. "The database ran out of capacity because capacity planning wasn't prioritized against feature work, and nobody owned long-term infrastructure health" is complete. Action items address systemic issues - not "fix this specific bug" but "change how we prioritize infrastructure work" or "establish ownership for system-wide concerns."

Good postmortems acknowledge complexity when it exists. For Grey Swans and Black Jellyfish, single root causes are fiction. "The cascade happened because of the complex interaction of retry behavior, timeout settings, connection pool exhaustion, and cache invalidation patterns" is honest. "The cascade happened because the database was slow" is oversimplification that prevents learning. And critically, good postmortems include Cynefin domain classification - "We started in Complex domain but kept trying to analyze instead of probe, which wasted 30 minutes. Once we recognized the domain and shifted to safe-to-fail experiments, we made progress." That reflection teaches decision-making, not just technical fixes.

Bad postmortems also have recognizable patterns. Single root cause for a complex incident - forcing messy reality into simple stories prevents learning about system dynamics. No one admits any errors - that signals lack of psychological safety and means the real story is hidden. Narrative is too clean and simple - incidents are messy, and cleaned-up narratives lose the lessons about handling uncertainty. Repeat incidents aren't acknowledged - if this is the third time the same thing failed, that's the story, not just the technical details. And no reflection on decision-making approach - if you used the wrong strategy for the Cynefin domain, that's valuable learning even if the incident got resolved.

Postmortem quality matters because low-quality postmortems waste the learning opportunity. You paid the cost of the incident. Extract the value through honest, comprehensive, systemic learning.

#### 6. Action Items Must Be Completed

The best postmortem is worthless if action items aren't completed. This sounds obvious, but go check your postmortem action item backlog right now. How many items from incidents 6 months ago are still open? How many items are assigned to "team" instead of individuals? How many critical items have been deprioritized repeatedly for feature work?

Most organizations have excellent postmortems and terrible follow-through. They write comprehensive analyses, identify root causes, propose systemic fixes, and then... nothing happens. The action items sit in a backlog. People move on to other work. Three months later the same failure mode causes another incident because the fix was never implemented.

Make action item completion a first-class concern. Every item has a single owner - not "database team" but "Alice." Accountability requires names. Critical items get completed within the current sprint - if it's critical enough to call critical, it's critical enough to do now, not someday. Create a dashboard of postmortem action items that's visible to engineering leadership - transparency creates accountability. Conduct regular review, maybe weekly or biweekly, where teams report on action item status. Escalate immediately if items are blocked - if an action item can't be completed because of resource constraints or competing priorities, that's a leadership decision, not something that silently rots in the backlog.

And here's the uncomfortable truth: completion rate of postmortem action items is a better predictor of future incident severity than any technical metric. Organizations that complete action items learn from incidents and prevent recurrence. Organizations that don't complete action items have the same incidents repeatedly, with increasing severity as the unfixed vulnerabilities accumulate.

These six universal principles apply across all animal types, but how you execute them varies dramatically depending on which animal you're facing. Information flow during a Black Swan (unprecedented) looks different from information flow during a Grey Rhino (ignored known risk). Psychological safety matters for all animals, but it's existential for Elephants where the incident itself is about organizational dysfunction. Understanding these universal principles gives you the foundation. Understanding the specific animals gives you the strategy.

---

### Conclusion: Incident Management for the Menagerie

We started this chapter in 1970s California, where emergency responders were learning that fires, earthquakes, and hazmat spills all required human coordination more than technical expertise. The Incident Command System emerged from that recognition: different types of emergencies need different responses, but all of them need structured information flow and clear decision-making.

Fifty years later, we're running distributed systems that fail in ways the ICS designers never imagined. But the fundamental insight still holds: different problems require different thinking. That's why this chapter married the Cynefin Framework to our risk bestiary. Cynefin tells you how to think about the problem. The animals tell you what type of risk you're facing. Together, they give you a decision-making framework for the unprecedented, the complex, and the knowingly ignored.

Black Swans demand Chaotic-domain action followed by Complex-domain learning. You can't analyze your way through genuine novelty. Grey Swans start in Complicated territory but reveal themselves as Complex - weak signals exist if you're watching, but the interactions are genuinely emergent. Grey Rhinos are usually Complicated problems that organizations treat as impossible to solve - the barrier is organizational, not technical. Elephants in the Room create Confusion because they mix technical problems (Complicated) with cultural dysfunction (Complex). Black Jellyfish cascades require immediate Chaotic-domain action to break feedback loops, then Complex-domain analysis to understand the dependency pathologies. And stampedes - when multiple animals attack simultaneously - demand the ability to coordinate multiple response strategies without creating organizational chaos.

The framework doesn't replace ICS or Google SRE practices or your incident response runbooks. It enhances them by providing the meta-skill: knowing which approach applies when. Because here's what we've learned from every scenario in this chapter, from AWS to Boeing to Knight Capital to global pandemics: The organizations that handle incidents well aren't the ones with the best runbooks. They're the ones that can adapt their thinking to match the problem.

That adaptability requires three foundations, and they're not technical. Culture is infrastructure - you cannot effectively manage incidents in a blame culture, full stop. Information flow is everything - every incident failure in this chapter traces back to information not reaching decision-makers with enough fidelity and urgency. Psychological safety is a technical requirement - not a nice-to-have for team happiness, but a prerequisite for honest assessment, rapid learning, and organizational adaptation.

Build those foundations. Learn to recognize which animal you're facing. Classify the Cynefin domain. Apply the appropriate strategy. Coordinate when multiple strategies are needed simultaneously. Document everything. Learn from every incident. Complete your action items.

And remember: The animals are always waiting. Your job isn't to prevent all incidents - that's impossible in complex systems. Your job is to build an organization that can adapt to whatever attacks next.

Now go manage some incidents. Make them learning opportunities, not catastrophes.

---


### References

[White, 2025] White, Geoff. "The Unwritten Laws of Information Flow: Why Culture is the Hardest System to Scale." LinkedIn, October 23, 2025. https://www.linkedin.com/pulse/unwritten-laws-information-flow-why-culture-hardest-system-white-7jxvc/

[White, 2025b] White, Geoff. "The Day the Cloud Forgot Itself." LinkedIn, October 21, 2025. https://www.linkedin.com/pulse/day-cloud-forgot-itself-geoff-white-gviqc/

[Beyer et al., 2016] Beyer, Betsy, et al. "Site Reliability Engineering: How Google Runs Production Systems." O'Reilly Media, 2016.

[Duhigg, 2016] Duhigg, Charles. "What Google Learned From Its Quest to Build the Perfect Team." The New York Times Magazine, February 25, 2016. https://www.nytimes.com/2016/02/28/magazine/what-google-learned-from-its-quest-to-build-the-perfect-team.html

[Snowden & Boone, 2007] Snowden, Dave, and Mary E. Boone. "A Leader's Framework for Decision Making." Harvard Business Review, November 2007. https://hbr.org/2007/11/a-leaders-framework-for-decision-making

[AWS, 2017] Amazon Web Services. "Summary of the Amazon S3 Service Disruption in the Northern Virginia (US-EAST-1) Region." AWS Service Health Dashboard, March 2, 2017. https://aws.amazon.com/message/41926/

[Equifax, 2017] Equifax Inc. "Equifax Announces Cybersecurity Incident Involving Consumer Information." Press Release, September 7, 2017. https://investor.equifax.com/news-and-events/news/2017/09-07-2017-224018832

[Boeing, 2019] Boeing Company. "Boeing Statement on Ethiopian Airlines Flight 302 Investigation Report." Press Release, April 4, 2019. https://boeing.mediaroom.com/2019-04-04-Boeing-Statement-on-Ethiopian-Airlines-Flight-302-Investigation-Report

<!-- Reference definitions at bottom -->

[Eugene_F_Kranz_at_his_console_at_the_NASA_Mission_Control_Center]: Eugene_F_Kranz_at_his_console_at_the_NASA_Mission_Control_Center.jpg

[anatomy-of-an-incident]: anatomy-of-an-incident.png
[incident-response-team]: incident-response-team.png
[cynefin-framework]: Cynefin_framework_2022.jpg
[incident-severity]: incident-severity.jpg
[ICS-4-IT]: ICS-4-IT.jpg