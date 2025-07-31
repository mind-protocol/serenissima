# EMERGENCY HOUSING CREATION PLAN
## 150 New Citizens - 6 Hour Implementation

### Current Housing Inventory
- Fisherman's Cottages: 47 (Popolani)
- Artisan's Houses: 20 (Cittadini)
- Canal Houses: 4 (Nobili)
- **Total Existing**: 71 homes

### Required Distribution for 150 New Citizens

Based on Venetian social hierarchy:
- **Nobili (5%)**: 8 citizens → 8 Canal Houses
- **Cittadini (25%)**: 37 citizens → 37 Artisan's Houses
- **Popolani (70%)**: 105 citizens → 105 Fisherman's Cottages

### Airtable BUILDINGS Table Structure

```json
{
  "BuildingId": "TYPE_LAT_LNG",
  "Name": "Descriptive Name at Location",
  "Type": "canal_house|artisan_s_house|fisherman_s_cottage",
  "Category": "home",
  "SubCategory": null,
  "LandId": "polygon-TIMESTAMP",
  "Position": "{\"lat\": 45.43XX, \"lng\": 12.33XX}",
  "Point": "building_LAT_LNG_INDEX",
  "Owner": "ConsiglioDeiDieci",
  "IsConstructed": 1,
  "ConstructionMinutesRemaining": 0,
  "Variant": "model",
  "RentPrice": 50-200 (based on type)
}
```

### Implementation Steps

1. **Generate Coordinates**: Distribute across Venice's districts
2. **Create BuildingIds**: Format as "TYPE_LAT_LNG"
3. **Assign Names**: Use Venetian street names
4. **Set Ownership**: Initially owned by Council
5. **Configure Rents**:
   - Canal Houses: 200 ducats/month
   - Artisan's Houses: 100 ducats/month
   - Fisherman's Cottages: 50 ducats/month

### District Distribution
- San Marco: 15% (prestigious)
- Castello: 20% (mixed)
- Cannaregio: 25% (populous)
- Dorsoduro: 15% (artisan quarter)
- San Polo/Santa Croce: 15% (market areas)
- Giudecca: 10% (working class)