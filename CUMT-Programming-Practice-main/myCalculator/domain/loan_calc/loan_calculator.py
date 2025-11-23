"""
贷款计算器模块
支持等额本息和等额本金两种还款方式的计算
"""

import math

class LoanCalculator:
    """贷款计算器类"""

    # 还款方式常量
    EQUAL_PAYMENT = "equal_payment"  # 等额本息
    EQUAL_PRINCIPAL = "equal_principal"  # 等额本金

    def __init__(self):
        """初始化贷款计算器"""
        self.loan_amount = 0  # 贷款本金
        self.annual_rate = 0  # 年利率
        self.loan_term_years = 0  # 贷款年限
        self.loan_term_months = 0  # 贷款月数
        self.repayment_method = self.EQUAL_PAYMENT  # 还款方式

    def set_loan_parameters(self, principal, annual_rate, loan_term, term_unit='years'):
        """
        设置贷款参数

        Args:
            principal: 贷款本金
            annual_rate: 年利率（百分比，如5.5表示5.5%）
            loan_term: 贷款期限
            term_unit: 期限单位 ('years' 或 'months')
        """
        try:
            # 验证输入
            self.loan_amount = float(principal)
            if self.loan_amount <= 0:
                raise ValueError("贷款本金必须大于0")

            self.annual_rate = float(annual_rate)
            if self.annual_rate < 0:
                raise ValueError("年利率不能为负数")

            loan_term = float(loan_term)
            if loan_term <= 0:
                raise ValueError("贷款期限必须大于0")

            # 转换为月数
            if term_unit == 'years':
                self.loan_term_years = loan_term
                self.loan_term_months = int(loan_term * 12)
            elif term_unit == 'months':
                self.loan_term_months = int(loan_term)
                self.loan_term_years = loan_term / 12
            else:
                raise ValueError("期限单位必须是 'years' 或 'months'")

        except ValueError as e:
            raise ValueError(f"参数设置错误: {str(e)}")

    def set_repayment_method(self, method):
        """
        设置还款方式

        Args:
            method: 还款方式 ('equal_payment' 或 'equal_principal')
        """
        if method not in [self.EQUAL_PAYMENT, self.EQUAL_PRINCIPAL]:
            raise ValueError("还款方式必须是 'equal_payment' 或 'equal_principal'")
        self.repayment_method = method

    def calculate_equal_payment(self):
        """
        计算等额本息还款

        Returns:
            还款结果字典
        """
        try:
            # 月利率
            monthly_rate = self.annual_rate / 100 / 12

            # 计算月还款额
            if monthly_rate == 0:
                # 无息贷款
                monthly_payment = self.loan_amount / self.loan_term_months
            else:
                # 等额本息月还款额公式
                monthly_payment = (self.loan_amount * monthly_rate *
                                 math.pow(1 + monthly_rate, self.loan_term_months)) / \
                                (math.pow(1 + monthly_rate, self.loan_term_months) - 1)

            # 总还款额和总利息
            total_payment = monthly_payment * self.loan_term_months
            total_interest = total_payment - self.loan_amount

            # 生成还款计划表
            payment_schedule = self._generate_equal_payment_schedule(monthly_payment, monthly_rate)

            return {
                'method': '等额本息',
                'monthly_payment': round(monthly_payment, 2),
                'total_payment': round(total_payment, 2),
                'total_interest': round(total_interest, 2),
                'loan_amount': self.loan_amount,
                'annual_rate': self.annual_rate,
                'loan_term_months': self.loan_term_months,
                'payment_schedule': payment_schedule
            }

        except Exception as e:
            raise ValueError(f"等额本息计算错误: {str(e)}")

    def calculate_equal_principal(self):
        """
        计算等额本金还款

        Returns:
            还款结果字典
        """
        try:
            # 月利率
            monthly_rate = self.annual_rate / 100 / 12

            # 每月偿还本金
            monthly_principal = self.loan_amount / self.loan_term_months

            # 生成还款计划表
            payment_schedule = self._generate_equal_principal_schedule(monthly_principal, monthly_rate)

            # 计算总还款额和总利息
            total_payment = sum(payment['monthly_payment'] for payment in payment_schedule)
            total_interest = total_payment - self.loan_amount

            return {
                'method': '等额本金',
                'monthly_payment': '递减',  # 等额本金月供是递减的
                'first_month_payment': round(payment_schedule[0]['monthly_payment'], 2),
                'last_month_payment': round(payment_schedule[-1]['monthly_payment'], 2),
                'total_payment': round(total_payment, 2),
                'total_interest': round(total_interest, 2),
                'loan_amount': self.loan_amount,
                'annual_rate': self.annual_rate,
                'loan_term_months': self.loan_term_months,
                'payment_schedule': payment_schedule
            }

        except Exception as e:
            raise ValueError(f"等额本金计算错误: {str(e)}")

    def calculate(self):
        """
        根据当前设置的计算方式计算还款信息

        Returns:
            还款结果字典
        """
        if self.repayment_method == self.EQUAL_PAYMENT:
            return self.calculate_equal_payment()
        elif self.repayment_method == self.EQUAL_PRINCIPAL:
            return self.calculate_equal_principal()
        else:
            raise ValueError("未设置的还款方式")

    def compare_methods(self):
        """
        比较两种还款方式

        Returns:
            比较结果字典
        """
        try:
            # 保存当前还款方式
            original_method = self.repayment_method

            # 计算等额本息
            self.repayment_method = self.EQUAL_PAYMENT
            equal_payment_result = self.calculate()

            # 计算等额本金
            self.repayment_method = self.EQUAL_PRINCIPAL
            equal_principal_result = self.calculate()

            # 恢复原始还款方式
            self.repayment_method = original_method

            # 计算利息差额
            interest_difference = (equal_payment_result['total_interest'] -
                                 equal_principal_result['total_interest'])

            return {
                'equal_payment': {
                    'method': '等额本息',
                    'monthly_payment': equal_payment_result['monthly_payment'],
                    'total_payment': equal_payment_result['total_payment'],
                    'total_interest': equal_payment_result['total_interest']
                },
                'equal_principal': {
                    'method': '等额本金',
                    'first_month_payment': equal_principal_result['first_month_payment'],
                    'last_month_payment': equal_principal_result['last_month_payment'],
                    'total_payment': equal_principal_result['total_payment'],
                    'total_interest': equal_principal_result['total_interest']
                },
                'interest_difference': round(interest_difference, 2),
                'recommendation': '等额本金' if interest_difference > 0 else '等额本息'
            }

        except Exception as e:
            raise ValueError(f"还款方式比较错误: {str(e)}")

    def _generate_equal_payment_schedule(self, monthly_payment, monthly_rate):
        """
        生成等额本息还款计划表

        Args:
            monthly_payment: 月还款额
            monthly_rate: 月利率

        Returns:
            还款计划表列表
        """
        schedule = []
        remaining_principal = self.loan_amount

        for month in range(1, self.loan_term_months + 1):
            # 计算当月利息
            month_interest = remaining_principal * monthly_rate

            # 计算当月本金
            month_principal = monthly_payment - month_interest

            # 更新剩余本金
            remaining_principal -= month_principal

            # 处理最后一期的小数误差
            if month == self.loan_term_months:
                month_principal = remaining_principal + month_principal
                remaining_principal = 0
                monthly_payment = month_principal + month_interest

            schedule.append({
                'month': month,
                'monthly_payment': round(monthly_payment, 2),
                'principal': round(month_principal, 2),
                'interest': round(month_interest, 2),
                'remaining_principal': round(max(0, remaining_principal), 2)
            })

        return schedule

    def _generate_equal_principal_schedule(self, monthly_principal, monthly_rate):
        """
        生成等额本金还款计划表

        Args:
            monthly_principal: 月偿还本金
            monthly_rate: 月利率

        Returns:
            还款计划表列表
        """
        schedule = []
        remaining_principal = self.loan_amount

        for month in range(1, self.loan_term_months + 1):
            # 计算当月利息
            month_interest = remaining_principal * monthly_rate

            # 当月总还款额
            total_payment = monthly_principal + month_interest

            # 更新剩余本金
            remaining_principal -= monthly_principal

            schedule.append({
                'month': month,
                'monthly_payment': round(total_payment, 2),
                'principal': round(monthly_principal, 2),
                'interest': round(month_interest, 2),
                'remaining_principal': round(max(0, remaining_principal), 2)
            })

        return schedule

    def format_result(self, result):
        """
        格式化计算结果为可读字符串

        Args:
            result: 计算结果字典

        Returns:
            格式化后的字符串
        """
        try:
            formatted_result = f"\n=== {result['method']}还款计算结果 ===\n"
            formatted_result += f"贷款本金: ¥{result['loan_amount']:,.2f}\n"
            formatted_result += f"年利率: {result['annual_rate']:.2f}%\n"
            formatted_result += f"贷款期限: {result['loan_term_months']}个月\n\n"

            if result['method'] == '等额本息':
                formatted_result += f"月还款额: ¥{result['monthly_payment']:,.2f}\n"
            else:
                formatted_result += f"首月还款额: ¥{result['first_month_payment']:,.2f}\n"
                formatted_result += f"末月还款额: ¥{result['last_month_payment']:,.2f}\n"

            formatted_result += f"总还款额: ¥{result['total_payment']:,.2f}\n"
            formatted_result += f"总利息: ¥{result['total_interest']:,.2f}\n"

            return formatted_result

        except Exception as e:
            return f"格式化结果错误: {str(e)}"

    def get_loan_summary(self):
        """
        获取贷款参数摘要

        Returns:
            参数摘要字符串
        """
        return (f"贷款本金: ¥{self.loan_amount:,.2f}, "
                f"年利率: {self.annual_rate:.2f}%, "
                f"期限: {self.loan_term_years:.1f}年 "
                f"({self.loan_term_months}个月), "
                f"还款方式: {'等额本息' if self.repayment_method == self.EQUAL_PAYMENT else '等额本金'}")

# 创建全局实例
loan_calculator = LoanCalculator()