# Email Workflow Examples

Complete walkthrough of cold outreach with portfolio pages and automatic Fastmail drafts.

## Full Workflow Example: HoliGlows

### Step 1: Create New Prospect Folder

```bash
./scripts/new-prospect.sh holiglows "HoliGlows"
```

Creates:
```
outreach/prospects/holiglows/
├── portfolio.html          (copy of portfolio-base.html)
├── email.md                (copy of base template with 2 variants)
├── notes.md                (template with fields to fill)
└── assets/
    └── headshot.jpg        (symlink to base headshot)
```

### Step 2: Research & Fill Notes

Edit `outreach/prospects/holiglows/notes.md`:

```markdown
# HoliGlows

**Status:** researching
**Date:** 2026-06-09
**Website:** https://www.holiglows.com/

## Company research

- Location: Denver Metro area
- Services: Residential and small commercial
- Notable: 3-5 year contracts
- Website has contact form

## Contact info

- Contact person: Anvar Batirov
- Contact email: anvar@holiglows.com
- Contact phone: 720-940-4562

## Personalization

- Custom angle: Their website has UX friction — could improve quote/contact flow
- Why relevant: Denver area means routing optimization is critical

## Page checklist

- [x] Contact info added
- [ ] Customize portfolio.html if needed
- [ ] Build PDF

## Send log

- [ ] Initial email sent:
- Variant used:
```

### Step 3: Customize Portfolio (HTML/PDF)

Edit `outreach/prospects/holiglows/portfolio.html`:
- Change company name references
- Customize the hook/opening
- Update dates

```bash
./scripts/build.sh outreach/prospects/holiglows/portfolio.html
```

### Step 4: Pick an Email Variant

`outreach/prospects/holiglows/email.md` is copied from `outreach/base/email-template.md` when the prospect is created. It contains the two variants we are testing:

```markdown
## Initial Email Variant 1

**To:** {CONTACT_NAME}
**Subject:** How many hours did you spending routing your customers last season?

Hey {CONTACT_NAME},

Does it take you more than a few hours to plan and route all your customers, or bill them?  Is chasing payments on invoices challenging?

I run a holiday lighting company too ([Tis the Season](https://tistheseasonkc.com) in Kansas City).  I had trouble in those areas, so I built some software that automates as much as possible - routing, billing, customer texts, everything.

Here are a few short videos showing how it works for us: {PORTFOLIO_URL}

I build this type of custom tooling for other lighting companies now too.  Take a look if interested, reply "get lost" if not and I'm gone.

-- Stetson

## Initial Email Variant 2

**To:** {CONTACT_NAME}
**Subject:** How I run my lighting company on software I built myself

Hey {CONTACT_NAME} — I run a holiday lighting company too ([Tis the Season](https://tistheseasonkc.com) in Kansas City).  I'm guessing your Oct–Dec looks like mine: 60 to 70 days of chaos.

Over the last 5 years I got tired of Zapier, spreadsheets, and other tools I only needed for one specific thing. So I built real software we use to route crews, bill customers, send text messages instead of emails -- all automated.  We close more sales, do way less admin, and my software bill is much smaller.

I recorded a few short videos of what I built to run my business so you can see it instead of taking my word for it: {PORTFOLIO_URL}

If it'd help to have the same built around your operation, that's what I do. Worth a 5-min watch?

(and if you never want to hear from me again, reply and tell me and I'll beat it.)

- Stetson

### Step 5: Preview One or Both Variants

```bash
./scripts/create-email-draft.py holiglows --variant 1 --dry-run
./scripts/create-email-draft.py holiglows --variant 2 --dry-run
```

Output shows what will be created:

```
📧 Initial Email Variant 1
   To: anvar@holiglows.com
   Subject: How many hours did you spending routing your customers last season?
   [DRY RUN - not sent to Fastmail]

--- Subject ---
How many hours did you spending routing your customers last season?

--- Body ---
Hey Anvar,

Does it take you more than a few hours to plan and route all your customers, or bill them?...

{PORTFOLIO_URL} → becomes https://holiglows.stetson.dev/
{YOUR_NAME} → becomes Stetson
{CONTACT_NAME} → becomes Anvar
...
```

### Step 6: Create One Draft

Pick exactly one variant for this prospect:

```bash
./scripts/create-email-draft.py holiglows --variant 1
# or
./scripts/create-email-draft.py holiglows --variant 2
```

Output:

```
📧 Initial Email Variant 1
   To: anvar@holiglows.com
   Subject: How many hours did you spending routing your customers last season?
   ✓ Draft created in Fastmail
```

### Step 7: Review in Fastmail

- Open https://www.fastmail.com
- Go to Drafts folder
- Find your draft (lock icon)
- Review and edit if needed
- Add personal touches
- Send!

### Step 8: Update Notes & Track

Update `outreach/prospects/holiglows/notes.md`:

```markdown
## Send log

- [x] Initial email sent: 2026-06-09 (anvar@holiglows.com)
- Variant used:
- Responses: (none yet)
```

### Step 9: No Follow-ups For Now

We are currently only creating the initial email draft, using one of two variants. Do not create follow-up drafts unless the campaign strategy changes.

## Using the Helper Script

If you prefer shorter commands, use `send-emails.sh`:

```bash
# Variant 1 (default)
./scripts/send-emails.sh holiglows

# Variant 2
./scripts/send-emails.sh holiglows variant-2

# Preview both variants without creating drafts
./scripts/send-emails.sh holiglows preview
```

## Quick Variations

### High-Volume Outreach (Multiple Prospects)

```bash
# Create 5 new prospects
./scripts/new-prospect.sh prospect-1 "Company One"
./scripts/new-prospect.sh prospect-2 "Company Two"
# ... etc

# Fill notes.md contact info for each; email.md is scaffolded from the base template

# Preview variant 1 for each
for slug in prospect-{1..5}; do
  ./scripts/create-email-draft.py "$slug" --variant 1 --dry-run
done

# If they look good, create one draft per prospect
for slug in prospect-{1..5}; do
  ./scripts/create-email-draft.py "$slug" --variant 1
done

# Review all drafts in Fastmail, personalize, and send
```

### Personalization in Fastmail

The script creates *drafts*, not sent emails. This lets you:

1. Review exact formatting in your inbox
2. Add custom touches (reference a specific project, mention mutual connection)
3. Fix any typos or phrasing issues
4. Change subject line if needed
5. Then send

This is intentional — cold emails need human judgment!

## Template Variables Reference

Your `email.md` can use:

| Variable | Source | Example |
|----------|--------|---------|
| `{PROSPECT_NAME}` | notes.md `# Title` | `HoliGlows` |
| `{CONTACT_NAME}` | notes.md `Contact person:` | `Anvar` |
| `{CONTACT_EMAIL}` | notes.md `Contact email:` | `anvar@holiglows.com` |
| `{WEBSITE_URL}` | notes.md `Website:` | `https://holiglows.com` |
| `{PORTFOLIO_URL}` | notes.md `Prospect URL:` | `https://holiglows.stetson.dev` |
| `{YOUR_NAME}` | Hardcoded (Stetson) | `Stetson` |
| `{YOUR_EMAIL}` | Hardcoded (me@stetson.dev) | `me@stetson.dev` |
| `{YOUR_PHONE}` | Hardcoded (307-214-5159) | `307-214-5159` |

To use a variable, just write it in curly braces:

```markdown
Hey {CONTACT_NAME},

I noticed {PROSPECT_NAME} does...

{PORTFOLIO_URL}
```

## Troubleshooting

### Draft doesn't appear in Fastmail

- Check you have the right account/token in `.env`
- Try creating a test draft: `./scripts/create-email-draft.py holiglows --dry-run`
- Check Fastmail's Drafts folder (refresh page)
- Check spam/junk

### Variable not substituting

- Make sure `notes.md` has the field. Example:
  ```markdown
  ## Contact info
  - Contact person: Anvar Batirov
  ```
- Variable is `{CONTACT_NAME}` (note the `NAME` part)
- Check for typos in notes.md or email.md

### Email formatting looks weird

- Rich text (bold, etc.) not supported yet — use plain text
- Line breaks preserved
- Consider using plain text in Fastmail drafts

## Pro Tips

1. **Template once, reuse always**: Create a great `email.md` for one prospect type, then copy it to others
2. **Preview before first email**: Always use `--dry-run` to check variable substitution
3. **Batch creation**: Create 5+ drafts, review them all, then send one per day
4. **Track responses**: Update notes.md with responses and dates
5. **A/B test cleanly**: choose `--variant 1` or `--variant 2` per prospect and record the variant in `notes.md`

## See Also

- `docs/QUICK-START.md` — 5-minute setup
- `docs/fastmail-setup.md` — Full Fastmail API reference
