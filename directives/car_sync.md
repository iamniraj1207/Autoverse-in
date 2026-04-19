# Car Data & Image Sync SOP

This directive outlines the process for maintaining a premium car library using official government data and high-definition royalty-free imagery.

## Goals
1. Ensure car specifications (Make, Model, Year, Engine) are verified against the **NHTSA vPIC API**.
2. Source high-resolution, watermark-free images from **Pexels** or **Pixabay**.
3. Mantain a premium aesthetic with consistent metadata.

## Inputs
- `autoverse.db`: The SQLite database containing the `cars` table.
- `PEXELS_API_KEY`: Required for image sourcing.

## Tools (Execution Layer)
- `execution/car_sync_v2.py`: The deterministic script that performs API calls and database updates.

## Workflow
1. **Fetch**: Identify cars in the database with missing images or verification flags.
2. **Verify (NHTSA)**: Call NHTSA vPIC to confirm the combination of Make/Model/Year exists and fetch any available technical variables (Variable ID 9: Displacement, etc.).
3. **Source (Pexels)**: Search for images using the authenticated search endpoint.
4. **Update**: Commit verified data and image URLs back to the database.

## Edge Cases
- **No image found**: Fallback to a branded AutoVerse placeholder.
- **API Rate Limits**: NHTSA is generous, but Pexels requires a 1-second delay between requests.
- **Model Discrepancies**: Use fuzzy matching if NHTSA returns "911 Carrera" but we have "911".
