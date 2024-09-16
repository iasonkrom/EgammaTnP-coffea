from __future__ import annotations

import os

import pytest
from coffea.dataset_tools import preprocess

from egamma_tnp.triggers import ElePt_CaloIdVT_GsfTrkIdT


@pytest.mark.parametrize("do_preprocess", [True, False])
@pytest.mark.parametrize("allow_read_errors_with_report", [True, False])
def test_without_compute(do_preprocess, allow_read_errors_with_report):
    if allow_read_errors_with_report:
        fileset = {
            "sample": {
                "files": {
                    os.path.abspath("tests/samples/TnPNTuples_el.root"): "fitter_tree",
                    os.path.abspath("tests/samples/not_a_file.root"): "fitter_tree",
                }
            }
        }
    else:
        fileset = {"sample": {"files": {os.path.abspath("tests/samples/TnPNTuples_el.root"): "fitter_tree"}}}

    if do_preprocess:
        if allow_read_errors_with_report:
            with pytest.raises(FileNotFoundError):
                preprocess(fileset)
            fileset_available, fileset_updated = preprocess(fileset, skip_bad_files=True)
            fileset = fileset_available

    tag_n_probe = ElePt_CaloIdVT_GsfTrkIdT(
        fileset,
        trigger_pt=115,
        mode="from_mini_ntuples",
        tags_pt_cut=35,
        probes_pt_cut=5,
        use_sc_eta=False,
        avoid_ecal_transition_tags=False,
    )

    res = tag_n_probe.get_1d_pt_eta_phi_tnp_histograms(
        "passHltEle115CaloIdVTGsfTrkIdTGsf",
        uproot_options={"allow_read_errors_with_report": allow_read_errors_with_report},
        compute=False,
        scheduler=None,
        progress=False,
    )

    if allow_read_errors_with_report:
        histograms = res[0]["sample"]
    else:
        histograms = res["sample"]

    hpt_pass_barrel, hpt_all_barrel = histograms["pt"]["barrel"].values()
    hpt_pass_endcap, hpt_all_endcap = histograms["pt"]["endcap"].values()
    heta_pass, heta_all = histograms["eta"]["entire"].values()
    hphi_pass, hphi_all = histograms["phi"]["entire"].values()

    assert hpt_pass_barrel.sum(flow=True).value + hpt_pass_endcap.sum(flow=True).value == 0.0
    assert hpt_all_barrel.sum(flow=True).value + hpt_all_endcap.sum(flow=True).value == 0.0
    assert heta_pass.sum(flow=True).value == 0.0
    assert heta_all.sum(flow=True).value == 0.0
    assert hphi_pass.sum(flow=True).value == 0.0
    assert hphi_all.sum(flow=True).value == 0.0

    assert hpt_pass_barrel.values(flow=True)[0] + hpt_pass_endcap.values(flow=True)[0] == 0.0
    assert hpt_all_barrel.values(flow=True)[0] + hpt_all_endcap.values(flow=True)[0] == 0.0
    assert heta_pass.values(flow=True)[0] == 0.0
    assert heta_all.values(flow=True)[0] == 0.0
    assert hphi_pass.values(flow=True)[0] == 0.0
    assert hphi_all.values(flow=True)[0] == 0.0


@pytest.mark.parametrize("do_preprocess", [True, False])
@pytest.mark.parametrize("allow_read_errors_with_report", [True, False])
def test_local_compute(do_preprocess, allow_read_errors_with_report):
    if allow_read_errors_with_report:
        fileset = {
            "sample": {
                "files": {
                    os.path.abspath("tests/samples/TnPNTuples_el.root"): "fitter_tree",
                    os.path.abspath("tests/samples/not_a_file.root"): "fitter_tree",
                }
            }
        }
    else:
        fileset = {"sample": {"files": {os.path.abspath("tests/samples/TnPNTuples_el.root"): "fitter_tree"}}}

    if do_preprocess:
        if allow_read_errors_with_report:
            with pytest.raises(FileNotFoundError):
                preprocess(fileset)
            fileset_available, fileset_updated = preprocess(fileset, skip_bad_files=True)
            fileset = fileset_available

    tag_n_probe = ElePt_CaloIdVT_GsfTrkIdT(
        fileset,
        trigger_pt=115,
        mode="from_mini_ntuples",
        tags_pt_cut=35,
        probes_pt_cut=5,
        use_sc_eta=False,
        avoid_ecal_transition_tags=False,
    )

    res = tag_n_probe.get_1d_pt_eta_phi_tnp_histograms(
        "passHltEle115CaloIdVTGsfTrkIdTGsf",
        uproot_options={"allow_read_errors_with_report": allow_read_errors_with_report},
        compute=True,
        scheduler=None,
        progress=True,
    )

    if allow_read_errors_with_report:
        histograms = res[0]["sample"]
        report = res[1]["sample"]
        if not do_preprocess:
            assert report.exception[1] == "FileNotFoundError"
    else:
        histograms = res["sample"]

    hpt_pass_barrel, hpt_all_barrel = histograms["pt"]["barrel"].values()
    hpt_pass_endcap, hpt_all_endcap = histograms["pt"]["endcap"].values()
    heta_pass, heta_all = histograms["eta"]["entire"].values()
    hphi_pass, hphi_all = histograms["phi"]["entire"].values()

    assert hpt_pass_barrel.sum(flow=True).value + hpt_pass_endcap.sum(flow=True).value == 2.0
    assert hpt_all_barrel.sum(flow=True).value + hpt_all_endcap.sum(flow=True).value == 490.0 - 2.0
    assert heta_pass.sum(flow=True).value == 2.0
    assert heta_all.sum(flow=True).value == 505.0 - 2.0
    assert hphi_pass.sum(flow=True).value == 2.0
    assert hphi_all.sum(flow=True).value == 505.0 - 2.0

    assert hpt_pass_barrel.values(flow=True)[0] + hpt_pass_endcap.values(flow=True)[0] == 0.0
    assert hpt_all_barrel.values(flow=True)[0] + hpt_all_endcap.values(flow=True)[0] == 0.0
    assert heta_pass.values(flow=True)[0] == 0.0
    assert heta_all.values(flow=True)[0] == 0.0
    assert hphi_pass.values(flow=True)[0] == 0.0
    assert hphi_all.values(flow=True)[0] == 0.0


@pytest.mark.parametrize("do_preprocess", [True, False])
@pytest.mark.parametrize("allow_read_errors_with_report", [True, False])
def test_distributed_compute(do_preprocess, allow_read_errors_with_report):
    from distributed import Client

    if allow_read_errors_with_report:
        fileset = {
            "sample": {
                "files": {
                    os.path.abspath("tests/samples/TnPNTuples_el.root"): "fitter_tree",
                    os.path.abspath("tests/samples/not_a_file.root"): "fitter_tree",
                }
            }
        }
    else:
        fileset = {"sample": {"files": {os.path.abspath("tests/samples/TnPNTuples_el.root"): "fitter_tree"}}}

    if do_preprocess:
        if allow_read_errors_with_report:
            with pytest.raises(FileNotFoundError):
                preprocess(fileset)
            fileset_available, fileset_updated = preprocess(fileset, skip_bad_files=True)
            fileset = fileset_available

    tag_n_probe = ElePt_CaloIdVT_GsfTrkIdT(
        fileset,
        trigger_pt=115,
        mode="from_mini_ntuples",
        tags_pt_cut=35,
        probes_pt_cut=5,
        use_sc_eta=False,
        avoid_ecal_transition_tags=False,
    )

    with Client():
        res = tag_n_probe.get_1d_pt_eta_phi_tnp_histograms(
            "passHltEle115CaloIdVTGsfTrkIdTGsf",
            uproot_options={"allow_read_errors_with_report": allow_read_errors_with_report},
            compute=True,
            scheduler=None,
            progress=True,
        )

        if allow_read_errors_with_report:
            histograms = res[0]["sample"]
            report = res[1]["sample"]
            if not do_preprocess:
                assert report.exception[1] == "FileNotFoundError"
        else:
            histograms = res["sample"]

        hpt_pass_barrel, hpt_all_barrel = histograms["pt"]["barrel"].values()
        hpt_pass_endcap, hpt_all_endcap = histograms["pt"]["endcap"].values()
        heta_pass, heta_all = histograms["eta"]["entire"].values()
        hphi_pass, hphi_all = histograms["phi"]["entire"].values()

        assert hpt_pass_barrel.sum(flow=True).value + hpt_pass_endcap.sum(flow=True).value == 2.0
        assert hpt_all_barrel.sum(flow=True).value + hpt_all_endcap.sum(flow=True).value == 490.0 - 2.0
        assert heta_pass.sum(flow=True).value == 2.0
        assert heta_all.sum(flow=True).value == 505.0 - 2.0
        assert hphi_pass.sum(flow=True).value == 2.0
        assert hphi_all.sum(flow=True).value == 505.0 - 2.0

        assert hpt_pass_barrel.values(flow=True)[0] + hpt_pass_endcap.values(flow=True)[0] == 0.0
        assert hpt_all_barrel.values(flow=True)[0] + hpt_all_endcap.values(flow=True)[0] == 0.0
        assert heta_pass.values(flow=True)[0] == 0.0
        assert heta_all.values(flow=True)[0] == 0.0
        assert hphi_pass.values(flow=True)[0] == 0.0
        assert hphi_all.values(flow=True)[0] == 0.0
