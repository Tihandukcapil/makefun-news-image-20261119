# makefun-news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Tihandukcapil/makefun-news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/Tihandukcapil/makefun-news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A newspaper front page summing up Thursday 19 November 2026 in 40 stories — every one of them happened, or was first reported, on that day. The three lead stories are the first-ever Trump–Xi–Putin three-way summit in Shenzhen and its Declaration toward Peace; the UN International Court of Justice ruling, 9–6, that Myanmar committed genocide against the Rohingya; and Anthropic starting trading on Nasdaq after the biggest IPO on record ($81.3bn at $83 a share, opening at $111.50). Around them: GTA VI's midnight launch after 13 years, the COP31 draft dropping fossil fuels and the $120bn adaptation goal, Cyclone Akvan bearing down on Odisha, a Houthi missile striking Riyadh's PIF Tower, Ukraine hitting the Crimea bridge again, half a million Koreans sitting the Suneung, Denmark's 109–0 Arctic pact vote, Australia's jobless rate jumping to 4.9%, and 27 more stories from every continent — with a dotted world map, a number strip, and a DATE CHECK box that names the neighbouring days' news deliberately left out (the Qeshm strike of 17 Nov, the Kuwait/Bahrain drone interceptions of 18 Nov, Anthropic's $83 pricing of 18 Nov). The whole page — masthead, panels, map, text — is drawn in code by `compose.py` (PIL, DejaVu fonts); `main.py` (Python 3.13, standard library only) copies the bundled `entry.png` to `/output/entry.png`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=ks2r30ft&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
