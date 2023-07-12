
# Source: # C950 - Webinar-1 - Let’s Go Hashing
# # W-1_ChainingHashTable_zyBooks_Key-Value.py
# # Ref: zyBooks: Figure 7.8.2: Hash table using chaining.
# C950 - Webinar-1 - Let’s Go Hashing - Complete Python Code pdf
# https://srm--c.na127.visual.force.com/apex/coursearticle?Id=kA03x000000e1fuCAA

# Blueprint for CreateHashMap objects.  Creates HashMap.
# O(N)time --- O(N)space
class HashMap:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    # O(N)time --- O(N)space
    def __init__(self, initial_capacity=20):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts and updates key value pair in HashMap
    # O(N)time --- O(N^2)space
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # Retrieves value from HashMap using key
    # O(N)time --- O(1)space
    def lookup(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if key == kv[0]:
                return kv[1]
        return None

    # Removes key value from HashMap
    # O(N)time --- O(1)space
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        remove_bucket = self.table[bucket]
        for kv in remove_bucket:
            if kv[0] == key:
                remove_bucket.remove([kv[0], kv[1]])
