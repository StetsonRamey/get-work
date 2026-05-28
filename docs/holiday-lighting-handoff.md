# Holiday lighting prospect campaign — handoff

_Last updated: 2026-05-27_

## Current status

We created a new web-first prospect sheet campaign for local Denver-area holiday lighting companies.

Initial targets:

- Colorado Christmas Lights — `https://coloradochristmaslights.stetson.dev/`
- HoliGlows — `https://holiglows.stetson.dev/`
- Iceberg Christmas Lights — `https://icebergchristmaslights.stetson.dev/`

The pages are currently built as HTML files under `outreach/prospects/*/portfolio.html`. They are previewable via the preview server, but production custom-domain serving has **not** been changed yet.

## Important positioning

Use this wording:

> I own and operate ’Tis the Season, a Kansas City holiday lighting company. In the off season, I build practical software systems for other holiday lighting companies — quoting, billing, customer texting, renewals, and routing.

Credibility metrics added:

- 900–1,000 ’Tis the Season customers served each holiday season by three owners plus seasonal installers
- 94% ’Tis the Season year-over-year customer return rate
- 220 new ’Tis the Season customers sold in our biggest new-sales season

Important local angle:

> I’m local to the Denver area, so I’m happy to schedule a call or meet in person.

## Files created/updated

Campaign docs:

- `docs/holiday-lighting-campaign.md` — campaign plan, video outlines, email templates
- `docs/holiday-lighting-handoff.md` — this handoff
- `docs/design-source.md` — notes that Kami source was archived

Base template:

- `outreach/base/holiday-lighting-prospect-base.html`

Scaffold script:

- `scripts/new-holiday-prospect.sh`

Prospect pages and notes:

- `outreach/prospects/coloradochristmaslights/portfolio.html`
- `outreach/prospects/coloradochristmaslights/notes.md`
- `outreach/prospects/coloradochristmaslights/email-draft.md`
- `outreach/prospects/holiglows/portfolio.html`
- `outreach/prospects/holiglows/notes.md`
- `outreach/prospects/holiglows/email-draft.md`
- `outreach/prospects/icebergchristmaslights/portfolio.html`
- `outreach/prospects/icebergchristmaslights/notes.md`
- `outreach/prospects/icebergchristmaslights/email-draft.md`

README updated with holiday prospect workflow:

- `README.md`

## Contact info wired in

Public contact info has been added to pages and email drafts:

- Email: `me@stetson.dev`
- Phone/text: `307-214-5159`
- Tel/sms link value: `+13072145159`

## Preview commands

From `/home/exedev/get-work`:

```bash
./scripts/preview.sh
```

Then open from outside the VM/browser:

```text
http://get-work.exe.xyz:8765/prospects/coloradochristmaslights/portfolio.html
http://get-work.exe.xyz:8765/prospects/holiglows/portfolio.html
http://get-work.exe.xyz:8765/prospects/icebergchristmaslights/portfolio.html
```

Use plain `http` for preview port `8765`.

If port 8765 is already in use:

```bash
pkill -f "SimpleHTTPRequestHandler"
./scripts/preview.sh
```

## Current page state

The pages have:

- custom company headline
- Stetson / ’Tis the Season positioning
- ’Tis the Season operating snapshot metrics
- company-specific hook section
- four workflow demo cards
- tool stack section
- email/text CTAs

Company-specific angles:

### Colorado Christmas Lights

Angle: routing and communication across a big Colorado footprint.

Emphasis:

- Boulder / Denver / Breckenridge
- larger commercial customers
- routing
- billing
- automated customer communication

### HoliGlows

Angle: quote experience, conversions, and Denver-area routing.

Emphasis:

- Denver metro + surrounding markets
- website/quote-flow conversion
- quote intake
- customer follow-up
- routing

### Iceberg Christmas Lights

Angle: strong customer service, made more repeatable.

Emphasis:

- they already look like a strong local operator
- good reviews/customer service
- not “your systems are broken”
- automate good processes so they happen reliably every time
- quote templates, routing, billing notifications, customer communication

## Remaining placeholders / blockers

The video buttons are intentionally still disabled:

```html
class="btn disabled"
href="#"
```

Need final video URLs for:

1. Quote workflow
2. New customer setup + billing
3. Returning customer renewal
4. Routing + dispatch

Once videos are recorded/uploaded:

1. Replace each `href="#"` with the right video URL.
2. Remove `disabled` from the video button classes.
3. Update the page checklist in each `notes.md`.

## Video outlines

Detailed video outlines live in:

```text
docs/holiday-lighting-campaign.md
```

Short version:

1. **Website Lead → Roofline Markup → Personalized Quote Email**
2. **Accepted Quote → Stripe, TextMagic, CompanyCam, and Payment Link**
3. **Annual Renewal Texts, Forms, Stripe Checkout, and Paid Status Sync**
4. **Paid Customers → Area-Based Routes → Crew Dispatch**

## Production serving caution

Do **not** globally change `serve.py` to serve HTML instead of PDFs.

Existing live domains like these currently serve PDFs and should not break:

- `acs.stetson.dev`
- `local-nerds.stetson.dev`
- possibly others

Current production server:

- `serve.py` runs on port `8000`
- it maps `<slug>.stetson.dev` to `outreach/prospects/<slug>/portfolio.pdf`

When ready to publish these HTML pages, make a targeted allowlist change only:

```python
HTML_PROSPECTS = {
    "coloradochristmaslights",
    "holiglows",
    "icebergchristmaslights",
}
```

Then serve `portfolio.html` only for those slugs, while keeping PDF behavior for all existing prospects.

Optional future behavior:

- `<slug>.stetson.dev/` → `portfolio.html` for allowlisted HTML prospects
- `<slug>.stetson.dev/pdf` → `portfolio.pdf` if needed
- all non-allowlisted prospects keep existing PDF behavior

## DNS / exe.dev reminder

For each custom domain:

```bash
./scripts/add-domain.sh coloradochristmaslights
./scripts/add-domain.sh holiglows
./scripts/add-domain.sh icebergchristmaslights
```

Then register domains with exe.dev:

```bash
ssh exe.dev domain add get-work coloradochristmaslights.stetson.dev
ssh exe.dev domain add get-work holiglows.stetson.dev
ssh exe.dev domain add get-work icebergchristmaslights.stetson.dev
```

Only do this when ready to publish.

## Next recommended session steps

1. Review pages visually again after refresh.
2. Record/upload the four videos.
3. Add video URLs and enable video buttons.
4. Optionally tighten email drafts after video links are live.
5. Add DNS/custom domains.
6. Make safe allowlist-only `serve.py` change for these three HTML prospects.
7. Send initial emails from the company-specific `email-draft.md` files.
