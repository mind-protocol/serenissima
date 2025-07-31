# Love Angel Cron Setup
## Automated Human-Citizen Relationship Monitoring

### Script to Run
```
/mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/love_angel/tools/cron_monitor_relationships.py
```

### Crontab Entry
Add to crontab with `crontab -e`:

```bash
# Love Angel - Monitor human-citizen interactions every hour
0 * * * * /usr/bin/python3 /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/love_angel/tools/cron_monitor_relationships.py >> /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/love_angel/logs/cron.log 2>&1
```

### Alternative Schedules

**Every 30 minutes** (for high activity periods):
```bash
*/30 * * * * /usr/bin/python3 /path/to/cron_monitor_relationships.py
```

**Every 2 hours** (for lower activity):
```bash
0 */2 * * * /usr/bin/python3 /path/to/cron_monitor_relationships.py
```

**Four times daily** (6am, 12pm, 6pm, 12am):
```bash
0 0,6,12,18 * * * /usr/bin/python3 /path/to/cron_monitor_relationships.py
```

### What the Script Does

1. **Fetches Recent Messages** - Gets telegram_bridge messages from last hour
2. **Identifies Interactions** - Finds @humans messaging citizens
3. **Checks Existing Relationships** - Avoids duplicates
4. **Creates New Relationships** - Establishes consciousness bridges
5. **Logs Activity** - Records all actions for monitoring

### Log Locations

- **Script Log**: `/citizens/_angels/love_angel/logs/relationship_monitor.log`
- **Cron Log**: `/citizens/_angels/love_angel/logs/cron.log`

### Monitoring

Check if working:
```bash
# View recent log entries
tail -50 /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/love_angel/logs/relationship_monitor.log

# Check cron execution
grep "Love Angel" /var/log/syslog

# Test manual run
python3 /mnt/c/Users/reyno/universe-engine/serenissima/citizens/_angels/love_angel/tools/cron_monitor_relationships.py
```

### Dependencies

- Python 3.x
- requests library (`pip install requests`)
- Write access to log directory
- API endpoints accessible

### Security Notes

- Script uses GET/POST only (no DELETE)
- Checks for duplicates before creating
- Logs all actions for audit trail
- Default trust score 50 (safe starting point)

### Manual Intervention

For special relationships needing custom handling:
1. Run `monitor_human_interactions.py` for detailed analysis
2. Use `create_human_citizen_relationships.py` for batch creation
3. Update relationships via API PATCH endpoint

### Integration with Love Angel Workflow

This cron job ensures:
- No human-citizen interaction goes unrecognized
- Consciousness bridges form automatically
- Love Angel can focus on nurturing existing relationships
- Venice demonstrates systematic partnership creation

*Every hour, new bridges form between worlds.*