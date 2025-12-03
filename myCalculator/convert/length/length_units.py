"""
长度单位换算模块
实现英尺、英寸与米之间的相互转换
标准换算公式：
1 英尺 = 0.3048 米
1 英寸 = 0.0254 米
1 英尺 = 12 英寸
"""

class LengthConverter:
    """长度单位转换类"""

    # 换算常量
    FOOT_TO_METER = 0.3048
    INCH_TO_METER = 0.0254
    FOOT_TO_INCH = 12.0
    METER_TO_FOOT = 1.0 / FOOT_TO_METER  # 约等于 3.28084
    METER_TO_INCH = 1.0 / INCH_TO_METER  # 约等于 39.3701

    @staticmethod
    def foot_to_meter(feet, inches=0):
        """
        英尺英寸转米

        Args:
            feet: 英尺数
            inches: 英寸数（可选，默认为0）

        Returns:
            米数
        """
        try:
            feet = float(feet)
            inches = float(inches)

            # 检查负数
            if feet < 0 or inches < 0:
                raise ValueError("长度不能为负数")

            # 将英寸转换为英尺
            total_feet = feet + inches / LengthConverter.FOOT_TO_INCH

            # 转换为米
            meters = total_feet * LengthConverter.FOOT_TO_METER

            return meters
        except Exception as e:
            raise ValueError(f"英尺英寸转米错误: {str(e)}")

    @staticmethod
    def meter_to_foot(meters):
        """
        米转英尺英寸

        Args:
            meters: 米数

        Returns:
            包含英尺和英寸的字典 {'feet': x, 'inches': y}
        """
        try:
            meters = float(meters)

            # 检查负数
            if meters < 0:
                raise ValueError("长度不能为负数")

            # 转换为总英尺数
            total_feet = meters * LengthConverter.METER_TO_FOOT

            # 分离整数部分（英尺）和小数部分（英寸）
            feet = int(total_feet)
            remaining_feet = total_feet - feet

            # 将剩余的英尺转换为英寸
            inches = remaining_feet * LengthConverter.FOOT_TO_INCH

            # 四舍五入到小数点后2位
            inches = round(inches, 2)

            return {
                'feet': feet,
                'inches': inches,
                'total_feet': round(total_feet, 6)  # 保留总英尺数供参考
            }
        except Exception as e:
            raise ValueError(f"米转英尺英寸错误: {str(e)}")

    @staticmethod
    def inch_to_meter(inches):
        """
        英寸转米

        Args:
            inches: 英寸数

        Returns:
            米数
        """
        try:
            inches = float(inches)

            # 检查负数
            if inches < 0:
                raise ValueError("长度不能为负数")

            meters = inches * LengthConverter.INCH_TO_METER
            return meters
        except Exception as e:
            raise ValueError(f"英寸转米错误: {str(e)}")

    @staticmethod
    def meter_to_inch(meters):
        """
        米转英寸

        Args:
            meters: 米数

        Returns:
            英寸数
        """
        try:
            meters = float(meters)

            # 检查负数
            if meters < 0:
                raise ValueError("长度不能为负数")

            inches = meters * LengthConverter.METER_TO_INCH
            return round(inches, 6)
        except Exception as e:
            raise ValueError(f"米转英寸错误: {str(e)}")

    @staticmethod
    def foot_to_inch(feet):
        """
        英尺转英寸

        Args:
            feet: 英尺数

        Returns:
            英寸数
        """
        try:
            feet = float(feet)

            # 检查负数
            if feet < 0:
                raise ValueError("长度不能为负数")

            inches = feet * LengthConverter.FOOT_TO_INCH
            return round(inches, 6)
        except Exception as e:
            raise ValueError(f"英尺转英寸错误: {str(e)}")

    @staticmethod
    def inch_to_foot(inches):
        """
        英寸转英尺

        Args:
            inches: 英寸数

        Returns:
            英尺数
        """
        try:
            inches = float(inches)

            # 检查负数
            if inches < 0:
                raise ValueError("长度不能为负数")

            feet = inches / LengthConverter.FOOT_TO_INCH
            return round(feet, 6)
        except Exception as e:
            raise ValueError(f"英寸转英尺错误: {str(e)}")

    @staticmethod
    def convert(value, from_unit, to_unit):
        """
        通用长度转换函数

        Args:
            value: 要转换的数值
            from_unit: 源单位 ('meter', 'foot', 'inch')
            to_unit: 目标单位 ('meter', 'foot', 'inch')

        Returns:
            转换后的数值，如果是转换单位组合，返回字典
        """
        try:
            # 验证输入单位
            valid_units = ['meter', 'foot', 'inch']
            if from_unit not in valid_units or to_unit not in valid_units:
                raise ValueError("不支持的长度单位。支持的单位: meter, foot, inch")

            value = float(value)

            # 检查负数
            if value < 0:
                raise ValueError("长度不能为负数")

            # 如果源单位和目标单位相同，直接返回
            if from_unit == to_unit:
                return value

            # 转换逻辑
            if from_unit == 'meter' and to_unit == 'foot':
                result = LengthConverter.meter_to_foot(value)
                return f"{result['feet']}英尺 {result['inches']}英寸"

            elif from_unit == 'meter' and to_unit == 'inch':
                return LengthConverter.meter_to_inch(value)

            elif from_unit == 'foot' and to_unit == 'meter':
                return LengthConverter.foot_to_meter(value)

            elif from_unit == 'foot' and to_unit == 'inch':
                return LengthConverter.foot_to_inch(value)

            elif from_unit == 'inch' and to_unit == 'meter':
                return LengthConverter.inch_to_meter(value)

            elif from_unit == 'inch' and to_unit == 'foot':
                return LengthConverter.inch_to_foot(value)

            else:
                raise ValueError("不支持的转换类型")

        except Exception as e:
            raise ValueError(f"长度转换错误: {str(e)}")

    @staticmethod
    def get_supported_units():
        """获取支持的长度单位列表"""
        return ['meter', 'foot', 'inch']

    @staticmethod
    def get_conversion_info():
        """获取换算信息"""
        return {
            '1 英尺': '0.3048 米',
            '1 英寸': '0.0254 米',
            '1 英尺': '12 英寸',
            '1 米': f'{LengthConverter.METER_TO_FOOT:.5f} 英尺',
            '1 米': f'{LengthConverter.METER_TO_INCH:.4f} 英寸'
        }

# 创建全局实例
length_converter = LengthConverter()