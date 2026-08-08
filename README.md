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
- 不启用 MITM，不安装 Shadowrocket CA。

## 文件结构

```text
shadowrocket-dd/
├── shadowrocket-dd.conf
├── README.md
├── CHANGELOG.md
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

## 为什么默认不是机场 fallback

`⚡ 双机场自动` 会直接在两个机场全部有效节点中挑当前表现较好的节点，日常体验更接近 Mac 上的多 Provider 聚合。

`🛟 双机场容灾` 则保留“白月光主、BoostNet 备”的显式主备逻辑。需要稳定坚持某个机场优先时，可以在 `🚀 主节点` 中手动切到它。

## 维护与安全

机场订阅 URL、Token、Cookie、证书、账号密码等敏感信息**绝不提交 GitHub**。仓库只保存策略逻辑；真实订阅 URL 只保存在 Shadowrocket 本机。

主配置尽量少改。成熟服务规则主要引用 `blackmatrix7/ios_rule_script`；个别例外放进 `rules/`：

- `custom-direct.list`：强制直连
- `custom-proxy.list`：强制走主代理
- `custom-ai.list`：补充 AI 域名
- `custom-reject.list`：自定义屏蔽

每次 push / PR 会运行 `scripts/validate.py`，检查必要区段、重复策略组、规则引用、两个机场订阅筛选以及公开仓库 `[Proxy]` 是否保持为空。

## 在线更新

主配置已设置：

```text
update-url = https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/shadowrocket-dd.conf
```

以后 GitHub 上更新配置后，可以直接在 Shadowrocket 中检查更新，不需要重新维护一份本地配置。

## 上游

- 配置语法与策略组能力参考 `LOWERTOP/Shadowrocket`。
- 服务分流规则主要来自 `blackmatrix7/ios_rule_script`。
