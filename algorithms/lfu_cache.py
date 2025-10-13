# /algorithms/lfu_cache.py

from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.freq_count = {}
        self.freq_map = defaultdict(OrderedDict)
        self.min_freq = 0

    def _update_freq(self, key: int):
        old_freq = self.freq_count[key]
        self.freq_map[old_freq].pop(key)
        
        if not self.freq_map[old_freq] and old_freq == self.min_freq:
            self.min_freq += 1
            
        new_freq = old_freq + 1
        self.freq_count[key] = new_freq
        self.freq_map[new_freq][key] = None

    def get(self, key: int) -> str:
        if key not in self.cache:
            return None
        
        self._update_freq(key)
        return self.cache[key]

    def put(self, key: int, value: str):
        if self.capacity == 0:
            return

        if key in self.cache:
            self.cache[key] = value
            self._update_freq(key)
            return

        if len(self.cache) >= self.capacity:
            lfu_key, _ = self.freq_map[self.min_freq].popitem(last=False)
            del self.cache[lfu_key]
            del self.freq_count[lfu_key]

        self.cache[key] = value
        self.freq_count[key] = 1
        self.freq_map[1][key] = None
        self.min_freq = 1

    def clear(self):
        self.cache.clear()
        self.freq_count.clear()
        self.freq_map.clear()
        self.min_freq = 0