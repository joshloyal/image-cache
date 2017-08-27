import abc
import os
import functools
import pickle
import hashlib

import chest
import joblib


__all__ = ['BaseImageCache', 'ImageCache', 'InMemoryImageCache']


def hash_image(image_dir, file_path):
    """Basic image hashing function. Uses the md5 checksum of
    the binary image on disk."""
    with open(os.path.join(image_dir, file_path), 'rb') as image:
        return hashlib.md5(image.read()).hexdigest()


class BaseImageCache(metaclass=abc.ABCMeta):
    def __init__(self, cache_dir=None, image_dir=''):
        self.image_dir = image_dir

        self._cache_dir = cache_dir
        self._cache = None

    @abc.abstractmethod
    def get_cache(self):
        raise NotImplementedError(
            'You must implement this method in your class.')

    @abc.abstractmethod
    def clear(self):
        raise NotImplementedError(
            'You must implement this method in your class.')

    def __str__(self):
        return '<{class_name} at {location}>'.format(
            class_name=self.__class__.__name__,
            location=self.cache_dir)

    def __repr__(self):
        return '<{class_name} at {location}>'.format(
            class_name=self.__class__.__name__,
            location=self.cache_dir)

    def __len__(self):
        return len(self.cache)

    @property
    def cache(self):
        if not self._cache:
            self._cache = self.get_cache()
        return self._cache

    @property
    def cache_dir(self):
        return self._cache_dir

    def hash_image(self, image_file):
        """Image hash function. Default uses the md5 checksum of the binary
        image read from disk."""
        return hash_image(self.image_dir, image_file)

    def __setitem__(self, image_file, result):
        """Place an image in the cache."""
        image_hash = self.hash_image(image_file)
        self.cache[image_hash] = result

    def update(self, image_files, results):
        """Given a list of image files and results update the cache
        in batch."""
        for index, image_file in enumerate(image_files):
            result = results[index]
            self[image_file] = result

    def __getitem__(self, image_file):
        """Retrieve an image from the cache if present."""
        image_hash = self.hash_image(image_file)
        if image_hash in self.cache:
            return self.cache[image_hash]
        raise KeyError('Image not in cache.')

    def __contains__(self, image_file):
        return self.hash_image(image_file) in self.cache

    def __iter__(self):
        return self.cache.__iter__()

    def __delitem__(self, image_file):
        image_hash = self.hash_image(image_file)
        del self.cache[image_hash]


class ImageCache(BaseImageCache):
    def get_cache(self):
        joblib_dump = functools.partial(joblib.dump,
                                        compress=True,
                                        protocol=pickle.HIGHEST_PROTOCOL)
        return chest.Chest(path=self._cache_dir,
                           dump=joblib_dump,
                           load=joblib.load)

    @property
    def cache_dir(self):
        return self.cache.path

    def clear(self):
        """Clear the cache."""
        # permanently remove anything written to disk.
        self.cache.drop()

        # delete in-memory keys and items
        for key in list(self.cache):
            del self.cache[key]


class InMemoryImageCache(BaseImageCache):
    def get_cache(self):
        return {}

    def clear(self):
        self.cache.clear()
