# Network Planner

## Feature
- Calculate subnets with prefix from parent CIDR.
- Audit the number of total addresses from CIDR, and return its host addresses if their number is less than 64.
- Check if the default route points IGW. Expect the format from Azure.
- Save as timestamped JSON.

## Reference
- [Aamazon Virtual Private Cloud - User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html): Can change the valuation logic based on this guide. Don't use it this time because the project is for Azure.
- [Microsoft Learn - Azure - Microsoft.Network - routeTables/routes](https://learn.microsoft.com/en-us/azure/templates/microsoft.network/routetables/routes?pivots=deployment-language-arm-template): Check "addressPrefix" and "nextHopType" for inspecting default route.