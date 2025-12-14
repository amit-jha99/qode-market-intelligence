# Deduplication logic

import hashlib


def hash_tweet(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()