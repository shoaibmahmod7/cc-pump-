import pytest
import numpy as np
import matplotlib.pyplot as plt
from numpy.testing import assert_allclose
from ccp import ureg, Q_
from ccp.state import State
from ccp.point import Point
from ccp.curve import Curve


def test_raise_1_point():
    with pytest.raises(TypeError) as ex:
        Curve([1])
    assert 'At least 2 points' in str(ex)


@pytest.fixture
def curve0():
    suc = State.define(p=Q_(1, 'bar'), T=300, fluid='co2')
    disch = State.define(p=Q_(2, 'bar'), T=370, fluid='co2')
    disch1 = State.define(p=Q_(2.5, 'bar'), T=375, fluid='co2')
    p0 = Point(suc=suc, disch=disch, flow_v=1, speed=1)
    p1 = Point(suc=suc, disch=disch1, flow_v=2, speed=1)
    return Curve([p0, p1])


def test_curve_suc_parameters(curve0):
    assert curve0.suc.p().units == 'pascal'
    assert_allclose(curve0.suc.p(), np.array([100000., 100000.]))
    assert curve0.suc.T().units == 'kelvin'
    assert_allclose(curve0.suc.T(), np.array([300., 300.]))


def test_curve_disch_parameters(curve0):
    assert curve0.disch.p().units == 'pascal'
    assert_allclose(curve0.disch.p(), np.array([200000., 250000.]))
    assert curve0.disch.T().units == 'kelvin'
    assert_allclose(curve0.disch.T(), np.array([370., 375.]))


def test_curve_performance_parameters(curve0):
    assert curve0.head.units == 'joule/kilogram'
    assert curve0.eff.units == ureg.dimensionless
    assert curve0.power.units == 'watt'
    assert_allclose(curve0.head, np.array([43527.78012, 57942.686265]))
    assert_allclose(curve0.eff, np.array([0.709246, 0.881994]), rtol=1e-6)
    assert_allclose(curve0.power,
                    np.array([108814.010351, 232958.372613]), rtol=1e-6)


def test_curve_interpolation(curve0):
    assert_allclose(curve0.disch.T_interpolated(1), 370.)
    #  test for mutation of quantity magnitude
    a = Q_(1., 'm**3/h')
    assert_allclose(curve0.disch.T_interpolated(a), 370.)
    assert isinstance(a.m, float)



@pytest.fixture
def curve1():
    suc = State.define(p=Q_(1, 'bar'), T=300, fluid='co2')
    disch = State.define(p=Q_(2, 'bar'), T=370, fluid='co2')
    disch1 = State.define(p=Q_(2.5, 'bar'), T=375, fluid='co2')
    disch2 = State.define(p=Q_(2.6, 'bar'), T=376, fluid='co2')
    disch3 = State.define(p=Q_(2.7, 'bar'), T=377, fluid='co2')
    p0 = Point(suc=suc, disch=disch, flow_v=1, speed=1)
    p1 = Point(suc=suc, disch=disch1, flow_v=2, speed=1)
    p2 = Point(suc=suc, disch=disch2, flow_v=3, speed=1)
    p3 = Point(suc=suc, disch=disch3, flow_v=4, speed=1)
    return Curve([p0, p1, p2, p3])


def test_curve_p_plot(curve1):
    fig, ax = plt.subplots()
    ax = curve1.suc.p_plot(ax=ax)
    line0 = ax.get_lines()[0]
    exp_xydata = np.array([[1.00000000e+00, 1.00000000e+05],
                           [1.10344828e+00, 1.00000000e+05],
                           [1.20689655e+00, 1.00000000e+05],
                           [1.31034483e+00, 1.00000000e+05]])
    assert_allclose(line0.get_xydata()[:4], exp_xydata)


def test_curve_head_plot(curve1):
    fig, ax = plt.subplots()
    ax = curve1.head_plot(ax=ax)
    line0 = ax.get_lines()[0]
    exp_xydata = np.array([[1.00000000e+00, 4.35277801e+04],
                           [1.10344828e+00, 4.59134091e+04],
                           [1.20689655e+00, 4.80593494e+04],
                           [1.31034483e+00, 4.99786240e+04]])
    assert_allclose(line0.get_xydata()[:4], exp_xydata)
