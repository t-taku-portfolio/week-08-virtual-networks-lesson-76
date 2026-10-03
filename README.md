# Network Planner

## Feature
- Calculate subnets with prefix from parent CIDR.
- Audit the number of total addresses from CIDR, and return its host addresses if their number is less than 64.
- Check if the default route points IGW. Expect the format from Azure.
- Save as timestamped JSON.

## To execute
- Install uv

- Run with uv
```bash
uv run python3 src/lesson76/network_planner.py
```

## Development
- Use [Pytest](https://github.com/pytest-dev/pytest) for implementing test.

## Reference
- [Microsoft Learn - Azure - Microsoft.Network - routeTables/routes](https://learn.microsoft.com/en-us/azure/templates/microsoft.network/routetables/routes?pivots=deployment-language-arm-template): Check "addressPrefix" and "nextHopType" for inspecting default route.