import pytest
from copy import copy
from ccp.state import *
from numpy.testing import assert_allclose


def test_state_possible_name():
    with pytest.raises(ValueError) as exc:
        State.define(p=100000, T=300, fluid='fake_name')
    assert 'Fluid fake_name not available.' in str(exc)

    #  pure fluid
    State.define(p=100000, T=300, fluid='n2')


def test_state_define():
    with pytest.raises(TypeError) as exc:
        State.define(p=100000, T=300)
    assert 'A fluid is required' in str(exc)

    state = State.define(p=100000, T=300, fluid='Methane')
    assert state.p().units == 'pascal'
    assert state.T().units == 'kelvin'
    assert state.p().magnitude == 100000
    assert state.T().magnitude == 300
    assert state.rhomass() == 0.6442542612980722


def test_state_define_units():
    state = State.define(p=Q_(1, 'bar'), T=Q_(300 - 273.15, 'celsius'),
                         fluid='Methane')

    assert state.p().units == 'pascal'
    assert state.T().units == 'kelvin'
    assert state.rho().units == 'kilogram/meter**3'
    assert state.p().magnitude == 100000
    assert state.T().magnitude == 300
    assert state.rho().magnitude == 0.6442542612980722


def test_state_define_units_mix():
    state = State.define(p=Q_(1, 'bar'), T=Q_(300 - 273.15, 'celsius'),
                         fluid={'Methane': 0.5, 'Ethane': 0.5})

    assert state.fluid == {'METHANE': 0.5, 'ETHANE': 0.5}

    assert state.gas_constant().units == 'joule/(kelvin mole)'
    assert state.molar_mass().units == 'kilogram/mole'
    assert state.p().units == 'pascal'
    assert state.T().units == 'kelvin'
    assert state.rho().units == 'kilogram/meter**3'
    assert state.v().units == 'meter**3/kilogram'
    assert state.z().units == ''
    assert state.h().units == 'joule/kilogram'
    assert state.s().units == 'joule/(kelvin kilogram)'

    assert state.gas_constant().magnitude == 8.314491
    assert state.molar_mass().magnitude == 0.02305592
    assert state.p().magnitude == 100000
    assert state.T().magnitude == 300
    assert_allclose(state.rho().magnitude, 0.9280595769591103)
    assert_allclose(state.v().magnitude, (1 / 0.9280595769591103))
    assert_allclose(state.z().magnitude, 0.99597784424262)
    assert_allclose(state.h().magnitude, 755784.43407392, rtol=1e-5)
    assert_allclose(state.s().magnitude, 4805.332018156618, rtol=1e-5)
    assert state.__repr__() == 'State.define(p=Q_("100000 Pa"), T=Q_("300 K"), fluid={"METHANE": 0.50000, "ETHANE": 0.50000})'

    state.update(p=200000, T=310)
    assert state.p().units == 'pascal'
    assert state.T().units == 'kelvin'
    assert state.rho().units == 'kilogram/meter**3'
    assert state.p().magnitude == 200000
    assert state.T().magnitude == 310
    assert_allclose(state.rho().magnitude, 1.8020813868455758)
    assert state.__repr__() == 'State.define(p=Q_("200000 Pa"), T=Q_("310 K"), fluid={"METHANE": 0.50000, "ETHANE": 0.50000})'


def test_state_copy():
    state = State.define(p=100000, T=300, fluid='Methane')
    state1 = copy(state)

    assert state == state
    assert state != state1
    assert state.rho() == state1.rho()


def test_rho_p_inputs():
    state = State.define(rho=0.9280595769591103, p=Q_(1, 'bar'),
                         fluid={'Methane': 0.5, 'Ethane': 0.5})
    assert_allclose(state.T(), 300)


def test_rho_T_inputs():
    state = State.define(rho=0.9280595769591103, T=300,
                         fluid={'Methane': 0.5, 'Ethane': 0.5})
    assert_allclose(state.p(), 100000)


def test_h_s_inputs():
    state = State.define(h=755784.43407392, s=4805.332018156618,
                         fluid={'Methane': 0.5, 'Ethane': 0.5})
    assert_allclose(state.h().magnitude, 755784.43407392, rtol=1e-5)
    assert_allclose(state.s().magnitude, 4805.332018156618, rtol=1e-5)
    assert_allclose(state.rho().magnitude, 0.9280595769591103)


def test_h_p_inputs():
    state = State.define(h=755784.43407392, p=Q_(1, 'bar'),
                         fluid={'Methane': 0.5, 'Ethane': 0.5})
    assert_allclose(state.h().magnitude, 755784.43407392, rtol=1e-5)
    assert_allclose(state.s().magnitude, 4805.332018156618, rtol=1e-5)
    assert_allclose(state.rho().magnitude, 0.9280595769591103)


def test_T_s_inputs():
    state = State.define(T=300, s=4805.332018156618,
                         fluid={'Methane': 0.5, 'Ethane': 0.5})
    assert_allclose(state.h().magnitude, 755784.43407392, rtol=1e-5)
    assert_allclose(state.s().magnitude, 4805.332018156618, rtol=1e-5)
    assert_allclose(state.rho().magnitude, 0.9280595769591103)
