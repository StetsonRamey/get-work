# Email Draft System — Setup Summary

You now have everything to automatically create Fastmail drafts from email templates!

## What You Get

✅ **Automatic variable substitution** — Fill templates with prospect data from `notes.md`
✅ **Fastmail integration** — Create drafts directly in your Fastmail account
✅ **Two-variant initial emails** — Pick variant 1 or 2 per prospect
✅ **Preview before sending** — Dry-run mode to check everything
✅ **Tracked workflow** — Keep notes on who you've contacted

## Files Created

```
scripts/
├── create-email-draft.py    ← Main script (Python)
└── send-emails.sh           ← Convenience wrapper (bash)

outreach/
├── base/
│   └── email-template.md    ← Template starting point
└── prospects/holiglows/
    └── email.md             ← Example with real emails

docs/
├── QUICK-START.md           ← 5-minute setup
├── fastmail-setup.md        ← Full API reference
├── EMAIL-WORKFLOW.md        ← Complete workflow examples
└── SETUP-SUMMARY.md         ← This file

.env.example                  ← Config template
.gitignore                    ← Updated (contains .env)
```

## Getting Started (5 Minutes)

### 1. Install Dependencies

```bash
pip3 install requests python-dotenv
```

### 2. Create `.env`

```bash
cp .env.example .env
```

Edit `.env` with your account ID:

```env
FASTMAIL_ENDPOINT=https://fastmail.int.exe.xyz/jmap/session
FASTMAIL_ACCOUNT_ID=ubaa1403f  # Replace with your Fastmail account ID
FASTMAIL_MAILBOX_ID=Drafts
```

**Note:** The exe.dev integration automatically forwards your Fastmail bearer token—no need to add it to `.env`!

### 4. Test It

```bash
./scripts/create-email-draft.py coloradochristmaslights --dry-run
```

You should see the email preview with all variables substituted.

### 5. Create Your First Draft

```bash
./scripts/create-email-draft.py coloradochristmaslights
```

Open Fastmail → Drafts → review and send!

## Common Workflows

### Create one email variant for a prospect

```bash
./scripts/create-email-draft.py <slug> --variant 1
./scripts/create-email-draft.py <slug> --variant 2
```

Or using the helper:

```bash
./scripts/send-emails.sh <slug> variant-1
./scripts/send-emails.sh <slug> variant-2
```

### Preview before creating

```bash
./scripts/create-email-draft.py <slug> --variant 1 --dry-run
```

### Compare both variants

```bash
./scripts/create-email-draft.py <slug> --all --dry-run
```

Use `--all` for preview/comparison. For real outreach, create one variant per prospect.

## How It Works

### The Flow

1. You create a prospect folder with `notes.md`:
   ```markdown
   # HoliGlows

   ## Contact info
   - Contact person: Anvar
   - Contact email: anvar@holiglows.com
   ```

2. The new prospect script copies `email.md` from `outreach/base/email-template.md`:
   ```markdown
   ## Initial Email Variant 1
   **To:** {CONTACT_NAME}
   **Subject:** How many hours did you spending routing your customers last season?

   Hey {CONTACT_NAME}, I noticed {PROSPECT_NAME}...
   ```

3. You run the script:
   ```bash
   ./scripts/create-email-draft.py holiglows
   ```

4. The script:
   - Reads `notes.md` and extracts: Anvar, HoliGlows, anvar@holiglows.com
   - Reads `email.md` and parses sections
   - Substitutes: `{CONTACT_NAME}` → "Anvar", `{PROSPECT_NAME}` → "HoliGlows"
   - Calls Fastmail JMAP API to create a draft
   - Shows: ✓ Draft created in Fastmail

5. You review in Fastmail → personalize → send

### Variables

All substituted from your `notes.md` or hardcoded:

| Variable | Source |
|----------|--------|
| `{PROSPECT_NAME}` | notes.md title |
| `{CONTACT_NAME}` | Contact person field |
| `{CONTACT_EMAIL}` | Contact email field |
| `{WEBSITE_URL}` | Website field |
| `{PORTFOLIO_URL}` | Prospect URL field |
| `{YOUR_NAME}` | Hardcoded: Stetson |
| `{YOUR_EMAIL}` | Hardcoded: me@stetson.dev |
| `{YOUR_PHONE}` | Hardcoded: 307-214-5159 |

## Documentation

- **Quick start**: `docs/QUICK-START.md` (5 min setup)
- **Full workflow**: `docs/EMAIL-WORKFLOW.md` (detailed walkthrough)
- **API reference**: `docs/fastmail-setup.md` (all technical details)
- **Main readme**: Updated `README.md` with email system info

## Customization

### Change your details

Edit hardcoded values in `scripts/create-email-draft.py`:

```python
variables = {
    "your_name": "Your Name",
    "your_email": "your@email.com",
    "your_phone": "555-1234",
}
```

### Use different Fastmail folder

In `.env`:

```env
FASTMAIL_MAILBOX_ID=Custom Folder Name
```

### Add more variables

Add to `notes.md`:

```markdown
## Extra

- Company size: 50+ employees
- Industry: Holiday lighting
```

Then edit `create-email-draft.py` to parse and use them.

## Tips & Best Practices

1. **Always use --dry-run first** on new templates
2. **Keep emails in notes.md** — easy to track and see progression
3. **Test on existing prospects** before creating new ones
4. **Personalize in Fastmail** — these are drafts, not sent emails
5. **Track send dates** in notes.md under "## Send log"
6. **Batch create** — make 5+ drafts, review all, send one per day

## Troubleshooting

### "Missing Fastmail credentials"

Check `.env` exists with valid token and account ID.

### "Draft not in Fastmail"

- Refresh Fastmail page
- Check Drafts folder (it's set in `.env`)
- Verify token not expired at https://www.fastmail.com/settings/security/tokens

### Variables not substituting

Check `notes.md` format:

```markdown
# Company Name          ← Must be h1

## Contact info
- Contact person: Name
- Contact email: email@test.com
```

## Support

- See the full workflow example in `docs/EMAIL-WORKFLOW.md`
- Check Fastmail API docs: https://www.fastmail.com/help/clients/jmapapi.html
- Review test run with `--dry-run` flag

## What's Next?

1. ✅ Set up .env with Fastmail credentials
2. ✅ Test with existing prospect: `./scripts/create-email-draft.py coloradochristmaslights`
3. ✅ Create a new prospect; email.md is copied automatically
4. ✅ Batch create and manage campaigns
5. (Optional) Extend script for more features (auto-send, tracking, etc.)

---

**Ready to go!** Your cold email system is now set up. Check out `docs/QUICK-START.md` for the next steps.
