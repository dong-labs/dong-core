"""配置管理基础类

提供统一的配置管理，配置文件存储在 ~/.<cli_name>/config.json
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """
    配置管理基类
    
    子类需要实现：
    - get_name(): 返回 CLI 名称
    - get_defaults(): 返回默认配置字典
    """
    
    _config: Optional[Dict[str, Any]] = None
    
    @classmethod
    def get_name(cls) -> str:
        """返回 CLI 名称（子类必须实现）"""
        raise NotImplementedError
    
    @classmethod
    def get_defaults(cls) -> Dict[str, Any]:
        """返回默认配置（子类必须实现）"""
        raise NotImplementedError
    
    @classmethod
    def get_config_dir(cls) -> Path:
        """获取配置目录"""
        name = cls.get_name()
        return Path.home() / f".{name}"
    
    @classmethod
    def get_config_file(cls) -> Path:
        """获取配置文件路径"""
        return cls.get_config_dir() / "config.json"
    
    @classmethod
    def load(cls) -> Dict[str, Any]:
        """加载配置"""
        if cls._config is not None:
            return cls._config
        
        config_file = cls.get_config_file()
        defaults = cls.get_defaults()
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # 合并默认配置
                    cls._config = {**defaults, **loaded}
            except (json.JSONDecodeError, IOError):
                cls._config = defaults
        else:
            cls._config = defaults
        
        return cls._config
    
    @classmethod
    def save(cls, config: Dict[str, Any]) -> None:
        """保存配置"""
        config_dir = cls.get_config_dir()
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_file = cls.get_config_file()
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        cls._config = config
    
    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """获取配置项"""
        config = cls.load()
        return config.get(key, default)
    
    @classmethod
    def set(cls, key: str, value: Any) -> None:
        """设置配置项"""
        config = cls.load()
        config[key] = value
        cls.save(config)
    
    @classmethod
    def reset(cls) -> None:
        """重置配置到默认值"""
        cls._config = None
        config_file = cls.get_config_file()
        if config_file.exists():
            config_file.unlink()
