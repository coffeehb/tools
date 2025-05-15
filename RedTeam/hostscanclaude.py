#!/usr/bin/env python
# -*- coding: utf-8 -*-
import concurrent.futures
import re
import queue
import requests
import threading
import time
import logging
from urllib3.exceptions import InsecureRequestWarning

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 全局变量
result_queue = queue.Queue()
thread_lock = threading.RLock()  # 使用可重入锁
is_processing = True
total_requests = 0
successful_count = 0
results_buffer = []  # 用于批量写入结果
BUFFER_SIZE = 10  # 缓冲区大小，达到此数量时批量写入

# 禁用SSL警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def fetch_url(host_ip_pair):
    """
    请求URL并处理响应
    
    Args:
        host_ip_pair: 包含主机名和IP的元组
    """
    global successful_count
    
    host, ip = host_ip_pair
    results = []
    
    for protocol in ['http://', 'https://']:
        url = f"{protocol}{ip}"
        headers = {
            'Host': host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.baidu.com',
            'Connection': 'close'
        }
        
        try:
            response = requests.get(
                url=url, 
                headers=headers, 
                timeout=5,  # 增加超时时间
                verify=False, 
                allow_redirects=False
            )
            response.encoding = 'utf-8'
            
            with thread_lock:
                successful_count += 1
                progress = f"{successful_count}/{total_requests}"
                
            # 处理响应
            result = process_response(url, host, response.text, response.headers, response.status_code)
            if result:
                results.append(result)
                
            logger.info(f"访问成功: URL: {url} Host: {host} 进度: {progress}")
            
        except requests.exceptions.Timeout:
            logger.warning(f"访问超时: URL: {url} Host: {host}")
        except requests.exceptions.ConnectionError:
            logger.warning(f"连接错误: URL: {url} Host: {host}")
        except Exception as e:
            logger.error(f"访问异常: URL: {url} Host: {host} 错误: {str(e)}")
    
    return results

def process_response(url, host, data, headers, status_code):
    """处理响应内容，提取有用信息"""
    try:
        title_match = re.search('<title>(.*?)</title>', data, re.IGNORECASE)
        title = title_match.group(1) if title_match else "获取标题失败"
        
        # 处理重定向
        if status_code in (301, 302) and 'Location' in headers:
            info = (url, host, str(len(data)), f"{status_code}:{headers['Location']}")
            logger.info(f"重定向: {info}, 状态码: {status_code}")
            return info
            
        # 过滤无效数据
        elif '百度一下' in title:
            logger.debug(f"无效数据: URL: {url} Host: {host}")
            return None
            
        # 处理成功响应
        elif status_code == 200 and len(data) > 20:
            info = (url, host, str(len(data)), title)
            logger.info(f"成功: {info}, 状态码: {status_code}")
            return info
            
        else:
            logger.debug(f"未处理响应: URL: {url} Host: {host} 状态码: {status_code}")
            return None
            
    except Exception as e:
        logger.error(f"处理响应出错: {str(e)}")
        return None

def write_results_to_file(results, mode='a'):
    """将结果写入文件"""
    if not results:
        return
        
    try:
        with open('ok.txt', mode, encoding='utf-8') as f:
            for result in results:
                f.write(f"{str(result)}\n")
        logger.debug(f"已写入{len(results)}条结果到文件")
    except Exception as e:
        logger.error(f"写入文件出错: {str(e)}")

def result_handler():
    """处理和保存结果的线程函数"""
    unique_results = set()  # 使用集合去重
    buffer = []
    
    while is_processing or not result_queue.empty():
        try:
            result = result_queue.get(timeout=3)
            
            # 去重处理
            result_key = (result[0], result[2], result[3])
            if result_key not in unique_results:
                unique_results.add(result_key)
                buffer.append(result)
                
                # 达到缓冲区大小时批量写入
                if len(buffer) >= BUFFER_SIZE:
                    write_results_to_file(buffer)
                    buffer = []
                    
            result_queue.task_done()
            
        except queue.Empty:
            continue
        except Exception as e:
            logger.error(f"处理结果线程出错: {str(e)}")
    
    # 处理剩余的结果
    if buffer:
        write_results_to_file(buffer)

def load_data():
    """加载主机和IP数据"""
    task_pairs = []
    
    try:
        # 读取IP列表
        with open('ip.txt', 'r') as f:
            ip_list = [line.strip() for line in f if line.strip()]
            
        # 读取主机列表
        with open('host.txt', 'r') as f:
            host_list = [line.strip() for line in f if line.strip()]
        
        # 生成所有组合
        for host in host_list:
            for ip in ip_list:
                task_pairs.append((host, ip))
                
        global total_requests
        total_requests = len(task_pairs) * 2  # HTTP和HTTPS各一次
        
        logger.info(f"数据加载完成! 共需处理 {total_requests} 个请求")
        return task_pairs
        
    except FileNotFoundError as e:
        logger.error(f"无法找到输入文件: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"加载数据出错: {str(e)}")
        return []

def main():
    # 清空结果文件
    write_results_to_file([], mode='w')
    
    # 加载数据
    task_pairs = load_data()
    if not task_pairs:
        logger.error("没有任务数据，程序退出")
        return
    
    logger.info("===== 开始处理 =====")
    time.sleep(1)  # 给用户一点时间查看日志
    
    # 启动结果处理线程
    result_handler_thread = threading.Thread(target=result_handler)
    result_handler_thread.daemon = True
    result_handler_thread.start()
    
    # 使用线程池处理请求
    max_workers = min(32, len(task_pairs))  # 根据任务数量动态调整线程数，最大32
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_pair = {executor.submit(fetch_url, pair): pair for pair in task_pairs}
        
        for future in concurrent.futures.as_completed(future_to_pair):
            pair = future_to_pair[future]
            try:
                results = future.result()
                if results:
                    for result in results:
                        if result:
                            result_queue.put(result)
            except Exception as e:
                logger.error(f"处理任务出错: {pair}, 错误: {str(e)}")
    
    logger.info("===== 所有请求已完成 =====")
    
    # 等待结果处理完成
    global is_processing
    is_processing = False
    result_handler_thread.join()
    
    logger.info("已处理完成，匹配成功的结果已保存在ok.txt")

if __name__ == "__main__":
    main()
