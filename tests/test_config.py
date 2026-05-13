import unittest

from reddit_radar.config import Settings


class ConfigTests(unittest.TestCase):
    def test_settings_ignore_unrelated_environment_entries(self) -> None:
        settings = Settings(
            _env_file=None,
            github_access_token="not-used-by-this-app",
        )

        self.assertEqual("", settings.reddit_client_id)

    def test_reddit_validation_reports_missing_names_only(self) -> None:
        settings = Settings(_env_file=None)

        missing = settings.missing_reddit_credentials()

        self.assertEqual(
            ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"],
            missing,
        )

    def test_reddit_validation_reports_missing_user_agent(self) -> None:
        settings = Settings(
            _env_file=None,
            reddit_client_id="client",
            reddit_client_secret="secret",
            reddit_user_agent="",
        )

        self.assertEqual(["REDDIT_USER_AGENT"], settings.missing_reddit_credentials())


if __name__ == "__main__":
    unittest.main()
