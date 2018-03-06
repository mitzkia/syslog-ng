from src.common.random import Random


def test_get_unique_id_static_seed():
    random = Random(use_static_seed=True)
    first_10_random_numbers = []
    for _i in range(10):
        first_10_random_numbers.append(random.get_unique_id())

    random = Random(use_static_seed=True)
    second_10_random_numbers = []
    for _i in range(10):
        second_10_random_numbers.append(random.get_unique_id())

    assert first_10_random_numbers == second_10_random_numbers


def test_get_unique_id_static_seed_false():
    random = Random(use_static_seed=False)
    first_10_random_numbers = []
    for _i in range(10):
        first_10_random_numbers.append(random.get_unique_id())

    random = Random(use_static_seed=False)
    second_10_random_numbers = []
    for _i in range(10):
        second_10_random_numbers.append(random.get_unique_id())

    assert first_10_random_numbers != second_10_random_numbers
