import pytest

pytest.importorskip("numpy")
pytest.importorskip("scipy")

from contextlib import nullcontext as does_not_raise

import networkx as nx


class TestFlowClosenessCentrality:
    def test_K4(self):
        """Closeness centrality: K4"""
        G = nx.complete_graph(4)
        b = nx.current_flow_closeness_centrality(G)
        b_answer = {0: 2.0 / 3, 1: 2.0 / 3, 2: 2.0 / 3, 3: 2.0 / 3}
        for n in sorted(G):
            assert b[n] == pytest.approx(b_answer[n], abs=1e-7)

    def test_P4(self):
        """Closeness centrality: P4"""
        G = nx.path_graph(4)
        b = nx.current_flow_closeness_centrality(G)
        b_answer = {0: 1.0 / 6, 1: 1.0 / 4, 2: 1.0 / 4, 3: 1.0 / 6}
        for n in sorted(G):
            assert b[n] == pytest.approx(b_answer[n], abs=1e-7)

    def test_star(self):
        """Closeness centrality: star"""
        G = nx.Graph()
        nx.add_star(G, ["a", "b", "c", "d"])
        b = nx.current_flow_closeness_centrality(G)
        b_answer = {"a": 1.0 / 3, "b": 0.6 / 3, "c": 0.6 / 3, "d": 0.6 / 3}
        for n in sorted(G):
            assert b[n] == pytest.approx(b_answer[n], abs=1e-7)

    @pytest.mark.parametrize(
        ("G", "expectation"),
        [
            (
                nx.Graph(),
                pytest.raises(
                    nx.NetworkXPointlessConcept,
                    match="centrality is undefined for the null graph",
                ),
            ),
            (
                nx.path_graph(1),
                pytest.raises(
                    nx.NetworkXError,
                    match="graph with 1 node has fewer than three nodes",
                ),
            ),
            (
                nx.Graph([(0, 1)]),
                pytest.raises(
                    nx.NetworkXError,
                    match="graph with 2 nodes has fewer than three nodes",
                ),
            ),
            (nx.Graph([(0, 1), (1, 2)]), does_not_raise()),
            (
                nx.Graph([(0, 1), (2, 3)]),
                pytest.raises(nx.NetworkXError, match="graph is not connected"),
            ),
            (nx.DiGraph(), pytest.raises(nx.NetworkXNotImplemented)),
            (nx.MultiGraph(), pytest.raises(nx.NetworkXNotImplemented)),
            (nx.MultiDiGraph(), pytest.raises(nx.NetworkXNotImplemented)),
        ],
    )
    def test_current_flow_closeness_centrality_exceptions(self, G, expectation):
        with expectation:
            nx.current_flow_closeness_centrality(G)


class TestWeightedFlowClosenessCentrality:
    pass
