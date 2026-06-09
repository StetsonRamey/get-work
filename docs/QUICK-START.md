# Quick Start: Email Drafts

Get sending emails to Fastmail in 5 minutes.

## Setup (One Time)

### Option A: Using exe.dev Integration (Recommended)

```bash
# 1. Install dependencies
pip3 install requests python-dotenv

# 2. Create .env from template
cp .env.example .env

# 3. Edit .env with your account ID
#    (exe.dev integration handles the token securely)
nano .env
```

Your `.env` should have:

```env
FASTMAIL_ENDPOINT=https://fastmail.int.exe.xyz/jmap/session
FASTMAIL_ACCOUNT_ID=ubaa1403f  # Your Fastmail account ID
FASTMAIL_MAILBOX_ID=Drafts
```

The integration automatically forwards your Fastmail API token—no need to store it in .env!

### Option B: Direct Token Auth (Not Recommended)

If you prefer to manage the token directly (less secure):

```bash
# Get your token from: https://www.fastmail.com/settings/security/tokens
FASTMAIL_ACCESS_TOKEN=your_token_here
FASTMAIL_ACCOUNT_ID=your_account_id_here
FASTMAIL_MAILBOX_ID=Drafts
```

## Create Your First Draft

### 1. Create a new prospect folder

```bash
./scripts/new-prospect.sh holiglows "HoliGlows"
```

### 2. Fill in contact info in `notes.md`

```markdown
# HoliGlows

## Contact info

- Contact person: Gulisada Chistol
- Contact email: anvar@holiglows.com
- Website: https://www.holiglows.com/
```

### 3. Create `email.md` with your template

Copy the example template from `outreach/base/email-template.md` or:

```bash
cp outreach/prospects/coloradochristmaslights/email.md \
   outreach/prospects/holiglows/email.md
```

Edit it with your message using variables like `{PROSPECT_NAME}` and `{CONTACT_NAME}`.

### 4. Preview (optional)

```bash
./scripts/create-email-draft.py holiglows --dry-run
```

You'll see exactly what gets sent:

```
📧 Initial Email
   To: anvar@holiglows.com
   Subject: Local routing + workflow demos for HoliGlows
   [DRY RUN - not sent to Fastmail]

--- Subject ---
Local routing + workflow demos for HoliGlows

--- Body ---
Hey Gulisada,

I'm Stetson...
```

### 5. Send to Fastmail

```bash
./scripts/create-email-draft.py holiglows
```

Output:
```
📧 Initial Email
   To: anvar@holiglows.com
   Subject: Local routing + workflow demos for HoliGlows
   ✓ Draft created in Fastmail
```

### 6. Open Fastmail and send

- Go to https://www.fastmail.com
- Find the draft in your Drafts folder
- Edit if needed (add personal touches)
- Send!

## Send Follow-ups

```bash
# Create Follow-up 1 (second section in email.md)
./scripts/create-email-draft.py holiglows 1

# Create Follow-up 2 (third section)
./scripts/create-email-draft.py holiglows 2

# Or all at once
./scripts/create-email-draft.py holiglows --all
```

## Template Variables

In your `email.md`, use these:

- `{PROSPECT_NAME}` → Company name
- `{CONTACT_NAME}` → Contact person
- `{WEBSITE_URL}` → Their website
- `{PORTFOLIO_URL}` → Your portfolio for them
- `{YOUR_NAME}` → Your name
- `{YOUR_EMAIL}` → Your email
- `{YOUR_PHONE}` → Your phone

All are automatically pulled from your `notes.md` file.

## Workflow Tips

1. **One prospect at a time**: Create one prospect folder, email template, and send drafts together
2. **Always preview first**: Use `--dry-run` before sending to check formatting
3. **Personalize in Fastmail**: Create draft, review, add personal touches, send
4. **Track in notes.md**: Update send dates and responses:
   ```markdown
   ## Send log
   - [x] Initial email sent: 2026-06-09
   - [ ] Follow-up 1 sent:
   ```

## More Help

See `docs/fastmail-setup.md` for detailed troubleshooting and API info.
