#!/usr/bin/env python3
import requests,time,json,os,random
from colorama import *

# 自定义 User-Agent 列表
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.6",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.2",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.3",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.4",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

# 随机选择一个 User-Agent
user_agent = random.choice(user_agents)

class RomGoldenAgeBot:
    def __init__(self, account_info, settings):
        """
        初始化机器人

        Args:
            account_info: 账户信息字典
            settings: 设置信息字典
        """
        self.account_info = account_info
        self.settings = settings
        self.session = requests.Session()

        # 设置该账户的代理
        if account_info.get('proxy'):
            proxies = {'http': account_info['proxy'], 'https': account_info['proxy']}
            self.session.proxies.update(proxies)

        # 设置基础 headers
        self.base_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://romgoldenage.com',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': user_agent
        }

        # 设置 cookies
        self.cookies = {
            'g_state': '{"i_l":0}',
            'reserved': 'true',
            'i18next': 'en',
            'JSESSIONID': account_info['session_id'],
            'AWSALB': account_info['awsalb_cookie']
        }


    def submit_mission(self, mission_type):
        """
        提交任务

        Args:
            mission_type: 任务类型 (2, 3, 4)

        Returns:
            tuple: (success: bool, message: str, response)
        """
        url = 'https://romgoldenage.com/api/tbmission/en/insert.do'

        headers = self.base_headers.copy()
        headers['referer'] = 'https://romgoldenage.com/event02'

        data = {'type': str(mission_type)}

        try:
            response = self.session.post(
                url,
                headers=headers,
                cookies=self.cookies,
                data=data,
                timeout=self.settings.get('timeout', 30)
            )

            print(f"任务类型 {mission_type} 请求状态: {response.status_code}")

            if response.text:
                try:
                    # 尝试解析 JSON 响应
                    import json
                    result = json.loads(response.text)
                    result_code = result.get('resultCode', None)

                    # resultCode 是字符串格式
                    if result_code == "1":
                        message = f"✅ 任务类型 {mission_type} 提交成功！"
                        success = True
                    elif result_code == "-1":
                        message = f"⚠️ 任务类型 {mission_type} 提交失败：可能已完成或其他错误"
                        success = False
                    else:
                        message = f"❓ 任务类型 {mission_type} 未知结果码: {result_code}"
                        success = False

                    print(f"任务结果: {message}")
                    print(f"完整响应: {response.text}")

                    return success, message, response

                except json.JSONDecodeError:
                    # 如果不是 JSON 格式，直接显示原始响应
                    print(f"任务类型 {mission_type} 响应 (非JSON): {response.text}")
                    return False, f"响应格式异常: {response.text}", response
            else:
                print(f"任务类型 {mission_type} 响应为空")
                return False, "响应为空", response

        except Exception as e:
            error_msg = f"提交任务 {mission_type} 时出错: {e}"
            print(error_msg)
            return False, error_msg, None

    def submit_attendance(self):
        """
        提交签到

        Returns:
            tuple: (success: bool, message: str, response)
        """
        url = 'https://romgoldenage.com/api/tbattendance/en/insert.do'

        headers = self.base_headers.copy()
        headers['referer'] = 'https://romgoldenage.com/event03'
        headers['content-length'] = '0'

        try:
            response = self.session.post(
                url,
                headers=headers,
                cookies=self.cookies,
                timeout=self.settings.get('timeout', 30)
            )

            print(f"签到请求状态: {response.status_code}")

            if response.text:
                try:
                    # 尝试解析 JSON 响应
                    import json
                    result = json.loads(response.text)
                    result_code = result.get('resultCode', None)

                    # resultCode 是字符串格式
                    if result_code == "1":
                        message = "✅ 签到成功！"
                        success = True
                    elif result_code == "-1":
                        message = "⚠️ 签到失败：已经签到过了或者其他错误"
                        success = False
                    else:
                        message = f"❓ 未知结果码: {result_code}"
                        success = False

                    print(f"签到结果: {message}")
                    print(f"完整响应: {response.text}")

                    return success, message, response

                except json.JSONDecodeError:
                    # 如果不是 JSON 格式，直接显示原始响应
                    print(f"签到响应 (非JSON): {response.text}")
                    return False, f"响应格式异常: {response.text}", response
            else:
                print("签到响应为空")
                return False, "响应为空", response

        except Exception as e:
            error_msg = f"提交签到时出错: {e}"
            print(error_msg)
            return False, error_msg, None

    def run_daily_checkin(self):
        """执行每日签到"""
        print("📅 开始执行每日签到...")
        print("=" * 30)

        success, message, _ = self.submit_attendance()

        print("=" * 30)
        if success:
            print("🎉 每日签到完成！")
        else:
            print("⚠️ 签到未成功，请检查状态")

        return success, message

    def run_one_time_missions(self):
        """执行一次性任务 (任务2-4)"""
        print("🎯 开始执行一次性任务...")
        print("=" * 40)

        results = []

        # 提交任务 2, 3, 4 (一次性任务)
        for mission_type in [2, 3, 4]:
            print(f"\n📋 提交一次性任务 {mission_type}...")
            success, message, _ = self.submit_mission(mission_type)
            results.append(('一次性任务', mission_type, success, message))
            time.sleep(self.settings.get('request_delay', 1))  # 等待避免请求过快

        # 显示执行总结
        print("\n" + "=" * 40)
        print("� 一次性任务执行总结:")
        print("-" * 25)

        success_count = 0
        for task_type, task_id, success, message in results:
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {task_type} {task_id}: {message}")

            if success:
                success_count += 1

        print("-" * 25)
        print(f"🎯 成功: {success_count}/{len(results)} 项一次性任务")
        print("🏁 一次性任务执行完成!")

        return results

    def run_all_tasks(self):
        """执行所有任务 (一次性任务 + 每日签到)"""
        print("🚀 开始执行所有任务...")
        print("=" * 50)

        all_results = []

        # 执行一次性任务
        print("\n🎯 第一步：执行一次性任务 (任务2-4)")
        mission_results = self.run_one_time_missions()
        all_results.extend(mission_results)

        print("\n" + "=" * 50)

        # 执行每日签到
        print("\n📅 第二步：执行每日签到")
        checkin_success, checkin_message = self.run_daily_checkin()
        all_results.append(('每日签到', None, checkin_success, checkin_message))

        # 显示总体执行总结
        print("\n" + "=" * 50)
        print("📊 总体执行总结:")
        print("-" * 30)

        success_count = 0
        for task_type, task_id, success, message in all_results:
            status_icon = "✅" if success else "❌"
            if task_type == '每日签到':
                print(f"{status_icon} {task_type}: {message}")
            else:
                print(f"{status_icon} {task_type} {task_id}: {message}")

            if success:
                success_count += 1

        print("-" * 30)
        print(f"🎯 总成功: {success_count}/{len(all_results)} 项任务")
        print("🏁 所有任务执行完成!")

        return all_results


def load_config(config_file='config/config.json'):
    """加载配置文件"""
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"❌ 配置文件不存在: {config_file}")
            return {}
    except Exception as e:
        print(f"❌ 加载配置文件失败: {e}")
        return {}


def run_account_tasks(account, settings, is_first_run=False):
    """运行单个账户的任务"""
    account_name = account.get('name', '未命名账户')

    try:
        print(f"👤 开始处理账户: {account_name}")
        if account.get('proxy'):
            print(f"🌐 使用代理: {account['proxy']}")

        bot = RomGoldenAgeBot(account, settings)

        results = []

        # 首次运行时执行一次性任务
        if is_first_run:
            print("🎯 执行一次性任务...")
            for mission_type in [2, 3, 4]:
                _, message, _ = bot.submit_mission(mission_type)
                results.append(f"任务{mission_type}: {message}")
                time.sleep(settings.get('request_delay', 1))

        # 执行每日签到
        print("📅 执行每日签到...")
        _, message = bot.run_daily_checkin()
        results.append(f"签到: {message}")

        return True, results

    except Exception as e:
        error_msg = f"账户 {account_name} 处理失败: {e}"
        print(f"❌ {error_msg}")
        return False, [error_msg]


def run_24h_cycle():
    """24小时循环运行"""
    print("🚀 启动24小时循环模式")
    print("=" * 50)

    config = load_config()
    if not config:
        return

    accounts = [acc for acc in config.get('accounts', []) if acc.get('enabled', True)]
    settings = config.get('settings', {})

    if not accounts:
        print("❌ 没有找到启用的账户")
        return

    print(f"📋 找到 {len(accounts)} 个启用的账户")

    cycle_count = 0
    is_first_run = True

    try:
        while True:
            cycle_count += 1
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n🔄 第 {cycle_count} 轮循环 - {current_time}")
            print("=" * 50)

            # 处理所有账户
            for i, account in enumerate(accounts, 1):
                print(f"\n[{i}/{len(accounts)}] ", end="")
                _, results = run_account_tasks(account, settings, is_first_run)

                # 显示结果
                for result in results:
                    print(f"  {result}")

                # 账户间延迟
                if i < len(accounts):
                    delay = settings.get('account_delay', 5)
                    print(f"⏳ 等待 {delay} 秒...")
                    time.sleep(delay)

            is_first_run = False  # 第一轮后不再执行一次性任务

            # 循环间延迟
            cycle_delay = settings.get('cycle_delay', 3600)  # 默认1小时
            next_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                    time.localtime(time.time() + cycle_delay))

            print(f"\n✅ 第 {cycle_count} 轮循环完成")
            print(f"😴 等待 {cycle_delay} 秒后开始下一轮...")
            print(f"⏰ 下次运行时间: {next_time}")
            print("=" * 50)

            time.sleep(cycle_delay)

    except KeyboardInterrupt:
        print(f"\n\n👋 用户停止循环，共完成 {cycle_count} 轮")
    except Exception as e:
        print(f"\n❌ 循环出错: {e}")

# 版权
def show_copyright():
    """展示版权信息"""
    copyright_info = f"""{Fore.CYAN}
    *****************************************************
    *           X:https://x.com/ariel_sands_dan         *
    *           Tg:https://t.me/sands0x1                *
    *           Romgoldenage BOT Version 1.0            *
    *           Copyright (c) 2025                      *
    *           All Rights Reserved                     *
    *****************************************************
    """
    {Style.RESET_ALL}
    print(copyright_info)
    print('=' * 50)
    print(f"{Fore.GREEN}申请key: https://661100.xyz/ {Style.RESET_ALL}")
    print(f"{Fore.RED}联系Dandan: \n QQ:712987787 QQ群:1036105927 \n 电报:sands0x1 电报群:https://t.me/+fjDjBiKrzOw2NmJl \n 微信: dandan0x1{Style.RESET_ALL}")
    print('=' * 50)

def main():
    """主函数"""
    show_copyright()
    time.sleep(3)
    print("=" * 50)
    print("1. 🚀 运行脚本")
    print("2. ❌ 退出")
    print("=" * 50)

    try:
        choice = input("请选择操作 (1-2): ").strip()

        if choice == "1":
            run_24h_cycle()
        elif choice == "2":
            print("👋 再见！")
            return
        else:
            print("❌ 无效选择，请输入 1-2")

    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作，再见！")
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")



if __name__ == "__main__":
    main()
