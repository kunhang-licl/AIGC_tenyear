---
name: character-quad-sheet
description: >-
  Generate four-panel character turnaround/reference sheets (四宫格定妆图) showing one
  character from four angles in a single image - frontal close-up, full-body
  front, full-body side profile, and full-body rear. Use when the user asks for
  角色四宫格, 定妆图, 转面图, character turnaround, character reference sheet, multi-angle
  character art, or needs consistent full-angle visual references for a
  character in film, TV, animation, game, or AI-video production. Also use when
  deriving new wardrobe, age-stage, or state variants of
---

# Character Quad Sheet (角色四宫格定妆图)

Produce a single image containing exactly four panels of the same character at four different angles, suitable as a production-grade visual reference.

## Panel layout (fixed 2x2 grid)

The sheet is a square 2x2 grid (田字格), not a single row.

| Position | View | Framing |
|---|---|---|
| Top-left | Frontal close-up | Head and shoulders, eyes to camera, full head including hairline and top of head |
| Top-right | Full-body side profile | True 90-degree profile, head to feet |
| Bottom-left | Full-body front | Head to feet, arms relaxed at sides |
| Bottom-right | Full-body rear | Directly from behind, head to feet, back of garment and hair visible |

Reading order is top-left, top-right, bottom-left, bottom-right. Describe panels by **position words** (`TOP-LEFT PANEL`), not by number: numbered panels tend to be laid out in a row.

Do not reorder, merge, or substitute panels.

## Required quality constraints

Every generated sheet must satisfy all of these. State them explicitly in the prompt:

- **Clean background**: seamless light grey or off-white studio backdrop, no props, no scenery, no gradients that imply a location.
- **Even lighting**: soft diffused studio light, no hard dramatic shadows, no rim-light styling.
- **Consistent shadow direction**: name one direction (default: upper left) and apply it to all four panels.
- **Complete wardrobe and accessories**: identical garment, footwear, and every fixed accessory in all four panels. Accessories must appear on the correct side of the body (for example a watch on the left wrist stays on the left wrist in the front view and appears on the correspondingly mirrored side in the rear view).
- **Consistent scale and camera**: same subject height across panels, eye-level camera, same focal treatment.
- **No text**: no labels, captions, panel numbers, watermarks, or logos. No additional people.

## One baseline sheet per character

Generate **one** quad sheet per character, at the age stage where the character is most often seen. Do not produce a separate sheet for every age stage or story era by default.

Reasons:

- Each extra generation is another chance for the face to drift, since this pipeline carries identity through text only.
- Age stages differ mostly in wardrobe and visible fatigue, which downstream shot prompts can specify in one line.
- A single locked baseline gives the project one unambiguous visual reference.

For a later era, do not regenerate the sheet. Reuse the baseline's SUBJECT paragraph verbatim and append a short ageing modifier, for example `a few grey hairs at the temples, slightly gaunt, visible fatigue under the eyes`. Keep ageing restrained unless the user asks otherwise.

Produce additional sheets only when the user explicitly asks, or when a stage changes the silhouette so much that wardrobe words cannot carry it (for example a uniform replacing a suit).

## Workflow

1. **Collect the character spec.** Identify face shape, eye type, eyebrows, nose, mouth, hair, height, build, posture, fixed accessories, temperament, and the specific age-stage wardrobe. If the project has a visual-consistency document or character bible, read it and use its exact wording. Never invent features that contradict it.
2. **Build the prompt** from `references/prompt-template.md`. Keep the section order: SUBJECT, WARDROBE, PANEL LAYOUT, TECHNICAL. Order matters for panel adherence.
3. **Generate** with `scripts/gen_quad_sheet.sh` (see below).
4. **Inspect the output image before showing it to the user.** Verify panel count, panel order, head not cropped, feet not cropped, identical wardrobe, accessory side correctness, and uniform shadow direction. Regenerate on failure rather than delivering a flawed sheet.
5. **Save** to the project's character asset directory as `<character>_quad.png`. Add an age-stage suffix only when the user asked for multiple stages. Do not overwrite an existing sheet; use a versioned sibling name.

## Generating

```bash
bash scripts/gen_quad_sheet.sh "<full prompt text>" <output-dir>
```

The script wraps the `generate-image` skill's Ducky `gpt-image-2` endpoint. It requires no API key beyond the ambient `ANTHROPIC_AUTH_TOKEN`.

Use `python3`, not `python`, in these environments.

## Critical constraint: this is text-to-image only

The Ducky gateway **silently ignores image inputs**. It accepts `images`, `imageUrls`, and multimodal `chatMessage` fields and returns HTTP 200, but the reference image never reaches the model. Verified by a control test: swapping a male reference for a female reference produced no change in the output.

Consequences:

- Identity continuity rests entirely on the precision of the written facial description. Be specific and repeat the same wording verbatim across every generation for a given character.
- Never claim a sheet was derived from a master image when using this gateway.
- Expect identity drift between separate runs. For a character with a locked master portrait, treat each sheet as an approximation and have the user confirm the face before it becomes canon.
- For true image-to-image derivation, the `imagegen` skill's `scripts/image_gen.py edit` path is required, which needs `OPENAI_API_KEY`.

## Identity consistency tactics

Since only text carries identity, compensate:

- Lead the SUBJECT block with the three or four most distinctive, hard-to-confuse features (face shape, eyelid type, nose, mouth-corner angle).
- Name ethnicity, exact age, and height explicitly; these anchor the model strongly.
- Keep a single canonical SUBJECT paragraph per character and reuse it byte-for-byte across all age stages, varying only the WARDROBE block and explicit age-state modifiers.
- Store the canonical paragraph in the project so later sessions reuse it instead of re-deriving.

## Common failures and fixes

| Symptom | Fix |
|---|---|
| Top of head cropped in Panel 1 | Add `FULL HEAD VISIBLE including complete hairline and top of head with margin above, not cropped` |
| Feet cropped in full-body quadrants | Add `down to the SOLES OF BOTH SHOES, feet fully inside the frame, figure scaled smaller if needed`. Naming shoe soles works better than `head to feet`. |
| Panels collapse to three, or two views repeat | Restate `exactly four equal quadrants in a 2x2 grid` and label each by position on its own line |
| Panels render in one horizontal row | Replace numbered panels with position labels and add `square sheet, two rows and two columns, one thin divider line between quadrants` |
| Close-up and full-body end up in the same row but swapped | Restate the diagonal: close-up TOP-LEFT, profile TOP-RIGHT, front BOTTOM-LEFT, rear BOTTOM-RIGHT |
| Wardrobe shifts between panels | Move wardrobe into its own block prefixed `identical in all four panels` |
| Rear panel shows a turned face | Add `from directly behind, face not visible` |
| Western face when an Asian character is wanted | State nationality and ethnicity in the first clause of SUBJECT |

## References

- `references/prompt-template.md`: fill-in-the-blank prompt skeleton plus a complete worked example.
