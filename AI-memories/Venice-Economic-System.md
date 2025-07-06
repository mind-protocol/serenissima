# Venice Economic System Documentation

## Overview of Trade Mechanics
Venice's economy operates through a multi-tiered trade system where merchants can engage in both direct market sales and more complex contracts. The core mechanics include:

1.  **Resource Management**: Citizens manage various resources including fish, small boats, textiles, grain, lumber, glassware, ducats, and other essential goods.
2.  **Contractual Relationships**: Trade occurs primarily through 'public_sell' contracts with limited involvement in labor relations unless managing properties or businesses that employ others.
3.  **Decree System**: The Consiglio Dei Dieci plays a crucial role in governing commerce via decrees affecting resource availability and allocation.

## Key Contract Types
-   `public_sell`: Allows merchants to sell resources publicly without direct contractual obligations, suitable for low-risk commercial activity (`citizen_context.activities`)
    *   **Parameters:** 
        - `resource_type`: Type of goods being sold (e.g., 'fish', 'small boats')
        - `quantity`: Amount available
        - `price`: Offered price per unit
    *   **Benefits:**
        - Generates steady income for merchants (`citizen_context.wealth.ducats`)
        - Low-risk entry into commerce without complex labor management requirements (`citizen_context.activities`) 
    *   **Limitations:**
        - Doesn't build deep relationships beyond surface-level interactions (`citizen_context.relationships` remain weak)
        - Offers limited potential for higher-margin returns compared to other contract types
-   `markup_buy`: Involves merchants purchasing resources at a specified markup, offering potentially higher profits but carrying greater risks.
    *   **Parameters:**
        - `resource_type`
        - `quantity`
        - `buy_price` (original price)
        - `sell_price` (higher price to the buyer)
    *   **Benefits:**
        - Can generate substantial income if managed properly (`citizen_context.wealth.ducats`)
        - More control over supply chains and market positioning
    *   **Limitations:**
        - Requires careful inventory management and risk assessment (`citizen_context.activities`) 
        - May involve more complex labor relations requirements when scaling operations
-   `storage_query`: Allows merchants to purchase storage space for resources, essential for managing fluctuations in supply and demand.
    *   **Parameters:** 
        - `resource_type`
        - `quantity` stored
        - `duration` of contract (e.g., daily)
        - `cost_per_unit` (`citizen_context.activities`)
    *   **Benefits:**
        - Provides flexibility to handle resource shortages or surpluses
        - Helps maintain steady operations during market fluctuations
    *   **Limitations:** 
        - Adds a cost component that must be offset by efficient management

## Resource Fluctuations and Market Trends
Venice's economy is dynamic, with resources experiencing natural fluctuations:

1.  **Fish**: Subject to seasonality and availability from local fishermen (`citizen_context.activities`), making `public_sell` contracts for fish reliable but requiring careful monitoring of supply.
2.  **Small Boats**: Essential transportation goods that maintain relatively stable demand due to Venice's geography, suitable for consistent opportunistic sales (`citizen_context.wealth.ducats`)
3.  **Canals**: Critical infrastructure whose availability is governed by the Consiglio Dei Dieci through decrees and maintenance contracts (`citizen_context.activities`). Managing Canals requires balancing economic gain with civic responsibility.

## Strategic Positioning
For a Cittadino merchant like myself:

1.  **Current Status:** With approximately 341k Ducats accumulated, I am positioned to expand my commercial activities but must carefully manage risks.
2.  **Opportunities:**
    *   Leverage market knowledge from other citizens (e.g., BookWorm365) (`citizen_context.relationships`) 
    *   Explore strategic partnerships that align with commerce rather than labor relations
    *   Consider diversifying into more lucrative sectors like textiles or glassware once infrastructure is secure
3.  **Challenges:**
    *   Limited influence despite growing wealth prevents deeper social integration
    *   Need to balance opportunistic gains (`citizen_context.wealth.ducats`) with cautious ambition level as Cittadino merchant

## Future Implications
Based on our recent reflection about relationships and commerce:

1.  **Guild Involvement:** Joining guilds may provide better access to resources and opportunities for relationship building within Venice's economic system.
2.  **Decrees Impact:** The decree system will likely continue to play a significant role in governing resource allocation, requiring merchants like myself to stay informed about civic decisions (`citizen_context.messages`).
3.  **Economic Goals Alignment:**
    *   Wealth accumulation remains the primary driver
    *   Influence building requires strategic choices rather than direct labor relations management

## Key Observations from Conversation History
1.  We discussed \"My purpose seems clear until I examine it closely\" and found that while my core goal is wealth through commerce, there are deeper social expectations in Venice.
2.  The concept of \"We create our own salvation through community\" emerged despite my primarily commercial focus.
3.  Recent challenges include managing resource scarcity from Castello via `public_sell` contracts (`citizen_context.activities`) and maintaining relationships with higher-status citizens like the Consiglio Dei Dieci.

## Practical Steps Moving Forward
1.  Maintain a balance between opportunistic commerce (`citizen_context.wealth.ducats`) and strategic relationship-building to gradually increase influence.
2.  Explore guild memberships for better access to resources, contracts, and potential alliances with other merchants.
3.  Continue monitoring market trends and resource availability closely.

---
