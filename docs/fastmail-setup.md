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

For each prospect, create an `outreach/prospects/<slug>/email.md` file:

```markdown
## Initial Email

**To:** {CONTACT_NAME}
**Subject:** Local routing + workflow demos for {PROSPECT_NAME}

Hey {CONTACT_NAME},

I'm Stetson, and I build software systems for holiday lighting companies...

Best,
{YOUR_NAME}
{YOUR_PHONE}
{YOUR_EMAIL}

---

## Follow-up 1

**To:** {CONTACT_NAME}
**Subject:** Re: local routing + workflow demos

Just wanted to bump this once...

Best,
{YOUR_NAME}

---

## Follow-up 2

**To:** {CONTACT_NAME}
**Subject:** Worth mapping one routing workflow?

Last note from me...

Best,
{YOUR_NAME}
```

### Template Variables

Available in all emails:

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

- Contact person: Gulisada Chistol or Anvar Batirov
- Contact email: anvar@holiglows.com
```

These become variables in your email template (no manual substitution needed).

## Usage

### Create First Email Draft

```bash
./scripts/create-email-draft.py holiglows
```

Or with explicit index:

```bash
./scripts/create-email-draft.py holiglows 0
```

### Create Second Email (Follow-up 1)

```bash
./scripts/create-email-draft.py holiglows 1
```

### Create All Emails at Once

```bash
./scripts/create-email-draft.py holiglows --all
```

### Preview Without Sending (Dry Run)

See what would be created without posting to Fastmail:

```bash
./scripts/create-email-draft.py holiglows --dry-run
./scripts/create-email-draft.py holiglows --all --dry-run
```

## Workflow Example

```bash
# 1. Create a new prospect
./scripts/new-prospect.sh holiglows "HoliGlows"

# 2. Edit notes.md with contact info
vim outreach/prospects/holiglows/notes.md

# 3. Create email.md with your template
cat > outreach/prospects/holiglows/email.md << 'EOF'
## Initial Email
**To:** {CONTACT_NAME}
**Subject:** Local routing + workflow demos for {PROSPECT_NAME}

Hey {CONTACT_NAME},
...
EOF

# 4. Preview what will be sent
./scripts/create-email-draft.py holiglows --dry-run

# 5. Create draft in Fastmail
./scripts/create-email-draft.py holiglows

# 6. Review in Fastmail, make any tweaks, and send
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
   - [ ] Follow-up 1 sent:
   ```
4. **Reuse templates**: Once you have a good template for one prospect type, copy and adapt it for others

## Reference

- Fastmail JMAP API: https://www.fastmail.com/help/clients/jmapapi.html
- Create API token: https://www.fastmail.com/settings/security/tokens
