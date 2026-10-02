// Group 5 – Cheetah vs Dog: a simple, fully editable deck (native shapes, charts, tables).
const pptxgen = require("pptxgenjs");
const SKILL = "/root/.claude/skills/synced/28712946-eba7-49ab-bd08-63a1cae22e26_96b094df-8a7d-43b7-b404-abddffc5817c/pptx";
const { applyTheme } = require(SKILL + "/scripts/apply_theme.js");

const THEME = {
  name: "Cheetah vs Dog",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2937", lt1: "FFFFFF", dk2: "4B5563", lt2: "F3F4F6",
    accent1: "D97706", // cheetah
    accent2: "0F766E", // dog
    accent3: "B45309", // cheetah text
    accent4: "115E59", // dog text
    accent5: "6B7280", // muted
    accent6: "FEF3C7", // soft highlight
    hlink: "0563C1", folHlink: "954F72",
  },
};
const HEX = { cheetah: "D97706", dog: "0F766E", grid: "E5E7EB", muted: "6B7280" };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.title = "Group 5 – The Cheetah and the Dog";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
const C = pres.SchemeColor;

// ---------- layouts ----------
pres.defineSlideMaster({
  title: "TITLE",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.8, y: 2.2, w: 11.7, h: 1.5, fontSize: 48, bold: true, color: C.text1, align: "left", valign: "bottom" }, text: "Title" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.8, y: 3.85, w: 11.7, h: 1.2, fontSize: 22, color: C.text2, align: "left", valign: "top" }, text: "Subtitle" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.35, w: 12.1, h: 0.9, fontSize: 32, bold: true, color: C.text1, align: "left", valign: "middle" }, text: "Title" } },
  ],
  slideNumber: { x: 12.35, y: 6.95, w: 0.6, h: 0.35, fontSize: 11, color: HEX.muted, align: "right" },
});

// ---------- helpers ----------
// "a_{c} = V^{2}/D"  ->  runs with real subscripts / superscripts (stays editable text)
function m(str, base = {}) {
  const runs = [];
  const re = /(_\{[^}]*\}|\^\{[^}]*\})/g;
  let last = 0, mt;
  while ((mt = re.exec(str))) {
    if (mt.index > last) runs.push({ text: str.slice(last, mt.index), options: { ...base } });
    const kind = mt[0][0] === "_" ? "subscript" : "superscript";
    runs.push({ text: mt[0].slice(2, -1), options: { ...base, [kind]: true } });
    last = re.lastIndex;
  }
  if (last < str.length) runs.push({ text: str.slice(last), options: { ...base } });
  return runs;
}
// several paragraphs; each item is a string or {t, o} with extra options for that line
function para(items, base = {}) {
  const out = [];
  items.forEach((it, i) => {
    const s = typeof it === "string" ? it : it.t;
    const o = { ...base, ...(typeof it === "string" ? {} : it.o) };
    const r = m(s, o);
    if (i < items.length - 1) r[r.length - 1].options.breakLine = true;
    out.push(...r);
  });
  return out;
}
function card(slide, x, y, w, h, fill, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fill }, line: { color: fill }, objectName: name });
}
function resultBox(slide, x, y, w, h, text, name) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.1, fill: { color: C.accent6 }, line: { color: C.accent1, width: 1.5 }, objectName: name });
  slide.addText(m(text, { fontSize: 26, bold: true, color: C.text1 }), { x, y, w, h, align: "center", valign: "middle", isTextBox: true, margin: 0.1 });
}
function newSlide(section, title, layout = "CONTENT") {
  const s = pres.addSlide({ masterName: layout, sectionTitle: section });
  s.addText(typeof title === "string" ? m(title) : title, { placeholder: "title" });
  return s;
}

// =====================================================================
pres.addSection({ title: "Introduction" });
{
  const s = newSlide("Introduction", "The Cheetah and the Dog", "TITLE");
  s.addText("Group 5 · A uniform acceleration problem", { placeholder: "body" });
  // two small "runner" markers as a simple visual
  s.addShape(pres.shapes.OVAL, { x: 0.8, y: 5.6, w: 0.55, h: 0.55, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: "cheetah marker" });
  s.addText("Cheetah", { x: 1.5, y: 5.6, w: 2.0, h: 0.55, fontSize: 18, color: C.accent3, bold: true, valign: "middle", isTextBox: true, margin: 0 });
  s.addShape(pres.shapes.OVAL, { x: 3.6, y: 5.6, w: 0.55, h: 0.55, fill: { color: C.accent2 }, line: { color: C.accent2 }, objectName: "dog marker" });
  s.addText("Dog", { x: 4.3, y: 5.6, w: 2.0, h: 0.55, fontSize: 18, color: C.accent4, bold: true, valign: "middle", isTextBox: true, margin: 0 });
  s.addNotes("Hi everyone, we're Group 5. Our problem is a race between a cheetah and a dog that start together and finish together, but run in very different ways. We'll show how we solved it step by step, check it with real numbers, and look at it on graphs.");
}

{
  const s = newSlide("Introduction", "The problem");
  card(s, 0.6, 1.45, 7.3, 5.2, C.background2, "problem card");
  s.addText(
    "“A cheetah starts from rest and accelerates uniformly as it chases prey, until it reaches its sustainable top speed exactly at the midpoint of the chase, after which it runs at that constant speed for the remainder. A pursuing dog, starting from rest at the same moment, instead accelerates uniformly over the entire distance, covering it in exactly the same total time as the cheetah. Find the ratio of the dog's acceleration to the cheetah's, and determine which animal is moving faster at the end of the chase, and by what factor.”",
    { x: 0.9, y: 1.7, w: 6.7, h: 4.7, fontSize: 17, italic: true, color: C.text1, valign: "top", isTextBox: true, margin: 0, lineSpacingMultiple: 1.15 }
  );
  s.addText("What we need to find", { x: 8.4, y: 1.45, w: 4.3, h: 0.5, fontSize: 22, bold: true, color: C.text1, isTextBox: true, margin: 0 });
  card(s, 8.4, 2.15, 4.3, 1.9, "FFFFFF", "question 1 card");
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.4, y: 2.15, w: 4.3, h: 1.9, rectRadius: 0.12, fill: { color: "FFFFFF" }, line: { color: C.accent1, width: 1.5 }, objectName: "question 1 outline" });
  s.addText(para([{ t: "1", o: { fontSize: 28, bold: true, color: C.accent3 } }, "The ratio of the accelerations", { t: "a_{dog} / a_{cheetah}", o: { bold: true } }], { fontSize: 17, color: C.text1 }),
    { x: 8.65, y: 2.25, w: 3.9, h: 1.7, valign: "top", isTextBox: true, margin: 0 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 8.4, y: 4.45, w: 4.3, h: 2.2, rectRadius: 0.12, fill: { color: "FFFFFF" }, line: { color: C.accent2, width: 1.5 }, objectName: "question 2 outline" });
  s.addText(para([{ t: "2", o: { fontSize: 28, bold: true, color: C.accent4 } }, "Who is moving faster at the end of the chase,", { t: "and by what factor?", o: { bold: true } }], { fontSize: 17, color: C.text1 }),
    { x: 8.65, y: 4.55, w: 3.9, h: 2.0, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("Here's the problem exactly as it was given to us. Two things to find: the ratio of the two accelerations, and which animal is faster at the very end and by how much.");
}

{
  const s = newSlide("Introduction", "Picture the chase");
  const x0 = 2.6, x1 = 12.3, mid = (x0 + x1) / 2;
  // labels for the two lanes
  [[2.15, "Cheetah", C.accent1, C.accent3], [4.45, "Dog", C.accent2, C.accent4]].forEach(([y, name, col, tcol]) => {
    s.addShape(pres.shapes.OVAL, { x: 0.6, y: y - 0.3, w: 0.6, h: 0.6, fill: { color: col }, line: { color: col }, objectName: name + " marker" });
    s.addText(name, { x: 1.3, y: y - 0.3, w: 1.2, h: 0.6, fontSize: 18, bold: true, color: tcol, valign: "middle", isTextBox: true, margin: 0 });
  });
  // cheetah lane: speeding up to the midpoint, then constant speed
  s.addShape(pres.shapes.LINE, { x: x0, y: 2.15, w: mid - x0, h: 0, line: { color: C.accent1, width: 3, dashType: "dash" }, objectName: "cheetah speeding up" });
  s.addShape(pres.shapes.LINE, { x: mid, y: 2.15, w: x1 - mid, h: 0, line: { color: C.accent1, width: 6, endArrowType: "triangle" }, objectName: "cheetah top speed" });
  s.addText(m("speeding up (acceleration a_{c})"), { x: x0, y: 1.45, w: mid - x0, h: 0.5, fontSize: 15, color: C.accent3, align: "center", isTextBox: true, margin: 0 });
  s.addText("constant top speed V", { x: mid, y: 1.45, w: x1 - mid, h: 0.5, fontSize: 15, color: C.accent3, align: "center", isTextBox: true, margin: 0 });
  // dog lane: speeding up the whole way
  s.addShape(pres.shapes.LINE, { x: x0, y: 4.45, w: x1 - x0, h: 0, line: { color: C.accent2, width: 3, dashType: "dash", endArrowType: "triangle" }, objectName: "dog speeding up" });
  s.addText(m("speeding up the whole way (acceleration a_{d})"), { x: x0, y: 3.75, w: x1 - x0, h: 0.5, fontSize: 15, color: C.accent4, align: "center", isTextBox: true, margin: 0 });
  // start / midpoint / finish markers
  [[x0, "Start\n(both at rest)"], [mid, "Midpoint\nD/2"], [x1, "Finish\nD"]].forEach(([x, label], i) => {
    s.addShape(pres.shapes.LINE, { x, y: 1.85, w: 0, h: 3.0, line: { color: "9CA3AF", width: 1, dashType: "sysDot" }, objectName: "marker line " + i });
    s.addText(label, { x: x - 1.0, y: 4.95, w: 2.0, h: 0.75, fontSize: 14, color: C.text2, align: "center", isTextBox: true, margin: 0 });
  });
  card(s, 0.6, 5.95, 12.1, 0.9, C.background2, "key idea card");
  s.addText("Same start, same distance D, same finish time T, but two very different ways of running it.",
    { x: 0.9, y: 5.95, w: 11.5, h: 0.9, fontSize: 18, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
  s.addNotes("This is how we pictured it. Dashed lines mean the animal is speeding up, the thick line means steady speed. The cheetah speeds up only until halfway, then cruises at its top speed V. The dog keeps speeding up all the way. They start at the same moment and cross the finish line at the same moment, at time T.");
}

{
  const s = newSlide("Introduction", "What we know, and the symbols we use");
  s.addText(para([
    { t: "Given in the problem", o: { bold: true, fontSize: 20, color: C.text1 } },
    "Both animals start from rest (u = 0).",
    "Cheetah: uniform acceleration for the first half of the distance, then constant speed V.",
    "Dog: uniform acceleration for the whole distance.",
    "Both cover the same distance D in the same total time T.",
    { t: "Our assumption", o: { bold: true, fontSize: 20, color: C.text1 } },
    "“Midpoint of the chase” means halfway along the distance (D/2).",
  ], { fontSize: 16, color: C.text1, paraSpaceAfter: 8 }), { x: 0.6, y: 1.45, w: 6.4, h: 5.3, valign: "top", isTextBox: true, margin: 0 });
  const H = { bold: true, color: "FFFFFF", fill: { color: "374151" }, fontSize: 16 };
  const row = (sym, meaning) => [{ text: m(sym, { fontSize: 16, bold: true }) }, { text: meaning, options: { fontSize: 16 } }];
  s.addTable([
    [{ text: "Symbol", options: H }, { text: "Meaning", options: H }],
    row("D", "total distance of the chase"),
    row("V", "cheetah's top speed"),
    row("T", "total time of the chase"),
    row("a_{c}", "cheetah's acceleration"),
    row("a_{d}", "dog's acceleration"),
    row("t_{1}", "time for the cheetah to reach V"),
  ], { x: 7.5, y: 1.45, w: 5.2, colW: [1.3, 3.9], rowH: 0.55, border: { type: "solid", color: "D1D5DB", pt: 1 }, color: "1F2937", valign: "middle", objectName: "symbols table" });
  s.addNotes("These are the facts we were given. One thing we had to decide: 'midpoint of the chase' could mean halfway in distance or halfway in time. We took it as halfway in distance, which is the usual meaning. At the end we show what changes if you read it the other way.");
}

{
  const s = newSlide("Introduction", "Our toolbox: the equations of uniform acceleration");
  const eqs = [
    ["v = u + at", "speed after time t"],
    ["s = ut + ½at^{2}", "distance after time t"],
    ["v^{2} = u^{2} + 2as", "speed after distance s"],
  ];
  eqs.forEach(([eq, note], i) => {
    const x = 0.6 + i * 4.1;
    card(s, x, 1.55, 3.8, 2.3, C.background2, "equation card " + (i + 1));
    s.addText(m(eq, { fontSize: 28, bold: true, color: C.text1 }), { x, y: 1.75, w: 3.8, h: 1.1, align: "center", valign: "middle", isTextBox: true, margin: 0 });
    s.addText(note, { x, y: 2.9, w: 3.8, h: 0.7, fontSize: 16, color: C.text2, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  });
  s.addText(para([
    { t: "Both animals start from rest, so u = 0 and the equations get even simpler:", o: { fontSize: 18, color: C.text1 } },
    { t: "v = at        s = ½at^{2}        v^{2} = 2as", o: { fontSize: 24, bold: true, color: C.accent3 } },
    { t: "For the cheetah's steady part we just use  distance = speed × time.", o: { fontSize: 18, color: C.text1 } },
  ], { paraSpaceAfter: 10 }), { x: 0.6, y: 4.3, w: 12.1, h: 2.4, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("These three equations are all we need. Since both animals start from rest, u is zero, so they simplify nicely. For the part where the cheetah runs at a steady speed, it's just distance equals speed times time.");
}

// =====================================================================
pres.addSection({ title: "Solution" });
{
  const s = newSlide("Solution", "Step 1 · The cheetah speeds up (first half)");
  s.addText(para([
    { t: "Distance D/2, starting at 0 and ending at top speed V.", o: { fontSize: 18, color: C.text2 } },
    { t: "Use  v^{2} = 2as :", o: { fontSize: 18, color: C.text1 } },
    { t: "V^{2} = 2 · a_{c} · (D/2) = a_{c} D", o: { fontSize: 24, bold: true, color: C.text1 } },
    { t: "Time to reach top speed, using  v = at :", o: { fontSize: 18, color: C.text1 } },
    { t: "t_{1} = V / a_{c} = D / V", o: { fontSize: 24, bold: true, color: C.text1 } },
  ], { paraSpaceAfter: 12 }), { x: 0.6, y: 1.45, w: 7.0, h: 4.0, valign: "top", isTextBox: true, margin: 0 });
  resultBox(s, 0.6, 4.3, 5.0, 1.1, "a_{c} = V^{2} / D", "cheetah acceleration result");
  card(s, 8.2, 1.45, 4.5, 3.95, C.background2, "plain words card");
  s.addText(para([
    { t: "In plain words", o: { bold: true, fontSize: 20, color: C.accent3 } },
    "The cheetah has to go from standing still to full speed in just half the distance, so it needs a big acceleration: V² divided by D.",
    "Its average speed while speeding up is only V/2, so this half takes time D/V.",
  ], { fontSize: 17, color: C.text1, paraSpaceAfter: 12 }), { x: 8.5, y: 1.7, w: 3.9, h: 3.5, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("First part of the cheetah's run. It covers half the distance while speeding up from zero to V. Using v squared equals 2as, we get a_c equals V squared over D. Then v equals at gives the time for this part: D over V.");
}

{
  const s = newSlide("Solution", "Step 2 · The cheetah at top speed (second half)");
  s.addText(para([
    { t: "Distance D/2 at constant speed V:", o: { fontSize: 18, color: C.text1 } },
    { t: "t_{2} = (D/2) / V = D / (2V)", o: { fontSize: 24, bold: true, color: C.text1 } },
    { t: "Total time of the chase:", o: { fontSize: 18, color: C.text1 } },
    { t: "T = t_{1} + t_{2} = D/V + D/(2V)", o: { fontSize: 24, bold: true, color: C.text1 } },
  ], { paraSpaceAfter: 12 }), { x: 0.6, y: 1.45, w: 6.6, h: 3.3, valign: "top", isTextBox: true, margin: 0 });
  resultBox(s, 0.6, 4.0, 5.0, 1.1, "T = 3D / (2V)", "total time result");
  // distance vs time split bars
  s.addText("Same two halves, measured two ways", { x: 7.6, y: 1.45, w: 5.1, h: 0.5, fontSize: 18, bold: true, color: C.text1, isTextBox: true, margin: 0 });
  s.addText("Distance", { x: 7.6, y: 2.15, w: 5.1, h: 0.4, fontSize: 15, color: C.text2, isTextBox: true, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 7.6, y: 2.6, w: 2.55, h: 0.7, fill: { color: "FDE68A" }, line: { color: "FFFFFF", width: 2 }, objectName: "distance half 1" });
  s.addShape(pres.shapes.RECTANGLE, { x: 10.15, y: 2.6, w: 2.55, h: 0.7, fill: { color: C.accent1 }, line: { color: "FFFFFF", width: 2 }, objectName: "distance half 2" });
  s.addText("½ (speeding up)", { x: 7.6, y: 2.6, w: 2.55, h: 0.7, fontSize: 14, color: C.text1, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  s.addText("½ (top speed)", { x: 10.15, y: 2.6, w: 2.55, h: 0.7, fontSize: 14, color: "FFFFFF", bold: true, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  s.addText("Time", { x: 7.6, y: 3.55, w: 5.1, h: 0.4, fontSize: 15, color: C.text2, isTextBox: true, margin: 0 });
  s.addShape(pres.shapes.RECTANGLE, { x: 7.6, y: 4.0, w: 3.4, h: 0.7, fill: { color: "FDE68A" }, line: { color: "FFFFFF", width: 2 }, objectName: "time part 1" });
  s.addShape(pres.shapes.RECTANGLE, { x: 11.0, y: 4.0, w: 1.7, h: 0.7, fill: { color: C.accent1 }, line: { color: "FFFFFF", width: 2 }, objectName: "time part 2" });
  s.addText("⅔ of T", { x: 7.6, y: 4.0, w: 3.4, h: 0.7, fontSize: 14, color: C.text1, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  s.addText("⅓ of T", { x: 11.0, y: 4.0, w: 1.7, h: 0.7, fontSize: 14, color: "FFFFFF", bold: true, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  s.addText("The first half of the distance takes two-thirds of the time, because the cheetah starts slowly.",
    { x: 7.6, y: 5.0, w: 5.1, h: 1.0, fontSize: 16, italic: true, color: C.text2, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("The second half is easy: steady speed V over a distance D over 2, so it takes D over 2V. Adding both parts, the whole chase takes T equals 3D over 2V. A nice detail: the first half of the distance takes two thirds of the time, because the cheetah starts from standing still.");
}

{
  const s = newSlide("Solution", "Step 3 · The dog speeds up the whole way");
  s.addText(para([
    { t: "The dog covers the whole distance D in the same time T, starting from rest.", o: { fontSize: 18, color: C.text2 } },
    { t: "Use  s = ½at^{2} :", o: { fontSize: 18, color: C.text1 } },
    { t: "D = ½ a_{d} T^{2}   ⟹   a_{d} = 2D / T^{2}", o: { fontSize: 24, bold: true, color: C.text1 } },
    { t: "Put in T = 3D/(2V), so T^{2} = 9D^{2}/(4V^{2}):", o: { fontSize: 18, color: C.text1 } },
    { t: "a_{d} = 2D × 4V^{2} / (9D^{2})", o: { fontSize: 24, bold: true, color: C.text1 } },
  ], { paraSpaceAfter: 12 }), { x: 0.6, y: 1.45, w: 7.4, h: 4.0, valign: "top", isTextBox: true, margin: 0 });
  resultBox(s, 0.6, 4.75, 5.0, 1.1, "a_{d} = 8V^{2} / (9D)", "dog acceleration result");
  card(s, 8.4, 1.45, 4.3, 3.0, C.background2, "dog note card");
  s.addText(para([
    { t: "Why this works", o: { bold: true, fontSize: 20, color: C.accent4 } },
    "We don't know D, V or T as numbers, and we don't need them.",
    "Writing everything in terms of D and V lets the unknowns cancel out in the next step.",
  ], { fontSize: 17, color: C.text1, paraSpaceAfter: 12 }), { x: 8.7, y: 1.7, w: 3.7, h: 2.6, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("Now the dog. It speeds up the whole way and covers D in the same time T. From s equals one half a t squared, a_d equals 2D over T squared. We put in the cheetah's total time and get a_d equals 8 V squared over 9 D. We never needed actual numbers, because everything cancels in the ratio.");
}

{
  const s = newSlide("Solution", "Answer 1 · The ratio of the accelerations");
  s.addText(para([
    { t: "Divide the dog's acceleration by the cheetah's:", o: { fontSize: 18, color: C.text1 } },
    { t: "a_{d} / a_{c} = [8V^{2}/(9D)] ÷ [V^{2}/D]", o: { fontSize: 24, bold: true, color: C.text1 } },
    { t: "V^{2} and D cancel, leaving just a number.", o: { fontSize: 18, color: C.text2 } },
  ], { paraSpaceAfter: 12 }), { x: 0.6, y: 1.45, w: 7.0, h: 2.6, valign: "top", isTextBox: true, margin: 0 });
  card(s, 8.0, 1.45, 4.7, 3.3, C.accent6, "ratio stat card");
  s.addText(m("a_{d} / a_{c}", { fontSize: 22, color: C.text2 }), { x: 8.0, y: 1.6, w: 4.7, h: 0.6, align: "center", isTextBox: true, margin: 0 });
  s.addText("8/9", { x: 8.0, y: 2.15, w: 4.7, h: 1.6, fontSize: 72, bold: true, color: C.accent3, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  s.addText("≈ 0.89", { x: 8.0, y: 3.75, w: 4.7, h: 0.7, fontSize: 24, color: C.text1, align: "center", isTextBox: true, margin: 0 });
  card(s, 0.6, 4.35, 7.0, 2.35, C.background2, "meaning card");
  s.addText(para([
    { t: "What it means", o: { bold: true, fontSize: 20, color: C.text1 } },
    "The dog's acceleration is 8/9 of the cheetah's, about 11 % smaller.",
    "The dog can afford a gentler acceleration because it keeps accelerating for the whole chase, while the cheetah stops halfway.",
  ], { fontSize: 17, color: C.text1, paraSpaceAfter: 8 }), { x: 0.9, y: 4.5, w: 6.4, h: 2.1, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("Here's our first answer. Dividing one acceleration by the other, V squared and D cancel and we're left with 8 over 9, about 0.89. So the dog's acceleration is about 11 percent smaller than the cheetah's. That makes sense: the dog keeps accelerating for the whole chase, so it doesn't need to push as hard.");
}

{
  const s = newSlide("Solution", "Answer 2 · Who is faster at the finish?");
  // two speed cards
  [[0.6, "Cheetah", C.accent1, C.accent3, "V", "It stopped speeding up at halfway, so it finishes at its top speed V."],
   [4.75, "Dog", C.accent2, C.accent4, "4V/3", "v = a_{d} T = [8V^{2}/(9D)] × [3D/(2V)] = 4V/3"]].forEach(([x, name, col, tcol, val, why]) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.45, w: 3.85, h: 3.2, rectRadius: 0.12, fill: { color: "FFFFFF" }, line: { color: col, width: 2 }, objectName: name + " speed card" });
    s.addText(name + "'s final speed", { x: x + 0.25, y: 1.6, w: 3.35, h: 0.5, fontSize: 18, bold: true, color: tcol, isTextBox: true, margin: 0 });
    s.addText(val, { x: x + 0.25, y: 2.1, w: 3.35, h: 1.1, fontSize: 54, bold: true, color: C.text1, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(m(why, { fontSize: 15, color: C.text2 }), { x: x + 0.25, y: 3.3, w: 3.35, h: 1.2, valign: "top", isTextBox: true, margin: 0 });
  });
  card(s, 8.9, 1.45, 3.8, 3.2, C.accent6, "factor stat card");
  s.addText("The dog is faster by", { x: 8.9, y: 1.6, w: 3.8, h: 0.5, fontSize: 18, color: C.text2, align: "center", isTextBox: true, margin: 0 });
  s.addText("4/3", { x: 8.9, y: 2.1, w: 3.8, h: 1.4, fontSize: 72, bold: true, color: C.accent4, align: "center", valign: "middle", isTextBox: true, margin: 0 });
  s.addText("≈ 1.33 (33 % faster)", { x: 8.9, y: 3.6, w: 3.8, h: 0.6, fontSize: 20, color: C.text1, align: "center", isTextBox: true, margin: 0 });
  card(s, 0.6, 4.95, 12.1, 1.75, C.background2, "shortcut card");
  s.addText(para([
    { t: "A quicker way to see it", o: { bold: true, fontSize: 19, color: C.text1 } },
    "Both animals cover D in time T, so both have the same average speed, D/T = 2V/3. For steady acceleration from rest, the final speed is twice the average speed: 2 × 2V/3 = 4V/3.",
  ], { fontSize: 17, color: C.text1, paraSpaceAfter: 6 }), { x: 0.9, y: 5.05, w: 11.5, h: 1.55, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("Second answer. The cheetah stops speeding up at halfway, so it finishes at V. The dog is still speeding up, and by the end it's going at a_d times T, which works out to 4V over 3. So the dog is faster at the finish, by a factor of 4 over 3, about 33 percent. There's also a shortcut: both have the same average speed, and for steady acceleration from rest the final speed is twice the average.");
}

// =====================================================================
pres.addSection({ title: "Graphs and checks" });
{
  const s = newSlide("Graphs and checks", "The speed–time graph");
  s.addChart(pres.charts.SCATTER, [
    { name: "time", values: [0, 2 / 3, 0.75, 1] },
    { name: "Cheetah", values: [0, 1, 1, 1] },
    { name: "Dog", values: [0, 8 / 9, 1, 4 / 3] },
  ], {
    x: 0.6, y: 1.4, w: 7.6, h: 5.4, objectName: "speed-time chart",
    lineSize: 3, lineDataSymbol: "circle", lineDataSymbolSize: 7, chartColors: [HEX.cheetah, HEX.dog],
    showLegend: true, legendPos: "t", legendFontSize: 14, legendFontFace: "+mn-lt",
    valAxisMinVal: 0, valAxisMaxVal: 1.4, valAxisMajorUnit: 0.2, valAxisLabelFormatCode: "0.00",
    catAxisMinVal: 0, catAxisMaxVal: 1, catAxisMajorUnit: 0.25, catAxisLabelFormatCode: "0.00",
    showValAxisTitle: true, valAxisTitle: "speed (as a multiple of V)", valAxisTitleFontSize: 13,
    showCatAxisTitle: true, catAxisTitle: "time (as a fraction of T)", catAxisTitleFontSize: 13,
    valAxisLabelFontSize: 12, catAxisLabelFontSize: 12, valAxisLabelFontFace: "+mn-lt", catAxisLabelFontFace: "+mn-lt",
    valAxisTitleFontFace: "+mn-lt", catAxisTitleFontFace: "+mn-lt",
    valAxisLabelColor: HEX.muted, catAxisLabelColor: HEX.muted,
    valGridLine: { color: HEX.grid, size: 0.75 }, catGridLine: { color: HEX.grid, size: 0.75 },
  });
  s.addText(para([
    { t: "How to read it", o: { bold: true, fontSize: 20, color: C.text1 } },
    "The slope of each line is the acceleration: the dog's line is a little less steep (8/9).",
    "The cheetah's line goes flat at t = 2T/3, when it hits top speed.",
    "The lines cross at t = 3T/4: after that the dog is moving faster.",
    "The area under each line is the distance. Both areas equal 2VT/3 = D, so they finish together.",
  ], { fontSize: 16, color: C.text1, paraSpaceAfter: 10 }), { x: 8.6, y: 1.45, w: 4.1, h: 5.3, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("This is the speed-time graph for both animals. The slope is the acceleration, so the dog's line is slightly less steep. The cheetah's line flattens at two thirds of the time. The lines cross at three quarters of the time, and the dog ends at 4V over 3. The area under each line is the distance, and both areas come out the same, which is why they finish together.");
}

{
  const s = newSlide("Graphs and checks", "Who is ahead during the chase?");
  const xs = [], xc = [], xd = [];
  for (let i = 0; i <= 40; i++) {
    const t = i / 40;
    xs.push(t);
    xc.push(t <= 2 / 3 ? (9 / 8) * t * t : 0.5 + 1.5 * (t - 2 / 3));
    xd.push(t * t);
  }
  s.addChart(pres.charts.SCATTER, [
    { name: "time", values: xs },
    { name: "Cheetah", values: xc },
    { name: "Dog", values: xd },
  ], {
    x: 0.6, y: 1.4, w: 7.6, h: 5.4, objectName: "distance-time chart",
    lineSize: 3, lineDataSymbol: "none", chartColors: [HEX.cheetah, HEX.dog],
    showLegend: true, legendPos: "t", legendFontSize: 14, legendFontFace: "+mn-lt",
    valAxisMinVal: 0, valAxisMaxVal: 1, valAxisMajorUnit: 0.25, valAxisLabelFormatCode: "0.00",
    catAxisMinVal: 0, catAxisMaxVal: 1, catAxisMajorUnit: 0.25, catAxisLabelFormatCode: "0.00",
    showValAxisTitle: true, valAxisTitle: "distance covered (as a fraction of D)", valAxisTitleFontSize: 13,
    showCatAxisTitle: true, catAxisTitle: "time (as a fraction of T)", catAxisTitleFontSize: 13,
    valAxisLabelFontSize: 12, catAxisLabelFontSize: 12, valAxisLabelFontFace: "+mn-lt", catAxisLabelFontFace: "+mn-lt",
    valAxisTitleFontFace: "+mn-lt", catAxisTitleFontFace: "+mn-lt",
    valAxisLabelColor: HEX.muted, catAxisLabelColor: HEX.muted,
    valGridLine: { color: HEX.grid, size: 0.75 }, catGridLine: { color: HEX.grid, size: 0.75 },
  });
  s.addText(para([
    { t: "The cheetah leads the whole way", o: { bold: true, fontSize: 20, color: C.text1 } },
    "It accelerates harder at the start, so it pulls ahead straight away.",
    "Its lead is biggest at t = 3T/4, when both are running at the same speed: D/16 ahead.",
    "After that the faster dog closes the gap and draws level exactly at the finish line.",
  ], { fontSize: 16, color: C.text1, paraSpaceAfter: 10 }), { x: 8.6, y: 1.45, w: 4.1, h: 5.3, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("We also wondered who's actually in front during the race. The cheetah's curve is always above the dog's, so the cheetah leads the whole time. Its lead is biggest at three quarters of the time, when they're moving at the same speed, and it's one sixteenth of the distance. After that the dog is faster and catches up exactly on the finish line.");
}

{
  const s = newSlide("Graphs and checks", "Checking with real numbers");
  s.addText("Example: a 200 m chase, cheetah top speed 30 m/s (108 km/h)", { x: 0.6, y: 1.45, w: 12.1, h: 0.5, fontSize: 18, color: C.text2, isTextBox: true, margin: 0 });
  const H = { bold: true, color: "FFFFFF", fill: { color: "374151" }, fontSize: 16, align: "center" };
  const cell = (t, extra = {}) => ({ text: t, options: { fontSize: 16, align: "center", ...extra } });
  s.addTable([
    [{ text: "", options: H }, { text: "Cheetah", options: { ...H, fill: { color: HEX.cheetah } } }, { text: "Dog", options: { ...H, fill: { color: HEX.dog } } }],
    [cell("Distance", { align: "left", bold: true }), cell("200 m"), cell("200 m")],
    [cell("Acceleration", { align: "left", bold: true }), cell("V²/D = 4.5 m/s²"), cell("2D/T² = 4.0 m/s²")],
    [cell("Time to top speed", { align: "left", bold: true }), cell("V/a = 6.67 s"), cell("never stops speeding up")],
    [cell("Total time", { align: "left", bold: true }), cell("6.67 s + 3.33 s = 10 s"), cell("10 s")],
    [cell("Speed at the finish", { align: "left", bold: true }), cell("30 m/s"), cell("4.0 × 10 = 40 m/s")],
  ], { x: 0.6, y: 2.1, w: 8.2, colW: [2.6, 2.8, 2.8], rowH: 0.6, border: { type: "solid", color: "D1D5DB", pt: 1 }, color: "1F2937", valign: "middle", objectName: "numbers table" });
  card(s, 9.2, 2.1, 3.5, 1.9, C.accent6, "check card");
  s.addText(para([
    { t: "Ratios check out", o: { bold: true, fontSize: 19, color: C.text1 } },
    "4.0 / 4.5 = 0.889 = 8/9 ✓",
    "40 / 30 = 1.33 = 4/3 ✓",
  ], { fontSize: 18, color: C.text1, paraSpaceAfter: 10 }), { x: 9.45, y: 2.3, w: 3.1, h: 1.6, valign: "top", isTextBox: true, margin: 0 });
  s.addText("Fun fact: no real dog can reach 40 m/s (144 km/h); greyhounds top out at around 20 m/s. So in real life the cheetah would win easily, but the maths doesn't care!",
    { x: 0.6, y: 6.0, w: 12.1, h: 0.8, fontSize: 15, italic: true, color: C.text2, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("To make sure our algebra was right, we tried real numbers: a 200 metre chase with a cheetah top speed of 30 metres per second, which is realistic. Everything checks: the accelerations are 4.5 and 4.0, ratio 8 over 9, and the final speeds are 30 and 40, ratio 4 over 3. The funny part is that no real dog can run 40 metres per second, so in real life the cheetah wins easily.");
}

// =====================================================================
pres.addSection({ title: "Summary" });
{
  const s = newSlide("Summary", "Summary");
  [[0.6, "Ratio of accelerations", m("a_{d} / a_{c} = 8/9 ≈ 0.89", { fontSize: 30, bold: true, color: C.accent3 }), "The dog accelerates about 11 % less than the cheetah.", C.accent1],
   [6.85, "Faster at the finish", [{ text: "Dog, by 4/3 ≈ 1.33", options: { fontSize: 30, bold: true, color: C.accent4 } }], "The dog ends at 4V/3, the cheetah at V.", C.accent2]].forEach(([x, head, big, small, col]) => {
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.45, w: 5.85, h: 2.4, rectRadius: 0.12, fill: { color: "FFFFFF" }, line: { color: col, width: 2 }, objectName: head + " card" });
    s.addText(head, { x: x + 0.3, y: 1.6, w: 5.25, h: 0.5, fontSize: 18, color: C.text2, isTextBox: true, margin: 0 });
    s.addText(big, { x: x + 0.3, y: 2.15, w: 5.25, h: 0.9, valign: "middle", isTextBox: true, margin: 0 });
    s.addText(small, { x: x + 0.3, y: 3.1, w: 5.25, h: 0.6, fontSize: 16, color: C.text1, isTextBox: true, margin: 0 });
  });
  card(s, 0.6, 4.2, 12.1, 2.5, C.background2, "takeaways card");
  s.addText(para([
    { t: "What we learned", o: { bold: true, fontSize: 20, color: C.text1 } },
    { t: "Same distance and same time doesn't mean the same motion: the cheetah leads all the way, but the dog finishes faster.", o: { bullet: true } },
    { t: "Writing everything in symbols (D, V, T) let the unknowns cancel, so the answers don't depend on the actual numbers.", o: { bullet: true } },
    { t: "Graphs help: the area under a speed–time graph is the distance, and the slope is the acceleration.", o: { bullet: true } },
  ], { fontSize: 17, color: C.text1, paraSpaceAfter: 8 }), { x: 0.9, y: 4.35, w: 11.5, h: 2.25, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("To sum up: the ratio of the dog's acceleration to the cheetah's is 8 over 9, and the dog is faster at the finish by a factor of 4 over 3. Even though they start and finish together, they move very differently, and drawing graphs helped us see why. Thanks for listening, any questions?");
}

{
  const s = newSlide("Summary", "Backup · What if “midpoint” meant halfway in time?");
  s.addText(para([
    { t: "If the cheetah reached top speed at t = T/2 instead of at D/2:", o: { fontSize: 18, color: C.text1 } },
    { t: "a_{c} = V / (T/2) = 2V/T", o: { fontSize: 22, bold: true, color: C.text1 } },
    { t: "D = ½ · V · (T/2) + V · (T/2) = 3VT/4", o: { fontSize: 22, bold: true, color: C.text1 } },
    { t: "a_{d} = 2D / T^{2} = 3V / (2T)", o: { fontSize: 22, bold: true, color: C.text1 } },
  ], { paraSpaceAfter: 12 }), { x: 0.6, y: 1.45, w: 7.4, h: 3.6, valign: "top", isTextBox: true, margin: 0 });
  card(s, 8.4, 1.45, 4.3, 2.2, C.background2, "alternative results card");
  s.addText(para([
    { t: "Results in that case", o: { bold: true, fontSize: 19, color: C.text1 } },
    "a_{d} / a_{c} = 3/4",
    "Dog faster at the end by 3/2",
  ], { fontSize: 20, color: C.text1, paraSpaceAfter: 12 }), { x: 8.7, y: 1.7, w: 3.8, h: 1.8, valign: "top", isTextBox: true, margin: 0 });
  s.addText("We used the distance meaning in our main answer, because the problem talks about covering the distance. The method is exactly the same either way.",
    { x: 0.6, y: 4.6, w: 12.1, h: 1.0, fontSize: 16, italic: true, color: C.text2, valign: "top", isTextBox: true, margin: 0 });
  s.addNotes("Only if someone asks: 'midpoint' could also be read as halfway in time. Then the ratio would be 3 over 4 and the dog would be faster by a factor of 3 over 2. Same method, different numbers. We used the distance reading in our main answer.");
}

(async () => {
  await pres.writeFile({ fileName: "Group5_Cheetah_vs_Dog.pptx" });
  await applyTheme("Group5_Cheetah_vs_Dog.pptx", THEME);
  console.log("written");
})();
