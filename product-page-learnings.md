# Product page generation: everything learned so far

**Audience:** another Claude model building product pages for this user.
**Source:** three runs in session `zen-dijkstra-s4z0rc`: a toy blaster, a plush can and a butter squeeze toy. The user's words are quoted exactly, with spelling fixed. Everything else is my analysis.

**Read §1 first. It is the most important rule in this document and it comes before any other work.**

---

## 1. ▶ RESEARCH FIRST: mandatory, before any work

### 1.1 What the user said

> **"First thing to do before doing any work is research, as we learned. Research, find identical, literally the same product photos on the internet, use them as a guide to create a 3D model or just general aesthetic product photos."**

The instruction has four parts. Do all four, in this order, before writing any code or choosing any design:

| # | The user's instruction | What it means in practice |
|---|---|---|
| 1 | **"First thing… before doing any work is research"** | Research is step one. No layout, colour, copy or animation until it's done. |
| 2 | **"find identical, literally the same product photos on the internet"** | Find photos of *this exact product*: the same mould, print, size and proportions, usually sold by other shops from the same factory. Similar products don't count. |
| 3 | **"use them as a guide to create a 3D model"** | Build the 3D model from those photos: proportions, edge radius, label layout and typeface, true colour, surface finish, and how it squashes and recovers. |
| 4 | **"or just general aesthetic product photos"** | Or use them to art-direct clean, attractive product photos: angles, light, props and backgrounds that suit the product. Recreate the look; don't copy the photo. |

### 1.2 Why: what research changed in run 3
Run 3 (the butter toy) was the first run with research, and the user said "This was good." These findings changed the pages:

| Question | What research found | What it changed |
|---|---|---|
| What is it, exactly? | A solid TPR slow-rise toy, not foam; 13.5 cm is the common size | The material-true motion and the spec copy |
| Is there a famous original or brand? | The viral original is sold as "Squeezy" by Sunny Days / Schylling | The name: never use "Squeezy" |
| How does it behave and fail? | Slow rise; tears if folded or over-stretched; picks up lint; softens in heat | The care copy ("squeeze, don't fold") and the recovery animation |
| Any safety history? | The 2018 Danish EPA warning about foam squishies | No "non-toxic" claim; "not food, not for under-3s" |
| Which listing claims can't be backed? | "Anxiety relief" | Removed; the Breathe page says "a minute, not a method" |
| How big is it next to the real thing? | A real US butter stick is about 12.1 × 3.2 cm and 113 g | The True Size comparison page |

Run 2 (the plush) had no research, and it missed the category completely (§4). A two-minute search would have shown the product is a soft toy, not a can.

### 1.3 How to do the research

**A. Product facts.** Answer each question in the §1.2 table and cite a source for each answer.
- Search the title's key nouns plus the size (e.g. "butter stick squishy 13.5cm").
- Then add "review", "tears", "material", "recall" and "viral".
- Read owner reviews for how it really behaves and how it breaks.

**B. Photos of the identical product** (the user's rule, §1.1 parts 2–4).
- **Where to look:**
  - AliExpress, Temu, Amazon, Walmart, eBay, Etsy and TikTok Shop listings.
  - Wholesale and trade listings, which often state exact dimensions.
  - Owner photos and videos inside reviews.
  - TikTok and YouTube clips.
  - Reverse image search (Google Lens, Bing Visual Search, TinEye) using the supplier photo, if the environment allows it or the user can run it.
- **How to confirm it's identical:** all of these must match.
  - The same print: text, typeface and placement. Run 3: "4 OZ. · NET WT. (113 G) · SALTED · BUTTER".
  - The same listed size, weight and pack options.
  - The same proportions and edge radius.
  - A branded original with a different print is **not** identical. Record it as a trademark to avoid.
- **Collect:** several angles, the product in a hand (for scale), the product pressed or in use, colour in daylight, and a video showing how it moves. The video lets you time the animation from reality instead of by eye.

**C. Use the photos as the guide.**
- **For a 3D model:** match proportions, edge radius, label, colour, finish and deformation to the references. Then render clean stills for the gallery and packs, and label them as renders.
- **For aesthetic product photos:** study which angles, light, props and backgrounds make this product look good. Recreate that look with renders, the cleaned supplier photo, or new photography.
- **Publishing the found photos themselves:** only with permission. Another seller's photo is that seller's copyright. Ask the user whether their supplier grants rights to the factory photos; if yes, they can be cleaned and used.

**D. Judge every image and record the verdict.** Run 3's verdicts:
- **Used:** the user's own supplier photo, cleaned (banner and lines removed, cut out, upscaled).
- **Replaced:** a supplier photo too damaged to fix (the cropped 3-pack).
- **Made:** renders from a 3D model built to the listing's measurements.
- **Rejected:** other sellers' listings (copyright, sometimes a different product or brand) and paid stock (licence needed; shows real butter, not the toy).
- **Candidate:** free-licence images (Unsplash License; CC BY with credit) for context shots, like real butter next to the toy.

**E. Show the research in the deliverable.** The gallery index carries two sections, and the user liked this structure:
- "What the research changed": findings with source links.
- "Photo judgement": every image with its verdict and reason.

See `butter_pages/index.html`.

### 1.4 If the environment blocks it
- In run 3, web search worked, but downloading from image and shop sites was blocked by the environment's network policy: Unsplash, Pexels, Wikimedia uploads, Pixabay, Imgur, Flickr and several shop pages. **So run 3 never got the identical-product photos, and the 3D model was built from one low-resolution supplier photo plus the listed measurements.** That's the gap the user's rule closes.
- When this happens, tell the user at the start and offer two fixes:
  - Widen network access: the environment menu in the session title bar → Edit → Network access, then a broader level or Custom with the hosts added to Allowed domains. Docs: https://code.claude.com/docs/en/cloud-environments#network-access
  - Ask the user to paste reference photos or listing links.
- Never let a block silently downgrade the research. Write down what couldn't be fetched.

---

## 2. The task

The user runs **js.17**, a studio that builds "AI-generated, awwwards-winning websites". Each request has the same shape:

- **Input:** a marketplace listing (AliExpress): a long SEO-style title plus one or two supplier photos. The photos are often messy, with text banners, dimension lines, cropped products and other brands' logos.
- **Ask:** "10 different website layouts for a product page… awwwards winning, tons of animations, interactive components, adjust colours for the product."
- **Accepted output:** 10 complete HTML product pages plus a gallery index, published as one Artifact.
  - All pages share one JS kit: cart drawer, bundle pricing, toasts, an SVG sprite and a layout switcher.
  - The files are in `product_pages/` (run 1), `plush_pages/` (run 2) and `butter_pages/` (run 3).

Because the studio sells *AI-made* sites, **anything that looks obviously AI-made hurts their business directly.** Treat "feels like AI" as a defect, not a matter of taste.

## 3. The three runs

| | Run 1: toy blaster ("Popshell") | Run 2: can plush ("Zero Can") | Run 3: butter squeeze toy ("Butter Squish") |
|---|---|---|---|
| Listing | "2011/M92 Tactical Shell Ejecting Toy Gun … EVA Soft Bullet … Birthday Gift" | "Zero Sugar White [Brand] Energy Drink **Plush Toy** Simulation Can **Stuffed Doll Soft Figure** Decor Gift" | "5/1PCS Squishy Elastic Butter Stick Fidget Toy Cheese Stress Relief Game Decompression Prank Squeeze Toy for Anxiety Relief" |
| Research done? | No | **No** | **Yes** (§1) |
| Supplier photos | Usable after logo removal | Usable after logo removal | **Not clean:** red banners, dimension lines, the 3-pack cropped off the edge |
| What the product really is | A toy blaster for kids; the memorable feature is the brass shell flying out | A **fluffy stuffed toy** shaped like a can, bought for comfort and cuteness | A **slow-rise rubber squeeze toy**: press it and the dent fills back in over a few seconds; also a prank |
| How I framed it | Correctly: play, action, the shell-eject moment | **Wrongly:** as a *can* (vending machine, fridge, nutrition label) | Correctly: slow rise, silence, the prank, real size |
| User verdict | "Popshell is perfect. Perfect… this was kids product and you did exact correct colours and everything." | "Key problem is that it is a fluffy toy." Picked **06 Unwind** for its animation only: "you had brilliant ideas there but it still felt this sense of AI with those animations." | "This was good." Then the research rule in §1.1. |

## 4. What worked and what missed

### Worked (runs 1 and 3)
1. **Research before design** (run 3, §1). It decided the name, the care and safety copy, the claims to cut, and one whole page (True Size).
2. **Colours sampled from the product photo.** Run 1: purple, lime, orange tip, brass. Run 3: butter yellow `#f2e792` and label navy `#374a62`. The user praised the exact colours.
3. **Every layout built around the product's one real feature.** Run 1: the shell ejecting. Run 3: the slow rise, one interaction per page.
4. **The right category,** from the title's nouns plus research.
5. **A product model when the photos are bad.** Run 3's true-size 3D model (`butter_pages/assets/butter3d.js`) gave every page clean, consistent angles and a squeezable product.
6. **Honesty on the page.**
   - Logos and banners removed.
   - Labels everywhere they apply: sample prices and reviews, renders, simulated data, synthesized sound.
   - No unsupported health or safety claims, and no other company's trademark as the product name.
7. **Ten genuinely different structures** (run 3): lab report, Swiss grid, video player, blueprint, wax-paper wrapper and others.
8. **Testing:** every page at 390, 1024 and 1440 px, with no console errors and no sideways scrolling, checked in real screenshots.

### Missed (run 2)
1. **No research,** and the category in the title was ignored. The title says *Plush Toy, Stuffed Doll, Soft Figure, Decor Gift*; I followed the photo and the brand name instead.
2. **The design fought the material.** Metal, glass, coins, claws and fridges say *hard and cold*; the product is *soft and warm*. The one layout the user picked (Unwind) is the one where the can **turns into** the soft toy.
3. **The motion was physically wrong.** I used `bounce.out` and `back.out` overshoot plus snappy springs, which read as plastic. A plush should sink, sag and settle slowly.

## 5. What "sense of AI" means here

Most of these patterns are mine from runs 1–2; the reused easing curves are counted from the code.

- **One motion vocabulary everywhere.** Three easing curves reused about 85 times across 20 pages: `cubic-bezier(.2,.8,.2,1)` ×51, `(.3,1.6,.5,1)` ×20, `(.3,1.8,.5,1)` ×15.
- **The same reveal on every section:** `translateY(60px)` driven by `animation-timeline: view()`, 15–30 per page.
- **Off-the-shelf "playful" effects:** confetti, sparkle cursor trails, magnetic buttons, marquee bands, numbers counting up, pill chips, offset-shadow buttons, gradient text, word-by-word headline rises.
- **The same page template ten times:** kicker, huge headline, muted paragraph, hero, marquee, feature cards, buy panel, three reviews, FAQ.
- **Random decoration unrelated to the product:** 26 random bubbles and a comic "tssst!" in Unwind.
- **A swap instead of a transformation:** a flat SVG fades out and a photo fades in.
- **Mechanical timing:** evenly spaced beats, with no anticipation and no pause.
- **Gimmicks instead of art direction:** many clever mechanics, no single crafted moment.

Run 3 avoided all of these. Each page has one motion system driven by the product's own physics.

## 6. The full workflow, in order

1. **Research** (§1): product facts, then identical-product photos.
2. **Classify** in one line, using the title's nouns and the research: *material · who it's for · why they buy · the emotion*.
   - Run 2 should have been: *plush fabric · teens and adults, gifting · comfort and cuteness · "aww"*.
   - Run 3 was: *slow-rise TPR · office, classroom, pranksters · the slow dent and the joke · calm, amused*.
3. **Judge every image** (§1.3 D).
4. **Build the 3D model or the clean photo set,** guided by the identical-product photos (§1.3 C). Sample the colours from the photos.
5. **Design ten pages:** one signature each, material-true motion, varied structure (§7).
6. **Test** at 390, 1024 and 1440 px, and look at real screenshots.
7. **Publish the gallery** with the research and photo-judgement sections (§1.3 E).

## 7. Rules

0. **Research first** (§1). Find identical-product photos and use them as the guide for the 3D model or the product photography. Publish other people's photos only with permission.
1. **The title's nouns set the category; the photo sets the look.** If the title says *plush, stuffed, soft, doll, fluffy*, the soft object is the subject, even if it's shaped like something else. The user will state the category from now on; still check it against the title.
2. **One signature moment per page,** tied to what the product actually is. Cut generic extras.
3. **Match the easing to the material.**
   - Soft and slow-rise things: a fast press (about 0.2 s), then an overdamped recovery with a long tail and no overshoot. Run 3 drove every page from one curve: `d(t) = d0 · (0.3·e^(−t/0.12) + 0.7·e^(−t/1.5))`. Better still, time it from a reference video (§1.3 B).
   - Hard things like the blaster: quick, mechanical, a crisp recoil.
   - Vary timing within a page: anticipation, action, follow-through, a pause.
4. **Keep the product photographic.** No flat illustrations next to the photo. A true-size 3D model matched to the reference photos counts as photographic, as long as it's labelled as a render.
5. **Use motion sparingly.** One or two moments done well; leave the rest still.
6. **Vary the structure, not just the skin.** At least half of the layouts break the hero → features → buy → reviews → FAQ order.
7. **Be honest on the page.** Label renders, previews, sample prices and reviews, simulated data and synthesized sound. Make no health or safety claims the research can't support. Never use another company's trademark as the product name.
8. **Carry over what worked:** sampled colours, logo and banner removal, the shared cart kit, testing at three widths, real screenshots before publishing.

## 8. The user's preferences

- **Research before any work.** Find identical-product photos and use them to guide the 3D model or the product photography (§1.1).
- Wants the research and photo decisions visible in the gallery.
- Wants the whole set: 10 finished, interactive pages and a gallery, delivered with a link.
- Values exact product colours and the right product category.
- Prefers a **scroll-driven narrative** (Unwind) over gimmicks (claw machine, vending machine), and judges animation on whether it feels *hand-crafted*.
- Gives short, direct feedback. Treat praise as "keep doing this" and complaints as hard rules.
- For kids' and gift products: friendly tone, safety copy where relevant, no overpromising.

## 9. Useful files

- `butter_pages/index.html`: the gallery with the research and photo-judgement sections. Use it as the template for §1.3 E.
- `butter_pages/assets/butter3d.js`: the deformable 3D product model (press, squeeze, stretch, recovery curve, pose, snapshot). Adapt it for other squeezable products.
- `butter_pages/tools/cut.py`: cuts the product out of a cluttered supplier photo by colour mask.
- `plush_pages/pages/06-scroll-story.html` (Unwind): the scroll-narrative structure the user chose.
- `product_pages/` (Popshell): the reference for how this user wants colour and product framing done.
- `*/assets/kit.js`: the shared cart kit. Change `PRODUCT`, `LAYOUTS` and `img()` per product.
- `plush_pages/tools/` and `product_pages/tools/`: scripts for cutting out the product, removing logos and making colour variants.
