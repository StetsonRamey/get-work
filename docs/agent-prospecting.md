# Agent prospecting playbook

How an agent turns *"find me holiday lighting companies in «CITY, ST» and build out prospects"* into finished prospect folders + an updated summary table.

## 1. Search

Web-search for the target market. Good queries:

- `christmas light installation «city state»`
- `holiday lighting company «city»`
- `professional christmas light installers «city»`

Selection criteria:

- **Local operators** with their own website (not lead-gen directories, not Angi/Thumbtack/Yelp listings, not national franchise corporate pages — a local franchisee with its own site is OK but note it).
- Active business: real service pages, phone number, service area matching the target city.
- Not already in `outreach/prospects/` (check slugs and `**Website:**` lines in notes.md).
- Aim for 3–8 solid prospects per city rather than a long junk list.

## 2. Scrape & qualify

```bash
./getwork scrape https://example-lights.com/
```

Extracts emails (mailto + text), phones, possible owner names, contact-form URLs, service keywords, social links from the homepage + contact/about pages. Use it to qualify: if there is no email and no contact form, the prospect is low value — note it but deprioritize.

If the scraper comes up empty (JS-heavy site), fall back to the browser tool: load the site, read the contact page, and capture info manually.

## 3. Build the prospect folder

```bash
./getwork build-prospect tulsalights "Tulsa Holiday Lights" https://tulsaholidaylights.com/ --location "Tulsa, OK"
```

Creates `outreach/prospects/<slug>/` with:

- `portfolio.html` — holiday-lighting prospect sheet from the base template
- `email.md` — email variant template
- `notes.md` — research/contact sections pre-filled from the scrape
- `scrape.json` — raw scrape data for review

and regenerates `outreach/summary.html` + `outreach/index.html`.

## 4. Enrich

Open the site (browser tool if needed) and finish notes.md:

- Residential vs commercial focus
- Current quote/contact process observed
- Personalized opening line + why the workflows are relevant (routing for big service areas, renewals for contract-based companies, etc.)
- Verify the chosen contact email/person — prefer an owner's direct address over info@.

## 5. Draft the email

Write `outreach/prospects/<slug>/email-draft.md`. Match the voice of existing drafts (`outreach/prospects/holiglows/email-draft.md`). Positioning and credibility numbers: `docs/holiday-lighting-handoff.md`. Then in notes.md Send log set:

```
- Email drafted: YYYY-MM-DD
```

Optionally bump `**Status:** ready`.

## 6. Summary & wrap-up

```bash
./getwork summary
```

Commit the new prospect folders. Report to Stetson: companies found, contact quality, anything that needs manual review. He reviews everything via the preview (`make dev` → directory → "Prospect summary table"), sends emails manually, and records `Email sent:` dates himself.

## Status lifecycle

| Status   | Meaning                              | Who sets it |
|----------|--------------------------------------|-------------|
| drafting | folder built, email not done         | build-prospect |
| ready    | email-draft.md written, ready to send| agent |
| sent     | email sent (`Email sent:` filled)    | Stetson |
| replied  | got a response                       | Stetson |
| dead     | not pursuing                         | Stetson |
