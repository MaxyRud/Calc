# Product page generation: lessons from two runs

**Audience:** another Claude model building product pages for this user.
**Source:** two runs in session `zen-dijkstra-s4z0rc`. The user's feedback is quoted word for word. Everything else is my analysis.

---

## 1. The task

The user runs **js.17**, a studio that builds "AI-generated, awwwards-winning websites". Each request has the same shape:

- **Input:** a marketplace listing (AliExpress), meaning a long SEO-style title plus one or two supplier photos.
- **Ask:** "10 different website layouts for a product page… awwwards winning, tons of animations, interactive components, adjust colours for the product."
- **Output that was accepted:** 10 complete HTML product pages plus a gallery index, published as one Artifact.
  - All pages share one JS kit: cart drawer, bundle pricing, fly-to-cart animation, toasts, an SVG sprite and a layout switcher.
  - The files are in `product_pages/` (run 1) and `plush_pages/` (run 2).

Because the studio sells *AI-made* sites, **anything that looks obviously AI-made hurts their business directly.** Treat "feels like AI" as a defect, not a matter of taste.

## 2. What happened

| | Run 1: toy blaster ("Popshell") | Run 2: soft-drink-can plush ("Zero Can") |
|---|---|---|
| Listing | "2011/M92 Tactical Shell Ejecting Toy Gun … EVA Soft Bullet … Birthday Gift" | "Zero Sugar White [Brand] Energy Drink **Plush Toy** Simulation Can **Stuffed Doll Soft Figure** Decor Gift" |
| What the product really is | A toy blaster for kids. The memorable feature is the brass shell flying out. | A **fluffy stuffed toy** shaped like a can. What sells it is softness, cuteness and comfort. It's bought as a gift or as decor. |
| How I framed it | Correctly: play, action, the shell-eject moment | **Wrongly:** as a *can*. I built vending machine, fridge, drink puns, a nutrition label and a drawn metal can. |
| User verdict | "Popshell is perfect. Perfect… this was kids product and you did exact correct colours and everything." | "Key problem is that it is a fluffy toy." Picked **06 Unwind**, but only for its animation, adding: "you had brilliant ideas there but it still felt this sense of AI with those animations." |

## 3. Why run 1 worked

1. **Colours came straight from the photo.** I sampled them from the product itself: purple slide, lime grip, orange safety tip, brass shell. Each layout used those four in different proportions. The user specifically praised the exact colours.
2. **Every layout was built around the product's one real feature.** That was the shell ejecting, and almost every interaction came back to it: the shooting-range game, the exploded view, the scroll sequence (load → rack → fire).
3. **I got the product category right.** Toy, kids, gift, play. I wrote safety copy (orange tip, eye protection) and the tone matched.
4. **It was honest and polished.**
   - I removed the supplier's logo from the photo.
   - Recoloured variants were labelled "preview".
   - Prices and reviews were labelled "sample".
   - I tested every page at 390, 1024 and 1440 px, with no console errors and no sideways scrolling.

## 4. Why run 2 missed

1. **The category was in the title and I didn't use it.** The title says *Plush Toy, Stuffed Doll, Soft Figure, Decor Gift*. I followed the photo and the brand name ("energy drink can") instead.
   - **Rule:** the title's nouns set the category. The photo sets the look.
   - Before designing anything, write one line: *material · who it's for · why they buy · the emotion*.
   - For run 2 that line should have been: *plush fabric · teens and adults, gifting · comfort and cuteness · "aww"*.
2. **What I built fought the material.**
   - Metal, glass, coins, claws and fridges all say *hard and cold*. The product is *soft and warm*.
   - The one layout the user picked (Unwind) is the one where the can **turns into** the soft toy. It works because it reveals the twist: it's not a can, it's a plush.
3. **The motion was physically wrong for a soft object.** I used `bounce.out` and `back.out` overshoot, plus snappy springs. Those make it read like plastic or rubber. A plush should *sink, sag, and settle slowly*. The motion should have fabric weight.

## 5. What "sense of AI" means here

Most of these patterns are mine from these runs; the reused easing curves are counted from the code below.

- **One motion vocabulary everywhere.** Across 20 pages I reused three easing curves about 85 times: `cubic-bezier(.2,.8,.2,1)` ×51, `(.3,1.6,.5,1)` ×20, `(.3,1.8,.5,1)` ×15. Every element moves with the same feel.
- **The same reveal on every section:** `translateY(60px)` driven by `animation-timeline: view()`. Each page has 15–30 of them.
- **Off-the-shelf "playful" effects:** confetti, sparkle cursor trail, magnetic buttons, scrolling marquee bands, numbers counting up, pill chips, buttons with offset shadows, gradient text.
- **The same page template ten times:** kicker label, huge headline, muted paragraph, then hero, marquee, feature cards, buy panel, three review cards, FAQ. Only the skin changes.
- **Random decoration that doesn't relate to the product:** in Unwind, 26 random bubbles and a comic-style "tssst!" pop-up.
- **A swap instead of a transformation.** In Unwind the flat SVG can squashes and fades out, then the photo plush scales in. It's a cut between two different visual styles (clip-art and photograph), not one object becoming another.
- **Mechanical timing.** Story beats sit on evenly spaced timeline slots, with no anticipation before an action and no pause after it.
- **Gimmicks instead of art direction.** Many clever mechanics (claw game, vending machine, de-fogging glass) but no single crafted moment.

## 6. Rules for the next run

1. **Classify first.** Write the one-line product truth from the title nouns before choosing anything. If the title says *plush, stuffed, soft, doll, fluffy*, the soft object is the subject, even if it's shaped like something else. The user said they will state the category from now on. Still check it against the title.
2. **One signature moment per page, tied to what the product actually is.** For the plush: compression and slow recovery, the fibres of the pile, a hug, the face. Cut generic extras unless the brand needs them.
3. **Make easing match the material.**
   - Soft things: long, damped curves, a little sag, slow settling, and no hard overshoot.
   - Hard things like the blaster: quick, mechanical, a crisp recoil.
   - Vary timing within a page: anticipation, action, follow-through, a pause.
4. **Keep the product photographic.** Don't put flat illustrations of the product next to the photo. If a transformation is needed, morph the same image (masks, displacement, frame sequence) instead of cross-fading between two drawings.
5. **Use motion sparingly.** Animate two or three moments well and leave the rest still. Don't attach a reveal to every block.
6. **Vary the structure, not just the skin.** At least half of the 10 layouts should break the hero → features → buy → reviews → FAQ order.
7. **Carry over what worked:** colours sampled from the photo, removing logos and trademarks from supplier images, labelling previews and sample content, the shared cart kit, testing at three widths, and checking every page in real screenshots before publishing.

## 7. The user's preferences

- Wants the whole set: 10 finished, interactive pages and a gallery, delivered with a link.
- Values exact product colours and getting the product category right.
- Picks a **scroll-driven narrative** (Unwind) over gimmick interactions (claw machine, vending machine), and judges animation on whether it feels *hand-crafted*.
- Gives short, direct feedback. Treat praise as "keep doing this" and complaints as hard rules.
- For pages meant for kids and gifting: friendly tone, safety copy where relevant, no overpromising.

## 8. Useful files

- `plush_pages/pages/06-scroll-story.html` (Unwind): the structure the user chose. Keep the scroll narrative and redo the motion using §5–6.
- `product_pages/` (Popshell): the reference for how this user wants colour and product framing done.
- `*/assets/kit.js`: the shared cart kit. Change `PRODUCT`, `LAYOUTS` and `img()` per product.
- `plush_pages/tools/` and `product_pages/tools/`: scripts for cutting out the product, removing logos and making colour variants.
