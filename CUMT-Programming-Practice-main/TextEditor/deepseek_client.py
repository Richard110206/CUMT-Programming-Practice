#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek API 客户端类
负责与DeepSeek API交互
支持从.env文件读取配置
"""

import os
import requests
from dotenv import load_dotenv


class DeepSeekClient:
    """
    DeepSeek API 客户端类
    负责与DeepSeek API交互
    """
    def __init__(self):
        # 加载.env文件中的环境变量
        load_dotenv()
        
        # 从环境变量读取API密钥和基础URL
        self.api_key = os.getenv("DEEPSEEK_API_KEY", "YOUR_API_KEY_HERE")
        self.base_url = os.getenv("BASE_URL", "https://api.deepseek.com/v1")
        
    def call_api(self, function_type, prompt):
        """
        调用DeepSeek API
        :param function_type: 功能类型 ("文本续写" 或 "文本总结")
        :param prompt: 生成的提示文本
        :return: API返回的结果
        """
        try:
            # 如果API密钥还是默认值，返回模拟数据
            if self.api_key == "YOUR_API_KEY_HERE":
                print("使用模拟数据，因为未配置有效的API密钥")
                # 模拟API返回结果
                if function_type == "文本续写":
                    return f"这是续写的内容。{prompt[:30]}..."
                elif function_type == "文本总结":
                    return f"这是对原文的总结。摘要: 这是一段关于{prompt[:20]}...的文本总结。"
                else:
                    return "未知的功能类型"
            
            # 构建请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            # 构建请求体
            data = {
                "model": "deepseek-chat",  # 使用适合的模型名称
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            # 打印调试信息
            print(f"调用DeepSeek API: 功能={function_type}, URL={self.base_url}")
            
            # 发送API请求
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()  # 检查是否有HTTP错误
            
            # 解析响应
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            print(f"API请求错误: {str(e)}")
            return f"网络请求错误: {str(e)}"
        except KeyError as e:
            print(f"响应解析错误: 缺少字段 {str(e)}")
            return f"API响应格式错误: 缺少必要字段"
        except Exception as e:
            print(f"API调用错误: {str(e)}")
            return f"错误: {str(e)}"
    
    def set_api_key(self, api_key):
        """
        设置API密钥
        :param api_key: 新的API密钥
        """
        self.api_key = api_key
    
    def set_base_url(self, base_url):
        """
        设置API基础URL
        :param base_url: 新的API基础URL
        """
        self.base_url = base_url
    
    def generate_prompt(self, function_type, text_content):
        """
        根据功能类型生成对应的prompt
        :param function_type: 功能类型
        :param text_content: 文本内容
        :return: 生成的prompt
        """
        if function_type == "文本续写":
            return f"请续写以下文本，注意不要使用markdown文本输出，使用文档形式，同时续写内容不要多于50字：{text_content}"
        elif function_type == "文本总结":
            return f"请总结以下文本，注意不要使用markdown文本输出，使用文档形式：{text_content}"
        else:
            return text_content