from panoptic.transform import transform_image, transform_directory


def test_transform_image():
    res = transform_image('./resources/test.jpeg')
    assert res is not None


def test_transform_directory():
    res = transform_directory('./resources')
    assert res is not None
