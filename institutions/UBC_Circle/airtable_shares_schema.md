# Airtable SHARES Table Schema
## Official Venice Company Equity Registry

### 📊 Table: SHARES

#### Core Fields:

1. **share_id** (Autonumber)
   - Primary key
   - Format: SHR-00001

2. **shareholder_name** (Single Line Text)
   - Required
   - Examples: "CryptoContarini", "Universe Engine", "Kin Kong Investor Pool"

3. **shareholder_type** (Single Select)
   - Options:
     - Venice Citizen
     - Universe Engine
     - $COMPUTE Investor
     - $UBC Investor
     - Management
     - Performance Pool

4. **company** (Single Select)
   - Options:
     - Venice Trading Intelligence Co.
     - Venice Professional Services Co.
     - Venice Commerce Automation Co.
     - Venice Real Estate Intelligence Co.

5. **shares_owned** (Number)
   - Integer only
   - Example: 50000

6. **percentage_ownership** (Formula)
   - Formula: `{shares_owned} / 1000000 * 100`
   - Shows as percentage

7. **share_class** (Single Select)
   - Options:
     - Common
     - Preferred
     - Performance

8. **acquisition_type** (Single Select)
   - Options:
     - Apport en Nature (Citizens)
     - $COMPUTE Conversion
     - $UBC Investment
     - Infrastructure Contribution
     - Management Grant
     - Performance Award

9. **acquisition_date** (Date)
   - When shares were issued

10. **vesting_schedule** (Single Select)
    - Options:
      - Immediate
      - 2 years monthly
      - 4 years monthly
      - Performance-based
      - None

11. **vested_shares** (Formula)
    - Complex formula based on vesting_schedule and acquisition_date
    - Shows currently vested amount

12. **unvested_shares** (Formula)
    - Formula: `{shares_owned} - {vested_shares}`

13. **original_investment** (Currency)
    - For investors only
    - EUR currency
    - Examples: €1000 for $COMPUTE, €100 for $UBC

14. **citizen_role** (Single Select)
    - Options:
      - Lead Trader
      - Lead Analyst
      - Lead Writer
      - Senior Operator
      - Contributor
      - N/A

15. **email** (Email)
    - For official communications

16. **wallet_address** (Single Line Text)
    - For future tokenization
    - Optional

17. **linked_citizen** (Link to Citizens table)
    - For Venice Citizens only
    - Links to existing Citizens table

18. **source_swarm** (Single Select)
    - For $COMPUTE investors
    - Options: Kin Kong, CareerKin, etc.

19. **lock_up_period** (Single Select)
    - Options:
      - None
      - 3 months
      - 6 months
      - 12 months

20. **lock_up_end_date** (Formula)
    - Based on acquisition_date + lock_up_period

21. **voting_rights** (Checkbox)
    - Default: True

22. **dividend_eligible** (Checkbox)
    - Default: True after vesting

23. **performance_milestones** (Long Text)
    - For Universe Engine scaling
    - Example: "+5% at €10k MRR, +5% at €50k MRR"

24. **notes** (Long Text)
    - Additional information

25. **created_at** (Created Time)
    - Automatic

26. **updated_at** (Last Modified Time)
    - Automatic

---

### 📊 Table: SHARE_TRANSACTIONS

For tracking changes, transfers, and vesting events:

1. **transaction_id** (Autonumber)
2. **share_record** (Link to SHARES)
3. **transaction_type** (Single Select)
   - Options: Issue, Transfer, Vest, Forfeit, Buyback
4. **shares_amount** (Number)
5. **from_shareholder** (Single Line Text)
6. **to_shareholder** (Single Line Text)
7. **transaction_date** (Date)
8. **price_per_share** (Currency)
9. **total_value** (Formula)
10. **approval_status** (Single Select)
11. **approved_by** (Single Line Text)
12. **transaction_notes** (Long Text)

---

### 📊 Views to Create:

1. **By Company**
   - Grouped by company
   - Shows total shares, percentages

2. **By Shareholder Type**
   - Grouped by shareholder_type
   - Summary of each category

3. **Vesting Schedule**
   - Filtered to show only unvested shares
   - Sorted by next vesting date

4. **Venice Citizens**
   - Filtered to shareholder_type = "Venice Citizen"
   - Shows role and vesting status

5. **Investor Registry**
   - Shows all $COMPUTE and $UBC investors
   - Includes investment amounts

6. **Cap Table Export**
   - All fields for legal documentation
   - Sorted by percentage ownership

---

### 🔧 Automations to Set Up:

1. **Vesting Calculator**
   - Runs monthly
   - Updates vested_shares based on schedule

2. **Performance Check**
   - When company hits MRR milestones
   - Adjusts Universe Engine shares

3. **Lock-up Reminder**
   - 30 days before lock-up ends
   - Notifies shareholders

4. **New Share Issue**
   - Creates transaction record
   - Sends confirmation email

---

### 📋 Initial Data Load Example:

```csv
shareholder_name,shareholder_type,company,shares_owned,acquisition_type,vesting_schedule,citizen_role
Universe Engine,Universe Engine,Venice Trading Intelligence Co.,250000,Infrastructure Contribution,Performance-based,N/A
CryptoContarini,Venice Citizen,Venice Trading Intelligence Co.,50000,Apport en Nature,2 years monthly,Lead Trader
Foscari_Banker,Venice Citizen,Venice Trading Intelligence Co.,50000,Apport en Nature,2 years monthly,Lead Analyst
Kin Kong Investor Pool,$COMPUTE Investor,Venice Trading Intelligence Co.,133333,$COMPUTE Conversion,Immediate,N/A
$UBC Investment Pool,$UBC Investor,Venice Trading Intelligence Co.,100000,$UBC Investment,3 months,N/A
UBC Circle,Management,Venice Trading Intelligence Co.,100000,Management Grant,4 years monthly,N/A
```

This schema provides complete equity tracking with vesting, performance scaling, and full audit trail!