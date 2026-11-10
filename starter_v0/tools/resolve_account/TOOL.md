---
name: resolve_account
track: core
kind: local_knowledge
provider: Sourced local account directory
requires_env: []
inputs: [name]
outputs: [status, candidates, lookup_source, live_verified]
side_effect: false
---
# resolve_account

Reads `data/accounts.json` and matches names, aliases or handles. Returns found,
ambiguous or not_found. A directory hit does not prove current account ownership;
each candidate retains its verification provenance and source URL. Unknown names
are not turned into guessed usernames. To extend the directory, add a name,
aliases, screenname without @, source URL and verification details.
