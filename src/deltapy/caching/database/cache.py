'''
Created on May 21, 2010

@author: Abi.Mohammadi & Majid.Vesal
'''

import time
import cPickle

from deltapy.caching.cache import CacheBase, CacheItem
from deltapy.core import DeltaException
from deltapy.utils.storm_aux import create_raw_cursor
import deltapy.application.services as application
import deltapy.transaction.services as transaction

class DatabaseCacheException(DeltaException):
    '''
    '''

class DatabaseCache(CacheBase):
    '''
    Database cache class.
    '''
    
    CACHE_TYPE_NAME = 'database_cache'
    CACHE_CONTENT = 'DELTA_CACHE_CONTENT'
    CACHE_HEADER = 'DELTA_CACHE_HEADER'

    def __init__(self, cache_name, **options):
        self._cache_id = None
        self._pool_name = options.get('pool_name')
        CacheBase.__init__(self, cache_name, **options)
        self._app_name = application.get_name()
        self._instance_name = application.get_instance_name() 
        if self._instance_name is None:
            self._instance_name = self._app_name
        self._id = self.get_id()
        self._remove_expired_items_()
        
    def remove(self, key):
        '''
        Removes specified item from cache. 
        
        @param key: item key
        '''
        
        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''delete from DELTA_CACHE_CONTENT 
                                where cache_id = :cache_id 
                                    and item_key = :item_key''',
                           [self._id, key])

    def get_len(self):
        '''
        Returns cache items count.
        
        @return: int
        '''      
        
        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''select count(*) from DELTA_CACHE_CONTENT 
                                where cache_id = :cache_id ''',
                           [self._id])
            
            length, = cursor.fetchone()
            return length
    
    def get_id(self):
        '''
        Returns cache id.
        
        @return: object
        '''
        
        if self._cache_id is None:
            with transaction.begin_root(pool_name = self._pool_name):
                store = transaction.get_current_transaction(self._pool_name).get_connection()
                cursor = create_raw_cursor(store)
                cursor.execute('''select cache_id from DELTA_CACHE_HEADER 
                                    where app_name = :app_name
                                        and app_instance = :app_instance
                                        and cache_name = :cache_name''',
                               [self._app_name, self._instance_name, self.get_name()])
                
                result = cursor.fetchone()
                if result is not None:
                    cache_id, = result
                else:
                    cache_id = hash(self._app_name + self._instance_name + self.get_name())
                    cursor.execute('''insert into 
                                        DELTA_CACHE_HEADER(app_name,
                                                           app_instance,
                                                           cache_name,
                                                           cache_id,
                                                           cache_size)
                                        values(:app_name,
                                               :app_instance,
                                               :cache_name,
                                               :cache_id,
                                               :cache_size)''',
                                   [self._app_name, 
                                    self._instance_name, 
                                    self.get_name(),
                                    cache_id,
                                    CacheBase.get_size(self)])
                self._cache_id = cache_id
            return self._cache_id

    def set_size(self, size):
        '''
        Returns cache size.
        
        @return: int
        '''

        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''update DELTA_CACHE_HEADER set cache_size = :cache_size 
                                where app_name = :app_name
                                    and app_instance = :app_instance
                                    and cache_name = :cache_name''',
                           [size,
                            self._app_name, 
                            self._instance_name, 
                            self.get_name()])
            size, = cursor.fetchone()
            return size

    def get_size(self):
        '''
        Returns cache size.
        
        @return: int
        '''
        
        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''select cache_size from DELTA_CACHE_HEADER 
                                where app_name = :app_name
                                    and app_instance = :app_instance
                                    and cache_name = :cache_name''',
                           [self._app_name, self._instance_name, self.get_name()])
            
            size, = cursor.fetchone()
            return size

    def reset_item(self, key):
        '''
        Resets cache item.
        '''

        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''update DELTA_CACHE_CONTENT 
                                    set item_last_reset_time = :item_last_reset_time,
                                        item_expired = :item_expired
                                    where cache_id = :cache_id
                                        and item_key = :item_key''',
                           [time.time(),
                            True,
                            self._id,
                            key])
    def clear(self):
        '''
        Removes all cache items.
        '''

        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''delete from DELTA_CACHE_CONTENT 
                                where cache_id = :cache_id''',
                           [self._id])
            
            size, = cursor.fetchone()
            return size
    
    def reset(self):
        '''
        Resets the cache.
        '''

        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''update DELTA_CACHE_CONTENT 
                                    set item_last_reset_time = :item_last_reset_time,
                                        item_expired = :item_expired
                                    where cache_id = :cache_id''',
                           [time.time(),
                            True,
                            self._id])
    
    def set(self, key, value):
        '''
        Sets given item using specified key.
        
        @param key: item key
        @param value: item value
        '''
        
        with transaction.begin_root(pool_name = self._pool_name):
            try:
                store = transaction.get_current_transaction(self._pool_name).get_connection()
                cursor = create_raw_cursor(store)
                if self.has_key(key):
                    cursor.execute('''update DELTA_CACHE_CONTENT 
                                        set item_value = :item_value,
                                            item_last_reset_time = :item_last_reset_time,
                                            item_expired = :item_expired
                                        where cache_id = :cache_id
                                            and item_key = :item_key''',
                                   [buffer(cPickle.dumps(value, protocol = 0)),
                                    time.time(),
                                    False, 
                                    self._id, 
                                    key])
                else:
                    size = self.get_size()
                    if size != 0 and self.get_len() >= size:
                        self._remove_oldest_item_()
                    cursor.execute('''insert into 
                                        DELTA_CACHE_CONTENT(cache_id, 
                                                            item_key, 
                                                            item_value, 
                                                            item_creation_time, 
                                                            item_last_reset_time, 
                                                            item_expired) 
                                        values(:cache_id, 
                                               :item_key, 
                                               :item_value, 
                                               :item_creation_time, 
                                               :item_last_reset_time, 
                                               :item_expired)''',
                                   [self._id,
                                    key,
                                    buffer(cPickle.dumps(value, protocol = 0)),
                                    time.time(),
                                    time.time(),
                                    False])
            except:
                raise    
            
    def _get_item_(self, key):
        '''
        Returns cache item by specifed key.
        
        @param key: item key
        '''
        with transaction.begin_root(pool_name = self._pool_name):
            try:
                store = transaction.get_current_transaction(self._pool_name).get_connection()
                cursor = create_raw_cursor(store)
                cursor.execute('''select item_value, 
                                         item_creation_time,                                      
                                         item_last_reset_time, 
                                         item_expired from DELTA_CACHE_CONTENT 
                                    where cache_id = :cache_id
                                        and item_key = :item_key''',
                               [self._id, key])
                result = cursor.fetchone()
                if result is not None:
                    (item_value, 
                     item_creation_time, 
                     item_last_reset_time, 
                     item_expired,) = result
                    item = CacheItem(key, cPickle.loads(item_value))
                    item.creation_time = item_creation_time
                    item.last_reset_time = item_last_reset_time
                    item.expired = item_expired
                    return item
                return None
            except:
                raise    
        
    def get(self, key, default = None):
        '''
        Gets given item using specified key.
        
        @param key: item key
        @return : object
        '''
        
        item = self._get_item_(key)
        if item is None:
            return default
        
        scavenger = self.get_scavenger()
        
        if scavenger:
            scavenger.scavenge(self, item)
            
        if item.expired:
            raise DatabaseCacheException('Item [%s] is expired in cache[%s]' % (key, self.get_name()))
            
        return item.value
    
    def has_key(self, key):
        '''
        Checks if given key is exist or not.
        
        @param key: item key
        @return: bool
        '''
        
        item = self._get_item_(key)
        
        if item is None or item.expired:
            return False
        
        return True
        
    def get_items(self):
        '''
        Returns all items in cache.
        
        @return: [object]
        '''
        
        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''select item_key, 
                                 item_value, 
                                 item_creation_time, 
                                 item_last_reset_time, 
                                 item_expired 
                                from DELTA_CACHE_CONTENT 
                                where cache_id = :cache_id''',
                           [self._id])
            items = []
            for (item_key, 
                 item_value, 
                 item_creation_time, 
                 item_last_reset_time, 
                 item_expired,) in cursor.fetchall():
                item = CacheItem(item_key, cPickle.loads(item_value))
                self.creation_time = item_creation_time
                self.last_reset_time = item_last_reset_time
                self.expired = item_expired
                items.append(item)
            return items
        
    def keys(self):
        '''
        Returns all keys.
        
        @return: [object]
        '''
        
        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''select item_key from DELTA_CACHE_CONTENT 
                                where cache_id = :cache_id''',
                           [self._id])
            keys = []
            for item_key in cursor.fetchall():
                keys.append(item_key)
            return keys

    def values(self):
        '''
        Returns all values.
        
        @return: [object]
        '''
        
        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''select item_value from DELTA_CACHE_CONTENT 
                                where cache_id = :cache_id''',
                           [self._id])
            values = []
            for item_value, in cursor.fetchall():
                values.append(cPickle.loads(item_value))
            return values
        
    def get_last_reset_time(self):
        '''
        Returns last reset time of the cache.
        
        @return: float
        '''
        
        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''select item_last_reset_time from DELTA_CACHE_CONTENT
                                where cache_id = :cache_id
                              order by item_last_reset_time desc''',
                           [self._id])
            result = cursor.fetchone()
            item_last_reset_time = None
            if result is not None:
                item_last_reset_time, = cursor.fetchone()
            return item_last_reset_time
                
    def _remove_oldest_item_(self):
        '''
        Removes oldest item from cache.
        '''
        with transaction.begin_root(pool_name = self._pool_name):
            last_reset_time = self.get_last_reset_time()
            if last_reset_time is not None: 
                store = transaction.get_current_transaction(self._pool_name).get_connection()
                cursor = create_raw_cursor(store)
                cursor.execute('''delete from DELTA_CACHE_CONTENT 
                                    where cache_id = :cache_id 
                                        and item_last_reset_time <= :item_last_reset_time''',
                               [self._id,
                                last_reset_time])

    def _remove_expired_items_(self):
        '''
        Removes oldest item from cache.
        '''
        
        with transaction.begin_root(pool_name = self._pool_name):
            store = transaction.get_current_transaction(self._pool_name).get_connection()
            cursor = create_raw_cursor(store)
            cursor.execute('''delete from DELTA_CACHE_CONTENT 
                                where cache_id = :cache_id 
                                    and item_expired = 1 ''',
                           [self._id])
        
