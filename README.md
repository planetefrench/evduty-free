# evdutyfree
 Unofficial Python Module interface for EVduty chargers api

Based on https://github.com/cliviu74/wallbox

## Example

```
from evdutyfree import EVdutyFree

w = EVdutyFree("user@domain.com", "password")

# Authenticate with the credentials above
w.authenticate()
stations = w.get_stations()
terminals = w.get_terminals(stations[0])

print(w.get_max_charging_current(stations[0],terminals[0]))
w.set_max_charging_current(stations[0], terminals[0], 30)
print(w.get_max_charging_current(stations[0],terminals[0]))
```