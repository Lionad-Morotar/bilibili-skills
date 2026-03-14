#!/usr/bin/env python3
"""
从 bilibili-cli 存储的凭证构造 bilibili-api 的 Credential 对象。

Usage:
    from references.bili-api.get_credential import get_credential

    credential = get_credential()
    print(f"已登录: UID {credential.dedeuserid}")
"""

import json
from pathlib import Path
from bilibili_api import Credential


def get_credential(cli_credential_path: str | Path | None = None) -> Credential:
    """
    从 bilibili-cli 的凭证文件构造 Credential 对象。

    Args:
        cli_credential_path: bilibili-cli 凭证文件路径，
                            默认为 ~/.bilibili-cli/credential.json

    Returns:
        Credential: bilibili-api 所需的凭证对象

    Raises:
        FileNotFoundError: 凭证文件不存在
        KeyError: 凭证文件缺少必要字段
    """
    if cli_credential_path is None:
        cli_credential_path = Path.home() / ".bilibili-cli" / "credential.json"
    else:
        cli_credential_path = Path(cli_credential_path)

    if not cli_credential_path.exists():
        raise FileNotFoundError(
            f"未找到 bilibili-cli 凭证文件: {cli_credential_path}\n"
            "请先运行: bili login"
        )

    with open(cli_credential_path, encoding="utf-8") as f:
        cred_data = json.load(f)

    # 检查必要字段
    required_fields = ["sessdata", "bili_jct"]
    for field in required_fields:
        if field not in cred_data:
            raise KeyError(f"凭证文件缺少必要字段: {field}")

    return Credential(
        sessdata=cred_data["sessdata"],
        bili_jct=cred_data["bili_jct"],
        buvid3=cred_data.get("buvid3", ""),
        buvid4=cred_data.get("buvid4", ""),
        dedeuserid=cred_data.get("dedeuserid", "")
    )


def main():
    """命令行测试入口"""
    try:
        credential = get_credential()
        print(f"✅ 已成功构造 Credential")
        print(f"   UID: {credential.dedeuserid or 'N/A'}")
        print(f"   Sessdata: {credential.sessdata[:20]}..." if credential.sessdata else "   Sessdata: N/A")
        print(f"   Bili_jct: {credential.bili_jct[:20]}..." if credential.bili_jct else "   Bili_jct: N/A")
        print(f"   Buvid3: {credential.buvid3[:20]}..." if credential.buvid3 else "   Buvid3: (empty)")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        exit(1)
    except KeyError as e:
        print(f"❌ 凭证文件格式错误: {e}")
        exit(1)


if __name__ == "__main__":
    main()
