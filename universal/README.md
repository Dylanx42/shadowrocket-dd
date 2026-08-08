# Shadowrocket Universal

这是 `shadowrocket-dd` 的通用版配置，目标是：**不要求用户的机场/订阅名称固定，也不需要知道对方订阅叫什么。**

## 与个人版的区别

个人版 `shadowrocket-dd.conf` 会按 `白月光`、`BoostNet` 两个订阅名称做机场级优选与容灾。

通用版完全不写订阅名称，也没有“机场 A / 机场 B / 机场容灾”的概念。策略组直接从 Shadowrocket 当前已经导入的所有代理节点中筛选：

```text
所有订阅/手工节点
      ↓
⚡ 全部自动
      ↓
🚀 主节点
```

地区组同样从全部节点中按节点名称匹配香港、日本、新加坡、美国、台湾、韩国。

## 用户使用步骤

1. 用户先在 Shadowrocket 首页添加自己的一个或多个订阅。
2. 导入通用配置：

```text
https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/universal/shadowrocket-universal.conf
```

3. 全局路由选择 `配置`。
4. `🚀 主节点` 默认使用 `⚡ 全部自动`。
5. 如果使用 ChatGPT / Claude / Gemini 等服务，进入 `🤖 AI固定美国节点`，手工选择一条长期稳定的美国节点。

## 为什么不能自动显示机场名称

Shadowrocket 的静态配置支持：

- 指定已知订阅名称，并使用 `use=true` 筛选该订阅节点；
- 不指定订阅名称，直接通过 `policy-regex-filter` 扫描当前全部节点。

但静态配置本身没有“枚举当前订阅名称并动态创建策略组”的模板/循环能力。因此无法在完全不知道订阅名称的情况下，自动生成“机场 A 优选 / 机场 B 优选”这种组。

通用版选择更稳妥的方式：直接聚合全部节点，不依赖订阅名称。

## 路由原则

- AI / Google 账号与 Google API：固定美国出口，减少同一账号短时间跨多个代理 IP。
- Google 搜索、开发服务、流媒体、Telegram、TikTok/社交：默认全部自动选优。
- Apple / Microsoft / 国内服务：默认直连。
- 不启用 MITM。

## 安全

配置文件不包含机场订阅 URL、Token、Cookie、证书或账号密码。真实订阅仅保存在用户自己的 Shadowrocket 中。
