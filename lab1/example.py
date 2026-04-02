from cache_project import LRUCache

def main():
    cache = LRUCache(100)
    
    cache.set('Jesse', 'Pinkman')
    cache.set('Walter', 'White')
    cache.set('Jesse', 'James')
    
    print(f"Get Jesse: {cache.get('Jesse')}")  # * должен вывести 'James'
    
    cache.rem('Walter')
    
    print(f"Get Walter: {cache.get('Walter')}")  # * должен вывести return ''

    # cache.clear()

    # cache.rem('Walter')

if __name__ == "__main__":
    main()