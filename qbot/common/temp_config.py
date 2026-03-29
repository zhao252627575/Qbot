#! /usr/bin/env python
# -*- encoding: utf-8 -*-
"""
临时配置存储模块
用于存储临时性的敏感信息（如API Key、密码等）
程序关闭后这些信息将丢失
"""

import os
import logging

logger = logging.getLogger(__name__)

# 全局临时存储字典
_temp_storage = {
    "tushare_api_key": None,
    "postgresql_config": None,
    "csv_path": None
}

# 临时文件路径（程序退出时删除）
_temp_files = []


def set_tushare_api_key(api_key):
    """设置Tushare API Key（临时存储）"""
    _temp_storage["tushare_api_key"] = api_key
    logger.info("Tushare API Key 已设置（临时存储）")


def get_tushare_api_key():
    """获取Tushare API Key"""
    # 首先尝试从内存获取
    if _temp_storage["tushare_api_key"]:
        return _temp_storage["tushare_api_key"]
    
    # 尝试从临时文件读取
    try:
        temp_file = os.path.join(os.path.dirname(__file__), "configs", "temp_tushare_token.txt")
        if os.path.exists(temp_file):
            with open(temp_file, "r", encoding="utf-8") as f:
                api_key = f.read().strip()
                _temp_storage["tushare_api_key"] = api_key
                return api_key
    except Exception as e:
        logger.warning(f"读取临时token文件失败: {e}")
    
    return None


def clear_tushare_api_key():
    """清除Tushare API Key"""
    _temp_storage["tushare_api_key"] = None
    # 删除临时文件
    try:
        temp_file = os.path.join(os.path.dirname(__file__), "configs", "temp_tushare_token.txt")
        if os.path.exists(temp_file):
            os.remove(temp_file)
            logger.info("Tushare API Key 临时文件已删除")
    except Exception as e:
        logger.warning(f"删除临时token文件失败: {e}")


def set_postgresql_config(config):
    """设置PostgreSQL配置（临时存储密码）"""
    _temp_storage["postgresql_config"] = config
    logger.info(f"PostgreSQL配置已设置: {config.get('host')}/{config.get('database')}")


def get_postgresql_config():
    """获取PostgreSQL完整配置（包含密码）"""
    return _temp_storage.get("postgresql_config")


def set_csv_path(path):
    """设置CSV存储路径"""
    _temp_storage["csv_path"] = path
    logger.info(f"CSV存储路径已设置: {path}")


def get_csv_path():
    """获取CSV存储路径"""
    return _temp_storage.get("csv_path")


def get_data_store_config():
    """获取数据存储配置"""
    from qbot.gui.common.SysFile import Base_File_Oper
    
    sys_para = Base_File_Oper.load_sys_para("sys_para.json")
    data_store = sys_para.get("data_store_config", {})
    
    store_type = data_store.get("type")
    
    if store_type == "csv":
        return {
            "type": "csv",
            "path": get_csv_path() or data_store.get("path")
        }
    elif store_type == "mysql":
        mysql_config = get_mysql_config()
        if mysql_config:
            return {
                "type": "mysql",
                "config": mysql_config
            }
        return data_store
    
    return data_store


def cleanup_temp_files():
    """清理所有临时文件（程序退出时调用）"""
    temp_token_file = os.path.join(os.path.dirname(__file__), "configs", "temp_tushare_token.txt")
    if os.path.exists(temp_token_file):
        try:
            os.remove(temp_token_file)
            logger.info("清理临时token文件")
        except Exception as e:
            logger.warning(f"清理临时文件失败: {e}")


def query_mysql_data(config=None, limit=100):
    """
    从MySQL查询数据
    
    Args:
        config: MySQL配置，如果为None则使用临时存储的配置
        limit: 返回的最大行数
    
    Returns:
        list: 查询结果列表
    """
    if config is None:
        config = get_mysql_config()
    
    if not config:
        logger.error("MySQL配置未设置")
        return None
    
    try:
        import pymysql
        import pandas as pd
        
        conn = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            port=int(config.get('port', 3306))
        )
        
        table = config.get('table', 'stock_data')
        query = f"SELECT * FROM {table} ORDER BY trade_date DESC LIMIT {limit}"
        
        df = pd.read_sql(query, conn)
        conn.close()
        
        logger.info(f"MySQL查询成功，返回 {len(df)} 条记录")
        return df
        
    except ImportError:
        logger.error("未安装pymysql或pandas，请执行: pip install pymysql pandas")
        return None
    except Exception as e:
        logger.error(f"MySQL查询失败: {str(e)}")
        return None


# 程序退出时自动清理
import atexit
atexit.register(cleanup_temp_files)
