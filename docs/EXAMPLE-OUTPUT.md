# Example Output — What to Expect

## Preview Variant 1

```bash
$ ./scripts/create-email-draft.py holiglows --variant 1 --dry-run
```

```
📧 Initial Email Variant 1
   To: anvar@holiglows.com
   Subject: How many hours did you spending routing your customers last season?
   [DRY RUN - not sent to Fastmail]

--- Subject ---
How many hours did you spending routing your customers last season?

--- Body ---
Hey Anvar,

Does it take you more than a few hours to plan and route all your customers, or bill them? Is chasing payments on invoices challenging?
...
```

## Preview Variant 2

```bash
$ ./scripts/create-email-draft.py holiglows --variant 2 --dry-run
```

```
📧 Initial Email Variant 2
   To: anvar@holiglows.com
   Subject: How I run my lighting company on software I built myself
   [DRY RUN - not sent to Fastmail]

--- Subject ---
How I run my lighting company on software I built myself

--- Body ---
Hey Anvar — I run a holiday lighting company too (Tis the Season in Kansas City). I'm guessing your Oct–Dec looks like mine: 60 to 70 days of chaos.
...
```

## Create One Draft (For Real)

```bash
$ ./scripts/create-email-draft.py holiglows --variant 1
```

```
📧 Initial Email Variant 1
   To: anvar@holiglows.com
   Subject: How many hours did you spending routing your customers last season?
   ✓ Draft created in Fastmail
```

## Compare Both Variants Without Creating Drafts

```bash
$ ./scripts/create-email-draft.py holiglows --all --dry-run
```

This prints both variants. Use it for comparison/testing only; for real outreach, create exactly one draft per prospect.

## Using Helper Script

```bash
$ ./scripts/send-emails.sh holiglows variant-2
```

```
📧 Creating email variant 2 for holiglows...

📧 Initial Email Variant 2
   To: anvar@holiglows.com
   Subject: How I run my lighting company on software I built myself
   ✓ Draft created in Fastmail

✓ Done!
  Open https://www.fastmail.com to review drafts
```

## Error Cases

### Missing .env

```bash
$ ./scripts/create-email-draft.py holiglows
```

```
✗ Missing Fastmail credentials. See .env.example for setup instructions.
```

**Fix:** Copy `.env.example` to `.env` and add your credentials.

### Missing email.md

```bash
$ ./scripts/create-email-draft.py nonexistent
```

```
✗ No email.md found for prospect 'nonexistent'
  Expected: /home/exedev/get-work/outreach/prospects/nonexistent/email.md
  Create one from: /home/exedev/get-work/outreach/base/email-template.md
```

**Fix:** Create the prospect; new prospect scripts copy `outreach/base/email-template.md` automatically.

### Invalid API Token

```bash
$ ./scripts/create-email-draft.py holiglows
```

```
📧 Initial Email Variant 1
   To: anvar@holiglows.com
   Subject: How many hours did you spending routing your customers last season?
   ✗ Failed: Fastmail API error (401):
{"type":"error","status":401,"message":"Invalid authentication credentials"}
```

**Fix:** Check your token at https://www.fastmail.com/settings/security/tokens

## In Fastmail

After you run:

```bash
./scripts/create-email-draft.py holiglows --variant 1
```

Go to Fastmail → Drafts. Review the draft, edit/personalize if needed, send it, then update `notes.md`:

```markdown
## Send log
- [x] Initial email sent: 2026-06-09 to anvar@holiglows.com
- Variant used: 1
- Response notes:
```

## Success Indicators

✅ Dry-run shows all variables substituted (no `{PLACEHOLDERS}`)  
✅ `✓ Draft created in Fastmail` message  
✅ Draft appears in Fastmail Drafts folder  
✅ No error messages  
