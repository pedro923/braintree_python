from tests.test_helper import *
import datetime

class TestCreditCard(unittest.TestCase):
    def test_create_raises_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            CreditCard.create({"bad_key": "value"})

    def test_update_raises_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            CreditCard.update("token", {"bad_key": "value"})

    def test_create_signature(self):
        expected = ["billing_address_id", "cardholder_name", "cvv", "expiration_date", "expiration_month",
            "expiration_year", "number", "token", "venmo_sdk_payment_method_code",
            "device_data", "payment_method_nonce",
            "device_session_id", "fraud_merchant_id",
            {
                "billing_address": [
                    "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
                    "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address"
                ]
            },
            {"options": [
                "fail_on_duplicate_payment_method",
                "make_default",
                "skip_advanced_fraud_checking",
                "venmo_sdk_session",
                "verification_account_type",
                "verification_amount",
                "verification_merchant_account_id",
                "verify_card",
                {"adyen":["overwrite_brand", "selected_brand"]}
            ]},
            {
                "three_d_secure_pass_thru": [
                    "cavv", "ds_transaction_id", "eci_flag", "three_d_secure_version", "xid"
                ]
            },
            "customer_id"
        ]
        self.assertEqual(expected, CreditCard.create_signature())

    def test_update_signature(self):
        expected = ["billing_address_id", "cardholder_name", "cvv", "expiration_date", "expiration_month",
            "expiration_year", "number", "token", "venmo_sdk_payment_method_code",
            "device_data", "payment_method_nonce",
            "device_session_id", "fraud_merchant_id",
            {
                "billing_address": [
                    "company", "country_code_alpha2", "country_code_alpha3", "country_code_numeric", "country_name",
                    "extended_address", "first_name", "last_name", "locality", "postal_code", "region", "street_address",
                    {"options": ["update_existing"]}
                ]
            },
            {"options": [
                "fail_on_duplicate_payment_method",
                "make_default",
                "skip_advanced_fraud_checking",
                "venmo_sdk_session",
                "verification_account_type",
                "verification_amount",
                "verification_merchant_account_id",
                "verify_card",
                {"adyen":["overwrite_brand", "selected_brand"]}
            ]},
            {
                "three_d_secure_pass_thru": [
                    "cavv", "ds_transaction_id", "eci_flag", "three_d_secure_version", "xid"
                ]
            },
        ]
        self.assertEqual(expected, CreditCard.update_signature())

    def test_finding_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            CreditCard.find(" ")

    def test_finding_none_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            CreditCard.find(None)

    def test_from_nonce_empty_id_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            CreditCard.from_nonce(" ")

    def test_from_nonce_none_raises_not_found_exception(self):
        with self.assertRaises(NotFoundError):
            CreditCard.from_nonce(None)

    def test_multiple_verifications_sort(self):
        verification1 = {"created_at": datetime.datetime(2014, 11, 18, 23, 20, 20), "id": 123, "amount": "0.00"}
        verification2 = {"created_at": datetime.datetime(2014, 11, 18, 23, 20, 21), "id": 456, "amount": "1.00"}
        credit_card = CreditCard(Configuration.gateway(), {"verifications": [verification1, verification2]})
        self.assertEqual(456, credit_card.verification.id)
        self.assertEqual(1.00, credit_card.verification.amount)
