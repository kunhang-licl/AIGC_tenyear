# Quad sheet prompt template

Keep the four blocks in this order. Replace every `<...>` placeholder. Delete nothing else.

## Skeleton

```
Character design reference sheet, ONE SQUARE SHEET divided into exactly four equal quadrants in a strict 2x2 grid, two rows and two columns, thin divider lines between quadrants.

SUBJECT (identical person in all four panels): <ethnicity/nationality> <gender>, <age> years old, <height>, <build>, <posture note>. <FACE SHAPE> face shape, <eyelid type> eyes, <eyebrow description>, <nose description>, <mouth description>. <hair description>. <expression/temperament>. <fixed accessory with explicit body side>.

WARDROBE (identical in all four panels): <garment>, <top>, <footwear>, <grooming note>.

QUADRANT LAYOUT (2x2 grid):
TOP-LEFT QUADRANT: frontal head-and-shoulders close-up portrait, FULL HEAD VISIBLE including complete hairline and top of head with margin above, eyes to camera, not cropped.
TOP-RIGHT QUADRANT: full-body side profile view at 90 degrees, entire figure head to feet.
BOTTOM-LEFT QUADRANT: full-body frontal standing view, entire figure head to feet, arms relaxed at sides.
BOTTOM-RIGHT QUADRANT: full-body rear view from directly behind, entire figure head to feet, face not visible, showing back of garment and hair.

TECHNICAL: clean seamless light grey studio background, even soft diffused lighting, consistent shadow direction from upper left in every panel, consistent subject scale and eye-level camera, photorealistic, square 1:1 sheet, each of the three full-body quadrants must show the COMPLETE standing figure from the top of the head down to the SOLES OF BOTH SHOES, feet fully inside the frame, clear empty margin above the head and below the shoes, figure scaled smaller if needed, no text, no labels, no watermark, no extra people.
```

## Worked example

Character: 周启航 (Zhou Qihang), age stage ZQH-B (2016–2018), from a Chinese urban realist drama.

```
Character design reference sheet, ONE SQUARE SHEET divided into exactly four equal quadrants in a strict 2x2 grid, two rows and two columns, thin divider lines between quadrants.

SUBJECT (identical person in all four panels): East Asian Chinese man, 32 years old, 178cm, medium build, straight shoulders. LONG face shape, single-eyelid (monolid) eyes, thick but neat eyebrows, straight nose bridge, mouth corners angled slightly downward. Short side-parted black hair, not dyed. Calm, restrained, reliable expression. Old steel wristwatch on LEFT wrist.

WARDROBE (identical in all four panels): well-fitted dark navy business suit, no visible brand, white dress shirt, dark leather shoes, hair neatly groomed.

QUADRANT LAYOUT (2x2 grid):
TOP-LEFT QUADRANT: frontal head-and-shoulders close-up portrait, FULL HEAD VISIBLE including complete hairline and top of head with margin above, eyes to camera, not cropped.
TOP-RIGHT QUADRANT: full-body side profile view at 90 degrees, entire figure head to feet.
BOTTOM-LEFT QUADRANT: full-body frontal standing view, entire figure head to feet, arms relaxed at sides.
BOTTOM-RIGHT QUADRANT: full-body rear view from directly behind, entire figure head to feet, face not visible, showing back of garment and hair.

TECHNICAL: clean seamless light grey studio background, even soft diffused lighting, consistent shadow direction from upper left in every panel, consistent subject scale and eye-level camera, photorealistic, square 1:1 sheet, each of the three full-body quadrants must show the COMPLETE standing figure from the top of the head down to the SOLES OF BOTH SHOES, feet fully inside the frame, clear empty margin above the head and below the shoes, figure scaled smaller if needed, no text, no labels, no watermark, no extra people.
```

## Writing notes

- Say `2x2 grid`, `two rows and two columns`, and `square sheet` together; any one alone can still produce a single row.
- Use position words (`TOP-LEFT QUADRANT`), never `Panel 1/2/3/4`. Numbering biases the model toward a horizontal strip.
- The close-up sits diagonally opposite the rear view. If the model swaps quadrants, restate the diagonal explicitly.

- Capitalize the single most distinctive facial trait (for example `LONG face shape`) to weight it.
- Always write accessory sides as `LEFT`/`RIGHT` in caps; lowercase sides get dropped.
- For age-stage variants, change only WARDROBE and add explicit state modifiers to SUBJECT such as `visible fatigue under the eyes`, `slightly gaunt`, `a few grey hairs at the temples`. Keep every other word identical.
- Avoid negative-only phrasing for body type. `slim build` works; `not fat` does not.
- Do not request brand names, real logos, or real product interfaces.
