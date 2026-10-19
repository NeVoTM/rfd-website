# Migrate rfd-website from Render to Cloudflare Pages

Render rewrite `/clip` → `/clip.html` is in [`_redirects`](../_redirects) at the site root (publish path `.`).

## Cloudflare Pages

1. [dash.cloudflare.com](https://dash.cloudflare.com/) → **Workers & Pages** → **Create** → **Pages** → **Connect to Git** → **`NeVoTM/rfd-website`**.
2. Build: **None** · Build command: *(empty)* · Output directory: **`/`**.
3. Deploy, then test `https://<project>.pages.dev/clip?id=…`.
4. **Custom domain `rfd.com`**: Pages → **Custom domains** → add `www.rfd.com` and apex if supported. Replace Render DNS (see [DEPLOY.md](../DEPLOY.md)) with Cloudflare’s CNAME targets.

## Turn off Render

Render → **rfd-website** → delete or suspend after DNS points to Pages and SSL is active.

Push to `main` on GitHub auto-deploys Pages (no Render hook needed).
