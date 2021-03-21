import pytest
from numpy.testing import assert_allclose
from ccp import ureg
from ccp.point import *
from pathlib import Path
from tempfile import tempdir

skip = False  # skip slow tests


@pytest.fixture
def suc_0():
    fluid = dict(CarbonDioxide=0.76064, R134a=0.23581, Nitrogen=0.00284, Oxygen=0.00071)
    return State.define(p=Q_(1.839, "bar"), T=291.5, fluid=fluid)


@pytest.fixture
def disch_0():
    fluid = dict(CarbonDioxide=0.76064, R134a=0.23581, Nitrogen=0.00284, Oxygen=0.00071)
    return State.define(p=Q_(5.902, "bar"), T=380.7, fluid=fluid)


def test_raises_no_b_D(suc_0, disch_0):
    with pytest.raises(ValueError) as ex:
        Point(suc=suc_0, disch=disch_0, flow_v=1, speed=1)
        assert "Arguments b and D" in str(ex.value)
    with pytest.raises(ValueError) as ex:
        Point(suc=suc_0, disch=disch_0, flow_v=1, speed=1, b=1)
        assert "Arguments b and D" in str(ex.value)
    with pytest.raises(ValueError) as ex:
        Point(suc=suc_0, disch=disch_0, flow_v=1, speed=1, D=1)
        assert "Arguments b and D" in str(ex.value)


@pytest.fixture
def point_disch_flow_v_speed_suc(suc_0, disch_0):
    point_disch_suc = Point(suc=suc_0, disch=disch_0, flow_v=1, speed=1, b=1, D=1)
    return point_disch_suc


def test_point_disch_flow_v_speed_suc(suc_0, disch_0, point_disch_flow_v_speed_suc):
    assert point_disch_flow_v_speed_suc.suc == suc_0
    assert point_disch_flow_v_speed_suc.disch == disch_0
    assert_allclose(point_disch_flow_v_speed_suc.flow_v, 1.0)
    assert_allclose(point_disch_flow_v_speed_suc.flow_m, 4.43677)
    assert_allclose(point_disch_flow_v_speed_suc.speed, 1.0)
    assert_allclose(point_disch_flow_v_speed_suc.head, 55377.404355)
    assert_allclose(point_disch_flow_v_speed_suc.eff, 0.71243, rtol=1e-4)
    assert_allclose(point_disch_flow_v_speed_suc.phi, 2.546479)
    assert_allclose(point_disch_flow_v_speed_suc.psi, 443019.234838)
    assert_allclose(point_disch_flow_v_speed_suc.volume_ratio, 2.467451, rtol=1e-4)
    assert_allclose(point_disch_flow_v_speed_suc.power, 344871.32195)


@pytest.fixture
def point_eff_phi_psi_suc_volume_ratio(suc_0):
    point_eff_phi_psi_suc_volume_ratio = Point(
        suc=suc_0, eff=0.71243, phi=2.546479, psi=443019.234838, volume_ratio=2.467451, b=1, D=1
    )
    return point_eff_phi_psi_suc_volume_ratio


def test_point_eff_suc_volume_ratio(suc_0, disch_0, point_eff_phi_psi_suc_volume_ratio):
    assert point_eff_phi_psi_suc_volume_ratio.suc == suc_0
    assert point_eff_phi_psi_suc_volume_ratio.disch == disch_0
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.flow_v, 1.0, rtol=1e-4)
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.flow_m, 4.43677, rtol=1e-4)
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.speed, 1.0, rtol=1e-4)
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.head, 55377.404355, rtol=1e-4)
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.eff, 0.71243, rtol=1e-4)
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.phi, 2.546479, rtol=1e-4)
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.psi, 443019.234838, rtol=1e-4)
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.volume_ratio, 2.467451, rtol=1e-4)
    assert_allclose(point_eff_phi_psi_suc_volume_ratio.power, 344871.32195, rtol=1e-3)


@pytest.fixture
def point_eff_flow_v_head_speed_suc(suc_0):
    point_eff_flow_v_head_speed_suc = Point(suc=suc_0, head=55377.404355, eff=0.71243, flow_v=1, speed=1, b=1, D=1)
    return point_eff_flow_v_head_speed_suc


def test_point_eff_flow_v_head_speed_suc(suc_0, disch_0, point_eff_flow_v_head_speed_suc):
    assert point_eff_flow_v_head_speed_suc.suc == suc_0
    assert point_eff_flow_v_head_speed_suc.disch == disch_0
    assert_allclose(point_eff_flow_v_head_speed_suc.flow_v, 1.0, rtol=1e-4)
    assert_allclose(point_eff_flow_v_head_speed_suc.flow_m, 4.43677, rtol=1e-4)
    assert_allclose(point_eff_flow_v_head_speed_suc.speed, 1.0, rtol=1e-4)
    assert_allclose(point_eff_flow_v_head_speed_suc.head, 55377.404355, rtol=1e-4)
    assert_allclose(point_eff_flow_v_head_speed_suc.eff, 0.71243, rtol=1e-4)
    assert_allclose(point_eff_flow_v_head_speed_suc.phi, 2.546479, rtol=1e-4)
    assert_allclose(point_eff_flow_v_head_speed_suc.psi, 443019.234838, rtol=1e-4)
    assert_allclose(point_eff_flow_v_head_speed_suc.volume_ratio, 2.467451, rtol=1e-4)
    assert_allclose(point_eff_flow_v_head_speed_suc.power, 344871.32195, rtol=1e-4)


def test_point_n_exp(suc_0, disch_0):
    assert_allclose(n_exp(suc_0, disch_0), 1.2910625831119145, rtol=1e-6)


def test_point_head_pol(suc_0, disch_0):
    assert head_polytropic(suc_0, disch_0).units == "joule/kilogram"
    assert_allclose(head_polytropic(suc_0, disch_0), 55280.691617)


def test_point_head_pol_mallen_saville(suc_0, disch_0):
    assert head_pol_mallen_saville(suc_0, disch_0).units == "joule/kilogram"
    assert_allclose(head_pol_mallen_saville(suc_0, disch_0), 55497.486223)


def test_point_eff_polytropic(suc_0, disch_0):
    assert_allclose(eff_polytropic(suc_0, disch_0), 0.711186, rtol=1e-5)


def test_point_eff_pol_schultz(suc_0, disch_0):
    assert_allclose(eff_pol_schultz(suc_0, disch_0), 0.71243, rtol=1e-5)


def test_point_head_isen(suc_0, disch_0):
    assert head_isentropic(suc_0, disch_0).units == "joule/kilogram"
    assert_allclose(head_isentropic(suc_0, disch_0).magnitude, 53165.986507, rtol=1e-5)


def test_eff_isentropic(suc_0, disch_0):
    assert_allclose(eff_isentropic(suc_0, disch_0), 0.68398, rtol=1e-5)


def test_schultz_f(suc_0, disch_0):
    assert_allclose(schultz_f(suc_0, disch_0), 1.00175, rtol=1e-5)


def test_head_pol_schultz(suc_0, disch_0):
    assert head_pol_schultz(suc_0, disch_0).units == "joule/kilogram"
    assert_allclose(head_pol_schultz(suc_0, disch_0), 55377.406664, rtol=1e-6)


def test_equality(point_disch_flow_v_speed_suc):
    point_1 = Point(
        suc=point_disch_flow_v_speed_suc.suc,
        speed=point_disch_flow_v_speed_suc.speed,
        flow_v=point_disch_flow_v_speed_suc.flow_v,
        head=point_disch_flow_v_speed_suc.head,
        eff=point_disch_flow_v_speed_suc.eff,
        b=point_disch_flow_v_speed_suc.b,
        D=point_disch_flow_v_speed_suc.D,
    )
    assert point_disch_flow_v_speed_suc == point_1


# def test_converted_from():
#     fluid = dict(
#         methane=0.69945,
#         ethane=0.09729,
#         propane=0.0557,
#         nbutane=0.0178,
#         ibutane=0.0102,
#         npentane=0.0039,
#         ipentane=0.0036,
#         nhexane=0.0018,
#         n2=0.0149,
#         co2=0.09259,
#         h2s=0.00017,
#         water=0.002,
#     )
#     suc = State.define(p=Q_(1.6995, "MPa"), T=311.55, fluid=fluid)
#
#     p0 = Point(
#         suc=suc,
#         flow_v=Q_(6501.67, "m**3/h"),
#         speed=Q_(11145, "RPM"),
#         head=Q_(179.275, "kJ/kg"),
#         eff=0.826357,
#         b=Q_(28.5, "mm"),
#         D=Q_(365, "mm"),
#     )
#
#     suc1 = State.define(
#         p=Q_(0.2, "MPa"), T=301.58, fluid={"n2": 1 - 1e-15, "co2": 1e-15}
#     )
#     p1 = Point.convert_from(p0, suc=suc1)
#
#     assert_allclose(p1.b, p0.b)
#     assert_allclose(p1.D, p0.D)
#     assert_allclose(p1.speed, p0.speed)
#     assert_allclose(p1.eff, p0.eff, rtol=1e-4)
#     assert_allclose(p1.phi, p0.phi, rtol=1e-2)
#     assert_allclose(p1.psi, p0.psi, rtol=1e-2)
#     assert_allclose(p1.volume_ratio_ratio, 1.0)
#     # assert_allclose(p1.head, 208933.668804, rtol=1e-2)
#     # assert_allclose(p1.power, 1101698.5104, rtol=1e-2)
#     # assert_allclose(p1.speed, 1257.17922, rtol=1e-3)


def test_save_load(point_disch_flow_v_speed_suc):
    file = Path(tempdir) / "suc_0.toml"
    point_disch_flow_v_speed_suc.save(file)
    point_0_loaded = Point.load(file)
    assert point_disch_flow_v_speed_suc == point_0_loaded
