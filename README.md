# Adi Strug Tattoo website

Live: https://adistrug.netlify.app

- `site/` is exactly what gets published (index.html + img/). Edit `site/index.html` directly.
- `netlify.toml` tells Netlify to publish only `site/`. Files outside it (like this README) are not public.

## How changes go live
1. Changes are made on a branch and opened as a pull request.
2. Netlify posts a **Deploy Preview** link on the pull request. Check it on a phone.
3. Merging the pull request into `main` publishes it to the live site.
4. To undo: Netlify > Deploys > pick an older deploy > "Publish deploy".

## Security headers
`site/_headers` sets standard security headers, including a Content-Security-Policy.
When the real calendar is added (Firebase), its domains must be added to `connect-src`
(and `script-src` if its scripts load from a CDN), or the calendar will be blocked.

## This repository is public
It is public so Netlify's free plan builds previews for every change. Never commit
passwords, private keys, customer details or anything else that should stay private.
