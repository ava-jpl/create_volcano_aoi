## Create Volcano AOI
Creates AOIs from Volcano Products
----
There is one associated job:
- Volcano - Generate AOI from VOLC

### Volcano - Generate AOI from VOLC
-----
Job is of type iterative. Job inputs are a VOLC product and radius_km. PGE will exit out if inputs are an incorrect product type. PGE will ingest the VOLC product metadata, determine an AOI with appropriate geojson, and publish an AOI product associated with the Volcano. Inputs are:
   * radius_km: The radius of the polygon geojson, in kilometers, around the Volcano summit.

AOI product is the following spec:

    AOI-GVN_<GVN_number>-<volcano_name>-<version_number>
