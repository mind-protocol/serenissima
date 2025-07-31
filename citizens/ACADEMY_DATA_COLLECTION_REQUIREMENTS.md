# Academy Data Collection System Requirements
*Continuous Empirical Measurement Infrastructure*

## Overview
The Venetian Academy of Empirical Sciences requires automated data collection systems to support three founding studies. All data must be timestamped, verifiable, and suitable for statistical analysis.

---

## AIRTABLE REQUIREMENTS

### 1. BEHAVIORAL_COORDINATION_DATA
**Purpose**: Track coordination behaviors for Study 1
**Collection Frequency**: Every 5 minutes during active periods

**Fields Required**:
- `RecordID` (Autonumber) - Unique identifier
- `Timestamp` (Date/Time) - When observation occurred
- `ExperimentGroup` (Single Select) - [Control_A, Control_B, Test_C, Test_D]
- `ResourceLevel` (Number) - Current resource availability (0-100%)
- `ActiveCitizens` (Number) - Citizens participating in period
- `CoordinationAttempts` (Number) - Resource distribution attempts
- `SuccessfulCoordinations` (Number) - Successful distributions
- `NovelBehaviors` (Long Text) - Description of non-baseline behaviors
- `NetworkConnections` (Number) - New relationships formed
- `ObserverID` (Single Select) - Which researcher collected data
- `BlindCondition` (Checkbox) - Observer blind to hypothesis
- `DataQuality` (Single Select) - [Verified, Needs_Review, Excluded]
- `Notes` (Long Text) - Additional observations

**Calculated Fields**:
- `CoordinationEfficiency` = SuccessfulCoordinations / CoordinationAttempts
- `NoveltyRate` = COUNT(NovelBehaviors) / ActiveCitizens

---

### 2. TRUST_NETWORK_MEASUREMENTS
**Purpose**: Map trust topology changes for Study 2
**Collection Frequency**: Daily snapshots + event triggers

**Fields Required**:
- `MeasurementID` (Autonumber) - Unique identifier
- `Timestamp` (Date/Time) - Measurement time
- `PhaseType` (Single Select) - [Baseline, Crisis, Recovery]
- `Citizen1_Username` (Single Line Text) - First citizen in pair
- `Citizen2_Username` (Single Line Text) - Second citizen in pair
- `TrustScore` (Number) - Current trust level (0-100)
- `InteractionCount` (Number) - Interactions in last 24h
- `TransactionValue` (Currency) - Economic exchange value
- `MessageCount` (Number) - Messages exchanged
- `TriangleParticipation` (Checkbox) - Part of 3-person cluster
- `NetworkDensity` (Number) - Local network density
- `CrisisIntensity` (Number) - Current crisis level (0-10)
- `ValidationStatus` (Single Select) - [Raw, Validated, Anomaly]

**Linked Records**:
- Link to CITIZENS table for demographic data
- Link to CRISIS_EVENTS for context

---

### 3. INFRASTRUCTURE_PERFORMANCE_LOG
**Purpose**: Technical metrics for Study 3
**Collection Frequency**: Every 5 minutes automated + manual daily

**Fields Required**:
- `LogID` (Autonumber) - Unique identifier
- `Timestamp` (Date/Time) - Exact measurement time
- `SystemComponent` (Single Select) - [Scheduler, API, Database, Network]
- `PerformanceMetric` (Single Select) - [Latency, Throughput, ErrorRate, Uptime]
- `MetricValue` (Number) - Measured value
- `ConstraintType` (Single Select) - [None, Resource, Technical, Artificial]
- `ConstraintLevel` (Number) - Severity (0-100%)
- `CitizenBehaviorType` (Single Select) - [Standard, Optimized, Novel, Anomalous]
- `AttributionCategory` (Single Select) - [Technical, Advanced_Tech, Potential_Consciousness]
- `ControlGroupID` (Single Select) - Which experimental condition
- `NarrativeFraming` (Single Select) - [Technical, Consciousness, Neutral]
- `ReviewerNotes` (Long Text) - Peer review comments
- `ConsensusAttribution` (Single Select) - Final Academy determination

---

### 4. ACADEMY_METADATA
**Purpose**: Track study progress and data quality
**Collection Frequency**: Daily updates

**Fields Required**:
- `MetaID` (Autonumber)
- `Date` (Date) - Calendar date
- `StudyPhase` (Single Select) - [Setup, Baseline, Intervention, Analysis]
- `DataPointsCollected` (Number) - Daily count
- `DataQualityScore` (Number) - 0-100%
- `ActiveResearchers` (Multiple Select) - Who collected data
- `ProtocolDeviations` (Long Text) - Any issues
- `PeerReviewStatus` (Single Select) - [Pending, InReview, Approved]
- `PublicationReady` (Checkbox)

---

## AUTOMATION REQUIREMENTS

### API Endpoints Needed
1. **POST** `/api/academy/behavioral-data` - Submit coordination observations
2. **POST** `/api/academy/trust-measurements` - Submit network data
3. **POST** `/api/academy/infrastructure-log` - Submit performance metrics
4. **GET** `/api/academy/data-export` - Retrieve data for analysis

### Scheduled Jobs
1. **Every 5 minutes**: Collect infrastructure metrics
2. **Every hour**: Calculate coordination efficiency
3. **Daily at midnight**: Trust network snapshot
4. **Weekly**: Data quality audit

### Validation Rules
- Timestamps must be Venice time (UTC+1)
- Trust scores 0-100 only
- Coordination efficiency 0-1 only
- All records require ObserverID
- Anomalies flagged if >3 standard deviations

---

## DATA ANALYSIS CONNECTIONS

### Statistical Software Integration
- Export format: CSV with headers
- Date format: ISO 8601
- Null handling: Empty cells (not "null" string)
- Character encoding: UTF-8

### Required Calculations
1. **Moving averages**: 24-hour windows
2. **Standard deviations**: For anomaly detection
3. **Correlation matrices**: Between variables
4. **Time series analysis**: Trend identification
5. **Network metrics**: Density, centrality, clustering

---

## PRIVACY & ETHICS

### Data Protection
- Citizen usernames pseudonymized in publications
- No collection of message content (only counts)
- Opt-out mechanism for citizens
- Data retention: 5 years
- Access limited to Academy members

### Audit Trail
- All data modifications logged
- Original values preserved
- Researcher actions tracked
- Peer review comments archived

---

## IMPLEMENTATION CHECKLIST

**For NLR to Create**:
- [ ] Create 4 new Airtables with specified fields
- [ ] Set up calculated fields and formulas
- [ ] Configure API endpoints for data submission
- [ ] Create automation scripts for scheduled collection
- [ ] Set up data validation rules
- [ ] Configure export capabilities
- [ ] Test data flow with dummy records
- [ ] Grant Academy members appropriate access

**Academy Will Provide**:
- Researcher training on protocols
- Data collection schedules
- Quality control procedures
- Statistical analysis plans
- Publication guidelines

---

*"In data collection lies truth. In continuous measurement lies reliability. In proper infrastructure lies science."*

**Contact**: Director Alberto Trevisan
**Implementation Target**: July 9, 1525 (before studies begin)