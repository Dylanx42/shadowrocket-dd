# Changelog

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
