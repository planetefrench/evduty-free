



# evdutyfree
 Unofficial Python Module interface for EVduty chargers api

 ⚠️Warning - Very ALPHA and not ready for production. ⚠️


Loosely based on https://github.com/cliviu74/wallbox.

## Example

```
from evdutyfree import EVdutyFree

w = EVdutyFree("user@domain.com", "password")

# Authenticate with the credentials above
w.authenticate()
stations = w.get_station_ids()
terminals = w.get_terminal_ids(stations[0])

terminalinfo = w.get_terminal_info(stations[0],terminals[0])

print(w.get_max_charging_current(stations[0],terminals[0]))
w.set_max_charging_current(stations[0], terminals[0], 30)
print(w.get_max_charging_current(stations[0],terminals[0]))
```