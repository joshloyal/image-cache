import pytest
import numpy as np

import image_cache


@pytest.mark.parametrize('CacheClass', [
    image_cache.InMemoryImageCache,
    image_cache.ImageCache
    ])
def test_simple_write_and_read(CacheClass, rgb_image_data):
    image_dir, image_list = rgb_image_data

    cache = CacheClass(image_dir=image_dir)

    for idx, image_file in enumerate(image_list[:-1]):
        cache[image_file] = idx

    for idx, image_file in enumerate(image_list[:-1]):
        assert cache[image_file] == idx

    # new file that has not been cached raises an error
    with pytest.raises(KeyError):
        cache[image_list[-1]]


@pytest.mark.parametrize('CacheClass', [
    image_cache.InMemoryImageCache,
    image_cache.ImageCache
    ])
def test_file_does_not_exist(CacheClass):
    cache = CacheClass()

    # non-existent file raises an error
    with pytest.raises(FileNotFoundError):
        cache['dummy_file']


@pytest.mark.parametrize('CacheClass', [
    image_cache.InMemoryImageCache,
    image_cache.ImageCache
    ])
def test_batch_update(CacheClass, rgb_image_data):
    image_dir, image_list = rgb_image_data

    cache = CacheClass(image_dir=image_dir)

    cache.batch_update(image_list, list(range(len(image_list))))

    for idx, image_file in enumerate(image_list):
        assert cache[image_file] == idx


@pytest.mark.parametrize('CacheClass', [
    image_cache.InMemoryImageCache,
    image_cache.ImageCache
    ])
def test_batch_update_array(CacheClass, rgb_image_data):
    image_dir, image_list = rgb_image_data

    cache = CacheClass(image_dir=image_dir)

    result = np.tile(np.arange(len(image_list)).reshape(-1, 1), 10)
    cache.batch_update(image_list, result)
    for idx, image_file in enumerate(image_list):
        cache[image_file] = np.repeat(idx, 10)


@pytest.mark.parametrize('CacheClass', [
    image_cache.InMemoryImageCache,
    image_cache.ImageCache
    ])
def test_clear_cache(CacheClass, rgb_image_data):
    image_dir, image_list = rgb_image_data

    cache = CacheClass(image_dir=image_dir)

    for idx, image_file in enumerate(image_list):
        cache[image_file] = idx

    assert len(cache) == len(image_list)

    cache.clear()

    assert len(cache) == 0