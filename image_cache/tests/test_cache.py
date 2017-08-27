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


def test_numpy_write_and_read(rgb_image_array):
    cache = image_cache.NumpyCache()
    for idx, img in enumerate(rgb_image_array[:-1]):
        cache[img] = idx

    for idx, img in enumerate(rgb_image_array[:-1]):
        assert cache[img] == idx

    with pytest.raises(KeyError):
        cache[rgb_image_array[-1, :, :]]


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
def test_update(CacheClass, rgb_image_data):
    image_dir, image_list = rgb_image_data

    cache = CacheClass(image_dir=image_dir)

    cache.update(image_list, list(range(len(image_list))))

    for idx, image_file in enumerate(image_list):
        assert cache[image_file] == idx


def test_numpy_update(rgb_image_array):
    cache = image_cache.NumpyCache()

    cache.update(rgb_image_array, list(range(len(rgb_image_array))))

    for idx, img in enumerate(rgb_image_array):
        assert cache[img] == idx


@pytest.mark.parametrize('CacheClass', [
    image_cache.InMemoryImageCache,
    image_cache.ImageCache
    ])
def test_iteration(CacheClass, rgb_image_data):
    image_dir, image_list = rgb_image_data

    cache = CacheClass(image_dir=image_dir)

    cache.update(image_list, list(range(len(image_list))))

    expected = [cache.hash_image(image) for image in image_list]
    for idx, image_hash in enumerate(cache):
        assert image_hash in expected


@pytest.mark.parametrize('CacheClass', [
    image_cache.InMemoryImageCache,
    image_cache.ImageCache
    ])
def test_update_array(CacheClass, rgb_image_data):
    image_dir, image_list = rgb_image_data

    cache = CacheClass(image_dir=image_dir)

    result = np.tile(np.arange(len(image_list)).reshape(-1, 1), 10)
    cache.update(image_list, result)
    for idx, image_file in enumerate(image_list):
        cache[image_file] = np.repeat(idx, 10)


def test_numpy_update_array(rgb_image_array):
    cache = image_cache.NumpyCache()

    result = np.tile(np.arange(len(rgb_image_array)).reshape(-1, 1), 10)
    cache.update(rgb_image_array, result)

    for idx, img in enumerate(rgb_image_array):
        assert np.all(cache[img] == np.repeat(idx, 10))


@pytest.mark.parametrize('CacheClass', [
    image_cache.InMemoryImageCache,
    image_cache.ImageCache
    ])
def test_delete_item(CacheClass, rgb_image_data):
    image_dir, image_list = rgb_image_data

    cache = CacheClass(image_dir=image_dir)

    for idx, image_file in enumerate(image_list):
        cache[image_file] = idx

    assert len(cache) == len(image_list)

    del cache[image_list[0]]

    assert image_list[0] not in cache


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
