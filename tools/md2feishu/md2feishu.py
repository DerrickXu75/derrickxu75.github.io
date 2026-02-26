#!/usr/bin/env python3
"""
Markdown to Feishu Document Converter
将本地 Markdown 文件上传到飞书文档

用法:
    python3 md2feishu.py <markdown_file> [--title "标题"] [--folder "文件夹token"] [--update <doc_token>]
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error

class FeishuClient:
    """飞书 API 客户端"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self.tenant_access_token = None
        self.token_expires = 0
    
    def get_tenant_access_token(self) -> str:
        """获取 tenant_access_token"""
        if self.tenant_access_token and time.time() < self.token_expires - 60:
            return self.tenant_access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
        
        if result.get("code") != 0:
            raise Exception(f"获取 token 失败: {result}")
        
        self.tenant_access_token = result["tenant_access_token"]
        self.token_expires = time.time() + result.get("expire", 7200)
        return self.tenant_access_token
    
    def _request(self, method: str, path: str, data: dict = None, params: dict = None) -> dict:
        """发送请求"""
        token = self.get_tenant_access_token()
        url = f"{self.base_url}{path}"
        
        if params:
            query = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{query}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        req_data = json.dumps(data).encode() if data else None
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            raise Exception(f"HTTP {e.code}: {error_body}")
        
        return result
    
    def create_document(self, title: str, folder_token: str = None) -> tuple:
        """创建新文档，返回 (document_id, title)"""
        data = {"title": title}
        if folder_token:
            data["folder_token"] = folder_token
        
        result = self._request("POST", "/docx/v1/documents", data)
        if result.get("code") != 0:
            raise Exception(f"创建文档失败: {result}")
        
        doc = result["data"]["document"]
        return doc["document_id"], doc["title"]
    
    def list_blocks(self, doc_token: str) -> list:
        """列出文档所有块"""
        blocks = []
        page_token = None
        
        while True:
            params = {"page_size": 50}
            if page_token:
                params["page_token"] = page_token
            
            result = self._request("GET", f"/docx/v1/documents/{doc_token}/blocks", params=params)
            
            if result.get("code") != 0:
                break
            
            blocks.extend(result.get("data", {}).get("items", []))
            page_token = result.get("data", {}).get("page_token")
            if not page_token:
                break
        
        return blocks
    
    def delete_block(self, doc_token: str, block_id: str) -> bool:
        """删除块"""
        result = self._request("DELETE", f"/docx/v1/documents/{doc_token}/blocks/{block_id}")
        return result.get("code") == 0
    
    def create_block(self, doc_token: str, parent_id: str, block: dict, index: int = None) -> dict:
        """创建块"""
        data = {
            "children": [block],
            "index": index
        }
        result = self._request("POST", f"/docx/v1/documents/{doc_token}/blocks/{parent_id}/children", data)
        if result.get("code") != 0:
            raise Exception(f"创建块失败: {result}")
        return result.get("data", {})


class MarkdownParser:
    """Markdown 解析器"""
    
    def parse(self, markdown: str) -> list:
        """解析 Markdown 文本"""
        blocks = []
        lines = markdown.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 跳过空行
            if not line.strip():
                i += 1
                continue
            
            # 标题
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                text = heading_match.group(2)
                blocks.append(self._heading(text, level))
                i += 1
                continue
            
            # 代码块
            if line.strip().startswith('```'):
                code_lines = []
                lang = line.strip()[3:].strip() or "PlainText"
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                if i < len(lines):
                    i += 1
                blocks.append(self._code_block('\n'.join(code_lines), lang))
                continue
            
            # 无序列表
            bullet_match = re.match(r'^[-*+]\s+(.+)$', line)
            if bullet_match:
                blocks.append(self._bullet(bullet_match.group(1)))
                i += 1
                continue
            
            # 有序列表
            ordered_match = re.match(r'^\d+\.\s+(.+)$', line)
            if ordered_match:
                blocks.append(self._ordered(ordered_match.group(1)))
                i += 1
                continue
            
            # 引用
            if line.strip().startswith('>'):
                text = line.strip()[1:].strip()
                blocks.append(self._quote(text))
                i += 1
                continue
            
            # 分割线
            if re.match(r'^[-*_]{3,}$', line.strip()):
                blocks.append(self._divider())
                i += 1
                continue
            
            # 图片（跳过）
            if re.match(r'^!\[([^\]]*)\]\(([^)]+)\)$', line.strip()):
                i += 1
                continue
            
            # 普通段落
            para_lines = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not self._is_special_line(lines[i]):
                para_lines.append(lines[i])
                i += 1
            blocks.append(self._paragraph('\n'.join(para_lines)))
        
        return blocks
    
    def _is_special_line(self, line: str) -> bool:
        stripped = line.strip()
        return bool(re.match(r'^(#{1,6}\s|[-*+]\s|\d+\.\s|>|```|[-*_]{3,}$|!\[)', stripped))
    
    def _clean_text(self, text: str) -> str:
        text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)
        text = re.sub(r'__([^_]+)__', r'\1', text)
        text = re.sub(r'_([^_]+)_', r'\1', text)
        text = re.sub(r'~~([^~]+)~~', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
        return text
    
    def _heading(self, text: str, level: int) -> dict:
        heading_key = f"heading{min(level, 9)}"
        return {
            "block_type": 4,
            heading_key: {
                "elements": [{"text_run": {"content": self._clean_text(text)}}]
            }
        }
    
    def _paragraph(self, text: str) -> dict:
        return {
            "block_type": 2,
            "text": {
                "elements": [{"text_run": {"content": self._clean_text(text)}}]
            }
        }
    
    def _code_block(self, code: str, lang: str = "PlainText") -> dict:
        return {
            "block_type": 23,
            "code": {
                "elements": [{"text_run": {"content": code}}],
                "style": {"language": lang}
            }
        }
    
    def _bullet(self, text: str) -> dict:
        return {
            "block_type": 5,
            "bullet": {
                "elements": [{"text_run": {"content": self._clean_text(text)}}]
            }
        }
    
    def _ordered(self, text: str) -> dict:
        return {
            "block_type": 6,
            "ordered": {
                "elements": [{"text_run": {"content": self._clean_text(text)}}]
            }
        }
    
    def _quote(self, text: str) -> dict:
        return {
            "block_type": 11,
            "quote": {
                "elements": [{"text_run": {"content": self._clean_text(text)}}]
            }
        }
    
    def _divider(self) -> dict:
        return {"block_type": 14, "divider": {}}


def main():
    parser = argparse.ArgumentParser(description='上传 Markdown 到飞书文档')
    parser.add_argument('markdown_file', help='Markdown 文件路径')
    parser.add_argument('--title', help='文档标题')
    parser.add_argument('--folder', help='目标文件夹 token')
    parser.add_argument('--update', help='更新现有文档（doc_token）')
    parser.add_argument('--account', default='custom-1', choices=['custom-1', 'custom-2'])
    args = parser.parse_args()
    
    # 读取配置
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    with open(config_path) as f:
        config = json.load(f)
    
    accounts = config.get("channels", {}).get("feishu", {}).get("accounts", {})
    if args.account not in accounts:
        print(f"错误: 账号 {args.account} 不存在")
        sys.exit(1)
    
    account = accounts[args.account]
    
    # 读取 Markdown
    if not os.path.exists(args.markdown_file):
        print(f"错误: 文件不存在 {args.markdown_file}")
        sys.exit(1)
    
    with open(args.markdown_file, encoding='utf-8') as f:
        markdown = f.read()
    
    # 解析
    md_parser = MarkdownParser()
    blocks = md_parser.parse(markdown)
    print(f"解析完成: {len(blocks)} 个块")
    
    # 创建客户端
    client = FeishuClient(account["appId"], account["appSecret"])
    
    # 标题
    title = args.title or os.path.basename(args.markdown_file).replace('.md', '')
    
    if args.update:
        doc_token = args.update
        print(f"更新文档: {doc_token}")
        
        # 获取根块（document_id 就是根块 ID）
        root_block_id = doc_token
        
        # 删除现有内容
        existing_blocks = client.list_blocks(doc_token)
        for block in existing_blocks:
            if block.get("block_type") != 1:  # 跳过 page 块
                client.delete_block(doc_token, block["block_id"])
        
        # 添加新内容
        for i, block in enumerate(blocks):
            try:
                client.create_block(doc_token, root_block_id, block, i)
                print(f"  已添加块 {i+1}/{len(blocks)}")
            except Exception as e:
                print(f"  警告: 块 {i+1} 添加失败: {e}")
        
        print(f"\n✅ 文档已更新: https://feishu.cn/docx/{doc_token}")
    
    else:
        print(f"创建文档: {title}")
        doc_token, _ = client.create_document(title, args.folder)
        print(f"文档ID: {doc_token}")
        
        # 添加内容
        for i, block in enumerate(blocks):
            try:
                client.create_block(doc_token, doc_token, block, i)
                print(f"  已添加块 {i+1}/{len(blocks)}")
            except Exception as e:
                print(f"  警告: 块 {i+1} 添加失败: {e}")
        
        print(f"\n✅ 文档已创建: https://feishu.cn/docx/{doc_token}")


if __name__ == "__main__":
    main()
