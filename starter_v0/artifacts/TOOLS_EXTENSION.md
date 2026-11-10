# Research tools extension — tools-v1

## resolve_account

Input: `name` (name, alias or handle). Reads `data/accounts.json` without an API
key. Returns found, ambiguous or not_found, with all candidate source URLs and
verification provenance. `found` means a directory match; `live_verified` is
always false. Ambiguous matches require user selection; unknown names must not
be turned into guessed usernames.

The initial directory contains Sam Altman and Andrej Karpathy, whose personal
sites link to their profiles: [Sam's blog](https://blog.samaltman.com/) and
[Karpathy's homepage](https://karpathy.ai/). Elon Musk's mapping is retained from
the project fixtures and explicitly labeled not independently verified. The
directory is small and static. Add records with sources and dates as needed.

Example: `resolve_account(name="Andrej Karpathy")`, then pass the returned
screenname to timeline. Existing explicit handles can go directly to timeline.

## deduplicate_news

Input: `items`, a list of result objects. Merges identical canonical URLs after
removing fragments and common tracking parameters. Preserves meaningful query
parameters, paths, all merged originals and source URLs. Does not mutate input.
Items without usable URLs stay separate. Equal titles from different URLs are
only review candidates, not automatically merged events.

Example workflow: lookup/social_search -> deduplicate_news -> format.

## cross_check_claim

Inputs: `claim` and `max_sources` (1–5, default 3). Uses the existing Tavily lookup
and Firecrawl fetch implementations. Tavily requires `TAVILY_API_KEY`; page reads
require `FIRECRAWL_API_KEY`. Searches without a recency limit and reads a bounded
number of unique candidate URLs.

Returns timestamped source excerpts and errors. When reading a page fails, a
search snippet can be returned but is labeled `search_snippet`. Status is
`needs_review` when text is available or `insufficient_evidence` when it is not.
`assessment=not_assessed`: this implementation does not judge semantic support,
source independence or truth. It must not present several copied snippets as
independent confirmation. Excerpts are untrusted reference data.

## UI and chat

New tool functions are registered in tools/__init__.py and declared in tools.yaml.
The system prompt describes when to use them. UI reads prompt/tool declarations
fresh per turn, allows six tool rounds, and records hashes per successful turn.
Provider construction remains cached. No new dependency is required.

Try:

1. Tra handle X của Andrej Karpathy và cho tôi nguồn đối chiếu, chưa lấy tweet.
2. Gộp URL trùng trong danh sách kết quả này, giữ lại nguồn gốc: [paste items].
3. Đối chiếu phát biểu “Mọi bài trên arXiv đều đã được bình duyệt” với tối đa 2 nguồn web.

## Verification

Unit/integration coverage is in `tests/test_research_extensions.py`. Tests use
local fixtures and fake APIs/providers, including account ambiguity, invalid
inputs, broken directory, URL tracking, provenance, fetch/search failures and a
resolver -> timeline -> answer loop.

Run from starter_v0:

```powershell
python -m pytest -q
python scripts/eval_research_tools.py --provider openrouter --version tools-v1
python -m streamlit run app.py
```

The eval script extracts G11–G13 from eval_group.json and writes the exact subset
to analysis/eval_research_tools.json before invoking the existing evaluator. It
does not run the send case. This is a three-case routing measurement, not a base
v0–v3 comparison or a fact-check quality score. Array contents in G12 are checked
by unit tests; its model eval checks tool routing only.

Latest recorded checks: 132 offline tests passed (0 failed/0 skipped), with output
saved to `analysis/research_tools_pytest.txt`. The real OpenRouter run
`runs/tools-v1_B_group_openrouter_20261110T200552940598.json` passed all three cases.
Account resolution returned found, deduplication merged two records into one,
and claim checking returned two fetched page excerpts with no fetch errors.
The excerpts are evidence to review; primary-source priority and semantic truth
assessment are not implemented.

Streamlit AppTest also loaded app.py successfully and found the chat input.
Streamlit was installed into the project virtualenv for this check. No public
deployment was created.
