from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from portofolio.settings import _load_security_settings, _parse_boolean_setting


class SecuritySettingsTests(SimpleTestCase):
    def test_production_must_be_explicit(self):
        for environ in ({}, {"PRODUCTION": "  "}):
            with self.subTest(environ=environ):
                with self.assertRaisesMessage(
                    ImproperlyConfigured,
                    "PRODUCTION must be explicitly set",
                ):
                    _load_security_settings(environ)

    def test_boolean_accepts_case_and_surrounding_whitespace(self):
        for raw_value, expected in (
            ("  TrUe  ", True),
            (" YES ", True),
            (" On ", True),
            (" 0 ", False),
            (" FaLsE ", False),
            (" No ", False),
            (" off ", False),
        ):
            with self.subTest(raw_value=raw_value):
                self.assertIs(
                    _parse_boolean_setting("FLAG", raw_value),
                    expected,
                )

    def test_invalid_boolean_is_rejected(self):
        with self.assertRaisesMessage(
            ImproperlyConfigured,
            "DEBUG must be a valid boolean",
        ):
            _parse_boolean_setting("DEBUG", "perhaps")

    def test_debug_true_cannot_enable_debug_in_production(self):
        production, _, debug = _load_security_settings(
            {
                "PRODUCTION": " true ",
                "SECRET_KEY": "test-only-key",
                "DEBUG": " TrUe ",
            }
        )

        self.assertTrue(production)
        self.assertFalse(debug)

    def test_empty_secret_key_is_rejected_in_production(self):
        for secret_key in (None, "", "  "):
            with self.subTest(secret_key_is_empty=not secret_key or not secret_key.strip()):
                environ = {"PRODUCTION": "true"}
                if secret_key is not None:
                    environ["SECRET_KEY"] = secret_key
                with self.assertRaisesMessage(
                    ImproperlyConfigured,
                    "SECRET_KEY must be configured",
                ):
                    _load_security_settings(environ)

    def test_development_generates_temporary_key_when_missing(self):
        production, secret_key, debug = _load_security_settings(
            {"PRODUCTION": " false ", "DEBUG": "false"}
        )

        self.assertFalse(production)
        self.assertTrue(secret_key)
        self.assertFalse(debug)
