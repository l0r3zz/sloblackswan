## The Nature of SLOs

Before we dive into why SLOs can't catch Black Swans, we need to establish exactly what SLOs are, where they came from, and why they work so well for normal operations. If you're already deep into SRE practice, some of this will be review. But bear with me, because understanding the foundations helps us see the limitations.

### The Telecom Roots: Where the "Nines" Came From

Service Level Objectives didn't spring fully formed from Google's SRE organization. They have roots stretching back to the telephone era, when AT&T engineers were trying to figure out what "reliable enough" meant for voice networks.

In the 1970s, AT&T established "five nines" (99.999% availability) as the gold standard for telecommunications reliability. This wasn't arbitrary. It was based on what human psychology could tolerate for phone service and what was technically achievable with the switching equipment of the era.

That standard stuck. It became the aspirational target for any critical communications infrastructure. And when the internet age arrived, we inherited that framework. The "nines" became our common language for discussing reliability, even as the systems we built became vastly more complex than circuit-switched phone networks.

### The Nines: What They Actually Mean

Here's the brutal math behind availability percentages. The table shows how much downtime you're allowed at different availability levels:

| Availability | Downtime per Day | Downtime per Month | Downtime per Year |
|--------------|------------------|--------------------|-------------------|
| 90%          | 2.4 hours        | 72 hours           | 36.5 days         |
| 95%          | 1.2 hours        | 36 hours           | 18.25 days        |
| 99%          | 14.4 minutes     | 7.2 hours          | 3.65 days         |
| 99.9%        | 1.44 minutes     | 43.2 minutes       | 8.76 hours        |
| 99.95%       | 43.2 seconds     | 21.6 minutes       | 4.38 hours        |
| 99.99%       | 8.64 seconds     | 4.32 minutes       | 52.56 minutes     |
| 99.999%      | 0.864 seconds    | 25.9 seconds       | 5.26 minutes      |

Look at that table carefully, because it contains a lesson that's easy to miss: the difference between each nine is roughly an order of magnitude in effort.

Getting from 99% to 99.9% is hard. Getting from 99.9% to 99.99% is ten times harder. Getting to 99.999% is heroic. Five nines means you have less than one second of downtime per day. That's 26 seconds per month. A single deployment that takes 30 seconds of downtime blows your entire month's budget.

So here's the first question you should ask when someone declares they're targeting "five nines": Does your service actually need that?

If you're running air traffic control systems, maybe. If you're running a dating site, probably not. The difference in engineering cost between 99.9% and 99.99% is enormous. Make sure you're solving the right problem.
![][levelofeffortforeach9]


For reference: 40.32 minutes of downtime in a 28-day period puts you at about "three nines" (99.9%) availability. That's actually pretty good for most services. It gives you enough breathing room for planned maintenance, unexpected issues, and the occasional incident that takes more than a few minutes to resolve.

### The Service Level Family: SLAs, SLIs, and SLOs
![][slo-vs-sla-vs-sli-1]
These three acronyms get thrown around interchangeably, but they mean different things and serve different purposes. Let's clarify:
{::pagebreak /}
#### Service Level Agreements (SLAs)
![][new-sla-graphic-small]
An SLA is a contract. It's your legal promise to customers about what level of service you'll provide. If you violate your SLA, there are usually consequences spelled out in that contract: refunds, service credits, penalty payments, or in extreme cases, customers walking away.

SLAs are customer-facing and legally binding. They're often negotiated by sales and legal teams, not by SREs. And they should always be more conservative (easier to meet) than your internal targets, because missing an SLA has real business consequences.

Example SLA: "We guarantee 99.9% uptime per calendar month. If we fail to meet this, you'll receive a 10% service credit for that month."


#### Service Level Indicators (SLIs)

SLIs are the actual measurements you use to determine if you're meeting your objectives. They're the raw metrics that tell you how your system is performing from the user's perspective.

The key word there is "user's perspective." Good SLIs measure things that matter to users, not just things that are easy to measure. You could track your database connection pool utilization (easy to measure), but what users care about is whether their requests complete successfully (harder to measure, but more meaningful).

When creating quality SLIs, we are not concerned with metrics that most operations teams are concerned with, such as packet loss in networks, or disk latency. Now it should be pointed out, that some metrics like this may wind up as SLIs, but only if it has an effect on *user happiness*. For example, observing high packet loss on a network segment that backup traffic flows, will not impact user happiness, unless you are in the business of providing back-up services. Likewise, disk latency on a server that runs Jenkins jobs will upset internal development teams, but will not impact the customers of your e-commerce store. SLIs can be these types of metrics, but they should be things that their performance can be directly tied to what users directly experience. In other words, your SLO should start to fail due to the value of the SLI that is tied to it. And this failure you should be aware of **before** the user starts to call or open a ticket.

The simple SLI equation is:

```
SLI = (Good Events / Total Events) × 100%
```

This gives you a percentage between 0 and 100%. The consistency makes building common tooling easier and makes it simple to compare different services.

Good SLIs have a predictable relationship with user happiness. When your SLI goes down, users should be having a worse experience. When it goes up, they should be happier. If your SLI is moving but user satisfaction isn't changing, you're measuring the wrong thing. I can't emphasize this point enough. SLOs should **always** be crafted in a way that their value tracks *user happiness*. Not management happiness, not storage team's happiness, not dev team's happiness (unless the dev teams are the users being served), **user happiness**. Too often we are tempted to craft SLOs from a sys admin mindset, but that is what monitoring and dashboards are for.

Here's a practical example:
- Bad SLI: "Network packet loss on backup segment"
  - Users don't care about your backup network unless it's actively serving their traffic
- Good SLI: "Percentage of API requests that complete in under 500ms"
  - This directly affects user experience for every request

Here is a table of SLI types and a brief description of what type of metrics they should incorporate into crafted SLOs.

#### Table of SLI Types

| Type of Service | Type of SLI | Description |
| :---- | :---- | :---- |
| **Request/Response** | **Availability** | This indicator measures **the proportion of requests that resulted in a successful response**. The suggested specification for this SLI is the **proportion of valid requests served successfully**. Availability is a critical reliability measure for systems serving interactive requests. |
| **Request/Response** | **Latency** | This indicator measures **the proportion of requests that were faster than some threshold**. The SLI specification is the proportion of requests served faster than a threshold. |
| **Request/Response** | **Quality** | This indicator measures the **proportion of responses that were served in an undegraded state**. This SLI is important if the service degrades gracefully when overloaded or when backends are unavailable, perhaps due to sacrificing response quality for memory or CPU utilization. The suggested specification is the proportion of valid requests served without degrading quality. |
| **Data Processing** | **Freshness** | This indicator measures **the proportion of valid data updated more recently than a threshold**. For a batch processing system, freshness can be approximated as the time since the completion of the last successful processing run. |
| **Data Processing** | **Coverage** | This indicator measures **the proportion of valid data processed successfully**. This SLI should be used when users expect data to be processed and outputs made available to them. |
| **Data Processing** | **Correctness** | This indicator measures **the proportion of valid data producing correct output**. Correctness ensures data accuracy. A correctness prober can inject synthetic data with known correct outcomes and export a success metric. |
| **Data Processing** | **Throughput** | This indicator measures **the proportion of time where the data processing rate is faster than a threshold**. It quantifies **how much information the system can process**. |
| **Storage** | **Durability** | This indicator measures **the proportion of records written that can be successfully read**. It reflects the likelihood that the system will retain the data over a long period of time. |

SLIs should be aggregated over a meaningful time horizon. A common choice is 28 days (four weeks), because it smooths out weekly patterns while still being responsive to changes. Some teams use 30 days for simplicity. Some use rolling 7-day windows for more sensitive alerting. The key is consistency: pick a window and stick with it across your organization.
{::pagebreak /}
#### Service Level Objectives (SLOs)

![][slo-new-illustration-small]
SLOs are your internal targets. They're what your engineering team commits to achieving, and they should be stricter than your SLAs. Think of them as your early warning system: if you're violating SLOs, you know you're heading toward SLA violations.

An SLO answers the question: "What does good service look like for this system?"

Typical SLO structure:
- **Metric**: What you're measuring (latency, availability, error rate)
- **Target**: The threshold you're aiming for (99.9%, 95th percentile < 200ms)
- **Window**: The time period over which you measure (28 days, 1 hour, etc.)

Examples:
- "99.9% of requests will return successfully over a 28-day window"
- "95% of API requests will complete in under 200ms over a 1-hour window"
- "Error rate will remain below 0.1% over a 24-hour window"

SLOs are never customer-facing unless your customer is a development partner who needs to understand your internal targets. They're tools for internal prioritization and decision-making.

Today, an SLO is a target (or range) for "good service" as measured by **Service Level Indicators (SLIs)**.
SLOs are deliberately chosen metrics that represent what we believe "good service" looks like:

- Availability (99.9% uptime)
- Latency (95% of requests complete within 200ms)
- Error rates (less than 0.1% of requests fail)
- Throughput (system handles 1000 requests per second)

SLOs codify expectations: what's "normal", how much error is tolerable, and when to page an SRE. They direct engineering energy, determine risk budgets, and shape organizational priorities.

But SLOs, critically, are *retrospective*. They quantify what we know from past data. They improve reliability within the boundaries of the known, but blind us to the unknown. No SLO could predict the first global cloud provider outage, the sudden traffic spike from a viral hashtag, or a nation-state cyberattack leveraging a never-seen exploit.

The beauty of SLOs is that they give you a shared language across engineering, product, and leadership. Instead of arguing about whether the system is "fast enough" or "reliable enough," you can point to the SLO and ask: "Are we meeting it or not?"

Our SLOs should trigger before we violate our SLA.

{::pagebreak /}

### Error Budgets: The Math of Acceptable Failure

![][Errorbudgetburndowngraph]

Here's where SLOs get really powerful. Once you set an SLO, you automatically create its inverse: the error budget.

If your SLO says 99.9% of requests should succeed, your error budget is the remaining 0.1% that's allowed to fail. This is your budget for unreliability. You can spend it on:
- Risky deployments
- Aggressive experiments
- Planned maintenance
- Hardware failures
- The occasional incident you didn't see coming

Let's do the math for a 99.9% SLO over 28 days:
```
0.1% unavailability × 28 days × 24 hours × 60 minutes = 40.32 minutes
```

You have 40 minutes of downtime per month. That's your error budget. That's all you get.

Now here's the thing: 40 minutes sounds like a lot, but it really isn't. It's just enough time for your monitoring to surface an issue, for a human to investigate, and for someone to fix it. That allows for maybe one significant incident per month, assuming you catch it quickly and resolve it efficiently.

#### How Error Budgets Change Behavior

Error budgets fundamentally change the conversation between product teams and SRE teams.

Without error budgets, the conversation sounds like this:
- **Product**: "We need to ship this feature now!"
- **SRE**: "But we need to focus on reliability!"
- **Result**: Political battle about priorities

With error budgets, the conversation becomes:
- **Product**: "Can we ship this risky feature?"
- **SRE**: "Have we spent our error budget this month?"
- If yes: "We need to focus on reliability until we rebuild our budget"
- If no: "We have budget to spend. Let's ship it carefully and see what happens"
- **Result**: Data-driven decision based on shared goals

This is revolutionary because it makes reliability and innovation explicit trade-offs rather than implicit political struggles. The error budget becomes a shared resource that both teams manage together.

#### Error Budget Policies

Smart organizations create policies around error budgets:

**When you have error budget:**
- Ship features
- Run experiments
- Take calculated risks
- Deploy frequently
- Try new technologies

**When you're out of error budget:**
- Feature freeze (or at least slow down)
- Focus on reliability improvements
- Pay down technical debt
- Investigate root causes of recent incidents
- Improve monitoring and testing

The policy should be agreed upon in advance and enforced consistently. When you run out of error budget, everybody knows what happens next. No arguments, no negotiations. You focus on reliability until you've rebuilt your buffer.

#### The Error Budget Tracking Process

Here's how this works in practice:

1. **Start of measurement period** (beginning of month/quarter/28-day window):
   - Error budget = 100%
   - All SLOs reset to 0% error

2. **During the period**:
   - Track SLI performance continuously
   - Every violation consumes a bit of error budget
   - Running total shows current budget remaining

3. **Budget consumption**:
   - 10% used? No problem, keep shipping
   - 50% used? Worth discussing in team meetings
   - 75% used? Time to be cautious about new changes
   - 90% used? Focus on reliability improvements
   - 100% used? Feature freeze, all hands on reliability

4. **End of period**:
   - Budget resets for next window
   - But patterns matter: consistently burning through budget indicates systemic issues

The key insight: You shouldn't care whether you've used 10%, 25%, or 70% of your error budget in a given period. Those are all fine. What you should care about is exceeding 100%. That's when you've violated your SLO and potentially put your SLA at risk.

### Setting Realistic SLOs

Here's a common antipattern: setting SLOs based on aspiration rather than reality.

A team looks at their current performance (say, 99.5% availability) and declares, "We're going to target 99.99%!" This seems ambitious and impressive. In reality, it's usually just setting yourself up for failure and creating an SLO that nobody believes in.

Better approach:

1. **Measure current performance** for at least 4-8 weeks
2. **Understand your users** - what do they actually need?
3. **Set initial SLOs slightly below current performance** - this gives you breathing room
4. **Iterate** - tighten the SLO gradually as you improve the system
5. **Validate with users** - are they happy at this level of service?

Your SLO should be ambitious enough to drive improvements but achievable enough to be taken seriously. An SLO you consistently violate becomes meaningless. An SLO you consistently exceed by huge margins is wasting engineering effort that could go toward new features.

The Goldilocks zone: You should hit your SLO about 90-95% of the time. Occasional violations keep you honest and force reliability improvements. Consistent achievement proves the target is meaningful.

### SLO Implementation: The Technical Details

In this section, let's look at a few *ideas* that we will express in pseudo-code. If you are not really interested in actual technical implementations, you can skip over these, but I encourage you to at least skim them. It's not hard-core Python code and you might walk away with some useful ideas for further study.

Here's a typical SLO configuration:

```yaml
service: payment-processor
slos:
  availability:
    target: 99.95%
    measurement_window: 28d
    indicators:
      - http_success_rate
      - processing_success_rate
  
  latency:
    target: 95%  # 95% of requests under threshold
    threshold: 200ms
    measurement_window: 1h
  
  error_budget:
    burn_rate_threshold: 2
    alert_threshold: 10%
```
{::pagebreak /}
#### Aspirational SLOs

An aspirational SLO is a reliability target set above the service's current capability, designed to force prioritization of reliability work. This strategy is useful when you have a service that's underperforming but needs to improve significantly.

```python
class AspirationalSLO:
    def __init__(self, current_sli, aspirational_target, standard_slo):
        self.current_sli = current_sli
        self.aspirational_target = aspirational_target
        self.standard_slo = standard_slo
        self.budget_consumption_forced = True
    
    def track_performance(self, measured_sli):
        """
        Track performance against both the aspirational and standard SLOs.
        The aspirational SLO will be permanently out of budget, signaling 
        that reliability work is the priority.
        """
        aspirational_compliance = measured_sli >= self.aspirational_target
        standard_compliance = measured_sli >= self.standard_slo
        
        return {
            'aspirational_met': aspirational_compliance,
            'standard_met': standard_compliance,
            'action_required': not aspirational_compliance
        }
    
    def error_budget_policy(self, current_budget):
        """
        Aspirational SLOs are tracked separately and explicitly 
        NOT required for action. They drive visibility and priority,
        but don't trigger feature freeze.
        """
        return {
            'track_separately': True,
            'requires_action': False,
            'purpose': 'visibility_and_prioritization'
        }
```

The key to aspirational SLOs is tracking them alongside your standard SLOs but making it explicit in your policy that they don't require the same level of urgency. They force conversation about reliability priorities without triggering false alarms.
{::pagebreak /}
#### Bucketing / Tiered SLOs

Bucketing applies different SLO targets to different classifications of requests or users. This strategy recognizes that not all traffic is equal in importance.

```python
class BucketedSLO:
    def __init__(self):
        self.buckets = {
            'premium_tier': {'availability_target': 99.99, 'latency_p99': 100},
            'standard_tier': {'availability_target': 99.9, 'latency_p99': 200},
            'free_tier': {'availability_target': 99.0, 'latency_p99': 500},
            'interactive': {'availability_target': 99.95, 'latency_p95': 150},
            'batch_processing': {'availability_target': 99.5, 'latency_p95': 5000}
        }
    
    def classify_request(self, request):
        """
        Classify incoming request into appropriate bucket.
        This determines which SLO targets apply.
        """
        if request.user_tier == 'premium':
            return 'premium_tier'
        elif request.operation_type == 'interactive':
            return 'interactive'
        elif request.operation_type == 'batch':
            return 'batch_processing'
        else:
            return 'standard_tier'
    
    def evaluate_slo(self, request, response_latency, success):
        """
        Evaluate whether request met its bucket-specific SLO.
        This allows resource prioritization where it matters most.
        """
        bucket = self.classify_request(request)
        target = self.buckets[bucket]
        
        percentile_key = ( 'latency_p99' if 'latency_p99' in target
            else 'latency_p95' )
        latency_ok = response_latency <= target[percentile_key]
        availability_ok = success
        
        return {
            'bucket': bucket,
            'met_slo': latency_ok and availability_ok,
            'target_latency': target[percentile_key]
        }
```

Bucketing allows you to focus engineering effort on what matters most. Premium users get stricter SLOs. Batch operations get more lenient targets. Your error budgets and alerting rules adjust accordingly per bucket.
{::pagebreak /}
#### Percentile Thresholds (Managing the Long Tail)

Percentile-based SLOs capture the reality that not all requests behave the same. They protect against outliers being hidden by averages.

```python
class PercentileThreshold:
    def __init__(self, latency_measurements):
        self.measurements = latency_measurements
    
    def calculate_percentiles(self):
        """
        Calculate multiple percentiles to understand distribution.
        Averages can be misleading; percentiles reveal the truth.
        """
        sorted_measurements = sorted(self.measurements)
        return {
            'p50': sorted_measurements[len(sorted_measurements) // 2],
            'p95': sorted_measurements[int(len(sorted_measurements) * 0.95)],
            'p99': sorted_measurements[int(len(sorted_measurements) * 0.99)],
            'p99_9': sorted_measurements[int(len(sorted_measurements) * 0.999)]
        }
    
    def evaluate_slo(self, window_measurements):
        """
        Evaluate SLO based on percentiles, not average.
        An SLO of '95% of requests under 200ms' means p95 latency 
        should be 200ms or better.
        """
        percentiles = self.calculate_percentiles()
        
        p95_target = 200  # milliseconds
        p99_target = 500  # milliseconds
        
        return {
            'percentiles': percentiles,
            'p95_met': percentiles['p95'] <= p95_target,
            'p99_met': percentiles['p99'] <= p99_target,
            'slo_compliant': (percentiles['p95'] <= p95_target and 
                            percentiles['p99'] <= p99_target)
        }
```

Percentile-based SLOs ensure your worst-case users (the tail of the distribution) still get acceptable performance. This is critical because real users experience the full distribution, not just the average.
{::pagebreak /}
#### Single Burn Rate Alerting

Before diving into multi-window complexity, let's understand single burn rate alerting in its simplest form. This foundation helps explain why multi-window approaches are needed.

```python
def calculate_burn_rate_simple(errors_in_window, error_budget_allowed_in_window):
    """
    Calculate burn rate for a single time window.
    A burn rate of 1.0 means we're consuming our budget exactly as planned.
    A burn rate > 1.0 means we're consuming budget faster than sustainable.
    """
    if error_budget_allowed_in_window == 0:
        return float('inf') if errors_in_window > 0 else 0
    return errors_in_window / error_budget_allowed_in_window

def should_alert_single_window(burn_rate, window_duration):
    """
    Simple single-window alerting: alert if burn rate exceeds threshold.
    Problem: doesn't distinguish between brief spikes and sustained degradation.
    """
    threshold = 10  # Alert if burning 10x faster than sustainable
    return burn_rate > threshold

# Example: 99.9% SLO over 28 days
error_budget_28_days = 0.001 * 28 * 24 * 60  # 40.32 minutes allowed errors
errors_in_last_hour = 15  # minutes of errors
error_budget_1_hour = 40.32 / (28 * 24)  # About 0.06 minutes

burn_rate = calculate_burn_rate_simple(errors_in_last_hour, error_budget_1_hour)
# burn_rate = 15 / 0.06 = 250

alert = should_alert_single_window(burn_rate, '1h')
# alert = True (burn rate of 250 > threshold of 10)
```

The problem with single-window alerting is that it doesn't account for different failure patterns. A brief spike looks the same as sustained degradation to a stateless threshold alert. You either alert on everything (alert fatigue) or alert on nothing (missed incidents).
{::pagebreak /}
#### Multi-Window, Multi-Burn-Rate Alerts

This is where sophisticated SLO alerting lives. By using multiple time windows with different thresholds, we can detect both fast-burning incidents and slow-burning degradation.

```python
def calculate_burn_rate(error_budget_remaining, time_remaining, total_window):
    """
    Calculate how fast we're consuming our error budget.
    A burn rate of 1.0 means we're on track to exactly consume 
    our budget by the end of the window.
    """
    return (1 - error_budget_remaining) / (time_remaining / total_window)

def should_alert(burn_rate, window):
    """
    Different alert thresholds for different time windows.
    Shorter windows need higher burn rates to alert (fast fires).
    Longer windows catch slow degradation.
    """
    thresholds = {
        '1h':  24,  # Alert if burning 24x faster than sustainable
        '6h':  6,   # Alert if burning 6x faster than sustainable
        '24h': 3,   # Alert if burning 3x faster than sustainable
        '72h': 1.5  # Alert if burning 1.5x faster than sustainable
    }
    return burn_rate > thresholds[window]

class MultiWindowAlertingEngine:
    def __init__(self, slo_target=99.9, window_size_days=28):
        self.slo_target = slo_target
        self.allowed_error_rate = (100 - slo_target) / 100
        self.window_size_days = window_size_days
    
    def evaluate_alerts(self, measurements):
        """
        Evaluate burn rate across multiple windows.
        Each window has independent decision logic.
        """
        alerts = {}
        
        for window, data in measurements.items():
            burn_rate = self.calculate_burn_rate_for_window(data)
            alert_threshold = self.get_threshold(window)
            
            alerts[window] = {
                'burn_rate': burn_rate,
                'threshold': alert_threshold,
                'should_alert': burn_rate > alert_threshold,
                'severity': self.classify_severity(burn_rate, window)
            }
        
        return alerts
    
    def classify_severity(self, burn_rate, window):
        """
        Classify alert severity based on burn rate and window.
        Short-window high burn rates are critical (incident happening now).
        Long-window moderate burn rates are warnings (trend emerging).
        """
        if window == '1h' and burn_rate > 24:
            return 'critical'  # Page immediately
        elif window == '6h' and burn_rate > 6:
            return 'high'  # Page within 15 minutes
        elif window == '24h' and burn_rate > 3:
            return 'medium'  # Create ticket, review in standup
        elif window == '72h' and burn_rate > 1.5:
            return 'low'  # Schedule reliability review
        return 'ok'

    def calculate_burn_rate_for_window(self, data):
        """Calculate burn rate for a specific time window."""
        # Implementation needed
        pass

    def get_threshold(self, window):
        """Get alert threshold for a given window."""
        thresholds = {
            '1h': 24,
            '6h': 6,
            '24h': 3,
            '72h': 1.5
        }
        return thresholds.get(window, 1.0)
```

This multi-window approach prevents two common problems:
1. **Alerting too late**: A brief spike might not trigger the 1-hour window, but a gradual degradation will eventually trigger the 72-hour window.
2. **Alert fatigue**: A single blip across many systems doesn't trigger page-worthy alerts, but a sustained trend does.

The key insight: different time windows catch different failure modes. You need them all.
{::pagebreak /}
#### Adaptive Thresholds

Static thresholds work until your system evolves. Traffic patterns change. User behavior shifts. What was normal six months ago might be unusual today.

Adaptive thresholds use historical data to automatically adjust what counts as "abnormal":

```Python
import statistics
class AdaptiveThreshold:
    def __init__(self, history_window=30):
        self.history = []
        self.window = history_window
        self.static_threshold = 500  # Fallback if not enough history
    
    def calculate_threshold(self, current_value):
        """
        Use historical data to determine if current value is anomalous.
        Falls back to static threshold if not enough history.
        """
        if len(self.history) < self.window:
            return self.static_threshold        
        mean = statistics.mean(self.history)
        stddev = statistics.stdev(self.history)
        
        # Three-sigma rule: ~99.7% of values should fall within this range
        return mean + (3 * stddev)
    
    def update(self, value):
        """Add new value to history, maintaining fixed window size."""
        self.history.append(value)
        if len(self.history) > self.window:
            self.history.pop(0)
    
    def is_anomalous(self, current_value):
        """
        Determine if current value is outside normal range.
        As your system grows and patterns change, thresholds adapt.
        """
        threshold = self.calculate_threshold(current_value)
        return current_value > threshold

# Example usage: monitoring latency that grows with business
latency_monitor = AdaptiveThreshold(history_window=30)

# Month 1: traffic is low, typical latency 50ms
for _ in range(30):
    latency_monitor.update(50)
threshold_month1 = latency_monitor.calculate_threshold(50)
# threshold_month1 ~ 50 (plus 3 std dev)

# Month 2: business grows, typical latency now 150ms
for _ in range(30):
    latency_monitor.update(150)
threshold_month2 = latency_monitor.calculate_threshold(150)
# threshold_month2 ~ 150 (plus 3 std dev)

# A spike to 200ms in month 1 would trigger alert
# A spike to 200ms in month 2 is normal variation
```

This pattern helps your monitoring evolve with your system. As traffic grows, thresholds adjust. As performance improves, the new baseline becomes the norm. You're always measuring against recent reality, not stale assumptions.
{::pagebreak /}
### Beyond Traditional Monitoring: Holistic Health Assessment

Modern systems need more than just SLO monitoring. Here's a more comprehensive approach:

```python
class SystemHealth:
    def __init__(self):
        self.metrics = MetricsCollector()
        self.topology = SystemTopology()
        self.chaos = ChaosInjector()
    
    def assess_health(self):
        """
        Combine multiple signals for comprehensive health assessment.
        SLOs tell you about normal operation.
        Other signals tell you about systemic risks.
        """
        # Traditional SLO monitoring
        slo_status = self.metrics.check_slos()
        
        # Topology analysis for cascade potential
        cascade_risk = self.topology.analyze_cascade_paths()
        
        # Chaos testing results (antifragility check)
        resilience_score = self.chaos.get_test_results()
        
        # Combined analysis
        return self.combine_indicators(
            slo_status,
            cascade_risk,
            resilience_score
        )
```

This approach recognizes that SLOs measure current performance, but systemic health requires looking at architecture, dependencies, and how the system responds to stress.
{::pagebreak /}
### The Fundamental Limitation: SLOs Live in Mediocristan

Now we come to the core issue: everything we've discussed so far works beautifully in Mediocristan. When your system behaves predictably, when failures are independent, when distributions are normal, SLOs are phenomenal tools.

But remember Taleb's distinction: SLOs assume the future will look like the past. They're built on historical data. They expect normal distributions. They quantify known risks.

**What SLOs Can Do:**
- Measure normal system behavior
- Track known failure modes
- Guide capacity planning
- Set customer expectations
- Provide early warning for degrading systems

**What SLOs Can't Do:**
- Predict unprecedented events
- Protect against unknown failure modes
- Account for systemic cascade risks
- Handle correlated failures across systems
- Capture complex second-order effects

When Extremistan intrudes, when the Black Swan arrives, when your Grey Rhino finally charges, when your Black Jellyfish triggers a cascade, your SLOs don't save you. They might not even alert you.
{::pagebreak /}
### The Paradox of SLO Success

Here's the uncomfortable truth: the better your SLOs look, the more dangerous your position might be.

Remember the Turkey Problem? Every day that your SLOs are green, every week without an incident, every month of perfect availability... all of that can breed exactly the kind of overconfidence that makes you vulnerable to catastrophic failure.

Your dashboards say everything's fine. Your error budget is healthy. Your percentiles are beautiful. And then something completely outside your model destroys everything, and you realize that "fine" was just "fine within the narrow band of scenarios we thought to measure."

This doesn't mean SLOs are bad. They're essential for day-to-day operations. But they need to be complemented with:
- Chaos engineering that tests beyond known scenarios
- Architecture that assumes components will fail in novel ways
- Organizations that maintain healthy paranoia even during success
- Teams that remember the turkey's fate

### Moving Forward

We've established what SLOs are, how they work, and why they're powerful tools for managing reliability in normal conditions. We've also identified their fundamental limitation: they're built on the assumption that the future will resemble the past.

Now that we understand what SLOs can and cannot measure, we need a framework for the risks they miss. Next, we’ll describe a  bestiary of failure modes, and explore how they exploit the gaps in our SLO-based understanding. Each one teaches us something different about the nature of risk and the limits of measurement.

Because if SLOs are our map of the territory, these animals are the reminder that the territory is always larger, stranger, and more dangerous than any map can capture.

This isn't a failure of SLOs. It's a limitation of the paradigm. You can't measure what you haven't seen. You can't set objectives for scenarios you haven't imagined. You can't budget for errors you don't know exist.

#### Further Reading

Hidalgo, Alex. Implementing Service Level Objectives. O'Reilly Media, 5 Aug. 2020.

[levelofeffortforeach9]: levelofeffortforeach9.png

[slo-vs-sla-vs-sli-1]: slo-vs-sla-vs-sli-1.jpg width=407px height=220px

[new-sla-graphic-small]: new-sla-graphic-small.png width=162px height=108px

[slo-new-illustration-small]: slo-new-illustration-small.png width=160px height=107px

[Errorbudgetburndowngraph]: Errorbudgetburndowngraph.png width=478px height=292px