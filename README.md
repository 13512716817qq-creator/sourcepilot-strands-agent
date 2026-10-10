# FENIX OS — 手机版国际业务工作台

专为手机设计的无依赖 Progressive Web App (PWA)，方便管理 Mirror Global Group 和其他项目。

## 已开发功能

- 中文移动工作台 / 响应式设计
- 客户 CRM：来源、国家、需求、跟进阶段与联系入口
- 供应商资料库：产地、MOQ、报价、联系方式、核验状态
- 多业务项目：国际贸易、牛油果、公司注册、加纳采购、韩国教育、泰国 TikTok 等
- 任务管理：优先级、截止日、完成状态与项目归属
- 报价及询盘：EXW / FOB / CIF / CFR / DAP，生成可复制英文报价摘要
- 内容发布计划：社交平台、目标市场、文案与时间
- 6 种英文商务沟通模板：采购询价、农场开发、供应商核验等
- 本机浏览器 localStorage 保存数据；JSON 导出和导入
- 安装到手机主屏幕需要稳定 HTTPS 站点；service worker 支持离线缓存

## 隐私与限制

1. 源代码可以公开托管，但**用户新增的数据仅保存在所用浏览器本地**，不会自动上传到 GitHub。
2. 不含账户登录、云同步、服务器加密、团队协作或推送提醒。请不要存储身份证件原件、银行卡信息或密码。
3. 更换设备、清理网站数据、使用无痕模式可能造成数据丢失。推荐每周在“设置与备份”导出 JSON 并妥善保存。
4. 已经内置的项目和待办是参考当前业务编排的**起始规划**，不是系统自动确认的客户、报价或已达成订单；客户/供应商/报价初始为空。
5. 商务英文模板和报价只是草稿，不自动发送，不构成法律、报关、财税或正式技术结论。
6. iOS 安装：使用 Safari 打开正式 HTTPS 网址 → 分享 → 添加到主屏幕。不是原生 App Store / IPA 安装包。

## 部署到 Cloudflare Pages (推荐)

在 GitHub 中为本应用建立一个独立仓库，上传本目录的**所有文件及 icons 子目录**。

Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git → 选择仓库 → Build command 留空 → Output directory 设为根目录 `.`（如果平台要求，可把文件移到 `public/` 并设为 `public`）→ Deploy。

成功后用平台分配的 `*.pages.dev` HTTPS 网址访问。
之后购买 `.com` 域名，在 Pages 自定义域名中绑定；配置 DNS 并验证 HTTPS。

> `raw.githack.com` 仅用于临时预览，不建议长期依赖作为企业生产环境。

## 本地运行

在包含 `index.html` 的目录使用：

```bash
python3 -m http.server 8080
```

在电脑浏览器打开 http://localhost:8080。安装/离线功能需 HTTPS 或 localhost。