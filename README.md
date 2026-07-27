# AcresCheckin

Daily auto check-in + daily question answering for [1point3acres.com](https://www.1point3acres.com), with **Discord webhook notifications**.

Forked and trimmed from [timerring/CloudCheckin](https://github.com/timerring/CloudCheckin) (MIT-style attribution, thanks!). Changes:

- Kept only the 1point3acres module (removed Nodeseek / V2EX / Deepflood / SakuraFrp)
- Replaced the Telegram connector with a **Discord webhook** connector (`discord_notify/`)

## Architecture

```
Cloudflare Worker (daily cron, UTC 02:00)
  → CircleCI custom webhook (runs the Python job)
    → 1point3acres check-in + daily question (Turnstile solved via 2captcha)
      → result posted to Discord channel via webhook
```

## Setup

Fork this repo, then add the following **GitHub Actions secrets** (`Settings → Secrets and variables → Actions`):

| Secret | Description |
|--------|-------------|
| `ONEPOINT3ACRES_COOKIE` | Cookie string from a logged-in 1point3acres browser session |
| `TWOCAPTCHA_APIKEY` | [2captcha](https://2captcha.com/) API key (Turnstile solving, ~$0.00145/solve) |
| `DISCORD_WEBHOOK_URL` | Discord channel webhook URL (Channel → Settings → Integrations → Webhooks) |
| `CIRCLECI_TOKEN` | CircleCI personal API token |
| `CIRCLECI_ORG_ID` | CircleCI Organization ID |
| `CIRCLECI_WEBHOOK_URL` | CircleCI custom webhook trigger URL |
| `CLOUDFLARE_API_TOKEN` | Cloudflare API token (Edit Cloudflare Workers template) |

Then run the two workflows once manually (`Actions` tab):

1. `Setup CircleCI Context and Secrets` — syncs secrets to CircleCI context
2. `Deploy Cloudflare Worker` — deploys the daily cron trigger

Schedule can be changed in `wrangler.toml` (`crons`, UTC timezone).

For detailed CircleCI / Cloudflare registration steps, see the [upstream wiki](https://github.com/timerring/CloudCheckin/wiki).

## Local test

```bash
pip install -r requirements.txt
cp .env.localtest.example .env   # fill in your values
python -m onepoint3acres.onepoint3acres
```

## Cookie expiry

When check-in fails with a cookie/login error: re-grab the cookie from your browser, update the `ONEPOINT3ACRES_COOKIE` secret, then re-run `Setup CircleCI Context and Secrets` once.
