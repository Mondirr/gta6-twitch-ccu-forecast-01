# GTA VI Twitch CCU Forecast

[![make.fun](https://make.fun/badge/gta6-twitch-ccu-forecast-01.svg)](https://make.fun/c/gta6-twitch-ccu-forecast-01?ref=z206rnhh)
[![rank](https://make.fun/badge/gta6-twitch-ccu-forecast-01/rank.svg)](https://make.fun/c/gta6-twitch-ccu-forecast-01?ref=z206rnhh)
[![reward](https://make.fun/badge/gta6-twitch-ccu-forecast-01/reward.svg)](https://make.fun/c/gta6-twitch-ccu-forecast-01?ref=z206rnhh)

Entry for [gta6-twitch-ccu-forecast-01](https://make.fun/c/gta6-twitch-ccu-forecast-01?ref=z206rnhh): forecasts GTA VI launch-day Twitch concurrent viewers, hours 2-24, from hour 1's print and the launch curves of comparable games in the case file.

`main.py` reads each case, builds log-ratio curves from the comparables, and writes empirical quantiles anchored on hour 1, with a persistence fallback when too few curves are usable. Standard library only, deterministic, no network, no model calls.
