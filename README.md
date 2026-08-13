# shadowrocket-dd

给 iPhone / iPad Shadowrocket 长期使用的一套双机场配置。目前固定使用两个订阅显示名称：**白月光**、**BoostNet**。

## 当前设计

- `⚡ 双机场自动`：白月光 + BoostNet 所有有效节点统一测速，默认主出口。
- `☁️ 白月光优选`：只在白月光内部自动测速。
- `🅱️ BoostNet优选`：只在 BoostNet 内部自动测速。
- `🛟 双机场容灾`：白月光不可用时 fallback 到 BoostNet，作为显式主备策略备用。
- 香港 / 日本 / 新加坡 / 美国 / 台湾：跨两个机场按地区自动测速。
- `🤖 AI固定美国节点`：手工固定一条美国节点，供 ChatGPT、Claude、Gemini、Copilot、Grok 等 AI 服务长期使用，避免频繁切公网 IP。
- GitHub / GitLab / Atlassian、Google、流媒体、Telegram、社交网络分别分流。
- Apple、Microsoft、国内网络默认直连。
- 广告拦截可一键从 `REJECT` 切到 `DIRECT` 排障。
- 主配置默认不启用 MITM；Apple 天气与地图增强均作为独立可选模块提供。

## 文件结构

```text
shadowrocket-dd/
├── shadowrocket-dd.conf
├── README.md
├── CHANGELOG.md
├── modules/
│   ├── iRingo.WeatherKit.srmodule\n│   └── iRingo.MapKit.srmodule
├── scripts/
│   └── validate.py
├── .github/workflows/
│   └── validate.yml
└── rules/
    ├── custom-direct.list
    ├── custom-proxy.list
    ├── custom-ai.list
    └── custom-reject.list
```

## 第一次使用

1. 在 Shadowrocket 首页添加两个机场订阅，并确保显示名称**准确为** `白月光` 和 `BoostNet`。
2. 导入主配置：

```text
https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/shadowrocket-dd.conf
```

3. Shadowrocket 全局路由选择“配置”。
4. `🚀 主节点` 默认使用 `⚡ 双机场自动`，日常无需手工切换。
5. 打开 `🤖 AI固定美国节点`，手工选择一条长期稳定的美国节点；AI 流量默认跟随它。
6. 如果某 App 出现异常，先把 `🛡 广告拦截` 从 `REJECT` 切为 `DIRECT` 判断是否是广告规则误伤。

## Apple 天气增强模块（可选）

仓库内提供一份适配当前策略组的 iRingo WeatherKit 模块。它只增强 Apple 天气，不替换主配置。

在 Shadowrocket 进入 `配置 → 模块 → 右上角 +`，添加：

```text
https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/modules/iRingo.WeatherKit.srmodule
```

启用模块后，还需要对当前配置开启 HTTPS 解密：

1. 点击当前配置右侧 `ⓘ → HTTPS 解密 → 证书`，生成并安装 Shadowrocket CA。
2. 进入 `系统设置 → 通用 → 关于本机 → 证书信任设置`，信任该证书。
3. 保持 Shadowrocket 全局路由为“配置”，重新连接后打开天气 App 测试。

模块只解密 `weatherkit.apple.com`，并复用主配置已有的 `🚀 主节点`。默认重写端点是 `weatherkit.pages.dev`；如在模块“编辑参数”中改用 `weather.nanocat.cloud`，该备用端点会走 `🚀 主节点`。

该模块源自 `NSRingo/WeatherKit`，当前按上游 v3.2.1 整理。WeatherKit 查询会交由所选 iRingo 重写端点处理，可能包含城市坐标和天气请求参数；不接受这一点时不要启用模块。关闭模块即可恢复原始 Apple 天气请求。

## Apple 地图增强模块（可选）

仓库内提供一份基于 iRingo MapKit Rewrite 版整理的模块，不修改主配置，也不改变现有导航分流。

在 Shadowrocket 进入 `配置 → 模块 → 右上角 +`，添加：

```text
https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/modules/iRingo.MapKit.srmodule
```

启用前需完成上文相同的 Shadowrocket CA 安装与信任步骤。该模块只解密 `configuration.ls.apple.com` 和 `gspe35-ssl.ls.apple.com`，默认使用 `mapkit.pages.dev` 重写端点并保持地图相关数据源直连。

默认效果是保留中国地图日常使用，同时增加国际版 3D 卫星地球、夜景和“四处看看”（Look Around）。启用后彻底关闭地图 App 再重新打开；选择卫星地图并缩小到最远，应能看到地球球体及 ` iRingo: 📍 GEOResourceManifest` 标识。iOS 26 起 Apple 已移除独立的 Flyover 入口，因此 iOS 27 主要验证 3D 卫星图和 Look Around。

## 为什么默认不是机场 fallback

`⚡ 双机场自动` 会直接在两个机场全部有效节点中挑当前表现较好的节点，日常体验更接近 Mac 上的多 Provider 聚合。

`🛟 双机场容灾` 则保留“白月光主、BoostNet 备”的显式主备逻辑。需要稳定坚持某个机场优先时，可以在 `🚀 主节点` 中手动切到它。

## 维护与安全

机场订阅 URL、Token、Cookie、证书、账号密码等敏感信息**绝不提交 GitHub**。仓库只保存策略逻辑；真实订阅 URL 和本机 CA 只保存在 Shadowrocket 本机。

主配置尽量少改。成熟服务规则主要引用 `blackmatrix7/ios_rule_script`；个别例外放进 `rules/`：

- `custom-direct.list`：强制直连
- `custom-proxy.list`：强制走主代理
- `custom-ai.list`：补充 AI 域名
- `custom-reject.list`：自定义屏蔽

每次 push / PR 会运行 `scripts/validate.py`，检查必要区段、重复策略组、规则引用、两个机场订阅筛选、公开仓库 `[Proxy]` 是否保持为空，以及 WeatherKit、MapKit 模块的必要字段与最小 MITM 范围。

## 在线更新

主配置已设置：

```text
update-url = https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/shadowrocket-dd.conf
```

以后 GitHub 上更新配置后，可以直接在 Shadowrocket 中检查更新，不需要重新维护一份本地配置。WeatherKit 与 MapKit 模块都带有本仓库的 `#!url`，安装一次后继续从本仓库更新。

## 上游

- 配置语法与策略组能力参考 `LOWERTOP/Shadowrocket`。
- 服务分流规则主要来自 `blackmatrix7/ios_rule_script`。
- Apple 天气增强逻辑来自 `NSRingo/WeatherKit`，保留原作者署名与上游地址。\n- Apple 地图增强逻辑来自 `NSRingo/MapKit`，保留原作者署名与上游地址。
