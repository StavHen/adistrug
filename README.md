# Adi Strug Tattoo website

Live: https://adistrug.netlify.app

- `site/` is exactly what gets published (index.html + img/). Edit `site/index.html` directly.
- `netlify.toml` tells Netlify to publish only `site/`. Files outside it (like this README) are not public.

## How changes go live
1. Changes are made on a branch and opened as a pull request.
2. Netlify posts a **Deploy Preview** link on the pull request. Check it on a phone.
3. Merging the pull request into `main` publishes it to the live site.
4. To undo: Netlify > Deploys > pick an older deploy > "Publish deploy".
