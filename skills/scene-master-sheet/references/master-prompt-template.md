# Scene master prompt template

## Skeleton

```
Wide establishing shot of an empty interior, no people.

SPACE: <room type>, <era and region>, <approximate area>, <ceiling height note>. <Where walls, doors and windows sit relative to each other>.

FIXED FURNISHINGS: <large furniture with explicit positions: left / right / center / against the back wall / by the window>.

CONTINUITY PROPS: <3-6 small recurring objects that also date the scene>.

LIGHTING: <dominant source, its position, its color temperature>, <secondary sources demoted>, <resulting time of day>.

PALETTE AND TEXTURE: <3-4 dominant colors>, <saturation and contrast>, <wear and clutter level>, <film texture>.

CAMERA: wide shot, <camera height>, positioned <where>, showing <foreground / mid-ground / what is visible through openings>.

TECHNICAL: photorealistic, no people, empty unoccupied room, no text, no signage, no brand logos, no watermark.
```

## Worked example

Scene: 周父母家客厅, 《潮落之前》第01集 场景1.

```
Wide establishing shot of an empty interior, no people.

SPACE: living room of a late-1990s Chinese apartment in a second-tier provincial capital, two-bedroom unit, about 14 square meters, standard ceiling height. Entrance door on the left wall, a bedroom door on the back wall, a window with thin curtains on the right wall showing dense residential buildings and city lights at night.

FIXED FURNISHINGS: a borrowed folding round dining table set up in the center, nearly filling the room. Mismatched seating around it: two wooden dining chairs, one folding metal stool, two red plastic stools. An old low TV cabinet against the back wall with a small flat television on it. A wooden cupboard in the left corner.

CONTINUITY PROPS: a paper wall calendar hanging on the off-white wall, a bamboo-cased thermos flask in the corner, a plastic tablecloth on the round table, a plug-in power strip with visible cable along the skirting board, a framed family photo on the TV cabinet.

LIGHTING: a single warm-yellow ceiling light as the dominant source, mounted center of the ceiling, soft downward spread, around 2700K. Secondary faint cool glow from the television screen. Night interior, no daylight.

PALETTE AND TEXTURE: off-white walls slightly aged, warm wood tones, dark red and muted brown accents. Low saturation, medium contrast, lived-in clutter, light film grain, soft highlight rolloff.

CAMERA: wide shot, eye level, positioned just inside the entrance looking toward the back wall, showing the round table in the mid-ground, the TV cabinet behind it, and the curtained window with city lights on the right.

TECHNICAL: photorealistic, no people, empty unoccupied room, no text, no signage, no brand logos, no watermark.
```

Negatives for this scene: 乡村土屋、院子、独栋住宅、酒店包间、豪华装修、现代极简、开放式厨房、落地窗、人物、乱码文字、品牌标志、水印.

## Scene bible entry format

After the image is approved, record the locked facts as text. This text is what actually propagates to later shots.

```
## <ID>. <场景名>

- 类型：<room type, era, social register>
- 固定结构：<spatial layout in one sentence>
- 固定陈设：<large furniture with positions>
- 连续性道具：<recurring props>
- 光源：<dominant source, direction, color temperature>
- 色彩关系：<3-4 colors>
- 年代变化：<what changes in later eras, if the scene recurs>
- 基准图：`<path to master png>`
```

Keep each field short. These lines get quoted verbatim into shot prompts, so length directly costs prompt budget.

## Era variants

When a location recurs across years, do not generate a second master. Record the delta in 年代变化 and let shot prompts apply it:

> 2015—2017：暖黄灯、旧桌布、纸质菜单
> 2018—2021：重新装修，增加电子点单牌
> 2024：装饰略旧，菜单改为扫码，但桌椅位置保持一致

Generate a second master only when a renovation changes the spatial layout itself, not merely its surfaces.
