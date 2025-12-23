## Incident Management for the Menagerie: When the Animals Attack

![][Eugene_F_Kranz_at_his_console_at_the_NASA_Mission_Control_Center]

### The Origins: From Forest Fires to Failing Servers

Incident management didn't start in Silicon Valley. It started in the wilderness.

In 1970, a wildfire in California killed 16 firefighters. The investigation revealed a pattern: fires were being fought by ad-hoc groups with unclear command structures, no communication protocols, and competing authorities. Chaos killed people.

The result was the Incident Command System (ICS), developed by FIRESCOPE (Firefighting Resources of California Organized for Potential Emergencies) in the 1970s. ICS wasn't about fires—it was about human coordination under extreme stress when lives are at stake.

The system worked. It spread from wildfire management to hazmat responses, to search and rescue, to emergency medical services, to disaster response. By the time 9/11 happened, ICS was the standard framework for managing any crisis involving multiple agencies and unclear situations.

Then IT discovered it had the same problems.

Early IT incident management was chaos. When the database crashed at 2 AM, whoever answered the phone became the "incident commander" by default. Information scattered across email threads, chat rooms, and phone calls. Multiple people made conflicting decisions. Recovery was slow because nobody knew who was doing what.

Sound familiar? It should. It's the same pattern that killed those firefighters in 1970.

IT adapted ICS because the problems were identical:
- High-stress environments where minutes matter
- Unclear situations requiring rapid sense-making
- Multiple specialists who need coordination
- Information overload requiring filtering and prioritization
- Need for clear authority without bureaucratic delay

The sophistication varied. ITIL codified incident management for enterprise IT in the 1980s. The DevOps movement brought it to software teams in the 2000s. But the real evolution happened at Google.

### The Google Model: SRE and the Incident Management Revolution

Google's Site Reliability Engineering organization didn't just adapt ICS—they transformed it for the reality of distributed systems operated by software engineers, not emergency responders.

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

This matters because most IT organizations have runbooks that are:
- Written once during a calm period
- Never updated
- Optimized for compliance audits, not operational use
- Tested only when the incident happens

Google's approach: if you haven't practiced the runbook in a game day, you don't have a runbook.

**Chaos Engineering as Incident Prevention**

Google (and Netflix, and Amazon) discovered something counterintuitive: the best way to get better at incidents is to cause more incidents.

Controlled chaos—deliberately breaking things in production—serves multiple purposes:
- Tests your runbooks under realistic conditions
- Trains your teams on incident response
- Reveals fragilities before they manifest as customer-impacting outages
- Builds organizational muscle memory for handling the unexpected

This is antifragility in action: getting stronger through stress.

**The Incident Commander Role**

Google formalized the Incident Commander (IC) as a dedicated role during incidents. The IC doesn't fix the problem—they coordinate the people who do.

Key responsibilities:
- Maintain situational awareness across all workstreams
- Make decisive calls when information is incomplete
- Shield the responders from external pressure
- Ensure communication flows appropriately
- Manage the incident timeline and documentation
- Declare incident closed and transition to learning

The IC role separates "managing the incident" from "fixing the technical problem." This is crucial because the skills are different. Your best database engineer might be terrible at coordinating five teams under stress.

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

### The Incident Command System: A Foundation, Not a Straitjacket
**Where ICS Breaks Down for IT:**

ICS assumes:
- Geographically bounded incidents (a fire, a building collapse)
- Physical response teams
- Clear roles based on agency (fire department, police, EMS)

IT incidents are:
- Geographically distributed (global services, remote teams)
- Virtual teams assembled ad-hoc
- Role boundaries based on technical domain, not organizational chart

Good incident management adapts ICS principles to IT reality rather than forcing IT reality into ICS structure.

![][incident-response-team]

ICS provides a structure for coordinating complex responses. The roles are:

| Role | Primary Responsibility | Why It Matters |
|------|----------------------|----------------|
| **Incident Commander (IC)** | Overall incident management, strategic decisions | Single point of authority prevents chaos |
| **Communications Lead (Comms)** |Internal and external messaging | Manages information flow to stakeholders|
| **Scribe** | Documentation, prediction, resource tracking | Ensures organizational memory and future planning |
| **Technical Lead** | Manages and directs technical resolution effort | Focus on problem resolution, not politics |
| **Subject Matter Expert (SME)** | In the weeds of the effort| Bringing to bear technical expertise to the situation |

For small incidents, one person might wear multiple hats. For large incidents (especially Black Swans or stampedes), you need the full structure.

**The ICS Principles That Matter for IT:**

1. **Unity of Command**: Every person reports to one person. No conflicting orders.

2. **Manageable Span of Control**: ICs should manage 3-7 direct reports. Beyond that, delegate.

3. **Common Terminology**: No acronyms that aren't shared. No jargon that creates confusion.

4. **Integrated Communications**: Everyone shares the same information environment. (This is where Slack, Zoom war rooms, and shared docs become critical infrastructure.)

5. **Establishment of Command**: The IC is declared early and clearly. "I'm taking IC" is an explicit handoff.


### Anatomy of an Incident
![][anatomy-of-an-incident]

Before moving further, let's get closure on some important traditional  terms around incidents. 

| Acronym | Name | Definition |
|--------|------|------------|
| **MTTF** | Mean Time To Failure | Duration of normal operation before an incident occurs. Represents system stability leading up to a failure. |
| **TTD** | Time To Diagnose | Time from the moment the incident begins until the underlying problem is identified—when responders understand what is failing and why. |
| **TIA** | Time To Action | Time from incident start (or investigation start) to the first meaningful corrective action. Covers human response and system triage before mitigation begins. |
| **ETRS** | Estimated Time to Restore Service | Time from incident start until service is restored to a functional, customer-usable state. Restoration does not necessarily imply full resolution. |
| **ETTR** | Estimated Time to Resolution | Time from incident start until the underlying issue is fully remediated and the system is back in normal operation (restore → fix → verify → monitor). |
| **MTBF** | Mean Time Between Failure | Full cycle time between the end of one incident and the beginning of the next: MTTF → (TTD + TIA + ETRS + ETTR) → next MTTF. |


We're going to go with these definitions for now. You may see these things defined differently in other documents or by other authors. To a certain extent, these definitions have become sort of a religious thing in the incident management community. We're just going to go with these for now. 

### NIST 800-61: The Framework Integration

NIST Special Publication 800-61 Revision 2 ("Computer Security Incident Handling Guide") provides the standard framework for incident response, particularly for security incidents but applicable more broadly.

The NIST incident response lifecycle has four phases:

#### 1. Preparation

**What NIST Says:**
- Establish incident response capability
- Develop policies and procedures
- Acquire tools and resources
- Train personnel

**What This Means for Our Bestiary:**
- **Black Swans**: You can't prepare for specific swans, but you can prepare to adapt rapidly to unprecedented events. This means: redundant systems, operational slack, cross-trained teams, and practiced incident response under chaos.
- **Grey Swans**: Preparation means instrumentation. If you can't see weak signals, you can't act on early warnings. Invest in observability.
- **Grey Rhinos**: Preparation means acknowledging the charging rhino exists. Maintain a rhino register. Have mitigation plans even if you're not executing them yet.
- **Elephants**: Preparation means building psychological safety so elephants can be named. This is cultural work, not technical.
- **Black Jellyfish**: Preparation means mapping dependencies, implementing circuit breakers, and designing for cascade resistance.

#### 2. Detection and Analysis

**What NIST Says:**
- Determine whether an incident has occurred
- Assess scope and impact
- Prioritize response based on severity

**What This Means for Our Bestiary:**

Detection varies dramatically by animal type:

| Animal | Detection Characteristics | Time to Detection | Primary Detection Method |
|--------|--------------------------|-------------------|-------------------------|
| Black Swan | Impossible before event, obvious during | Seconds to minutes | Customer reports, total system failure |
| Grey Swan | Possible with monitoring, requires pattern recognition | Hours to days | Anomaly detection, correlation analysis |
| Grey Rhino | Trivial (already visible), question is acknowledgment | Months (known) | Capacity monitoring, backlog review |
| Elephant | Everyone knows, question is who will say it | Years (chronic) | Engagement surveys, exit interviews |
| Black Jellyfish | Hard initially, exponential once cascade starts | Minutes | Error rate acceleration, cross-service correlation |

#### 3. Containment, Eradication, and Recovery

**What NIST Says:**
- Contain the incident to prevent further damage
- Remove the threat
- Restore systems to normal operation

**What This Means for Our Bestiary:**

Containment strategies differ:

- **Black Swans**: Containment is about stopping the bleeding while you figure out what's happening. Priority: prevent total system collapse. Expect to make decisions with 20% information.

- **Grey Swans**: Containment is about breaking the complex cascade before it fully manifests. You have slightly more time than Black Swans but not much. Use your monitoring to identify and isolate the spreading failure.

- **Grey Rhinos**: Containment is often straightforward (you knew what needed fixing). The challenge is doing it quickly under pressure after procrastinating for months.

- **Elephants**: Containment is about acknowledging the elephant so response can be coordinated. The technical fix might be simple; the organizational fix is hard.

- **Black Jellyfish**: Containment is about breaking positive feedback loops. Stop retry storms, open circuit breakers manually if needed, shed load aggressively. Recovery must happen in dependency order, not all-at-once.

#### 4. Post-Incident Activity

**What NIST Says:**
- Document lessons learned
- Improve incident response capability
- Update procedures based on experience

**What This Means for Our Bestiary:**

This is where information flow becomes critical. Per the Unwritten Laws [White, 2025]:

**Information flows to where it's safe.** If your post-incident review is blameful, engineers will hide what they know. You'll get theater, not learning.

**Information flows through trust networks.** The person who understands what really happened might not be the incident commander or the most senior person in the room. Create space for everyone to contribute.

**Information degrades crossing boundaries.** Write the postmortem while the context is fresh. Waiting two weeks means the nuance is gone.

Post-incident learning should explicitly classify the animal type:
- Was this a Black Swan we couldn't have predicted?
- Was this a Grey Swan we could have monitored for?
- Was this a Grey Rhino we'd been ignoring?
- Did this reveal an Elephant we need to address?
- Was this a Black Jellyfish cascade we need to design against?

Different animals demand different action items. Don't treat all incidents the same way.

### Key Performance Indicators: Measuring What Customers Feel

Most incident management KPIs are wrong. They measure internal process efficiency, not customer impact.

#### The Traditional KPIs (And Why They're Incomplete)

**Mean Time to Detect (MTTD)**
- **What it measures**: Time from incident start to detection
- **Why it matters**: Faster detection means faster response
- **Why it's incomplete**: Assumes all incidents are equally detectable. Black Swans by definition can't be detected before they happen. Grey Rhinos were detected months ago; detection time is irrelevant.

**Mean Time to Acknowledge (MTTA)**
- **What it measures**: Time from alert to human acknowledgment
- **Why it matters**: Measures on-call responsiveness
- **Why it's incomplete**: Acknowledging an alert ≠ understanding the incident. You can acknowledge instantly and still be confused for hours.

**Mean Time to Resolve (MTTR)**
- **What it measures**: Time from detection to resolution
- **Why it matters**: Directly correlates with customer pain duration
- **Why it's incomplete**: "Resolution" is often gamed. Did you fix the root cause or apply a band-aid? Did you learn anything or just restore service?

**Incident Frequency**
- **What it measures**: Number of incidents per time period
- **Why it matters**: Trend analysis
- **Why it's incomplete**: One Black Swan matters more than ten minor incidents. Frequency without severity context is noise.

#### The KPIs That Actually Matter

These align with what customers experience and what organizations learn:

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

### Culture as Incident Management Infrastructure

Before we dive into animal-specific incident management, we need to address the foundation that makes everything else possible: culture.

The quote from the State of the Art report is worth repeating:

> "The primacy of culture over tooling cannot be overstated. The advanced automation and AIOps platforms discussed later in this report are only as effective as the data they are fed. In a culture of blame, where incident data is hidden or distorted, these tools are rendered useless. The SRE cultural shift, with its emphasis on blamelessness, psychological safety, and data-driven learning, is the necessary precursor to, not a byproduct of, successful technological implementation. The state of the art is a socio-technical system where the social (culture) enables the technical (tools)."

This isn't inspirational poster material. It's infrastructure engineering.

#### The Unwritten Laws in Practice

As described in my earlier work on information flow [White, 2025], these laws manifest during incidents:

**First Law: Information Flows to Where It's Safe**

During incidents, you need information from people who:
- Might have made a mistake that contributed to the incident
- Are junior and afraid to speak up
- Work in different organizations with different incentives
- Have context that contradicts what leadership believes

If these people fear punishment, they stay silent. You operate with incomplete information. You make worse decisions. The incident lasts longer and causes more damage.

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
        → Incident Commander
```

By the time information traverses the org chart, the incident is over or the context is destroyed.

Good incident management creates direct channels between domain experts and decision-makers, regardless of hierarchy. War rooms, Slack channels, and Zoom bridges exist to short-circuit the org chart.

**Third Law: Information Degrades Crossing Boundaries**

Every hop in the communication chain loses fidelity:
- Technical precision becomes "there's a database problem"
- Urgency calibration fails ("P0 for them, P3 for us")
- Nuance dies ("just restart it" when restart will make it worse)

Good incident management minimizes hops:
- Bring domain experts into the war room directly
- Use shared documents everyone can edit
- Prefer synchronous communication (call > Slack > email)
- Record decisions and context in real-time

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

Google's Project Aristotle found psychological safety was the #1 predictor of team effectiveness. For incident management, it's not just important—it's foundational.

Psychological safety means:
- You can admit you don't know something
- You can disagree with senior people
- You can surface bad news without fear
- You can make mistakes and learn from them

Without this, your incident management degrades:
- People hide problems (late detection)
- People won't speak up with critical context (slow understanding)
- People won't admit mistakes (poor postmortems)
- People won't take reasonable risks (slow decision-making)

Building psychological safety:
- Leaders model vulnerability (admit mistakes, say "I don't know")
- Thank people for bad news and dissent
- Never punish someone for being wrong
- Punish hiding information, not making errors
- Celebrate learning, not perfection

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

---

## The Cynefin Framework for Incident Response

Before we dive into animal-specific incident management, we need one more tool: a way to think about how to think about incidents.

ICS gives us structure. NIST gives us phases. Google SRE gives us practices. But none of them answer the fundamental question: **How should we think about this problem?**

That's where the Cynefin Framework comes in. Developed by Dave Snowden in the late 1990s, Cynefin (pronounced "kuh-NEV-in") is a sense-making framework that categorizes situations based on the relationship between cause and effect. The name is Welsh for "the place of your multiple belongings"—representing the multiple factors in our environment that influence us in ways we can never fully understand.

For incident response, Cynefin provides something critical: **Different types of problems require different types of thinking.** Using the wrong approach wastes time, makes things worse, or both.

![][cynefin-framework]

### Why SREs Need This

Modern distributed systems are inherently complex. Incidents don't follow predictable patterns. The framework gives you a mental model for:

1. **Classifying the incident** - What kind of problem is this?
2. **Choosing the right response strategy** - How should we think about this?
3. **Avoiding common mistakes** - What not to do in this situation
4. **Transitioning between states** - How incidents evolve and how to guide that evolution

The key insight: **ordered domains** (right side of the framework) have discoverable cause-and-effect relationships. **Unordered domains** (left side) have relationships that can only be understood in hindsight or not at all.

### The Five Domains

The framework divides all situations into five domains arranged around a central area:

#### Domain 1: Clear (Simple/Obvious) - "The Recipe Domain"

**Characteristics:**
- Cause and effect are **obvious** to any reasonable person
- Best practices exist and are well-established
- The solution is known and repeatable
- Following procedures produces predictable results

**Decision Heuristic: Sense → Categorize → Respond**

**What This Means:**
1. **Sense:** Recognize the situation (e.g., "Service is down")
2. **Categorize:** Match it to a known pattern (e.g., "This matches our database connection pool exhaustion runbook")
3. **Respond:** Apply the standard solution (e.g., "Restart the service with increased pool size")

**Incident Response Examples:**
- Service restart following documented procedure
- Applying a known patch for a vulnerability
- Following a runbook for a common database issue
- Standard deployment rollback procedure

**What Works:**
- Runbooks and playbooks
- Standard operating procedures
- Best practices
- Automation and scripts
- Following established patterns

**What Doesn't Work:**
- Overthinking simple problems
- Calling in experts when a runbook exists
- Experimenting when a solution is known
- Ignoring established procedures

**The Cliff Edge:**
Clear domains have a dangerous boundary with Chaotic. If you're following a "recipe" and something fundamental changes, you can suddenly find yourself in chaos. Example: Your standard database restart procedure works 99% of the time, but when the underlying storage system fails, following the same procedure makes things worse.

**For Incident Management:**
Most routine incidents (P3, P4) live in the Clear domain. They're the "known knowns" - we know what they are, we know how to fix them. The danger is when teams treat Complex or Chaotic incidents as Clear, applying runbooks that don't fit.

#### Domain 2: Complicated - "The Expert Domain"

**Characteristics:**
- Cause and effect relationships **exist but are not obvious**
- Multiple valid solutions may exist
- Requires **expert analysis** to discover the solution
- The answer is discoverable through investigation
- Different experts might recommend different approaches

**Decision Heuristic: Sense → Analyze → Respond**

**What This Means:**
1. **Sense:** Gather information about the situation
2. **Analyze:** Use expert knowledge, tools, and investigation to understand cause and effect
3. **Respond:** Implement the solution based on analysis

**Incident Response Examples:**
- Database performance degradation requiring query analysis
- Network routing issues requiring packet capture and analysis
- Memory leak investigation requiring profiling tools
- Security incident requiring forensic analysis
- Root cause analysis of a production bug

**What Works:**
- Expert consultation
- Systematic investigation
- Data collection and analysis
- Multiple perspectives from different experts
- Diagnostic tools and techniques
- Formal analysis processes

**What Doesn't Work:**
- Rushing to action without analysis
- Ignoring expert advice
- Applying simple solutions to complicated problems
- Analysis paralysis (experts disagreeing indefinitely)
- Treating as simple when expertise is needed

**The Expert Trap:**
In Complicated domains, experts can become entrenched in their viewpoints. Multiple valid solutions exist, but experts may argue indefinitely about which is "best." The IC's job is to:
- Gather expert opinions
- Make a decision when experts disagree
- Avoid analysis paralysis
- Recognize when the situation has moved to Complex (no amount of analysis will reveal the answer)

**For Incident Management:**
Grey Swans often start in the Complicated domain - we know something is wrong, we can investigate, but the answer isn't immediately obvious. Grey Rhinos that finally charge often require Complicated-domain analysis to understand why they were ignored and how to prevent recurrence.

#### Domain 3: Complex - "The Experimentation Domain"

**Characteristics:**
- Cause and effect relationships can only be understood **in hindsight**
- The situation is **emergent** - patterns appear over time
- Multiple interacting factors create unpredictable outcomes
- No amount of analysis will reveal the answer upfront
- Solutions must be **discovered through experimentation**

**Decision Heuristic: Probe → Sense → Respond**

**What This Means:**
1. **Probe:** Run safe-to-fail experiments to explore the problem space
2. **Sense:** Observe what emerges from the experiments
3. **Respond:** Adapt based on what you learn, then probe again

**Incident Response Examples:**
- Novel system failure with no known precedent
- Cascading failures where root cause isn't clear
- Distributed system issues with emergent behavior
- Multi-service outages with unclear dependencies
- Black Swan incidents where mental models break
- Grey Swan incidents where weak signals exist but patterns are unclear

**What Works:**
- Safe-to-fail experiments
- Multiple parallel probes
- Observing emergent patterns
- Iterative adaptation
- Learning from small failures
- Building understanding over time

**What Doesn't Work:**
- Trying to analyze your way to an answer
- Waiting for perfect information before acting
- Applying expert solutions without testing
- Command-and-control management
- Expecting immediate results
- Treating as Complicated when it's truly Complex

**Safe-to-Fail Probes: The Key Technique**

Safe-to-fail probes are experiments designed so that:
- **Failure is acceptable** - The experiment won't make things worse
- **Learning is guaranteed** - Even if the experiment fails, you learn something
- **Cost is low** - The experiment doesn't consume critical resources
- **Reversibility** - You can undo the experiment if needed

**Examples of Safe-to-Fail Probes in Incident Response:**
- **Traffic shifting:** Route 10% of traffic to a different region to test if it's a regional issue
- **Feature flags:** Disable a specific feature to test if it's causing the problem
- **Circuit breaker testing:** Manually trip a circuit breaker to see if it breaks a cascade
- **Load shedding:** Gradually reduce load to find the breaking point
- **Dependency isolation:** Temporarily disable a dependency to test impact

**The Goal: Move from Complex to Complicated**
As you run probes and learn, patterns emerge. The situation should transition from Complex (unknown unknowns) to Complicated (known unknowns). Once in Complicated, you can apply expert analysis. The key is patience - Complex problems don't resolve quickly.

**For Incident Management:**
Black Swans almost always start in Complex or Chaotic domains. Grey Swans often transition from Complicated to Complex as you realize the problem is more emergent than analyzable. The framework provides a structured way to handle these situations without panicking or applying wrong strategies.

#### Domain 4: Chaotic - "The Crisis Domain"

**Characteristics:**
- Cause and effect relationships are **constantly shifting**
- No visible patterns exist
- **Immediate action is required** to stabilize
- The system is in crisis
- There's no time for analysis or experimentation
- The primary goal is to **establish order**

**Decision Heuristic: Act → Sense → Respond**

**What This Means:**
1. **Act:** Take immediate action to stabilize the situation
2. **Sense:** Once stabilized, assess what's happening
3. **Respond:** Make strategic decisions based on what you've learned

**Incident Response Examples:**
- Complete system outage affecting all users
- Active security breach in progress
- Data center failure
- Cascading failure spreading rapidly
- Black Swan incident in early stages
- Any P0 incident where the system is actively degrading

**What Works:**
- Immediate action to stop the bleeding
- Failover procedures
- Load shedding
- Emergency rollbacks
- Incident Commander taking control
- Rapid decision-making
- Stabilization first, understanding second

**What Doesn't Work:**
- Analysis before action
- Waiting for perfect information
- Experimentation (no time)
- Consensus-building (too slow)
- Tentative responses
- Trying to understand before stabilizing

**The Stabilization Goal:**
In Chaotic domains, the primary goal is to move the situation to a more manageable domain (usually Complex or Complicated). You don't need to understand everything - you need to stop the crisis from getting worse.

**Common Actions in Chaotic Incidents:**
- **Failover:** Route traffic away from failing systems
- **Load shedding:** Reduce load to prevent cascade
- **Kill switches:** Disable problematic services/features
- **Emergency rollback:** Revert to last known good state
- **Isolation:** Isolate affected systems to prevent spread

**The Transition:**
Once you've stabilized (Act), you can assess (Sense) and then make strategic decisions (Respond). The situation typically moves from Chaotic → Complex → Complicated as understanding increases.

**For Incident Management:**
Black Swans often start in Chaotic. The framework provides permission to act without full understanding - critical for Black Swan response. Many teams waste precious minutes trying to understand a Chaotic situation when they should be stabilizing first.

#### Domain 5: Confusion (Disorder) - "The Unknown Domain"

**Characteristics:**
- It's **unclear which domain applies**
- The situation has elements of multiple domains
- Team members may disagree about what type of problem this is
- No clear decision-making strategy is apparent

**Decision Heuristic: Break Down → Classify → Apply Appropriate Strategy**

**What This Means:**
1. **Break Down:** Decompose the situation into constituent parts
2. **Classify:** Assign each part to the appropriate domain
3. **Apply:** Use the appropriate strategy for each part

**Incident Response Examples:**
- Incident where some aspects are clear (known service down) but others are chaotic (cascading effects unclear)
- Multi-service outage where different services require different approaches
- Security incident with both known attack patterns and novel behaviors
- Team disagreement about incident severity and type

**What Works:**
- Breaking the problem into components
- Assigning different strategies to different parts
- Acknowledging uncertainty
- Explicitly discussing which domain applies
- Revisiting classification as understanding improves

**What Doesn't Work:**
- Treating the whole situation as one domain
- Ignoring the confusion
- Forcing a single approach
- Operating in "firefighting mode" without classification

**The Danger:**
When in Confusion, people often default to their preferred domain:
- Engineers default to Complicated (let's analyze)
- Managers default to Clear (follow the process)
- Operators default to Chaotic (act immediately)

The IC must explicitly classify the situation to avoid these defaults.

**For Incident Management:**
Many incidents start in Confusion. The framework provides a way out: break it down, classify the parts, apply appropriate strategies. This is especially important for stampedes (multiple animals attacking simultaneously).

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

**Complicated Domain Response:**
- Assemble experts
- Gather diagnostic data
- Analyze systematically
- Choose a solution based on analysis
- Avoid analysis paralysis

**Complex Domain Response:**
- Design safe-to-fail probes
- Run experiments in parallel
- Observe emergent patterns
- Adapt based on learning
- Be patient - solutions emerge over time

**Chaotic Domain Response:**
- Act immediately to stabilize
- Don't wait for understanding
- Use failover, load shedding, isolation
- Once stable, assess the situation
- Transition to Complex or Complicated as understanding improves

**Confusion Domain Response:**
- Break the incident into components
- Classify each component
- Apply appropriate strategy to each
- Revisit classification as situation evolves

#### Step 3: Recognize Domain Transitions

**Natural Progression (Clockwise):**
Chaotic → Complex → Complicated → Clear

This represents increasing understanding:
- **Chaotic:** Act to stabilize
- **Complex:** Experiment to learn
- **Complicated:** Analyze to understand
- **Clear:** Apply known solution

**Dangerous Transitions:**
- **Clear → Chaotic:** The "cliff edge" - following a recipe when context has fundamentally changed
- **Complicated → Chaotic:** Analysis paralysis during a crisis
- **Ordered → Complex:** Trying to analyze or follow procedures when the situation is emergent

**During an Incident:**
- Monitor which domain you're in
- Adjust strategy as the situation evolves
- Don't get stuck in one domain when you should transition
- Explicitly discuss transitions with the team

### Common Mistakes and How to Avoid Them

**Mistake 1: Applying the Wrong Strategy**
Using Clear-domain thinking (follow the runbook) for a Complex problem (novel failure mode).

**How to Avoid:** Explicitly classify the incident. Ask: "Is this a known problem with a known solution, or are we in uncharted territory?"

**Mistake 2: Analysis Paralysis in Crisis**
Trying to analyze a Chaotic situation before acting.

**How to Avoid:** Recognize Chaotic domains. Give yourself permission to act without full understanding. Stabilize first, analyze second.

**Mistake 3: Command-and-Control in Complex Situations**
Imposing expert solutions on Complex problems that require experimentation.

**How to Avoid:** Recognize Complex domains. Design safe-to-fail experiments. Learn through iteration.

**Mistake 4: Treating Complex as Complicated**
Bringing in more experts, gathering more data, analyzing harder - when the problem requires experimentation.

**How to Avoid:** Ask: "Can we analyze our way to an answer, or do we need to experiment to learn?" If the latter, you're in Complex.

**Mistake 5: Complacency in Clear Domains**
Following best practices without recognizing when context has changed.

**How to Avoid:** Periodically challenge best practices. Monitor for context shifts. Recognize when "this time is different."

Now that we understand Cynefin, let's see how it applies to each animal in our bestiary.

---

## Incident Management by Animal Type

### Black Swan Incidents: When the Unprecedented Strikes

#### Cynefin Domain Classification

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

**Key Insight:** Black Swans require you to abandon runbooks and expert analysis. You're in uncharted territory. The framework gives you permission to experiment and learn rather than pretending you can analyze your way to a solution.

#### Characteristics During the Incident

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

#### Scenario 1: The AWS S3 Outage (February 28, 2017)

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

1. **Decision**: Attempt full subsystem restart vs. partial recovery
   - **Context**: Partial recovery might be faster but risk corruption
   - **Information available**: ~30%
   - **Time to decide**: 15 minutes
   - **Outcome**: Full restart chosen, added time but ensured data integrity
   - **Cynefin Note:** This was a Complex-domain decision - no expert analysis could determine the answer, required experimentation

2. **Decision**: Public communication about lack of ETA
   - **Context**: Customers demanding timeline, but genuinely unknown
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

#### Scenario 2: The COVID-19 Digital Transformation Shock

**The Context:**
In March 2020, entire organizations shifted to remote work within days. For IT infrastructure, this created unprecedented load patterns that couldn't have been predicted from historical data.

**What Made It a Black Swan (or Swan-Adjacent):**

The pandemic itself was a Grey Rhino (WHO had warned for years). But the specific digital infrastructure impacts bordered on Black Swan because:
- No historical precedent for simultaneous global shift
- Scale (100x normal remote work, not 2x)
- Duration (sustained for years, not weeks)
- Behavioral changes (Zoom fatigue, asynchronous work patterns)

**The Incident Management Challenge:**

This wasn't a discrete incident—it was a permanent shift masquerading as a temporary surge.

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

1. **Declaring this is not a normal incident** (Week 2)
   - Recognition that incident response framework doesn't fit
   - Shift from "restore service" to "transform architecture"
   - Communication to stakeholders: this is permanent change
   - **Cynefin Note:** Recognizing domain transition from Chaotic to Complex

2. **Abandoning historical capacity models** (Week 3)
   - Traditional approach: forecast from past data
   - Black Swan approach: assume past is irrelevant
   - Build based on current reality, not historical trends
   - **Cynefin Note:** Complex domain thinking - past patterns don't apply

3. **Prioritizing architectural change over stability** (Month 2)
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
#### Black Swan Incident Management Principles

**1. Recognize You're in Unprecedented Territory (Cynefin: Classify as Chaotic or Complex)**

The first step is accepting this doesn't fit your mental models.

**Warning signs:**
- Your runbooks don't apply
- Domain experts are confused
- Multiple hypotheses being debated
- Scope keeps expanding unexpectedly

**What to do:**
- IC explicitly declares: "This is unprecedented, we're adapting in real-time"
- Classify the domain: Chaotic (act first) or Complex (experiment to learn)
- Communicate uncertainty to stakeholders honestly
- Assemble diverse expertise (not just usual responders)
- Expect to make decisions with incomplete information

**What not to do:**
- Force-fit this into known patterns ("it's just like that time...")
- Wait for certainty before acting
- Follow standard procedures if they clearly don't apply
- Pretend you know more than you do
- Try to analyze your way to a solution (if in Complex domain)

**2. Optimize for Information Flow, Not Chain of Command**

Black Swans require rapid adaptation. Hierarchical communication is too slow.

**Create direct channels:**
- War room with domain experts, regardless of seniority
- Shared documents everyone can edit simultaneously
- Real-time decision documentation
- Skip normal escalation paths

**The IC's role:**
- Synthesize information from diverse sources
- Make calls when consensus isn't possible
- Shield responders from external pressure
- Maintain coherent narrative despite chaos

**3. Make Reversible Decisions Rapidly, Irreversible Decisions Carefully (Cynefin: Safe-to-Fail Probes)**

You'll need to decide with 20-30% information. Use decision reversibility as your guide.

**Reversible decisions (make quickly):**
- Trying a potential fix (can roll back)
- Routing traffic differently (can revert)
- Adding capacity (can remove)
- Opening circuit breakers (can close)
- **These are safe-to-fail probes in Complex domain**

**Irreversible decisions (take more time):**
- Deleting data
- Declaring to customers this is permanent
- Major architectural changes
- Publicly committing to timelines

**4. Document Everything in Real-Time**

Your future self (and your organization) needs to understand what happened and why.

**What to document:**
- Timeline of events (automated where possible)
- Hypotheses considered and why they were rejected
- Decisions made and the reasoning with incomplete information
- Who knew what when
- Surprising findings
- **Cynefin domain classification and transitions**

**Why it matters:**
- Black Swans are learning opportunities
- Real-time documentation captures context that disappears
- Postmortem quality depends on contemporaneous notes
- Future incidents may be different but decision-making principles apply

**5. Plan for Extended Duration**

Black Swans often last longer than expected because you're learning as you go.

**Rotation planning:**
- IC should rotate every 6-8 hours (decision fatigue is real)
- Responders need breaks (burnout helps no one)
- Maintain situation awareness through handoffs
- Document decision rationale so next IC can continue

**Communication cadence:**
- Regular updates even if no progress ("still working on it" is information)
- Honest about uncertainty in timelines
- Escalate to executives early (they can provide air cover)

**6. Transition from Response to Learning**

The incident isn't over when service is restored. It's over when you've learned from it.

**Comprehensive postmortem:**
- What was genuinely unprecedented?
- What assumptions were broken?
- What other risks did this reveal? (Look for the stampede)
- How did the organization adapt?
- What would help next time? (Can't predict specific swan, can improve adaptability)
- **What Cynefin domain were we in, and did we use the right strategy?**

**Action items focus:**
- Building antifragility (systems that benefit from stress)
- Improving adaptability (people and process)
- Reducing fragility (single points of failure, brittle assumptions)

---

### Grey Swan Incidents: The Complex and Monitorable

#### Cynefin Domain Classification

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

#### Characteristics During the Incident

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

#### Scenario 1: The Knight Capital Trading Disaster (August 1, 2012)

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

1. **Pre-deployment:**
   - Configuration drift detection (1 of 8 servers different)
   - Pre-production validation (test algorithm still present)
   - Deployment verification (all servers updated)

2. **During incident:**
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

#### Grey Swan Incident Management Principles

**1. Instrument for Weak Signals (Cynefin: Recognize Complicated Domain Needs Monitoring)**

Grey Swans give early warnings if you're watching for them. The challenge is distinguishing signal from noise.

**What to monitor:**

**Rate of change, not just absolute values:**
- Error rate increasing 20% per minute (cascade starting)
- Latency growing exponentially (saturation approaching)
- Resource consumption accelerating (leak or attack)

**Correlation across systems:**
- Multiple services showing issues simultaneously
- Problems spreading through dependency graph
- Temporal correlation (all started around same time)

**Distribution shape changes:**
- Tail behavior shifting (p99 growing faster than p50)
- Bimodal distributions appearing (two distinct failure modes)
- Outliers becoming more frequent

**Interaction anomalies:**
- Normal components behaving abnormally together
- Unexpected traffic patterns
- Circular dependencies activating

**2. Recognize Complexity, Don't Oversimplify (Cynefin: Don't Force Complex into Complicated)**

Grey Swans are inherently complex. Forcing them into simple mental models delays understanding.

**Warning signs of oversimplification:**
- "It's just a database issue" (when it's actually interaction of DB + cache + load balancer)
- "This is like that other incident" (when it's similar but different)
- Single root cause fixation (when there are multiple contributing factors)

**Better approach:**
- Map the full interaction space
- Identify all contributing factors
- Understand feedback loops
- Accept that "root cause" might be "complex interaction of 5 factors"
- **Recognize when you're in Complex domain, not Complicated**

**3. Comprehensive Postmortem for Complex Events**

Grey Swan postmortems are more valuable than simple failure postmortems because they teach system thinking.

**What to document:**

**The interaction diagram:**
- All components involved
- How they interacted to produce the failure
- Feedback loops that amplified it
- Why this interaction wasn't anticipated

**The weak signals:**
- What early warnings existed
- Why they were missed or dismissed
- What monitoring would have caught this earlier

**The decision tree:**
- Hypotheses considered
- Why some were eliminated
- What data drove convergence
- Decision latency and why

**Cynefin reflection:**
- What domain were we in?
- Did we use the right strategy?
- When did we transition between domains?
- Could we have recognized the domain earlier?

---

### Grey Rhino Incidents: When Ignorance Ends Abruptly

#### Cynefin Domain Classification

Grey Rhinos are usually **Complicated** domain problems:

**State: Complicated**
- The problem is known
- Experts can analyze it
- Solutions exist but aren't being applied
- Organizational psychology, not technical complexity

**Key Insight:** Grey Rhinos are usually Complicated-domain problems that organizations treat as Clear (ignore) or Complex (too hard to solve). The framework helps recognize that expert analysis and decision-making can address them - the barrier is organizational, not technical.

#### Characteristics During the Incident

**What You Know:**
- This was entirely predictable
- You've known about it for months (or years)
- The fix is probably straightforward
- You're here because you ignored it

**The Psychological Challenge:**

Grey Rhino incidents create cognitive dissonance and organizational shame. Everyone knew this could happen. Now it has happened. The temptation is to pretend it was unpredictable (save face) rather than admit it was ignored (learn the lesson).

#### Scenario: The Equifax Data Breach (2017)

**The Grey Rhino:**

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

#### Grey Rhino Incident Management Principles

**1. Acknowledge the Rhino Immediately (Cynefin: Classify as Complicated, Not Complex)**

The first step in Grey Rhino incident management is admitting this was preventable. Don't waste time pretending it wasn't.

**During the incident:**
- IC acknowledges: "We knew about this risk"
- Classify as Complicated domain (expert analysis can solve this)
- Focus on resolution, not blame assignment
- Document what was known and when (for postmortem)
- Don't hide from stakeholders that this was preventable

**2. Look for the Herd**

Grey Rhinos travel in groups. If you ignored one, you probably ignored others.

**During incident response:**
- Quick scan for related rhinos
- "What else have we been ignoring that's similar to this?"
- Prioritize other charging rhinos for immediate action

**3. Conduct a "Why Did We Ignore This?" Postmortem (Cynefin: Analyze Organizational Barriers)**

Grey Rhino postmortems are different from other types because the technical failure is usually simple. The interesting question is organizational.

**Grey Rhino postmortem questions:**
- What happened? (usually simple answer)
- We knew this could happen. Why didn't we fix it? (hard answer)
- What organizational factors led to ignoring this?
- What incentives or disincentives exist?
- What other rhinos are we currently ignoring?
- How do we change our prioritization process?

**Cynefin reflection:**
- Why did we treat this as Clear or Complex instead of Complicated?
- What expert analysis would have revealed the organizational barriers?
- How do we ensure Complicated-domain problems get expert attention?

---

### Elephant in the Room Incidents: When Silence Breaks

#### Cynefin Domain Classification

Elephants in the Room often create **Confusion** or **Complicated** domains:

**State: Often Confusion**
- Unclear what the real problem is
- Cultural/psychological factors mixed with technical
- Requires breaking down into components

**Key Insight:** Elephants often create Confusion because the technical problem is Clear or Complicated, but the organizational problem (naming the elephant) is Complex. The framework helps separate these.

#### Characteristics During the Incident

**What You Know:**
- Everyone has known about this problem
- Nobody has been willing to discuss it openly
- The incident has finally forced the conversation
- This is as much cultural as technical

**The Psychological Challenge:**

Elephant incidents are fundamentally different because they're organizational dysfunctions manifesting as technical failures. The IC must navigate both technical response and cultural exposure.

#### Scenario: The Boeing 737 MAX Crisis

**The Elephant:**

Boeing had a cultural problem that everyone inside the company knew about but wouldn't openly discuss: increasing pressure to cut costs and accelerate schedules, compromising engineering rigor and safety culture.

**The Elephants (Widely Known Internally):**

1. **Schedule pressure over safety rigor**
   - Engineers felt rushed
   - Testing compressed
   - Concerns about MCAS design raised but minimized

2. **MCAS single-point-of-failure design**
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

#### Elephant Incident Management Principles

**1. Recognize You're Dealing with a Cultural Problem (Cynefin: Break Down Confusion)**

When the incident reveals an elephant, traditional incident management is insufficient.

**Break it down:**
- Technical component: Usually Clear or Complicated
- Organizational component: Usually Complex
- Apply appropriate Cynefin strategy to each

**2. Create Psychological Safety for Truth-Telling**

The incident is forcing the elephant into visibility. Make it safe to discuss.

**IC explicitly states:**
"We need to understand the full scope of this problem. That means hearing uncomfortable truths. Nobody will be punished for honestly sharing what they know about this situation."

**3. Postmortem Must Address Organizational Root Causes (Cynefin: Complex Domain for Cultural Change)**

Elephant postmortems are different. Technical root cause is often simple. Organizational root cause is complex and uncomfortable.

**Elephant-specific questions:**
- Who knew about this problem before it became an incident?
- Why wasn't it addressed earlier?
- What organizational factors prevented action?
- What happens to people who raise uncomfortable issues?
- What incentives created/sustained this problem?
- What other elephants exist in the organization?

**Cynefin reflection:**
- How do we address the Complex-domain organizational problem?
- What safe-to-fail experiments can we run for cultural change?
- How do we prevent Confusion from paralyzing us?

---

### Black Jellyfish Incidents: When Cascades Bloom

#### Cynefin Domain Classification

Black Jellyfish (cascades) start in **Chaotic** or **Complex** domains:

**Initial State: Chaotic**
- Cascade spreading rapidly
- Immediate action needed
- Break the feedback loop

**After Breaking Loop: Complex**
- Understanding why the cascade happened
- Experimenting with prevention
- Emergent behavior from dependencies

**Key Insight:** Cascades require immediate Chaotic-domain action (break the loop), then Complex-domain learning (understand the system interactions that caused it).

#### Characteristics During the Incident

**What You Know:**
- Something is spreading rapidly
- Multiple systems are failing
- Error rates are accelerating
- Dependencies are cascading

**The Psychological Challenge:**

Black Jellyfish incidents create urgency and confusion. Everything is happening fast. Multiple teams are paging. The scope keeps expanding. The temptation is to fix everything at once, which makes coordination impossible.

#### Scenario: The 2017 Amazon S3 US-EAST-1 Outage (Cascade Analysis)

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

#### Black Jellyfish Incident Management Principles

**1. Stop the Amplification First (Cynefin: Chaotic Domain Action)**

Jellyfish cascades accelerate. Your first priority is breaking positive feedback loops.

**Break the loops immediately:**
- Disable retries
- Shed load aggressively
- Isolate spreading failures
- Stop making it worse
- **This is Chaotic-domain thinking: act first, understand later**

**2. Recover in Dependency Order**

Fix dependencies first, not the biggest problem first.

**Wrong approach:**
"API Gateway is down affecting the most customers, fix it first"

**Right approach:**
"S3 → Lambda → API Gateway. Fix in that order"

**3. Identify and Break Circular Dependencies**

**Common patterns:**
- Service A uses Service B for health checks
- Service B uses Service A for configuration
- Both services down, neither can start

**Breaking strategies:**
- Manual bootstrap
- Temporary mocks
- Dependency injection
- Cold start procedures

**4. Post-Jellyfish Postmortem: Focus on Cascade Mechanics (Cynefin: Complex Domain Learning)**

**Document the full cascade path:**
- Draw the dependency graph
- Show how failure propagated
- Identify amplification mechanisms
- Note surprising dependencies

**Action items by category:**
- Dependency reduction
- Cascade resistance (circuit breakers, bulkheads)
- Monitoring improvements (cascade detection)
- Recovery procedures
- Architecture changes

**Cynefin reflection:**
- How do we design systems to resist cascades?
- What safe-to-fail experiments can we run to test cascade resistance?
- How do we move from Complex (emergent behavior) to Complicated (understood patterns)?

---

### Hybrid Animals and Stampedes: When Multiple Animals Attack

#### Cynefin Domain Classification for Stampedes

Stampedes almost always start in **Confusion** or **Chaotic** domains:

**Initial State: Confusion or Chaotic**
- Multiple risk types interacting
- Unclear which animal is primary
- Different parts require different strategies
- Immediate action needed but unclear what to do

**Key Insight:** Stampedes require breaking down into components, classifying each part, and applying appropriate Cynefin strategies to each. This is the framework's strength: handling situations that don't fit neatly into one domain.

#### The Stampede Pattern

Sometimes a single risk event—often a Black Swan—doesn't just cause direct damage. It stresses the system in ways that reveal all the other animals that were hiding in the shadows.

Think of it like a stampede in the wild: one lion (Black Swan) appears, and suddenly you realize the savannah is full of animals you didn't know were there. Grey Rhinos that were grazing peacefully start charging. Elephants in the Room become impossible to ignore. Jellyfish that were floating dormant suddenly bloom and sting everything.

The system was always full of these risks. The Black Swan just revealed them.

#### Cynefin Framework for Managing Stampedes

**Step 1: Break Down the Stampede**

When multiple animals attack simultaneously, you're in Confusion domain. The first step is decomposition:

**Identify each animal:**
- What Black Swan triggered this?
- What Grey Rhinos are now charging?
- What Elephants are now visible?
- What Jellyfish cascades are blooming?

**Classify each component:**
- Black Swan component: Chaotic or Complex
- Grey Rhino component: Complicated
- Elephant component: Confusion or Complex
- Jellyfish component: Chaotic or Complex

**Step 2: Apply Appropriate Strategy to Each Component**

**For Black Swan components (Chaotic/Complex):**
- Act immediately to stabilize (Chaotic)
- Then experiment to learn (Complex)
- Don't try to analyze your way to a solution

**For Grey Rhino components (Complicated):**
- Expert analysis can solve this
- The barrier is organizational, not technical
- Apply systematic solutions

**For Elephant components (Confusion/Complex):**
- Break down further: technical vs. organizational
- Technical: Usually Complicated
- Organizational: Usually Complex (requires experimentation)
- Create psychological safety for truth-telling

**For Jellyfish components (Chaotic/Complex):**
- Break feedback loops immediately (Chaotic)
- Then understand cascade mechanics (Complex)
- Recover in dependency order

**Step 3: Coordinate Multiple Strategies**

**The IC's challenge:**
- Different components need different thinking
- Can't apply one strategy to everything
- Must coordinate without creating confusion

**Coordination principles:**
- Explicitly discuss which domain each component is in
- Assign different responders to different components
- Use different communication channels for different strategies
- Document which strategy is being applied where

**Step 4: Recognize Domain Transitions**

As you address components, they transition:

**Natural progression:**
- Chaotic → Complex → Complicated → Clear
- Confusion → Components classified → Appropriate strategies applied

**Watch for:**
- Components moving between domains
- New components appearing (more animals revealed)
- Interactions between components creating new domains

#### Example 1: The AWS DynamoDB Outage (October 20, 2025) as a Stampede

**The Trigger:**
At 12:11 AM PDT (07:11 UTC) on October 20, 2025, AWS engineers detected a rise in error rates and latency across multiple services in the US-EAST-1 region. By 1:26 AM (08:26 UTC), the problem had escalated into full DynamoDB endpoint failures. The root cause was traced to a DNS resolution error affecting DynamoDB's control layer—a misconfigured DNS propagation update that triggered recursive health checks and retry storms.

**The Stampede Breakdown:**

This incident revealed a classic stampede: multiple animals attacking simultaneously [White, 2025b]:

**1. Black Jellyfish Component (Chaotic → Complex):**
- A minor DNS misconfiguration rippled across opaque dependencies in unpredictable ways
- DynamoDB's centrality in AWS's transaction and state management layers caused cascading dependency failures
- The disruption was nonlinear, hidden, and widely felt by users unaware of their reliance on DynamoDB
- **Cynefin Action:** Break feedback loops immediately (Chaotic), then understand cascade mechanics (Complex)

**2. Grey Rhino Component (Complicated):**
- The risks from talent loss and interdependencies were visible for years
- Industry voices had warned that attrition was undermining cloud stability
- Between 2022 and 2025, Amazon laid off over 27,000 employees, with attrition reaching 81% in key teams
- **Cynefin Action:** Expert analysis can solve this - the barrier is organizational, not technical

**3. Elephant in the Room Component (Confusion → Complex):**
- Inside Amazon, discussions around staff loss and burnout were politically radioactive
- The cultural silence prevented action, even as warning signs mounted
- Institutional memory—often invisible and untracked—evaporated
- Without that folklore, detection time ballooned to 75 minutes
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

The incident wasn't just a technical failure—it was a crisis of forgotten knowledge. A generation of dashboards had nobody left who could interpret them under stress. The outage exposed a deeper form of technical debt: epistemic debt. When memory leaves, the system's ability to self-repair dies quietly.

**The Coordination Challenge:**

The IC had to simultaneously:
- Break cascade loops (Chaotic action for Black Jellyfish)
- Address infrastructure capacity issues (Complicated analysis for Grey Rhino)
- Navigate organizational silence about talent loss (Complex experimentation for Elephant)

All while coordinating across 113 affected services and multiple regions. This is why stampedes are so dangerous—they require multiple types of thinking at once, and the organizational context (the Elephant) makes technical response more difficult.

**Cynefin Analysis:**

**Initial State: Chaotic Domain**
- Cascade spreading rapidly through DynamoDB dependencies
- Immediate action required to break retry storms
- No time for analysis or experimentation
- **Action:** Break the feedback loop immediately

**After Stabilization: Complex Domain**
- Understanding cascade mechanics across 113 services
- Experimenting with prevention strategies
- Learning about dependency interactions
- **Action:** Safe-to-fail probes to understand system behavior

**Grey Rhino Component: Complicated Domain**
- Known risks from talent loss and interdependencies
- Expert analysis could have identified the organizational barriers
- The barrier was organizational, not technical
- **Action:** Systematic solutions for knowledge retention and redundancy

**Elephant Component: Confusion → Complex**
- Technical problem: Complicated (DNS misconfiguration)
- Organizational problem: Complex (cultural silence preventing action)
- Mixed together: Confusion (unclear which domain applies)
- **Action:** Break down into components, apply appropriate strategy to each

**Postmortem Insights:**

**What was genuinely unpredictable:**
- The specific interaction between DNS misconfiguration and DynamoDB's control layer
- The speed and scope of cascade across 113 services
- The extent of hidden dependencies

**What could have been better:**
- Institutional memory retention (Grey Rhino that became visible)
- Cultural safety to discuss talent loss risks (Elephant that became visible)
- Dependency mapping and cascade resistance (Black Jellyfish prevention)

**The Meta-Learning:**
This stampede revealed all three animals simultaneously. The DNS misconfiguration (Black Jellyfish trigger) exposed the Grey Rhino (known but ignored talent loss risks) and forced acknowledgment of the Elephant (cultural silence about organizational issues). The incident demonstrates that when multiple animals attack, you can't address them sequentially—you must coordinate multiple response strategies simultaneously.

**Lessons for SREs:**
- Institutional memory is part of your reliability stack
- People need redundancy too—losing senior staff isn't just a headcount issue, it's a hazard amplifier
- Observe the topology, not just the service—map secondary dependencies
- Measure resilience by adaptability, not just uptime
- Evolve incident protocols—local fixes don't work in globally entangled systems

#### Example 2: The October 10, 2025 Crypto Crash as a Stampede

**The Trigger:**
President Trump's tweet about tariffs triggered a market crash that revealed multiple animals.

**The Stampede Breakdown:**

**1. Black Swan Component (Chaotic → Complex):**
- Unpredictable timing of tweet
- Market reaction unprecedented in scale
- **Cynefin Action:** Act immediately to stabilize markets, then experiment to understand new patterns

**2. Grey Rhino Component (Complicated):**
- Exchange capacity issues known for months
- Infrastructure limitations visible but ignored
- **Cynefin Action:** Expert analysis can solve this - apply systematic capacity fixes

**3. Black Jellyfish Component (Chaotic → Complex):**
- Cascade through exchanges
- Positive feedback loops amplifying losses
- **Cynefin Action:** Break feedback loops immediately, then understand cascade mechanics

**4. Elephant Component (Confusion → Complex):**
- Leverage culture widely known but unspoken
- Organizational dysfunction preventing honest discussion
- **Cynefin Action:** Break down into technical (Complicated) and organizational (Complex) components

**The Coordination Challenge:**

The IC had to:
- Stabilize markets (Chaotic action for Black Swan)
- Fix exchange capacity (Complicated analysis for Grey Rhino)
- Break cascade loops (Chaotic action for Jellyfish)
- Address leverage culture (Complex experimentation for Elephant)

All simultaneously. This is why stampedes are so dangerous - they require multiple types of thinking at once.

#### Stampede Incident Management Principles

**1. Break Down, Don't Simplify (Cynefin: Handle Confusion by Decomposition)**

Stampedes are Confusion-domain problems. Don't try to force them into one domain.

**What to do:**
- Identify each animal in the stampede
- Classify each component's Cynefin domain
- Apply appropriate strategy to each
- Coordinate without creating more confusion

**What not to do:**
- Treat the whole stampede as one type of problem
- Apply one strategy to everything
- Ignore the complexity
- Simplify when you should decompose

**2. Coordinate Multiple Strategies**

Different components need different thinking. The IC must coordinate without creating chaos.

**Coordination techniques:**
- Explicit domain classification for each component
- Separate workstreams for different domains
- Different communication channels for different strategies
- Regular synthesis of all workstreams

**3. Watch for Interactions**

Components interact. A Grey Rhino charging can trigger a Jellyfish cascade. An Elephant being named can reveal more Rhinos.

**Monitor for:**
- Components triggering other components
- Domain transitions as you address components
- New components appearing (more animals revealed)
- Interactions creating new domains

**4. Post-Stampede Postmortem: The Full Picture**

Stampede postmortems must address:
- Each animal individually
- How they interacted
- Which Cynefin domains were involved
- Whether appropriate strategies were used
- How coordination worked (or didn't)

**Cynefin reflection:**
- Did we properly classify each component?
- Did we use the right strategy for each domain?
- How did we coordinate multiple strategies?
- What would help next time?

---
{::pagebreak /}
### Universal Incident Management Principles Across the Bestiary

#### 1. Information Flow Is Everything

Across all animal types, incident management success depends on information flowing to where it's needed, when it's needed, with enough fidelity to act on it.

#### 2. Psychological Safety Is Infrastructure

You cannot effectively manage incidents in a blame culture. Period.

#### 3. Documentation Is Time-Shifted Information Flow

Real-time documentation during incidents serves multiple purposes:
- Maintains coherent narrative
- Enables high-quality postmortem
- Teaches future responders
- Builds organizational memory
- **Documents Cynefin domain classification and transitions**

#### 4. Decision-Making Under Uncertainty Is A Core Skill

**Decision framework:**

**Categorize decisions by reversibility:**

**Reversible decisions (make fast):**
- Can be undone if wrong
- Examples: routing changes, circuit breaker states
- **These are safe-to-fail probes in Complex domain**

**Irreversible decisions (take more time):**
- Can't be undone easily
- Examples: data deletion, public commitments

**Use Cynefin to guide decision-making:**
- Chaotic: Act immediately (reversible actions preferred)
- Complex: Safe-to-fail experiments (reversible by design)
- Complicated: Analyze then decide (may be irreversible)
- Clear: Follow procedure (usually reversible)

#### 5. Postmortems Are Organizational Learning

**Postmortem quality indicators:**

**Good signs:**
- People admit mistakes and confusion
- Root causes are organizational, not just technical
- Action items address systemic issues
- Complexity is acknowledged
- **Cynefin domain classification included**

**Bad signs:**
- Single root cause for complex incident
- No admission of errors by anyone
- Narrative is too clean and simple
- Repeat incidents not acknowledged
- **No reflection on decision-making approach**

#### 6. Action Items Must Be Completed

The best postmortem is worthless if action items aren't completed.

**Tracking action items:**
- Every item has a single owner
- Critical items done within sprint
- Dashboard of postmortem action items
- Regular review and escalation if blocked

---

## Conclusion: Incident Management for the Menagerie

We've covered a lot of ground. From forest fires to failing servers. From ICS to NIST to Google SRE. From the Cynefin Framework to animal-specific strategies.

The key insight: **Different animals require different thinking.** The Cynefin Framework gives us a way to classify incidents and choose appropriate strategies. The bestiary gives us a way to understand what types of risks we're facing.

**For Black Swans:** Start in Chaotic, transition to Complex. Act first, experiment to learn. Don't try to analyze your way to a solution.

**For Grey Swans:** Often start in Complicated, may transition to Complex. Monitor for weak signals. Don't oversimplify complexity.

**For Grey Rhinos:** Usually Complicated. Expert analysis can solve them. The barrier is organizational, not technical.

**For Elephants:** Often create Confusion. Break down into technical (Complicated) and organizational (Complex) components.

**For Black Jellyfish:** Start in Chaotic, transition to Complex. Break feedback loops first, then understand cascade mechanics.

**For Stampedes:** Start in Confusion. Break down into components, classify each, apply appropriate strategies, coordinate multiple approaches.

The framework doesn't replace ICS, NIST, or Google SRE practices. It enhances them by providing the decision-making strategy that guides when and how to apply other techniques.

Remember: Culture is infrastructure. Information flow is everything. And different problems require different thinking.

Now go manage some incidents. The animals are waiting.

---


## References

[White, 2025] White, Geoff. "The Unwritten Laws of Information Flow: Why Culture is the Hardest System to Scale." LinkedIn, October 23, 2025. https://www.linkedin.com/pulse/unwritten-laws-information-flow-why-culture-hardest-system-white-7jxvc/

[White, 2025b] White, Geoff. "The Day the Cloud Forgot Itself." LinkedIn, October 21, 2025. https://www.linkedin.com/pulse/day-cloud-forgot-itself-geoff-white-gviqc/

<!-- Reference definitions at bottom -->

[Eugene_F_Kranz_at_his_console_at_the_NASA_Mission_Control_Center]: Eugene_F_Kranz_at_his_console_at_the_NASA_Mission_Control_Center.jpg

[anatomy-of-an-incident]: anatomy-of-an-incident.png
[incident-response-team]: incident-response-team.png
[cynefin-framework]: Cynefin_framework_2022.jpg
