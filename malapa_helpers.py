"""Small shared helpers for the MaLAPA 2026 notebooks."""


def list_keys(obj, prefix=""):
    keys = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            full_key = f"{prefix}.{k}" if prefix else k
            keys.append(full_key)
            keys.extend(list_keys(v, full_key))
    elif isinstance(obj, list):
        if obj:  # Only analyze the first item if the list is not empty
            keys.extend(list_keys(obj[0], f"{prefix}[0]"))
    return keys


# The three roles a person can hold on a contribution.
PEOPLE_KEYS = ("speakers", "authors", "co_authors")


def iter_people(contribution):
    """Yield every person dict on a contribution (speakers, authors, co_authors).

    Skips missing/non-list role values and any non-dict entries, so callers can
    iterate over people without repeating those guards.
    """
    for key in PEOPLE_KEYS:
        people = contribution.get(key, [])
        if not isinstance(people, list):
            continue
        for person in people:
            if isinstance(person, dict):
                yield person


def first_speaker(contribution):
    """Return a contribution's first speaker (dict), or None.

    The bar chart, world map, and per-institution counts attribute each
    contribution to this speaker's institution / country / species.
    """
    speakers = contribution.get("speakers", [])
    if speakers and isinstance(speakers[0], dict):
        return speakers[0]
    return None
