# Per-axis vocabulary and worked example

## Vocabulary tables

### 景别 Shot size
特写（面部或手部细节）/ 近景（胸部以上）/ 中景（腰部以上）/ 全景（全身及周边空间）/ 远景（人物在环境中占比小）

### 机位高度 Camera height
平视（人物视线高度）/ 略俯（轻微压迫或旁观）/ 俯拍（孤立、渺小）/ 仰拍（压迫感或强势）/ 齐腰（儿童或物件视角）/ 地面（强调空间）

### 运镜 Camera movement
固定 / 缓推 / 缓拉 / 左右摇 / 上下摇 / 平移 / 跟拍 / 手持轻微晃动 / 环绕 / FPV穿越 / 升降

Mapping intent to movement:

| Intent | Movement |
|---|---|
| 进入情境、建立空间 | 缓推 或 固定 |
| 抽离、结束一段 | 缓拉 |
| 跟随人物动作 | 跟拍 |
| 强调细节或心理变化 | 缓推至特写 |
| 纪实感、临场感 | 手持轻微晃动 |
| 空间穿越、强视觉冲击 | FPV穿越 |

### 光线 Lighting
窗口自然光 / 顶部日光灯 / 暖黄台灯 / 手机屏幕光 / 路灯 / 车灯 / 阴天漫射光

Hardness: 柔光（阴天、纱帘、反射）/ 硬光（直射、点光源）
Direction: 顺光 / 侧光 / 侧逆光 / 逆光 / 顶光 / 底光

### 色调 Color
暖黄（家庭、回忆、旧时代）/ 冷白（办公、医院、制度）/ 日光中性（街道、日常）/ 低饱和冷调（低谷、夜景）

## Worked example

Source: 《潮落之前》第01集 镜00, a 4-second flashback of a one-month-old baby's celebration dinner in a 2013 provincial-capital apartment.

Original storyboard cell:

> 宴席进行中：客厅中央临时支起一张借来的折叠圆桌，几乎占满空间，七八位近亲紧挨着围坐，椅子不成套，靠墙的人贴着墙坐。周母端一盘菜侧身从人背后挤过去上桌，周父站起来举白瓷酒杯敬酒，苏琳抱着襁褓坐在靠里角落。

Expanded to six axes:

```
【镜00】4秒 | 中景（闪回）

■ 关键帧提示词
主体：周父，58岁中国男性，深色夹克内穿深灰色毛衣，身形偏瘦，站立举起白瓷酒杯；周母，56岁，暗红色针织衫，外罩深色围裙，双手端一只白色瓷盘，侧身从座椅背后挤过；苏琳，26岁，米色针织衫，齐肩黑发，产后略显疲惫，坐在靠里角落怀抱浅黄色襁褓；另有五至六位中老年近亲围坐，深色朴素家常衣着。
环境：2013年中国二线省会城市九十年代末商品房，两居室客厅，约十四平方米。中央临时支起一张借来的折叠圆桌，几乎占满空间。椅子不成套：两把木餐椅、一把折叠金属凳、两把红色塑料凳。桌面摆满家常菜盘、一碟红鸡蛋、白瓷酒杯和一瓶散装白酒。背景墙面米白色略旧，挂一本纸质挂历；靠墙立一台旧电视柜，上方电视低声播放；墙角一只竹壳暖水瓶。
光线：室内顶部暖黄吸顶灯为主光源，顶部偏柔，辅以电视屏幕的微弱冷光；整体暖黄，无窗外自然光，室内夜晚。
构图：中景，平视机位，略高于坐姿人物视线，相机位于餐桌斜前方，可同时看到站立的周父与坐在远端的苏琳；人物密度高，画面充满，9:16竖画幅，主要人物置于中央安全区。
色调：暖黄主调，低饱和、中对比，轻微胶片颗粒，高光柔和过渡；木色、暗红、米白构成主要色彩关系。

■ 视频提示词
运镜：固定机位，不移动。
主体运动：周父举杯起身完成敬酒动作，上身微微前倾；周母端盘侧身从人背后挤过，走向桌边放下盘子；围坐亲属有轻微交谈和举杯反应；苏琳低头看怀中婴儿。
时间控制：4秒内周父完成举杯动作，周母完成上菜落盘，其余人物保持自然微动，不完成额外叙事动作。

■ 负面提示词
人物变脸、额外手指、融合手掌、乡村土屋、院子、豪华餐厅、酒店包间、现代极简装修、过度磨皮、乱码文字、现实品牌标志、水印、夸张表情。
```

Note what the expansion added that the original cell lacked: exact garment colors, five named period props, a stated light source and direction, camera height, an explicit palette, and a per-shot negative list targeting this shot's specific risks (院子 and 酒店包间, because the location is a known review point).

## Composite-in-post flags

Current image and video models cannot reliably render Chinese text. Flag these for post-production compositing rather than prompting them:

- 手机屏幕上的消息内容
- 文件、审批表、辞职申请上的文字
- 工牌、员工证上的姓名和单位
- 任何需要观众读懂的数字

Prompt the physical object and leave its surface blank or illegible, then composite the text in editing.
