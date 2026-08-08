# shadowrocket-dd

一套面向长期使用的 Shadowrocket 配置，重点面向多机场、iPhone 主力使用与低维护成本。

## 设计目标

- 多机场 / 多订阅节点统一聚合
- 香港、日本、新加坡、美国、台湾地区节点自动测速
- AI 服务独立固定美国出口，避免 ChatGPT / Claude 等服务频繁切公网 IP
- GitHub / GitLab / Atlassian 独立开发策略
- Google、流媒体、Telegram、社交网络独立分流
- Apple 默认直连
- 广告拦截可一键切回 DIRECT
- 不启用 MITM，不安装 Shadowrocket CA
- 机场订阅 URL 永不进入 GitHub

## 文件结构

```text
shadowrocket-dd/
├── shadowrocket-dd.conf
├── README.md
├── CHANGELOG.md
└── rules/
    ├── custom-direct.list
    ├── custom-proxy.list
    ├── custom-ai.list
    └── custom-reject.list
```

## 第一次使用

1. 在 Shadowrocket 首页分别添加你的机场订阅。
2. 导入 `shadowrocket-dd.conf`。
3. 全局路由选择“配置”。
4. 打开策略组 `🤖 AI固定美国节点`，手工选一条长期稳定的美国节点。
5. `🚀 主节点` 默认使用 `⚡ 全部自动`，会在所有已添加机场的节点中测速选择。
6. 如果某个 App 因广告规则异常，把 `🛡 广告拦截` 临时切到 `DIRECT` 即可排查。

## 安全原则

不要把机场订阅 URL、Token、Cookie、证书、账号密码等敏感信息提交到公开仓库。订阅 URL 通常等同于访问凭据，应该只保存在 Shadowrocket 本机。

## 维护思路

主配置尽量保持稳定；成熟服务规则优先引用上游规则集；个别例外放在 `rules/` 目录中。以后修改自定义域名时，不需要大改主配置。

## 上游规则

主要使用 `blackmatrix7/ios_rule_script` 的 Shadowrocket 规则集。策略组设计参考当前 LOWERTOP/Shadowrocket 的公开配置方式。

## 更新地址

主配置内已设置：

```text
update-url = https://raw.githubusercontent.com/Dylanx42/shadowrocket-dd/main/shadowrocket-dd.conf
```

以后在 GitHub 更新主配置后，可直接在 Shadowrocket 中检查更新。
