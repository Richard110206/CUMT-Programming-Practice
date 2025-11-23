"""
进制换算模块
支持十进制、二进制、八进制、十六进制之间的相互转换
"""

class NumberSystemConverter:
    """进制转换类"""

    @staticmethod
    def decimal_to_binary(decimal_num):
        """十进制转二进制"""
        try:
            if isinstance(decimal_num, str):
                decimal_num = float(decimal_num)

            # 处理小数部分
            if isinstance(decimal_num, float) and not decimal_num.is_integer():
                integer_part = int(decimal_num)
                fractional_part = decimal_num - integer_part

                # 转换整数部分
                binary_integer = bin(integer_part)[2:]

                # 转换小数部分（最多8位）
                binary_fractional = NumberSystemConverter._fractional_to_base(
                    fractional_part, 2, 8
                )

                return binary_integer + binary_fractional if binary_fractional else binary_integer
            else:
                return bin(int(decimal_num))[2:]
        except Exception as e:
            raise ValueError(f"十进制转二进制错误: {str(e)}")

    @staticmethod
    def decimal_to_octal(decimal_num):
        """十进制转八进制"""
        try:
            if isinstance(decimal_num, str):
                decimal_num = float(decimal_num)

            # 处理小数部分
            if isinstance(decimal_num, float) and not decimal_num.is_integer():
                integer_part = int(decimal_num)
                fractional_part = decimal_num - integer_part

                # 转换整数部分
                octal_integer = oct(integer_part)[2:]

                # 转换小数部分（最多8位）
                octal_fractional = NumberSystemConverter._fractional_to_base(
                    fractional_part, 8, 8
                )

                return octal_integer + octal_fractional if octal_fractional else octal_integer
            else:
                return oct(int(decimal_num))[2:]
        except Exception as e:
            raise ValueError(f"十进制转八进制错误: {str(e)}")

    @staticmethod
    def decimal_to_hexadecimal(decimal_num):
        """十进制转十六进制"""
        try:
            if isinstance(decimal_num, str):
                decimal_num = float(decimal_num)

            # 处理小数部分
            if isinstance(decimal_num, float) and not decimal_num.is_integer():
                integer_part = int(decimal_num)
                fractional_part = decimal_num - integer_part

                # 转换整数部分
                hex_integer = hex(integer_part)[2:].upper()

                # 转换小数部分（最多8位）
                hex_fractional = NumberSystemConverter._fractional_to_base(
                    fractional_part, 16, 8
                )

                return hex_integer + hex_fractional if hex_fractional else hex_integer
            else:
                return hex(int(decimal_num))[2:].upper()
        except Exception as e:
            raise ValueError(f"十进制转十六进制错误: {str(e)}")

    @staticmethod
    def binary_to_decimal(binary_num):
        """二进制转十进制"""
        try:
            if isinstance(binary_num, str):
                binary_num = binary_num.strip()

            # 检查是否包含小数点
            if '.' in str(binary_num):
                integer_part, fractional_part = str(binary_num).split('.')

                # 转换整数部分
                integer_value = int(integer_part, 2) if integer_part else 0

                # 转换小数部分
                fractional_value = 0
                for i, digit in enumerate(fractional_part):
                    if digit not in '01':
                        raise ValueError(f"二进制数字符 '{digit}' 无效")
                    fractional_value += int(digit) * (2 ** -(i + 1))

                return integer_value + fractional_value
            else:
                return int(str(binary_num), 2)
        except Exception as e:
            raise ValueError(f"二进制转十进制错误: {str(e)}")

    @staticmethod
    def octal_to_decimal(octal_num):
        """八进制转十进制"""
        try:
            if isinstance(octal_num, str):
                octal_num = octal_num.strip()

            # 检查是否包含小数点
            if '.' in str(octal_num):
                integer_part, fractional_part = str(octal_num).split('.')

                # 转换整数部分
                integer_value = int(integer_part, 8) if integer_part else 0

                # 转换小数部分
                fractional_value = 0
                for i, digit in enumerate(fractional_part):
                    if digit < '0' or digit > '7':
                        raise ValueError(f"八进制数字符 '{digit}' 无效")
                    fractional_value += int(digit) * (8 ** -(i + 1))

                return integer_value + fractional_value
            else:
                return int(str(octal_num), 8)
        except Exception as e:
            raise ValueError(f"八进制转十进制错误: {str(e)}")

    @staticmethod
    def hexadecimal_to_decimal(hex_num):
        """十六进制转十进制"""
        try:
            if isinstance(hex_num, str):
                hex_num = hex_num.strip().upper()

            # 检查是否包含小数点
            if '.' in str(hex_num):
                integer_part, fractional_part = str(hex_num).split('.')

                # 转换整数部分
                integer_value = int(integer_part, 16) if integer_part else 0

                # 转换小数部分
                fractional_value = 0
                for i, digit in enumerate(fractional_part):
                    if digit not in '0123456789ABCDEF':
                        raise ValueError(f"十六进制数字符 '{digit}' 无效")
                    hex_digit = int(digit, 16)
                    fractional_value += hex_digit * (16 ** -(i + 1))

                return integer_value + fractional_value
            else:
                return int(str(hex_num), 16)
        except Exception as e:
            raise ValueError(f"十六进制转十进制错误: {str(e)}")

    @staticmethod
    def convert(number, from_base, to_base):
        """通用进制转换函数

        Args:
            number: 要转换的数字（字符串）
            from_base: 源进制（2, 8, 10, 16）
            to_base: 目标进制（2, 8, 10, 16）

        Returns:
            转换后的数字字符串
        """
        try:
            if from_base not in [2, 8, 10, 16] or to_base not in [2, 8, 10, 16]:
                raise ValueError("只支持二进制、八进制、十进制、十六进制之间的转换")

            # 先将源进制转换为十进制
            if from_base == 10:
                decimal_value = float(number) if '.' in str(number) else int(number)
            elif from_base == 2:
                decimal_value = NumberSystemConverter.binary_to_decimal(number)
            elif from_base == 8:
                decimal_value = NumberSystemConverter.octal_to_decimal(number)
            elif from_base == 16:
                decimal_value = NumberSystemConverter.hexadecimal_to_decimal(number)

            # 再将十进制转换为目标进制
            if to_base == 10:
                return str(decimal_value)
            elif to_base == 2:
                return NumberSystemConverter.decimal_to_binary(decimal_value)
            elif to_base == 8:
                return NumberSystemConverter.decimal_to_octal(decimal_value)
            elif to_base == 16:
                return NumberSystemConverter.decimal_to_hexadecimal(decimal_value)

        except Exception as e:
            raise ValueError(f"进制转换错误: {str(e)}")

    @staticmethod
    def _fractional_to_base(fractional, base, max_digits=8):
        """将小数部分转换为指定进制

        Args:
            fractional: 小数部分 (0 <= fractional < 1)
            base: 目标进制
            max_digits: 最大小数位数

        Returns:
            小数部分的字符串表示（不包含小数点）
        """
        if fractional == 0:
            return ""

        result = []
        remaining = fractional

        for _ in range(max_digits):
            remaining *= base
            digit = int(remaining)
            result.append(str(digit) if base < 10 else str(hex(digit))[2:].upper())
            remaining -= digit

            if remaining == 0:
                break

        return '.' + ''.join(result) if result else ""

    @staticmethod
    def validate_number(number_str, base):
        """验证数字字符串是否符合指定进制

        Args:
            number_str: 数字字符串
            base: 进制（2, 8, 10, 16）

        Returns:
            True if valid, False otherwise
        """
        try:
            if base == 2:
                valid_chars = set('01.')
            elif base == 8:
                valid_chars = set('01234567.')
            elif base == 10:
                valid_chars = set('0123456789.')
            elif base == 16:
                valid_chars = set('0123456789ABCDEFabcdef.')
            else:
                return False

            # 检查小数点数量
            if number_str.count('.') > 1:
                return False

            # 检查每个字符
            for char in number_str:
                if char not in valid_chars:
                    return False

            return True
        except:
            return False

# 创建全局实例
number_converter = NumberSystemConverter()