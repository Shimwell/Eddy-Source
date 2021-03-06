
import pytest
from eddymc.scale import mixtures


@pytest.fixture
def ce_file(tmpdir):
    with open('./scale_examples/cylinder_ce.out', 'r') as f:
        file = f.readlines()
    return file


@pytest.fixture
def multigroup_file(tmpdir):
    with open('./scale_examples/cylinder_multigroup.out', 'r') as f:
        file = f.readlines()
    return file


@pytest.fixture
def single_mixture_ce(tmpdir):
    with open('./scale_examples/single_mixture_ce.txt', 'r') as f:
        file = f.readlines()
    return file


@pytest.fixture
def single_mixture_multigroup(tmpdir):
    with open('./scale_examples/single_mixture_multigroup.txt', 'r') as f:
        file = f.readlines()
    return file


@pytest.fixture
def ce_table(tmpdir):
    with open('./scale_examples/mixture_table_ce.txt', 'r') as f:
        file = f.readlines()
    return file


@pytest.fixture
def multigroup_table(tmpdir):
    with open('./scale_examples/mixture_table_multigroup.txt', 'r') as f:
        file = f.readlines()
    return file


def test_get_mixture_data_ce(ce_file):
    # arrange
    file = ce_file
    # act
    output = mixtures.get_mixture_data(file)
    # assert
    assert len(output) == 56


def test_get_mixture_data_multigroup(multigroup_file):
    # arrange
    file = multigroup_file
    # act
    output = mixtures.get_mixture_data(file)
    # assert
    assert len(output) == 99


def test_create_mixtures_ce(ce_table, single_mixture_ce, mocker):
    # arrange
    mixture_table = ce_table
    single_mixture = single_mixture_ce
    mocked_Mixture_init = mocker.patch('eddymc.scale.mixtures.Mixture')
    # act
    mixtures.create_mixtures(mixture_table)
    # assert
    mocked_Mixture_init.assert_called()
    assert mocked_Mixture_init.call_count == 3
    assert mocked_Mixture_init.call_args_list[0].args[0] == single_mixture


def test_create_mixtures_multigroup(multigroup_table, single_mixture_multigroup, mocker):
    # arrange
    mixture_table = multigroup_table
    single_mixture = single_mixture_multigroup
    mocked_Mixture_init = mocker.patch('eddymc.scale.mixtures.Mixture')
    # act
    mixtures.create_mixtures(mixture_table)
    # assert
    mocked_Mixture_init.assert_called()
    assert mocked_Mixture_init.call_count == 3
    assert mocked_Mixture_init.call_args_list[0].args[0] == single_mixture



def test_mixture_init_ce_library(single_mixture_ce, mocker):
    # arrange
    mixture_table = single_mixture_ce
    gv = mocker.patch('eddymc.scale.mixtures.gv')
    gv.mixture_list = []
    # act
    mixtures.Mixture(mixture_table)
    mixture = gv.mixture_list[0]
    # assert
    assert len(gv.mixture_list) == 1
    assert mixture.number == '1'
    assert mixture.density == '7.8600'
    assert len(mixture.isotopes) == 13


def test_mixture_init_multigroup_library(single_mixture_multigroup, mocker):
    # arrange
    mixture_table = single_mixture_multigroup
    gv = mocker.patch('eddymc.scale.mixtures.gv')
    gv.mixture_list = []
    # act
    mixtures.Mixture(mixture_table)
    mixture = gv.mixture_list[0]
    # assert
    assert len(gv.mixture_list) == 1
    assert mixture.number == '1'
    assert mixture.density == '7.8600'
    assert len(mixture.isotopes) == 13
