# Romgoldenage_Bot 多账户24小时循环脚本
wemix公司旗下的链游预注册+签到

注册项目： https://romgoldenage.com/zh-hans/pre-registration

这是一个用于 Romgoldenage 游戏的多账户24小时循环自动化脚本。

## 功能特性

- 🔄 **24小时循环**：自动循环执行每日签到任务
- 👥 **多账户支持**：支持多个账户同时管理
- 🌐 **独立代理**：每个账户对应一个独立代理
- ✅ **一次性任务**：首次运行时自动完成任务2-4
- 📅 **每日签到**：循环执行每日签到任务
- 🎯 **智能判断**：自动识别任务成功/失败状态

## 安装要求

```bash
pip install requests
```

## 快速开始

### 1. 配置设置

1. 配置 `config.json`
2. 为每个账户配置：
   - 登录对应账户
   - 按 F12 打开开发者工具
   - 在 Network 标签页中找到任何请求
   - 在 Request Headers 中找到 Cookie
   - 复制 `JSESSIONID` 和 `AWSALB` 的值
   - 配置该账户专用的代理地址

### 2. 运行脚本

```bash
python bot.py
```

### 3. 选择操作

```
🎮 ROM Golden Age 多账户24小时循环脚本
==================================================
1. 🚀 运行脚本
2. ❌ 退出
==================================================
```

选择选项1运行脚本，将自动启动24小时循环模式：
- 首次运行时为所有账户执行一次性任务
- 然后每小时为所有账户执行签到任务
- 每个账户使用独立的代理

## 配置文件说明

### config.json 结构

```json
{
  "accounts": [
    {
      "name": "账户1",
      "session_id": "你的JSESSIONID_1",
      "awsalb_cookie": "你的AWSALB_Cookie_1",
      "proxy": "http://127.0.0.1:7890",
      "enabled": true
    },
    {
      "name": "账户2",
      "session_id": "你的JSESSIONID_2",
      "awsalb_cookie": "你的AWSALB_Cookie_2",
      "proxy": "http://127.0.0.1:7891",
      "enabled": true
    }
  ],
  "settings": {
    "request_delay": 1,
    "timeout": 30,
    "account_delay": 5,
    "cycle_delay": 3600
  }
}
```
## 代理设置

### 支持的代理类型

- **HTTP 代理**：`http://ip:port`
- **HTTPS 代理**：`https://ip:port`
- **带认证的代理**：`http://username:password@ip:port`
- **SOCKS5 代理**：`socks5://ip:port`

### 常见代理软件端口

- **Clash**：7890
- **V2Ray**：1080
- **Shadowsocks**：1080

## 使用建议

### 24小时循环模式
1. 配置好所有账户信息和代理
2. 运行脚本选择选项 1（运行脚本）
3. 脚本将自动：
   - 首次运行时执行一次性任务
   - 每小时循环执行签到任务
   - 使用 Ctrl+C 停止循环

### 配置管理
手动编辑 `config.json` 文件更新配置：
- 添加/删除账户
- 修改代理设置
- 调整循环间隔时间

## 故障排除

### 常见问题

1. **认证失败**
   - 检查 cookies 是否过期
   - 重新获取 JSESSIONID 和 AWSALB

2. **网络连接失败**
   - 检查网络连接
   - 如果使用代理，确认代理设置正确

3. **任务已完成**
   - 一次性任务只能完成一次
   - 签到每天只能签到一次

### 错误码说明

- `resultCode: "1"` - 操作成功
- `resultCode: "-1"` - 操作失败或已完成

## 文件结构

```
├── bot.py              # 主脚本文件（包含24小时循环功能）
├── config/config.json         # 配置文件
└── README.md          # 说明文档
```

## 注意事项

- 请勿频繁运行脚本，避免对服务器造成压力
- 定期更新 cookies 以保持脚本正常工作
- 使用代理时请确保代理服务器稳定可靠
