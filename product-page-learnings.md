# Product page generation: lessons from three runs

**Audience:** another Claude model building product pages for this user.
**Source:** three runs in session `zen-dijkstra-s4z0rc`. The user's feedback is quoted word for word, with spelling fixed. Everything else is my analysis.

**The short version:** research the product before designing anything. The user's own instruction after run 3:

> "First thing to do before doing any work is research, as we learned. Research, find identical, literally the same product photos on the internet, use them as a guide to create a 3D model or just general aesthetic product photos."

§6 is the workflow the user approved. §7 is the full rule list.

---

## 1. The task

The user runs **js.17**, a studio that builds "AI-generated, awwwards-winning websites". Each request has the same shape:

- **Input:** a marketplace listing (AliExpress), meaning a long SEO-style title plus one or two supplier photos. The photos are often messy, with text banners, dimension lines, cropped products and other brands' logos.
- **Ask:** "10 different website layouts for a product page… awwwards winning, tons of animations, interactive components, adjust colours for the product."
- **Output that was accepted:** 10 complete HTML product pages plus a gallery index, published as one Artifact.
  - All pages share one JS kit: cart drawer, bundle pricing, toasts, an SVG sprite and a layout switcher.
  - The files are in `product_pages/` (run 1), `plush_pages/` (run 2) and `butter_pages/` (run 3).

Because the studio sells *AI-made* sites, **anything that looks obviously AI-made hurts their business directly.** Treat "feels like AI" as a defect, not a matter of taste.

## 2. What happened

| | Run 1: toy blaster ("Popshell") | Run 2: can plush ("Zero Can") | Run 3: butter squeeze toy ("Butter Squish") |
|---|---|---|---|
| Listing | "2011/M92 Tactical Shell Ejecting Toy Gun … EVA Soft Bullet … Birthday Gift" | "Zero Sugar White [Brand] Energy Drink **Plush Toy** Simulation Can **Stuffed Doll Soft Figure** Decor Gift" | "5/1PCS Squishy Elastic Butter Stick Fidget Toy Cheese Stress Relief Game Decompression Prank Squeeze Toy for Anxiety Relief" |
| Supplier photos | Usable after logo removal | Usable after logo removal | **Not clean:** red "1PC Large" banners, dimension lines over the product, the 3-pack cropped off the edge |
| What the product really is | A toy blaster for kids. The memorable feature is the brass shell flying out. | A **fluffy stuffed toy** shaped like a can, bought for comfort and cuteness. | A **slow-rise rubber (TPR) squeeze toy**: press it and the dent fills back in over a few seconds. Also used as a prank. |
| How I framed it | Correctly: play, action, the shell-eject moment | **Wrongly:** as a *can* (vending machine, fridge, nutrition label) | Correctly, **after research**: slow rise, silence, the prank, real size |
| User verdict | "Popshell is perfect. Perfect… this was kids product and you did exact correct colours and everything." | "Key problem is that it is a fluffy toy." Picked **06 Unwind** for its animation only: "you had brilliant ideas there but it still felt this sense of AI with those animations." | "This was good." Asked for the run's structure to be written up here, with research as the new first step. |

## 3. Why runs 1 and 3 worked

1. **Colours came straight from the photo.** I sampled them from the product itself.
   - Run 1: purple slide, lime grip, orange tip, brass shell.
   - Run 3: butter yellow `#f2e792` and label navy `#374a62`.
   - Each layout used those colours in different proportions. The user praised the exact colours in run 1.
2. **Every layout was built around the product's one real feature.**
   - Run 1: the shell ejecting.
   - Run 3: the slow rise. Every page has one interaction, and it always shows the dent filling back in.
3. **I got the product category right.** In run 3 that came from research, not from guessing (see §6).
4. **It was honest and polished.**
   - Logos removed. Prices and reviews labelled "sample". Renders labelled as renders.
   - Simulated data labelled "simulated", and generated sound labelled "synthesized".
   - I tested every page at 390, 1024 and 1440 px, with no console errors and no sideways scrolling.
5. **Run 3 only: research changed the copy and the design.**
   - It found the trademark to avoid: the viral original is sold as "Squeezy".
   - It found the failure mode. The toy tears if folded, so the care copy became "squeeze, don't fold".
   - It found the safety history, so the pages make no "non-toxic" claim.
   - It found the true size: the toy is bigger than a real stick of butter, which became the True Size page.
   - It also cut the listing's untested health claim ("anxiety relief").
6. **Run 3 only: the research and the photo decisions were shown in the deliverable.** The gallery index has a "What the research changed" section with sources and a "Photo judgement" section that marks each candidate image *used*, *made*, *rejected* or *candidate*, with the reason. The user liked this structure.

## 4. Why run 2 missed

1. **The category was in the title and I didn't use it.** The title says *Plush Toy, Stuffed Doll, Soft Figure, Decor Gift*. I followed the photo and the brand name ("energy drink can") instead.
   - **Rule:** the title's nouns set the category. The photo sets the look.
2. **What I built fought the material.**
   - Metal, glass, coins, claws and fridges all say *hard and cold*. The product is *soft and warm*.
   - The one layout the user picked (Unwind) is the one where the can **turns into** the soft toy.
3. **The motion was physically wrong for a soft object.** I used `bounce.out` and `back.out` overshoot plus snappy springs, which read as plastic or rubber. A plush should *sink, sag, and settle slowly*.
4. **I did no research.** A two-minute search for the product would have shown the category.

## 5. What "sense of AI" means here

Most of these patterns are mine from runs 1–2; the reused easing curves are counted from the code.

- **One motion vocabulary everywhere.** Across 20 pages I reused three easing curves about 85 times: `cubic-bezier(.2,.8,.2,1)` ×51, `(.3,1.6,.5,1)` ×20, `(.3,1.8,.5,1)` ×15.
- **The same reveal on every section:** `translateY(60px)` driven by `animation-timeline: view()`, 15–30 per page.
- **Off-the-shelf "playful" effects:** confetti, sparkle cursor trail, magnetic buttons, scrolling marquee bands, numbers counting up, pill chips, offset-shadow buttons, gradient text, word-by-word headline rises.
- **The same page template ten times:** kicker label, huge headline, muted paragraph, then hero, marquee, feature cards, buy panel, three review cards, FAQ.
- **Random decoration that doesn't relate to the product:** in Unwind, 26 random bubbles and a comic-style "tssst!" pop-up.
- **A swap instead of a transformation:** a flat SVG drawing fades out and a photo fades in.
- **Mechanical timing:** evenly spaced beats, with no anticipation before an action and no pause after it.
- **Gimmicks instead of art direction:** many clever mechanics but no single crafted moment.

Run 3 avoided these on purpose:
- No confetti, count-ups, marquees or blanket reveals.
- Each page has one motion system, driven by the product's own physics.
- The ten pages use ten different structures: a lab report, a Swiss grid, a video player, a blueprint, a wax-paper wrapper and others.

## 6. The workflow the user approved (run 3)

Do these steps in order. **Do not start designing before step 3 is done.**

### Step 1. Classify from the title
Write one line: *material · who it's for · why they buy · the emotion*. The title's nouns set the category.
- Run 2 should have been: *plush fabric · teens and adults, gifting · comfort and cuteness · "aww"*.
- Run 3 was: *slow-rise TPR · office, classroom, pranksters · the slow dent and the joke · calm, amused*.

### Step 2. Research the product (this is now step one of the real work)
Search the web before touching code. Answer each of these with a source:

| Question | Run 3 answer | What it changed |
|---|---|---|
| What is it, exactly? Material, size, weight. | Solid TPR, not foam; 13.5 cm is the common size | The material-true motion and the spec copy |
| Is there a famous original or brand? | Sold as "Squeezy" by Sunny Days / Schylling | The name: never use "Squeezy" |
| How does it behave and fail? Read owner reviews. | Slow rise; tears if folded or over-stretched; picks up lint; softens in heat | The care copy and the recovery animation |
| Any safety history for the category? | 2018 Danish EPA warning about foam squishies | No "non-toxic" claim; "not food, not for under-3s" |
| Which claims in the listing can't be backed? | "Anxiety relief" | Removed; the Breathe page says "a minute, not a method" |
| What does it look like next to a real reference? | A real US butter stick is about 12.1 × 3.2 cm and 113 g | The True Size comparison |

Useful searches: the title's key nouns plus the size ("butter stick squishy 13.5cm"), plus "review", "tears", "TPR vs foam", "recall", and the category plus "viral".

### Step 3. Find photos of the identical product (the user's new rule)
Find **identical, literally the same product photos** online: the same mould, print and proportions, sold by other shops. The same factory usually supplies many sellers.

**How to confirm a match:**
- The print is the same: the text, typeface and placement match (run 3: "4 OZ. · NET WT. (113 G) · SALTED · BUTTER").
- The listed size, weight and pack options are the same.
- The proportions and edge radius look the same.
- A branded original with different print is **not** identical. Note it as a trademark to avoid, not as a reference.

**Where to look:**
- AliExpress, Temu, Amazon, Walmart, eBay, Etsy and TikTok Shop listings.
- Wholesale and trade listings, which often state exact dimensions.
- Owner photos and videos inside reviews, and TikTok or YouTube clips.
- Reverse image search (Google Lens, Bing Visual Search, TinEye) using the supplier photo, if the user can run it or the environment allows it.

**What the matches are for: a guide, not a source of assets.**
- **For a 3D model:** proportions, edge radius, label layout and typeface, true colour in neutral light, surface finish (gloss or matte). Also how it deforms: videos show how deep a press goes and how long it takes to recover, so the motion can be timed from a real video instead of by eye.
- **For aesthetic product photos:** which angles, props, light and backgrounds make this product look good. Recreate that look with renders, the cleaned supplier photo, or new photography. Don't copy the photo.
- **Publishing them directly:** only with permission. Another seller's photo is that seller's copyright. Ask the user whether their supplier grants rights to the factory photos; if yes, those photos can be cleaned and used.

### Step 4. Judge every image and record the verdict
For each candidate, give a verdict and the reason. Run 3's verdicts:
- **Used:** the user's own supplier photo, cleaned (banner and lines removed, cut out, upscaled).
- **Replaced:** a supplier photo too damaged to fix (the cropped 3-pack).
- **Made:** renders from a 3D model built to the listing's measurements.
- **Rejected:** other sellers' listings (copyright, sometimes a different product or brand) and paid stock (licence needed; shows real butter, not the toy).
- **Candidate:** free-licence images (Unsplash License; CC BY with credit) for context shots, like real butter next to the toy.

### Step 5. Build the product model or the clean photo set
- Run 3 built `butter_pages/assets/butter3d.js`: a deformable three.js stick at true size, with the colour sampled from the photo and the label redrawn. One file gave every page clean, consistent angles and a squeezable product.
- Render stills from the same model for the gallery and packs (front, top, end, pressed, 3-pack, 5-pack), and label them as renders.
- With identical-product references from step 3, the model's proportions, label and recovery timing can match the real product instead of one low-resolution photo.

### Step 6. Design the pages
One signature per page, material-true motion, varied structure (§7).

### Step 7. Show the research in the deliverable
The gallery index carries "What the research changed" (findings and source links) and "Photo judgement" (each image with its verdict). This is the structure the user praised.

## 7. Rules for the next run

0. **Research first** (§6, steps 2–4). Find identical-product photos and use them as the guide for the model and the art direction. Publish other people's photos only with permission.
1. **Classify first.** The title's nouns set the category. If the title says *plush, stuffed, soft, doll, fluffy*, the soft object is the subject, even if it's shaped like something else. The user said they will state the category from now on; still check it against the title.
2. **One signature moment per page, tied to what the product actually is.** For the butter: press, slow rise, prank reveal, real size. Cut generic extras.
3. **Make easing match the material.**
   - Soft and slow-rise things: a fast press (about 0.2 s), then an overdamped recovery with a long tail and no overshoot. Run 3 drove every page from one curve: `d(t) = d0 · (0.3·e^(−t/0.12) + 0.7·e^(−t/1.5))`.
   - Hard things like the blaster: quick, mechanical, a crisp recoil.
   - Vary timing within a page: anticipation, action, follow-through, a pause.
4. **Keep the product photographic.** No flat illustrations of the product next to the photo. A 3D model built at true size and matched to the photo counts as photographic, as long as it's labelled as a render.
5. **Use motion sparingly.** Animate one or two moments well and leave the rest still.
6. **Vary the structure, not just the skin.** At least half of the 10 layouts should break the hero → features → buy → reviews → FAQ order.
7. **Be honest in the page itself.** Label renders, previews, sample prices and reviews, simulated data and synthesized sound. Make no health or safety claims the research can't support. Never use another company's trademark as the product name.
8. **Carry over what worked:** colours sampled from the photo, logo and banner removal, the shared cart kit, testing at three widths, and checking every page in real screenshots before publishing.

## 8. The user's preferences

- Wants the whole set: 10 finished, interactive pages and a gallery, delivered with a link.
- Values exact product colours and getting the product category right.
- **Wants research done before any work**, and wants identical-product photos found and used as the guide for 3D models or product photography.
- Liked seeing the research and the photo decisions laid out in the gallery.
- Prefers a **scroll-driven narrative** (Unwind) over gimmick interactions (claw machine, vending machine), and judges animation on whether it feels *hand-crafted*.
- Gives short, direct feedback. Treat praise as "keep doing this" and complaints as hard rules.
- For pages meant for kids and gifting: friendly tone, safety copy where relevant, no overpromising.

## 9. Environment limits (cloud session)

- Web search works. **Fetching pages and images from many shop and image hosts was blocked** by the environment's network policy in run 3: Unsplash, Pexels, Wikimedia uploads, Pixabay, Imgur, Flickr, plus several shop pages.
- If step 3 needs images and the hosts are blocked, say so early, and offer two options:
  - The user widens network access: the environment menu in the session title bar → Edit → Network access, then a broader level or Custom with the hosts added to Allowed domains. Docs: https://code.claude.com/docs/en/cloud-environments#network-access
  - The user pastes reference photos or listing links directly.
- Don't let a block silently downgrade the research. Record what couldn't be fetched in the photo judgement.

## 10. Useful files

- `butter_pages/index.html`: the gallery with the research and photo-judgement sections. Use it as the template for step 7.
- `butter_pages/assets/butter3d.js`: the deformable 3D product model (press, squeeze, stretch, recovery curve, pose, snapshot). Adapt it for other squeezable products.
- `butter_pages/tools/cut.py`: cuts the product out of a cluttered supplier photo by colour mask.
- `plush_pages/pages/06-scroll-story.html` (Unwind): the scroll-narrative structure the user chose.
- `product_pages/` (Popshell): the reference for how this user wants colour and product framing done.
- `*/assets/kit.js`: the shared cart kit. Change `PRODUCT`, `LAYOUTS` and `img()` per product.
- `plush_pages/tools/` and `product_pages/tools/`: scripts for cutting out the product, removing logos and making colour variants.
