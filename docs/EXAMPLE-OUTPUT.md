# Example Output — What to Expect

Here's what the commands actually print when you run them.

## Test with Existing Prospect

```bash
$ ./scripts/create-email-draft.py coloradochristmaslights --dry-run
```

**Output:**

```
📧 Initial Email
   To: somerset@example.com
   Subject: Local routing + workflow demos for Colorado Christmas Lights
   [DRY RUN - not sent to Fastmail]

--- Subject ---
Local routing + workflow demos for Colorado Christmas Lights

--- Body ---
Hey Somerset,

I'm Stetson. I own and operate 'Tis the Season, a Kansas City holiday lighting company, and in the off season I build software systems for other holiday lighting companies. We serve 900–1,000 customers each season with three owners plus seasonal installers, have a 94% year-over-year return rate, and sold 220 new customers in our biggest new-sales season.

I'm local to the Denver area and put together a short page for Colorado Christmas Lights with a few workflows I've already built around quoting, Stripe billing, customer texting, returning customer renewals, and install routing:

https://coloradochristmaslights.stetson.dev/

I saw that you serve a pretty wide Colorado footprint — Boulder, Denver, Breckenridge — and have worked with larger customers like Vail Resorts, The Stanley Hotel, the City of Louisville, and the Outlets at Silverthorne. That made me think routing, customer communication, and commercial/residential billing workflows may be worth comparing notes on.

These are real systems from an operating holiday lighting business — not generic automation examples. The demos use Airtable, Stripe, TextMagic, CompanyCam, Spoke Dispatch, and custom handlers, but I can also build around whatever tools you already use.

If any of this overlaps with something you're trying to improve before next season, feel free to email or text me. I'd be happy to schedule a call or meet in person.

Best,
Stetson
307-214-5159
me@stetson.dev

📧 Follow-up 1
   To: somerset@example.com
   Subject: Re: local routing + workflow demos
   [DRY RUN - not sent to Fastmail]

--- Subject ---
Re: local routing + workflow demos

--- Body ---
Hey Somerset,

Just wanted to bump this once. The page I sent has short demos of the actual holiday lighting systems I've built for quoting, payment collection, returning customer renewals, and routing:

https://coloradochristmaslights.stetson.dev/

Given the territory Colorado Christmas Lights serves, I thought the routing and customer communication pieces might be especially relevant. No pressure — I'm local and would be happy to meet or hop on a quick call if it's useful.

Best,
Stetson

📧 Follow-up 2
   To: somerset@example.com
   Subject: Worth mapping one routing workflow?
   [DRY RUN - not sent to Fastmail]

--- Subject ---
Worth mapping one routing workflow?

--- Body ---
Hey Somerset,

Last note from me. If useful, I'd be happy to map out one workflow for Colorado Christmas Lights — for example routing by area, customer texting, or commercial/residential billing — and show what a lightweight version could look like around your current tools.

If not a priority right now, no worries at all.

Best,
Stetson
```

## Create First Draft (For Real)

```bash
$ ./scripts/create-email-draft.py coloradochristmaslights 0
```

**Output:**

```
📧 Initial Email
   To: somerset@example.com
   Subject: Local routing + workflow demos for Colorado Christmas Lights
   ✓ Draft created in Fastmail
```

## Create All Emails at Once

```bash
$ ./scripts/create-email-draft.py coloradochristmaslights --all
```

**Output:**

```
📧 Initial Email
   To: somerset@example.com
   Subject: Local routing + workflow demos for Colorado Christmas Lights
   ✓ Draft created in Fastmail

📧 Follow-up 1
   To: somerset@example.com
   Subject: Re: local routing + workflow demos
   ✓ Draft created in Fastmail

📧 Follow-up 2
   To: somerset@example.com
   Subject: Worth mapping one routing workflow?
   ✓ Draft created in Fastmail
```

## Using Helper Script

```bash
$ ./scripts/send-emails.sh holiglows
```

**Output:**

```
📧 Creating initial email for holiglows...
📧 Initial Email
   To: anvar@holiglows.com
   Subject: Local routing + workflow demos for HoliGlows
   ✓ Draft created in Fastmail

✓ Done!
  Open https://www.fastmail.com to review drafts
```

## Error Cases

### Missing .env

```bash
$ ./scripts/create-email-draft.py holiglows
```

**Output:**

```
✗ Missing Fastmail credentials. See .env.example for setup instructions.
```

**Fix:** Copy `.env.example` to `.env` and add your credentials.

### Missing email.md

```bash
$ ./scripts/create-email-draft.py nonexistent
```

**Output:**

```
✗ No email.md found for prospect 'nonexistent'
  Expected: /home/exedev/get-work/outreach/prospects/nonexistent/email.md
  Create one from: /home/exedev/get-work/outreach/base/email-template.md
```

**Fix:** Create the prospect and add `email.md`.

### Invalid API Token

```bash
$ ./scripts/create-email-draft.py holiglows
```

**Output:**

```
📧 Initial Email
   To: anvar@holiglows.com
   Subject: Local routing + workflow demos for HoliGlows
   ✗ Failed: Fastmail API error (401):
{"type":"error","status":401,"message":"Invalid authentication credentials"}
```

**Fix:** Check your token at https://www.fastmail.com/settings/security/tokens

## In Fastmail

After you run:
```bash
./scripts/create-email-draft.py holiglows
```

Go to https://www.fastmail.com → Drafts

You'll see your drafts with a lock icon:

```
📧 Local routing + workflow demos for HoliGlows
   From: me@stetson.dev
   To: anvar@holiglows.com
   [Lock icon - indicates draft]
   
   5 seconds ago | Draft
```

Click it to:
- Review the content
- Edit/personalize before sending
- Add attachments
- Change subject/recipients
- Then "Send"

## Success Indicators

✅ Dry-run shows all variables substituted (no `{PLACEHOLDERS}`)  
✅ `✓ Draft created in Fastmail` message  
✅ Draft appears in Fastmail Drafts folder  
✅ No error messages  

## Next Steps After Creating

1. Open https://www.fastmail.com
2. Go to Drafts folder
3. Find your draft (lock icon)
4. Click to review
5. Make any edits or personalizations
6. Click "Send"
7. Update `notes.md` with send date
