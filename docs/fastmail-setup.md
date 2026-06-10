# Fastmail Email Draft Integration

Automatically create draft emails in Fastmail from templates in your prospect folders.

## One-time Setup

### 1. Install Dependencies

```bash
pip3 install requests python-dotenv
```

### 2. Get Fastmail API Token

1. Go to https://www.fastmail.com/settings/security/tokens
2. Click "New API token"
3. Name it something like "get-work drafts"
4. Leave all permissions as default (or just `jmap:mail:write`)
5. Click "Create token"
6. Copy the token

### 3. Get Your Account ID

1. Go to https://www.fastmail.com/settings/security/tokens
2. Look at the API token you just created — the **Account ID** is shown on that page
3. Or go to https://www.fastmail.com/settings/account and look at Settings

### 4. Create `.env` File

```bash
cp .env.example .env
```

Edit `.env` and fill in:

```env
FASTMAIL_ACCESS_TOKEN=your_token_here
FASTMAIL_ACCOUNT_ID=your_account_id_here
FASTMAIL_MAILBOX_ID=Drafts
```

**⚠️ Important:** Add `.env` to `.gitignore` if you version control this project:

```bash
echo ".env" >> .gitignore
```

## Creating Email Templates

New prospect scripts now copy `outreach/base/email-template.md` into each prospect folder as `email.md`. That file contains exactly two sections:

- `## Initial Email Variant 1`
- `## Initial Email Variant 2`

Fill the contact data in `notes.md`, then choose which variant to draft.

### Template Variables

Available in both variants:

- `{PROSPECT_NAME}` — Company name (from notes.md h1)
- `{CONTACT_NAME}` — Contact person (from notes.md "Contact person:" field)
- `{WEBSITE_URL}` — Their website URL
- `{PORTFOLIO_URL}` — Your portfolio URL for this prospect
- `{YOUR_NAME}` — Your name (default: "Stetson")
- `{YOUR_EMAIL}` — Your email (default: "me@stetson.dev")
- `{YOUR_PHONE}` — Your phone (default: "307-214-5159")

### Data Extraction from notes.md

The script automatically pulls data from your prospect's `notes.md`:

```markdown
# HoliGlows                            ← PROSPECT_NAME

**Website:** https://www.holiglows.com/
**Prospect URL:** https://holiglows.stetson.dev/

## Contact info

- Contact person: Anvar Batirov
- Contact email: anvar@holiglows.com
```

These become variables in your email template (no manual substitution needed).

## Usage

### Preview a Variant Without Creating a Draft

```bash
./scripts/create-email-draft.py holiglows --variant 1 --dry-run
./scripts/create-email-draft.py holiglows --variant 2 --dry-run
```

The older positional form still works (`0` = variant 1, `1` = variant 2):

```bash
./scripts/create-email-draft.py holiglows 1 --dry-run
```

### Create a Fastmail Draft

```bash
./scripts/create-email-draft.py holiglows --variant 1
# or
./scripts/create-email-draft.py holiglows --variant 2
```

### Preview Both Variants

```bash
./scripts/create-email-draft.py holiglows --all --dry-run
```

Use `--all` mainly for comparison/testing. For real outreach, pick one variant per prospect so you do not accidentally create duplicate drafts to the same person.

## Workflow Example

```bash
# 1. Create a new holiday-lighting prospect. This creates portfolio.html,
#    notes.md, and email.md copied from outreach/base/email-template.md.
./scripts/new-holiday-prospect.sh holiglows "HoliGlows" "https://www.holiglows.com/"

# 2. Edit notes.md with contact info
vim outreach/prospects/holiglows/notes.md

# 3. Preview each variant
./scripts/create-email-draft.py holiglows --variant 1 --dry-run
./scripts/create-email-draft.py holiglows --variant 2 --dry-run

# 4. Create exactly one draft in Fastmail
./scripts/create-email-draft.py holiglows --variant 1

# 5. Review in Fastmail, make any tweaks, send, and record the variant in notes.md
```

## Troubleshooting

### "Missing Fastmail credentials"

- Check that `.env` file exists and has the right tokens
- Verify token is not expired: https://www.fastmail.com/settings/security/tokens

### "Could not find Drafts mailbox"

- Verify `FASTMAIL_MAILBOX_ID` is correct
- In Fastmail, your main drafts folder is usually called "Drafts"
- To check available mailboxes, add debug output to the script

### Email not showing up in Fastmail

- Check your Drafts folder (it's set in `.env`)
- Drafts appear with a lock icon in Fastmail
- Check Fastmail's spam/junk folders
- Run with `--dry-run` to see exactly what would be sent

### Variables Not Substituting

Make sure your `notes.md` has the right format:

```markdown
# Prospect Name        ← Use h1 for company name

## Contact info

- Contact person: Name
- Contact email: email@example.com
```

## Tips

1. **Start with dry-run**: Always test with `--dry-run` before creating real drafts
2. **Personalize in Fastmail**: Create the draft, then edit it in Fastmail before sending
3. **Track sends**: Update your notes.md with dates/responses:
   ```markdown
   ## Send log
   - [x] Initial email sent: 2026-06-09 to anvar@holiglows.com
   - Variant used: 1
   ```
4. **Reuse templates**: Once you have a good template for one prospect type, copy and adapt it for others

## Reference

- Fastmail JMAP API: https://www.fastmail.com/help/clients/jmapapi.html
- Create API token: https://www.fastmail.com/settings/security/tokens
