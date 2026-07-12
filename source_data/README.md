# Source data

Input files for the MaLAPA 2026 notebooks, checked in so everything runs out of
the box. These have **mixed provenance** — some were scraped from the event's
[Indico page](https://indico.rcnp.osaka-u.ac.jp/event/2676/), one was generated
with Claude, and one was standardized by hand — so each file is documented below.

## Files

### `contributions.json`
The main dataset: a list of **94** contributions (talks and posters). Each entry
has `submission_number`, `id`, `url`, `title`, `speakers`, `authors`,
`co_authors`, `description`, and `presentation_materials`.
- **Provenance:** scraped from the event's Indico website.
- **Used by:** `step_1_prepare_data.ipynb`.

### `poster_submission_numbers.json`
A list of **62** `{submission_number, type}` records marking which submissions
are posters (everything not listed here is a talk).
- **Provenance:** scraped from the event's Indico website.
- **Used by:** `step_1_prepare_data.ipynb`.

### `manual_to_standard_institutions_dictionary.json`
A lookup mapping each institution's raw name (as typed by submitters) to its
`{inst, country}` (**98** entries) — a best-effort, hand-built standardization of
the free-text institution names in the contributions. `country` is the full name
(e.g. `United States`), matching `institution_locations.json`.
- **Provenance:** compiled manually (best-effort name standardization).
- **Used by:** `step_1_prepare_data.ipynb`.

### `institution_locations.json`
A list of **52** institutions enriched with geographic and display metadata:
`institution`, `inst` (abbreviation), `country`, `country_iso3`, `city`,
`latitude`, `longitude`, `label`, `label_short`, and `species`.
- **Provenance:** generated with Claude.
- **Used by:** the world map in `step_2_explore_contributions.ipynb`.

### `group_photo.jpeg`
Group photo from the workshop, shown at the top of the repo's main `README.md`.
- **Provenance:** taken from the event's website.
- **Used by:** the top-level `README.md` (not the notebooks).

## Key glossary

What each key holds and what it describes. See the **cross-file notes** at the end
for how the institution keys line up across files.

### `contributions.json` (list of contribution objects)

| Key | Type | Describes |
| --- | --- | --- |
| `submission_number` | int | The contribution's submission number. **Join key** to `poster_submission_numbers.json`. |
| `id` | str | Indico's internal contribution id (the number in `url`). A *different* identifier from `submission_number`. |
| `url` | str | Link to the contribution's Indico page. |
| `title` | str | Contribution title. |
| `speakers`, `authors`, `co_authors` | list of person objects | The people on the contribution, by role. |
| `description` | str | Abstract text. |
| `presentation_materials` | list | Uploaded files, each `{filename, url}`. Often empty. |

Person object (inside `speakers` / `authors` / `co_authors`):

| Key | Type | Describes |
| --- | --- | --- |
| `name` | str | The person's name. |
| `manual_institution` | str | Their affiliation **as typed by the submitter** — raw, free-text, inconsistent. Matched against the keys of `manual_to_standard_institutions_dictionary.json`. |

### `poster_submission_numbers.json` (list)

| Key | Type | Describes |
| --- | --- | --- |
| `submission_number` | int | References a contribution's `submission_number`. |
| `type` | str | Always `"poster"`. Presence in this list is what marks a contribution as a poster. |

### `manual_to_standard_institutions_dictionary.json` (dict keyed by raw institution name)

| Key | Type | Describes |
| --- | --- | --- |
| *(dict key)* | str | A raw institution string, exactly as it appears in `manual_institution` in `contributions.json` — this is the matching key. |
| `inst` | str | Short institution code, e.g. `BNL`, `UTokyo`. |
| `country` | str | The institution's country, full name (e.g. `United States`). |

### `institution_locations.json` (list)

| Key | Type | Describes |
| --- | --- | --- |
| `institution` | str | **Canonical** institution name, e.g. `University of Tokyo`. |
| `inst` | str | Short institution code, e.g. `UTokyo`. |
| `country` | str | Country, **full name**, e.g. `United Kingdom`. |
| `country_iso3` | str | ISO 3166-1 alpha-3 code, e.g. `GBR`. |
| `city` | str | City. |
| `latitude`, `longitude` | float | Coordinates, used by the map. |
| `label` | str | Hover text: `"{institution}, {city}, {country}"`. |
| `label_short` | str | Short hover text: `"{inst}, {city}, {country_iso3}"`. |
| `species` | str | `electrons` or `hadrons` — the accelerator particle type, assigned one per institution (a Claude-generated simplification). |

### Cross-file notes

The institution keys are now consistent across files (they used to disagree):

- **`inst` and `country` mean the same thing everywhere.** The short code is
  `inst`, and `country` is a full name, in both
  `manual_to_standard_institutions_dictionary.json` and
  `institution_locations.json` (and in the step-1 enriched people). Countries
  join cleanly — no `UK`/`USA` vs `United Kingdom`/`United States` mismatch.
- **Raw vs canonical institution names are distinctly named.**
  `manual_institution` (in `contributions.json`, and the *keys* of
  `manual_to_standard_institutions_dictionary.json`) is the raw, submitter-typed
  affiliation (messy, e.g.
  `"Deutsches Elektronen Synchrotron Desy, Hamburg, Germany"`). `institution` (in
  `institution_locations.json`) is the cleaned canonical name
  (`"University of Tokyo"`). Different keys, no collision.

Still worth knowing:

- **Two identifiers in `contributions.json`.** `submission_number` (int, the join
  key to `poster_submission_numbers.json`) and `id` (str, Indico's internal id)
  are distinct — different types, don't cross them.
- **`type` is poster-only here.** In `poster_submission_numbers.json`, `type` is
  always `"poster"`; the `"oral"` value only appears once step 1 adds `type` to
  every contribution.
