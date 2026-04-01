"""
Unit tests for LRU Cache implementation.
"""

import unittest
from cache_project import LRUCache


class TestLRUCache(unittest.TestCase):
    
    def test_basic_operations(self):
        """Test basic set, get, and rem operations."""
        cache = LRUCache(100)
        
        cache.set('Jesse', 'Pinkman')
        cache.set('Walter', 'White')
        cache.set('Jesse', 'James')
        
        self.assertEqual(cache.get('Jesse'), 'James')
        
        cache.rem('Walter')
        self.assertEqual(cache.get('Walter'), '')
    
    def test_capacity_limit(self):
        """Test that cache respects capacity limit."""
        cache = LRUCache(3)
        
        cache.set('a', '1')
        cache.set('b', '2')
        cache.set('c', '3')
        cache.set('d', '4')  # Should evict 'a'
        
        self.assertEqual(cache.get('a'), '')
        self.assertEqual(cache.get('b'), '2')
        self.assertEqual(cache.get('c'), '3')
        self.assertEqual(cache.get('d'), '4')
    
    def test_lru_behavior(self):
        """Test LRU eviction behavior."""
        cache = LRUCache(3)
        
        cache.set('a', '1')
        cache.set('b', '2')
        cache.set('c', '3')
        
        # Access 'a' to make it most recently used
        cache.get('a')
        
        # Add new item, should evict 'b' (least recently used)
        cache.set('d', '4')
        
        self.assertEqual(cache.get('a'), '1')
        self.assertEqual(cache.get('b'), '')
        self.assertEqual(cache.get('c'), '3')
        self.assertEqual(cache.get('d'), '4')
    
    def test_update_existing_key(self):
        """Test updating existing key moves it to most recent."""
        cache = LRUCache(3)
        
        cache.set('a', '1')
        cache.set('b', '2')
        cache.set('c', '3')
        
        # Update existing key
        cache.set('a', 'updated')
        
        # Add new item, should evict 'b' (least recently used)
        cache.set('d', '4')
        
        self.assertEqual(cache.get('a'), 'updated')
        self.assertEqual(cache.get('b'), '')
        self.assertEqual(cache.get('c'), '3')
        self.assertEqual(cache.get('d'), '4')
    
    def test_get_non_existent_key(self):
        """Test getting non-existent key returns empty string."""
        cache = LRUCache(10)
        self.assertEqual(cache.get('nonexistent'), '')
    
    def test_remove_non_existent_key(self):
        """Test removing non-existent key doesn't cause errors."""
        cache = LRUCache(10)
        cache.rem('nonexistent')  # Should not raise exception
        self.assertEqual(len(cache), 0)
    
    def test_len_method(self):
        """Test __len__ method works correctly."""
        cache = LRUCache(5)
        self.assertEqual(len(cache), 0)
        
        cache.set('a', '1')
        cache.set('b', '2')
        self.assertEqual(len(cache), 2)
        
        cache.rem('a')
        self.assertEqual(len(cache), 1)


if __name__ == '__main__':
    unittest.main()