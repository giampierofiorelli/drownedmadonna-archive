# DrownedMadonna archive

Recovery of the earlier versions of drownedmadonna.com (Joomla and WordPress eras) from the Wayback Machine.

## Steps

1. **Inventory** — `scripts/inventory.py` lists every URL archive.org holds for the domain.
   Output: `inventory/urls.csv` and `inventory/SUMMARY.md`.
   Runs automatically through the "Wayback inventory" GitHub Action.
2. **Download** — fetch the original HTML, images, CSS and JS of each archived URL (planned).
3. **Extract** — turn articles into clean structured files ready to import into the current CMS (planned).
