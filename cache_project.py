from collections import OrderedDict
from typing import Optional


class LRUCache:
    
    def __init__(self, capacity: int = 10) -> None:
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")
        
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key: str) -> str:
        if key not in self.cache:
            return ""
        
        # * двигаем в конец, так как теперь он последний использованный
        value = self.cache.pop(key)
        self.cache[key] = value
        return value
    
    def set(self, key: str, value: str) -> None:
        if key in self.cache:
            # * убираем существующий чтобы апдейтнуть позицию
            self.cache.pop(key)
        elif len(self.cache) >= self.capacity:
            # * убираем самый менее использованный (он первыый)
            self.cache.popitem(last=False)
        
        # * добавляем новый последний использованный элемент
        self.cache[key] = value
    
    def rem(self, key: str) -> None:
        if key in self.cache:
            self.cache.pop(key)
    
    def __len__(self) -> int:
        return len(self.cache)
    
    def __contains__(self, key: str) -> bool:
        return key in self.cache
    
    def clear(self) -> None:
        self.cache.clear()