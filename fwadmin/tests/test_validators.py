import unittest
from django.core.exceptions import ValidationError
from fwadmin.validators import validate_port, validate_from_net


class ValidatorTests(unittest.TestCase):
    """ Unit tests for validator.py """

    def test_validate_port(self):
        # expected to be valid
        valid = (
            '10-20', '1-65535',
            '33', '44', '1024', '5000',
            ' 42     ', '    42', '1     - 5',
            '11-11',
        )
        # expected to raise ValidationError
        invalid = (
            '17-', '-6',
            '300000000000', '1-9000000000000',
            '1337-42',
            '14,15,16', '10 10 10',
            '', '-',
            'spam', '1-spam', 'spam-10', 'spam-spam',
            '1-2-3', '1--2', '-1-100'
        )
        for case in valid:
            self.assertEqual(validate_port(case), None)
        for case in invalid:
            with self.assertRaises(ValidationError):
                validate_port(case)

    def test_validate_from_net(self):
        # expected to be valid
        valid = (
            '127.0.0.1', '0.0.0.0', '255.255.255.255',
            '/23',
        )

        # expected to raise ValidationError
        invalid = (
            '123.123.123', '777.0.0.1', 'spam.0.0.1', '-1.0.0.1',
            '/34', '/-1', '/spam'
        )

        for case in valid:
            self.assertEqual(validate_from_net(case), None)
        for case in invalid:
            with self.assertRaises(ValidationError):
                validate_from_net(case)
