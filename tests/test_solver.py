import itertools

import pytest
import torch
from torch import nn

import cebra.data
import cebra.datasets
import cebra.solver

device = "cpu"

single_session_tests = []
for args in [
]:
    single_session_tests.append((*args, cebra.solver.SingleSessionSolver))

    single_session_hybrid_tests.append(
        (*args, cebra.solver.SingleSessionHybridSolver))
multi_session_tests = []
              cebra.data.ContinuousMultiSessionDataLoader)]:
    multi_session_tests.append((*args, cebra.solver.MultiSessionSolver))

print(single_session_tests)


def _get_loader(data_name, loader_initfunc):
    data = cebra.datasets.init(data_name)
    kwargs = dict(num_steps=10, batch_size=32)
    loader = loader_initfunc(data, **kwargs)
    return loader


def _make_model(dataset):


def _make_behavior_model(dataset):


@pytest.mark.parametrize("data_name, loader_initfunc, solver_initfunc",
                         single_session_tests)
def test_single_session(data_name, loader_initfunc, solver_initfunc):
    loader = _get_loader(data_name, loader_initfunc)
    model = _make_model(loader.dataset)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    solver = solver_initfunc(model=model,
                             criterion=criterion,
                             optimizer=optimizer)

    batch = next(iter(loader))
    assert batch.reference.shape == (32, loader.dataset.input_dimension, 10)
    log = solver.step(batch)
    assert isinstance(log, dict)

    solver.fit(loader)


@pytest.mark.parametrize("data_name, loader_initfunc, solver_initfunc",
                         single_session_tests)
def test_single_session_auxvar(data_name, loader_initfunc, solver_initfunc):

    loader = _get_loader(data_name, loader_initfunc)
    model = _make_model(loader.dataset)
    behavior_model = _make_behavior_model(loader.dataset)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    solver = solver_initfunc(
        model=model,
        criterion=criterion,
        optimizer=optimizer,
    )

    batch = next(iter(loader))
    assert batch.reference.shape == (32, loader.dataset.input_dimension, 10)
    log = solver.step(batch)
    assert isinstance(log, dict)

    solver.fit(loader)


                         single_session_hybrid_tests)
                              32, 3)
    assert isinstance(log, dict)

    solver.fit(loader)
@pytest.mark.parametrize("data_name, loader_initfunc, solver_initfunc",
                         multi_session_tests)
def test_multi_session(data_name, loader_initfunc, solver_initfunc):
    loader = _get_loader(data_name, loader_initfunc)
    model = nn.ModuleList(
        [_make_model(dataset) for dataset in loader.dataset.iter_sessions()])
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

    solver = solver_initfunc(model=model,
                             criterion=criterion,
                             optimizer=optimizer)

    batch = next(iter(loader))
    for session_id, dataset in enumerate(loader.dataset.iter_sessions()):
        assert batch[session_id].reference.shape == (32,
                                                     dataset.input_dimension,
                                                     10)
        assert batch[session_id].index is not None

    log = solver.step(batch)
    assert isinstance(log, dict)

    solver.fit(loader)