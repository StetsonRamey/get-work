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
├── email.md                (empty, you'll create this)
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
- [ ] Follow-up 1 sent:
- [ ] Follow-up 2 sent:
```

### Step 3: Customize Portfolio (HTML/PDF)

Edit `outreach/prospects/holiglows/portfolio.html`:
- Change company name references
- Customize the hook/opening
- Update dates

```bash
./scripts/build.sh outreach/prospects/holiglows/portfolio.html
```

### Step 4: Create Email Template

Create `outreach/prospects/holiglows/email.md` based on `outreach/base/email-template.md`:

```markdown
## Initial Email

**To:** {CONTACT_NAME}
**Subject:** Improving quote flow + routing for {PROSPECT_NAME}

Hey {CONTACT_NAME},

I noticed {PROSPECT_NAME} serves the Denver area and uses a web form for quotes. I build software systems for companies like you that optimize the entire customer journey — from quote-to-install.

I put together a quick page showing workflows I've built for similar companies around streamlining quotes, installing routing, and customer communication:

{PORTFOLIO_URL}

If optimizing your quote flow or install routing sounds useful, I'd be happy to schedule a quick call or meet in person.

Best,
{YOUR_NAME}
{YOUR_PHONE}
{YOUR_EMAIL}

---

## Follow-up 1

**To:** {CONTACT_NAME}
**Subject:** Re: Improving quote flow

Hey {CONTACT_NAME},

Just bumping this — if there's friction in your quote process or you want to streamline how you dispatch installs, I've built systems that can help.

{PORTFOLIO_URL}

No pressure — I'm local to Denver and would be happy to chat.

Best,
{YOUR_NAME}

---

## Follow-up 2

**To:** {CONTACT_NAME}
**Subject:** Quick routing optimization call?

Hey {CONTACT_NAME},

Last note. If you'd find it useful, I can show you a lightweight routing optimization for {PROSPECT_NAME} in 30 minutes — just a quick call to see if it's worth exploring.

No obligation either way.

Best,
{YOUR_NAME}
```

### Step 5: Preview Email Template

```bash
./scripts/create-email-draft.py holiglows --dry-run
```

Output shows what will be created:

```
📧 Initial Email
   To: anvar@holiglows.com
   Subject: Improving quote flow + routing for HoliGlows
   [DRY RUN - not sent to Fastmail]

--- Subject ---
Improving quote flow + routing for HoliGlows

--- Body ---
Hey Anvar,

I noticed HoliGlows serves the Denver area and uses a web form for quotes...

{PORTFOLIO_URL} → becomes https://holiglows.stetson.dev/
{YOUR_NAME} → becomes Stetson
{CONTACT_NAME} → becomes Anvar
...
```

### Step 6: Create First Draft

```bash
./scripts/create-email-draft.py holiglows
```

Output:

```
📧 Initial Email
   To: anvar@holiglows.com
   Subject: Improving quote flow + routing for HoliGlows
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
- [ ] Follow-up 1 sent:
- [ ] Follow-up 2 sent:
- Responses: (none yet)
```

### Step 9: Schedule & Send Follow-ups

After 3-5 days, create follow-up 1:

```bash
./scripts/create-email-draft.py holiglows 1
```

Then in Fastmail: review, tweak, send.

Update notes with date sent.

After another 3-5 days, send follow-up 2:

```bash
./scripts/create-email-draft.py holiglows 2
```

## Using the Helper Script

If you prefer shorter commands, use `send-emails.sh`:

```bash
# Initial email
./scripts/send-emails.sh holiglows

# All follow-ups
./scripts/send-emails.sh holiglows followup

# All at once
./scripts/send-emails.sh holiglows all

# Preview without sending
./scripts/send-emails.sh holiglows preview
```

## Quick Variations

### High-Volume Outreach (Multiple Prospects)

```bash
# Create 5 new prospects
./scripts/new-prospect.sh prospect-1 "Company One"
./scripts/new-prospect.sh prospect-2 "Company Two"
# ... etc

# Fill notes.md and email.md for each

# Create all first emails
for slug in prospect-{1..5}; do
  ./scripts/create-email-draft.py "$slug" --dry-run
done

# If they look good, create drafts
for slug in prospect-{1..5}; do
  ./scripts/create-email-draft.py "$slug"
done

# Review all drafts in Fastmail, personalize, and send
```

### Multi-Step Campaign (Like Holiday Lighting)

For the holiday lighting campaign, you might have 3+ sequences:

**email-initial.md:**
```markdown
## Initial Email
[Your cold outreach]

---

## Follow-up 1
[3-5 days later]

---

## Follow-up 2
[Another 3-5 days]
```

Then:

```bash
# Send first round
./scripts/create-email-draft.py coloradochristmaslights --all

# 5 days later, update and send next round
# (Would need multiple email.md files or a sequence manager)
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
5. **A/B test subjects**: Create different email.md files to test subject lines

## See Also

- `docs/QUICK-START.md` — 5-minute setup
- `docs/fastmail-setup.md` — Full Fastmail API reference
