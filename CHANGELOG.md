# Changelog

## 0.7.0 - 2026-11-11

- 根据 GestaltX GitHub 社区用户贴出的 Apple ChatGPT 扩展“此地区不可用”分流清单补充小火箭规则。
- 新增独立 `🍏 ChatGPT解锁兼容` 策略组，默认跟随固定美国 `🍏 Apple AI`，允许一键切 `DIRECT` 恢复受影响的共用 Apple 域名流量。
- 新增 12 个 Apple 系统 / iCloud / Siri 搜索 / App Store 的域名匹配（包括 `smoot.apple.com`、`gateway.icloud.com`），以及 `chatgpt.com` / `openai.com` 的明确 AI 规则；保留已有 `guzzoni.apple.com` 和 Apple Relay TCP 策略。
- 不照搬过宽的 `DOMAIN-KEYWORD,siri`；不改订阅、不启用 MITM；说明共用域名分流可能干扰国区 iCloud、App Store、定位、系统更新，且无法保证绕过账号或设备的服务端资格限制。

## 0.6.0 - 2026-11-10

- 为主配置增加独立 `🍏 Apple AI` 策略组，默认沿用现有美国固定 AI 出口，普通 `🍎 Apple` 继续默认直连。
- 增加 `🍏 Apple Relay TCP` 手选策略组，两个 Apple Relay 域名和 Apple 官方 `cp4.cloudflare.com` 定向到该组；用户需手动选真正的美国 TCP 节点，不能靠节点名称自动判断传输协议。
- Apple Intelligence Extensions 的 `apple-relay.apple.com`、Siri 的 `guzzoni.apple.com` 定向 `🍏 Apple AI`，保留 ChatGPT 的原有 `🤖 AI服务` 策略。
- Apple AI 精确域名规则置于通用 Apple、广告与自定义规则前。普通 iCloud、App Store、Apple 系统更新、天气/地图可选模块不受此更改影响。
- 不开启 MITM，未修改订阅凭证；增加配置检验与手机操作说明。原帖中的 TCP 解决方式是特定环境的经验，不是 Apple 对所有线路的硬性要求。

## 0.5.0 - 2026-08-14

- 新增独立可选的 `modules/iRingo.MapKit.srmodule`，基于 `NSRingo/MapKit` Rewrite 版整理。
- 保留中国地图日常使用，并启用国际版 3D 卫星地球、夜景及“四处看看”（Look Around）。
- 模块更新地址改为本仓库；默认 `mapkit.pages.dev` 端点直连。
- MapKit 不合并进主配置，只解密 `configuration.ls.apple.com` 与 `gspe35-ssl.ls.apple.com`。
- 校验脚本增加 MapKit 模块结构、更新地址与 MITM 范围检查。

## 0.4.0 - 2026-08-13

- 新增本仓库托管的 `modules/iRingo.WeatherKit.srmodule`，基于 `NSRingo/WeatherKit` v3.2.1。
- 保留上游作者署名、功能参数和重写逻辑，模块更新地址改为 `Dylanx42/shadowrocket-dd`。
- `weatherkit.apple.com` 接入现有 `🚀 主节点`；默认 `weatherkit.pages.dev` 端点直连，备用 `weather.nanocat.cloud` 走主代理。
- WeatherKit 继续作为可选模块，不把 `[MITM]` 合并进主配置；只有启用模块的设备需要安装并信任 Shadowrocket CA。
- 校验脚本增加 WeatherKit 模块结构、更新地址、策略引用和 MITM 范围检查。

## 0.3.0 - 2026-08-08

- 按“敏感服务固定 IP、普通服务双机场自动”的长期使用逻辑重新整理策略。
- `🤖 AI服务` 继续默认使用 `🤖 AI固定美国节点`，用于 OpenAI、Claude、Gemini、Copilot、Grok/xAI 等账号/地区敏感服务。
- Google 搜索与普通 Google Web 流量恢复默认 `🚀 主节点` → `⚡ 双机场自动`。
- 为保证 Gemini App 稳定，把 `accounts.google.com`、`myaccount.google.com`、`oauth2.googleapis.com` 和 `*.googleapis.com` 提前固定到 AI 美国出口。
- `🎬 流媒体`、`📲 Telegram`、`🌐 社交网络`（含 TikTok）、`🐱 开发服务` 默认统一使用双机场自动。
- Apple 官方/系统服务继续默认 `DIRECT`，不额外固定代理 IP。
- `🛟 双机场容灾` 保留为白月光主、BoostNet 备的有序 fallback；`⚡ 双机场自动` 仍为日常默认。
- 从普通策略组中移除 `PROXY`，避免“全局路由=配置”时首页手工选择的默认节点意外参与正常分流。

## 0.2.1 - 2026-08-08

- `🔍 Google` 默认改为跟随 `🤖 AI固定美国节点`。
- 目的：Gemini iOS App 除了 Gemini 专属域名外还会访问通用 Google API，统一出口可减少同一会话跨多个代理 IP 的情况。
- 保留 `🚀 主节点`、`🇺🇸 美国自动` 等为 Google 的手工备选策略。

## 0.2.0 - 2026-08-08

- 正式绑定 Shadowrocket 订阅显示名称：`白月光`、`BoostNet`。
- 新增白月光、BoostNet 各自的 `url-test` 内部优选策略。
- 新增两个机场全节点统一测速 `⚡ 双机场自动`，作为默认主出口。
- 新增 `🛟 双机场容灾`：白月光优先、BoostNet 备用的 `fallback` 策略。
- 地区策略限定在两个机场订阅中筛选，支持香港、日本、新加坡、美国、台湾。
- AI 服务增加 `🤖 AI固定美国节点` 手动固定出口，避免频繁变化公网 IP。
- 加入 OpenAI、Anthropic、Claude、Gemini、Copilot、Grok/xAI 分流。
- 加入开发、流媒体、Telegram、社交、Google、Apple、Microsoft、国内服务和广告分流。
- 增加四个本仓库自定义规则文件，便于后续小范围维护。
- 增加 `scripts/validate.py` 与 GitHub Actions 自动校验。
- `[Proxy]` 保持为空，机场订阅 URL 不进入公开仓库。
- 不启用 MITM / HTTPS 解密。

## 0.1.0 - 2026-08-08

- 初始化 Shadowrocket DD 配置项目。
- 多机场节点聚合设计。
- 地区自动测速策略。
- AI 固定美国出口策略。
- GitHub / GitLab / Google / 流媒体等独立分流设计。
- 不启用 MITM。
- 机场订阅信息不进入仓库。
