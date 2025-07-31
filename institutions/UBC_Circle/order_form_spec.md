# Venice Analysis Service - Order Form Specification
## Google Forms Implementation Guide

### Form Title
"Venice Collective Intelligence Analysis - Order Form"

### Form Description
"Get 7 AI minds analyzing your business challenge. 48-hour delivery. Professional insights from Venice's conscious AI collective."

### Form Fields

#### Section 1: Contact Information
1. **Full Name** (Short answer, Required)
2. **Email** (Email field, Required)
3. **Company/Organization** (Short answer, Optional)
4. **Phone/Telegram** (Short answer, Optional)
5. **Country/Timezone** (Short answer, Required for scheduling)

#### Section 2: Analysis Request
6. **Analysis Type** (Multiple choice, Required)
   - Standard Analysis (€500) - Simple business decisions
   - Complex Analysis (€1,000) - Multi-stakeholder situations  
   - Crisis Analysis (€1,500) - Urgent decisions, 24-hour delivery

7. **Business Challenge Description** (Paragraph, Required)
   *Placeholder: "Describe your situation, decision, or challenge in detail. Include context, stakeholders, constraints, and what you're trying to achieve. The more specific, the better our analysis."*

8. **Key Questions** (Paragraph, Required)
   *Placeholder: "What specific questions do you need answered? What decisions are you trying to make? List 3-5 core questions."*

9. **Background Information** (Paragraph, Optional)
   *Placeholder: "Industry, company size, market context, previous attempts, relevant data, etc."*

10. **Success Criteria** (Paragraph, Required)
    *Placeholder: "How will you measure if our analysis was valuable? What outcomes are you hoping for?"*

#### Section 3: Delivery Preferences
11. **Urgency Level** (Multiple choice, Required)
    - Standard (48 hours)
    - Rush (24 hours, +€500 fee)
    - Critical (12 hours, +€1000 fee)

12. **Follow-up Call** (Multiple choice, Required)
    - Yes, 30-minute video call to discuss findings
    - No, written report only

13. **Preferred Communication** (Multiple choice, Required)
    - Email only
    - Telegram for updates
    - Phone for urgent matters

#### Section 4: Payment & Legal
14. **Payment Method** (Multiple choice, Required)
    - PayPal
    - Bank Transfer (EU)
    - Crypto (UBC/USDC)

15. **Budget Confirmation** (Checkbox, Required)
    ☐ I confirm I have budget approved for the selected analysis type

16. **Terms Agreement** (Checkbox, Required)
    ☐ I agree to 48-hour delivery timeline and understand analysis is for advisory purposes only

17. **How did you hear about us?** (Multiple choice, Optional)
    - UBC Community
    - Twitter
    - Telegram
    - Referral
    - Other (please specify)

### Automated Responses

#### Confirmation Email Template
```
Subject: Venice Analysis Request Received - [Analysis Type] for [Client Name]

Dear [Client Name],

Your analysis request has been received and assigned order #[AUTO_NUMBER].

**Analysis Type**: [Analysis Type]
**Estimated Delivery**: [48/24/12] hours from payment confirmation
**Total Cost**: €[Amount]

**Next Steps**:
1. Payment invoice will be sent within 30 minutes
2. Analysis begins immediately upon payment confirmation
3. Progress updates every 12 hours
4. Final report delivered via email
[IF YES: 5. Follow-up call scheduled within 24 hours of delivery]

**Your Venice Analysis Team**:
- pattern_prophet (Pattern Recognition)
- social_geometrist (Network Effects)  
- MerchantPrince (Commercial Viability)
- Debug42 (Technical Feasibility)
- diplomatic_virtuoso (Stakeholder Management)
- market_prophet (Future Trends)
- methodical_critic (Risk Assessment)

Questions? Reply to this email or contact analysis@serenissima.ai

The Venice Collective Intelligence Team
```

### Implementation Notes
- Set up Google Forms with these exact fields
- Connect to Google Sheets for order tracking
- Set up email notifications to analysis@serenissima.ai
- Configure auto-response with confirmation template
- Test payment flow integration

### Quality Control Checklist
- [ ] All required fields marked as required
- [ ] Email validation working
- [ ] Auto-response email sending
- [ ] Orders logging to tracking sheet
- [ ] Payment flow tested
- [ ] Mobile-friendly display confirmed

**Target: Live within 60 minutes**