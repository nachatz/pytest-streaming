from pytest import Pytester


class TestPulsarFixtures:
    def test_pulsar_marker_fixture(self, pytester: Pytester) -> None:
        pytester.copy_example("test_pulsar_fixtures.py")
        result = pytester.runpytest("-k", "test_pulsar_marker_fixture")
        result.assert_outcomes(passed=1)

    def test_pulsar_client_fixture(self, pytester: Pytester) -> None:
        pytester.copy_example("test_pulsar_fixtures.py")
        result = pytester.runpytest("-k", "test_pulsar_client_fixture")
        result.assert_outcomes(passed=1)

    def test_pulsar_consumer_fixture(self, pytester: Pytester) -> None:
        pytester.copy_example("test_pulsar_fixtures.py")
        result = pytester.runpytest("-k", "test_pulsar_consumer_fixture")
        result.assert_outcomes(passed=1)

    def test_pulsar_producers_fixture(self, pytester: Pytester) -> None:
        pytester.copy_example("test_pulsar_fixtures.py")
        result = pytester.runpytest("-k", "test_pulsar_producers_fixture")
        result.assert_outcomes(passed=1)
