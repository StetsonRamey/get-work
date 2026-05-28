# Holiday lighting prospect campaign

## Goal

Create a new prospect sheet style directed at other holiday lighting companies, starting with three Denver-area targets:

- Colorado Christmas Lights — https://www.coloradochristmaslights.com/
- HoliGlows — https://www.holiglows.com/
- Iceberg Christmas Lights — https://icebergchristmaslights.com/

Each company gets a lightly customized page hosted on a `company.stetson.dev` subdomain. The sheet should make the outreach feel specific and local without over-assuming their internal needs.

## Core positioning

Stetson owns and operates **’Tis the Season** — https://tistheseasonkc.com/ — a Kansas City holiday lighting company. The company serves 900–1,000 customers each season with three owners plus seasonal installers, has a 94% year-over-year return rate, and sold 220 new customers in its biggest new-sales season. In the off season, Stetson builds software systems for other holiday lighting companies.

Primary message:

> I’m not pitching generic automation. I’ve already built working systems for an active holiday lighting operation that serves 900–1,000 customers each season: quoting, billing, customer texting, returning customer renewals, and routing. I’m local to the Denver area and can meet in person if it’s useful.

## Tone

- Operator-to-operator, not agency-to-prospect.
- Practical, seasonal, and workflow-specific.
- Local and accessible: Denver-area, available for a call or in-person meeting.
- Specific about tools, but flexible about implementation.
- Avoid assuming they are broken or disorganized.

Preferred language:

> If any of these workflows overlap with bottlenecks you run into during the season...

Avoid:

> Your company needs automation.

## Tools to mention

The current systems use:

- Airtable
- Stripe
- TextMagic
- CompanyCam
- Spoke Dispatch
- Google Maps / roofline screenshots
- Custom server handlers

Important caveat:

> If your company uses a different stack, the same workflows can usually be adapted around your current tools.

## Prospect sheet structure

1. Header / hero
   - Company-specific headline
   - Local operator positioning
   - Email/text/in-person CTA

2. Short intro
   - Stetson owns/operates ’Tis the Season
   - Builds software for holiday lighting companies in the off season
   - Local to Denver area

3. Why these workflows matter
   - Seasonal quote volume
   - Payment collection before scheduling
   - Returning customer renewals
   - Install routing / dispatch

4. Four demo cards
   - Quote workflow
   - New customer setup + billing
   - Returning customer renewal
   - Routing + dispatch

5. Tool stack / build-to-suit section
   - Exact stack used
   - Can adapt to their tools

6. Closing CTA
   - Email or text me
   - Schedule call or local meeting
   - Offer to map one of their workflows

## Demo videos to record

### Demo 1 — Quote workflow

**Title:** Website Lead → Roofline Markup → Personalized Quote Email

**Goal:** Show how a new lead becomes a structured quote workflow.

**Show:**

- Contact form submission lands in Airtable
- House is reviewed in Google Maps
- Roofline screenshot is marked up
- Linear footage is entered
- Quote email is generated/sent with pricing and photos
- Out-of-service-area flag triggers the right response

**Talk track:**

> This is the workflow we use when a new holiday lighting lead comes in. The goal is to keep quoting fast and consistent while still sending a customer something that feels personal and visual.

**End with:**

> A version of this could be adapted to your quote form, pricing rules, service area, and email/text process.

### Demo 2 — New customer setup and billing

**Title:** Accepted Quote → Stripe, TextMagic, CompanyCam, and Payment Link

**Goal:** Show what happens after a customer says yes.

**Show:**

- Customer gets created in Stripe
- Customer gets created in TextMagic
- Customer gets created in CompanyCam
- Marked roofline photo is uploaded to CompanyCam
- Stripe checkout/invoice link is created
- Payment link can be texted to the customer

**Talk track:**

> Once a customer decides to move forward, the important thing is to avoid retyping the same information into four different systems. This workflow sets up the customer everywhere they need to exist and prepares the payment link.

**End with:**

> The same pattern can work with whatever billing, texting, CRM, or field documentation tools you already use.

### Demo 3 — Returning customer renewal

**Title:** Annual Renewal Texts, Forms, Stripe Checkout, and Paid Status Sync

**Goal:** Show how past customers are reactivated each season.

**Show:**

- Existing customers receive a text
- Text links to renewal form
- Form updates Airtable customer record
- Yearly invoice line items are created
- Stripe checkout is generated dynamically
- Payment updates Airtable paid status

**Talk track:**

> Returning customers are some of the most valuable customers in holiday lighting. This workflow makes it easy to ask who wants service again, generate the right invoice, collect payment, and know who is ready to route.

**End with:**

> This can be customized around your renewal pricing, storage fees, install/removal model, and existing customer list.

### Demo 4 — Routing and dispatch

**Title:** Paid Customers → Area-Based Routes → Crew Dispatch

**Goal:** Show how paid customers become organized routes for the install team.

**Show:**

- Paid customers grouped by area
- Custom Airtable extension used to prepare routing
- Routes built in Spoke Dispatch
- Routes pushed to install/service team
- Crew sees next stops in app

**Talk track:**

> Once customers are paid and ready, the next bottleneck is usually routing. This system helps group customers by area, create efficient install runs, and push clear routes to the field team.

**End with:**

> A routing workflow can be built around your crews, service area, install capacity, and dispatch tools.

## Company research brief template

Use this for each target company before finalizing the page/email.

```text
Company:
Website:
Custom domain:
Contact person:
Contact email:
Contact phone/text:
Location / service area:
Primary services shown:
Residential / commercial focus:
Notable wording from their site:
Current quote/contact process observed:
Any relevant photos/projects/positioning:
Personalized opening line:
Reason these workflows may be relevant:
Best CTA:
Send status:
Follow-up notes:
```

## Base cold email

Subject options:

```text
Local holiday lighting workflow demos for {{COMPANY_NAME}}
Holiday lighting quoting + routing systems
Denver-area holiday lighting software workflows
```

Email:

```text
Hey {{FIRST_NAME_OR_TEAM}},

I’m Stetson. I own and operate ’Tis the Season, a Kansas City holiday lighting company, and in the off season I build software systems for other holiday lighting companies. We serve 900–1,000 customers each season with three owners plus seasonal installers, have a 94% year-over-year return rate, and sold 220 new customers in our biggest new-sales season.

I’m local to the Denver area and put together a short page for {{COMPANY_NAME}} with a few workflows I’ve already built around quoting, Stripe billing, customer texting, returning customer renewals, and install routing.

Here’s the page:
{{CUSTOM_URL}}

These are real systems from an operating holiday lighting business — not generic automation examples. The demos use Airtable, Stripe, TextMagic, CompanyCam, Spoke Dispatch, and custom handlers, but I can also build around whatever tools you already use.

If any of this overlaps with something you’re trying to improve before next season, feel free to email or text me. I’d be happy to schedule a call or meet in person.

Best,
Stetson
{{PHONE}}
{{EMAIL}}
```

## Follow-up 1

```text
Subject: Re: local holiday lighting workflow demos

Hey {{FIRST_NAME_OR_TEAM}},

Just wanted to bump this once. The page I sent has short demos of the actual holiday lighting systems I’ve built for quoting, payment collection, returning customer renewals, and routing.

{{CUSTOM_URL}}

No pressure — I just figured it may be useful to compare notes with another operator before the next season ramps up. I’m local, so I’m happy to meet in person if that’s easier.

Best,
Stetson
```

## Follow-up 2

```text
Subject: Worth mapping one workflow?

Hey {{FIRST_NAME_OR_TEAM}},

Last note from me. If it would be useful, I’d be happy to map out one workflow for {{COMPANY_NAME}} — for example quote intake, returning customer renewals, or routing — and show what a lightweight version could look like around your current tools.

If not a priority right now, no worries at all.

Best,
Stetson
```

## Info still needed from Stetson

Already provided:

- Public email: `me@stetson.dev`
- Public phone/text: `307-214-5159`

Still needed:

- Calendar link, if any
- Final video URLs
- Any contact/person updates for each target
