"""
货币换算模块
支持多种货币之间的实时汇率转换
使用ExchangeRate-API获取实时汇率数据
"""

import requests
import json
from datetime import datetime, timedelta
import time

class CurrencyConverter:
    """货币转换类"""

    def __init__(self):
        """初始化货币转换器"""
        # API配置
        self.base_url = "https://api.exchangerate-api.com/v4/latest/"
        self.backup_url = "https://api.fixer.io/latest"  # 备用API

        # 支持的货币代码和名称
        self.supported_currencies = {
            'CNY': {'name': '人民币', 'symbol': '¥'},
            'USD': {'name': '美元', 'symbol': '$'},
            'EUR': {'name': '欧元', 'symbol': '€'},
            'GBP': {'name': '英镑', 'symbol': '£'},
            'JPY': {'name': '日元', 'symbol': '¥'},
            'KRW': {'name': '韩元', 'symbol': '₩'},
            'HKD': {'name': '港币', 'symbol': 'HK$'},
            'CAD': {'name': '加元', 'symbol': 'C$'},
            'AUD': {'name': '澳元', 'symbol': 'A$'},
            'CHF': {'name': '瑞士法郎', 'symbol': 'Fr'}
        }

        # 汇率缓存
        self.rates_cache = {}
        self.cache_timestamp = {}
        self.cache_duration = 3600  # 缓存1小时

        # 网络请求超时时间
        self.timeout = 10

    def get_real_time_rates(self, base_currency='USD'):
        """
        获取实时汇率数据

        Args:
            base_currency: 基准货币代码，默认为USD

        Returns:
            汇率字典或错误信息
        """
        try:
            # 检查缓存是否有效
            current_time = time.time()
            if (base_currency in self.rates_cache and
                base_currency in self.cache_timestamp and
                current_time - self.cache_timestamp[base_currency] < self.cache_duration):
                return {
                    'success': True,
                    'rates': self.rates_cache[base_currency],
                    'cached': True
                }

            # 构建API请求URL
            url = f"{self.base_url}{base_currency}"

            # 发送请求
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()

            if 'rates' not in data:
                raise ValueError("API响应格式错误")

            # 更新缓存
            self.rates_cache[base_currency] = data['rates']
            self.cache_timestamp[base_currency] = current_time

            return {
                'success': True,
                'rates': data['rates'],
                'cached': False,
                'timestamp': data.get('date', datetime.now().strftime('%Y-%m-%d'))
            }

        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求失败: {str(e)}"
            # 如果有缓存数据，返回缓存数据并提示可能不是最新
            if base_currency in self.rates_cache:
                return {
                    'success': True,
                    'rates': self.rates_cache[base_currency],
                    'cached': True,
                    'warning': f'网络连接失败，使用缓存数据。{error_msg}'
                }
            return {'success': False, 'error': error_msg}

        except Exception as e:
            error_msg = f"获取汇率数据失败: {str(e)}"
            if base_currency in self.rates_cache:
                return {
                    'success': True,
                    'rates': self.rates_cache[base_currency],
                    'cached': True,
                    'warning': f'获取最新汇率失败，使用缓存数据。{error_msg}'
                }
            return {'success': False, 'error': error_msg}

    def convert_currency(self, amount, from_currency, to_currency):
        """
        货币转换

        Args:
            amount: 要转换的金额
            from_currency: 源货币代码
            to_currency: 目标货币代码

        Returns:
            转换结果字典
        """
        try:
            # 验证输入
            if not isinstance(amount, (int, float, str)):
                raise ValueError("金额必须是数字")

            try:
                amount = float(amount)
            except ValueError:
                raise ValueError("金额格式错误")

            if amount < 0:
                raise ValueError("金额不能为负数")

            from_currency = from_currency.upper()
            to_currency = to_currency.upper()

            if from_currency not in self.supported_currencies:
                raise ValueError(f"不支持的源货币: {from_currency}")

            if to_currency not in self.supported_currencies:
                raise ValueError(f"不支持的目标货币: {to_currency}")

            # 如果源货币和目标货币相同，直接返回
            if from_currency == to_currency:
                return {
                    'success': True,
                    'result': amount,
                    'rate': 1.0,
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'amount': amount
                }

            # 获取汇率数据
            rates_response = self.get_real_time_rates(from_currency)

            if not rates_response['success']:
                return {
                    'success': False,
                    'error': rates_response['error']
                }

            rates = rates_response['rates']

            if to_currency not in rates:
                raise ValueError(f"无法获取 {to_currency} 的汇率数据")

            # 执行转换
            rate = rates[to_currency]
            result = amount * rate

            return {
                'success': True,
                'result': round(result, 4),
                'rate': round(rate, 6),
                'from_currency': from_currency,
                'to_currency': to_currency,
                'amount': amount,
                'timestamp': rates_response.get('timestamp'),
                'cached': rates_response.get('cached', False),
                'warning': rates_response.get('warning')
            }

        except Exception as e:
            return {
                'success': False,
                'error': f"货币转换失败: {str(e)}"
            }

    def batch_convert(self, amount, from_currency, target_currencies):
        """
        批量货币转换

        Args:
            amount: 要转换的金额
            from_currency: 源货币代码
            target_currencies: 目标货币代码列表

        Returns:
            批量转换结果字典
        """
        try:
            results = {}
            failed_conversions = []

            for target_currency in target_currencies:
                conversion_result = self.convert_currency(amount, from_currency, target_currency)

                if conversion_result['success']:
                    results[target_currency] = {
                        'result': conversion_result['result'],
                        'rate': conversion_result['rate'],
                        'currency_name': self.supported_currencies[target_currency]['name'],
                        'currency_symbol': self.supported_currencies[target_currency]['symbol']
                    }
                else:
                    failed_conversions.append({
                        'currency': target_currency,
                        'error': conversion_result['error']
                    })

            return {
                'success': len(results) > 0,
                'results': results,
                'failed': failed_conversions,
                'total_conversions': len(target_currencies),
                'successful_conversions': len(results)
            }

        except Exception as e:
            return {
                'success': False,
                'error': f"批量转换失败: {str(e)}"
            }

    def get_currency_info(self, currency_code):
        """
        获取货币信息

        Args:
            currency_code: 货币代码

        Returns:
            货币信息字典
        """
        currency_code = currency_code.upper()
        return self.supported_currencies.get(currency_code, None)

    def get_supported_currencies(self):
        """
        获取所有支持的货币列表

        Returns:
            支持的货币列表
        """
        return {
            code: {
                'name': info['name'],
                'symbol': info['symbol']
            }
            for code, info in self.supported_currencies.items()
        }

    def format_result(self, conversion_result):
        """
        格式化转换结果为可读字符串

        Args:
            conversion_result: convert_currency的返回结果

        Returns:
            格式化后的字符串
        """
        if not conversion_result['success']:
            return f"转换失败: {conversion_result['error']}"

        from_info = self.supported_currencies[conversion_result['from_currency']]
        to_info = self.supported_currencies[conversion_result['to_currency']]

        result_str = (f"{from_info['symbol']}{conversion_result['amount']:.2f} "
                     f"({from_info['name']}) = "
                     f"{to_info['symbol']}{conversion_result['result']:.2f} "
                     f"({to_info['name']})")

        if conversion_result.get('cached'):
            result_str += " (使用缓存数据)"

        if conversion_result.get('warning'):
            result_str += f" - {conversion_result['warning']}"

        return result_str

    def clear_cache(self):
        """清除汇率缓存"""
        self.rates_cache.clear()
        self.cache_timestamp.clear()

    def get_cache_info(self):
        """获取缓存信息"""
        info = {}
        for currency, timestamp in self.cache_timestamp.items():
            cache_time = datetime.fromtimestamp(timestamp)
            info[currency] = {
                'cached_time': cache_time.strftime('%Y-%m-%d %H:%M:%S'),
                'age_seconds': int(time.time() - timestamp),
                'is_valid': (time.time() - timestamp) < self.cache_duration
            }
        return info

# 创建全局实例
currency_converter = CurrencyConverter()