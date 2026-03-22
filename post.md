The average ML paper is 15 pages. The average time I spend deciding if it's worth reading? About 4 minutes of skimming the abstract and squinting at figures.

I decided to automate those 4 minutes.

skim is a CLI that takes any arxiv paper and generates either a jargon-free narrative ("story") or a structured technical summary ("deep") — complete with methodology, key results, and contributions.

skim -p 2603.10165 -t all

that's literally it. paper downloaded, summarized, saved.

why I actually built this:
→ I was copy-pasting PDFs into ChatGPT like 3x a week
→ my prompts kept getting lost between conversations
→ I kept regenerating the same summary because I forgot I already did it last Tuesday

so now it caches everything and I stop wasting API credits on papers I've already skimmed.

it's open source and you can install it in one line:
uv tool install git+https://github.com/dipta007/skim
