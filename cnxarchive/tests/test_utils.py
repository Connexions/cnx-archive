# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2013, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
import os
import uuid
import unittest


class SplitIdentTestCase(unittest.TestCase):

    from ..utils import CNXHash

    def call_target(self, *args, **kwargs):
        from ..utils import split_ident_hash
        return split_ident_hash(*args, **kwargs)

    def test_empty_value(self):
        # Case of supplying the utility function with an empty indent-hash.
        ident_hash = ''

        with self.assertRaises(ValueError):
            self.call_target(ident_hash)

    def test_complete_data(self):
        # Simple case of supplying the correct information and checking
        # for the correct results.
        expected_id, expected_version = (
            '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2', '1.12',
            )
        ident_hash = "{}@{}".format(expected_id, expected_version)

        id, version, id_type = self.call_target(ident_hash)

        self.assertEqual(id, expected_id)
        self.assertEqual(version, expected_version)
        self.assertEqual(id_type, CNXHash.FULLUUID)

    def test_uuid_only(self):
        # Case where the UUID has been the only value supplied in the
        # ident-hash.
        # This is mostly testing that the version value returns None.
        expected_id, expected_version = (
            '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2', '',
            )
        ident_hash = "{}@{}".format(expected_id, expected_version)

        id, version, id_type = self.call_target(ident_hash)

        self.assertEqual(id, expected_id)
        self.assertEqual(version, None)

    def test_invalid_id(self):
        # Case for testing for an invalid identifier.
        ident_hash = "not-a-valid-id@"

        from ..utils import IdentHashSyntaxError
        with self.assertRaises(IdentHashSyntaxError):
            self.call_target(ident_hash)

    def test_invalid_syntax(self):
        # Case for testing the ident-hash's syntax guards.
        ident_hash = "85e57f7902b347d28eedc1bbb1e1d5c2@1.2@select*frommodules"

        from ..utils import IdentHashSyntaxError
        with self.assertRaises(IdentHashSyntaxError):
            self.call_target(ident_hash)

    def test_w_split_version(self):
        expected_id, expected_version = (
            '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2',
            ('1', '12', ),
            )
        ident_hash = "{}@{}".format(expected_id, '.'.join(expected_version))

        id, version, id_type = self.call_target(ident_hash, True)

        self.assertEqual(id, expected_id)
        self.assertEqual(version, expected_version)
        self.assertEqual(id_type, CNXHash.FULLUUID)

    def test_w_split_version_on_major_version(self):
        expected_id, expected_version = (
            '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2',
            ('1', None, ),
            )
        ident_hash = "{}@{}".format(expected_id, expected_version[0])

        id, version, id_type = self.call_target(ident_hash, True)

        self.assertEqual(id, expected_id)
        self.assertEqual(version, expected_version)
        self.assertEqual(id_type, CNXHash.FULLUUID)

    def test_w_split_version_no_version(self):
        expected_id, expected_version = (
            '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2',
            (None, None, )
            )
        ident_hash = expected_id

        id, version, id_type = self.call_target(ident_hash, True)

        self.assertEqual(id, expected_id)
        self.assertEqual(version, expected_version)
        self.assertEqual(id_type, CNXHash.FULLUUID)


class JoinIdentTestCase(unittest.TestCase):

    def call_target(self, *args, **kwargs):
        from ..utils import join_ident_hash
        return join_ident_hash(*args, **kwargs)

    def test(self):
        id = '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2'
        version = ('2', '4', )
        expected = "{}@{}".format(id, '.'.join(version))
        ident_hash = self.call_target(id, version)
        self.assertEqual(expected, ident_hash)

    def test_w_UUID(self):
        id = uuid.uuid4()
        version = None
        expected = str(id)
        ident_hash = self.call_target(id, version)
        self.assertEqual(expected, ident_hash)

    def test_w_null_version(self):
        id = '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2'
        version = None
        expected = id
        ident_hash = self.call_target(id, version)
        self.assertEqual(expected, ident_hash)

    def test_w_null_str_version(self):
        id = '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2'
        version = ''
        expected = id
        ident_hash = self.call_target(id, version)
        self.assertEqual(expected, ident_hash)

    def test_w_str_version(self):
        id = '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2'
        version = '2'
        expected = "{}@{}".format(id, version)
        ident_hash = self.call_target(id, version)
        self.assertEqual(expected, ident_hash)

    def test_w_major_version(self):
        id = '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2'
        version = ('2', None, )
        expected = "{}@{}".format(id, version[0])
        ident_hash = self.call_target(id, version)
        self.assertEqual(expected, ident_hash)

    def test_w_double_null_version(self):
        id = '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2'
        version = (None, None, )
        expected = id
        ident_hash = self.call_target(id, version)
        self.assertEqual(expected, ident_hash)

    def test_w_invalid_version_sequence(self):
        id = '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2'
        version = ('1', )
        with self.assertRaises(AssertionError):
            self.call_target(id, version)

    def test_w_integer_version(self):
        id = '85e57f79-02b3-47d2-8eed-c1bbb1e1d5c2'
        version = (1, 2, )
        expected = '{}@1.2'.format(id)
        ident_hash = self.call_target(id, version)
        self.assertEqual(expected, ident_hash)


class SlugifyTestCase(unittest.TestCase):

    def call_target(self, *args, **kwargs):
        from ..utils import slugify
        return slugify(*args, **kwargs)

    def test_ascii(self):
        self.assertEqual(self.call_target('How to Work for Yourself: 100 Ways'),
                         'how-to-work-for-yourself-100-ways')

    def test_hyphen(self):
        self.assertEqual(self.call_target('Any Red-Blooded Girl'),
                         'any-red-blooded-girl')

    def test_underscore(self):
        self.assertEqual(self.call_target('Underscores _hello_'),
                         'underscores-_hello_')

    def test_unicode(self):
        self.assertEqual(self.call_target('Radioactive (Die Verstoßenen)'),
                         u'radioactive-die-verstoßenen')

        self.assertEqual(self.call_target(u'40文字でわかる！'
                                          u'　知っておきたいビジネス理論'),
                         u'40文字でわかる-知っておきたいビジネス理論')


class EscapeTestCase(unittest.TestCase):

    def call_target(self, *args, **kwargs):
        from ..utils import escape
        return escape(*args, **kwargs)

    def test_ascii(self):
        self.assertEqual(self.call_target('How to Work for Yourself: 100 Ways'),
                         'How to Work for Yourself: 100 Ways')

    def test_greater(self):
        self.assertEqual(self.call_target('this > that'),
                         'this &gt; that')

    def test_less(self):
        self.assertEqual(self.call_target('this < that'),
                         'this &lt; that')

    def test_amp(self):
        self.assertEqual(self.call_target('this & that'),
                         'this &amp; that')


class Utf8TestCase(unittest.TestCase):
    def call_target(self, *args, **kwargs):
        from ..utils import utf8
        return utf8(*args, **kwargs)

    def test_str(self):
        self.assertEqual(self.call_target('inførmation'), u'inførmation')

    def test_unicode(self):
        self.assertEqual(self.call_target(u'inførmation'), u'inførmation')

    def test_not_str(self):
        self.assertEqual(self.call_target(1), 1)

    def test_list(self):
        self.assertEqual([u'infør', u'mation'],
                         self.call_target(['infør', 'mation']))

    def test_tuple(self):
        self.assertEqual((u'infør', u'mation', ),
                         self.call_target(('infør', 'mation', )))

    def test_dict(self):
        self.assertEqual({u'inførmation': u'inførm'},
                         self.call_target({'inførmation': 'inførm'}))




from ..utils import CNXHash, IdentHashSyntaxError
class TestCNXHash(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._uuid = uuid.uuid4()
        cls._cnxhash = CNXHash(cls._uuid)

    def setUp(self):
        self.uuid = self._uuid
        self.cnxhash = self._cnxhash

    def test_convert_uuid(self):
        for i in range(0, 10000):
            expected_id = uuid.uuid4()
            returned_id = CNXHash.uuid2base64(expected_id)
            self.assertGreater(len(str(expected_id)), len(returned_id))
            returned_id = CNXHash.base642uuid(returned_id)
            self.assertEqual(expected_id, returned_id)

    def test_class_init(self):
        expected_uuid = self.uuid
        returned_uuid = CNXHash(expected_uuid)
        self.assertEqual(str(expected_uuid), str(returned_uuid))
        returned_uuid = CNXHash(hex=expected_uuid.get_hex())
        self.assertEqual(str(expected_uuid), str(returned_uuid))
        returned_uuid = CNXHash(str(expected_uuid))
        self.assertEqual(str(expected_uuid), str(returned_uuid))
        returned_uuid = CNXHash(bytes=expected_uuid.get_bytes())
        self.assertEqual(str(expected_uuid), str(returned_uuid))

    def test_truncated_hash(self):
        cnxhash = CNXHash(self.uuid)
        self.assertLessEqual(len(cnxhash.get_shortid()), len(str(cnxhash)))
        self.assertEqual(len(cnxhash.get_shortid()), CNXHash.short_hash_length)

    def test_validate(self):
        with self.assertRaises(IdentHashSyntaxError):
            self.assertFalse(CNXHash.validate(1))
        with self.assertRaises(IdentHashSyntaxError):
            self.assertFalse(CNXHash.validate([]))
        with self.assertRaises(IdentHashSyntaxError):
            self.assertFalse(CNXHash.validate('a'))
        self.assertEqual(CNXHash.validate(self.uuid), CNXHash.FULLUUID)
        self.assertEqual(CNXHash.validate(self.cnxhash), CNXHash.FULLUUID)
        self.assertEqual(CNXHash.validate(CNXHash.uuid2base64(self.uuid)), CNXHash.BASE64HASH)
        self.assertEqual(CNXHash.validate(self.cnxhash.get_shortid()), CNXHash.SHORTID) 
        self.assertEqual(CNXHash.validate(unicode(self.cnxhash.get_shortid())), CNXHash.SHORTID)

    def test_error_handling(self):
        with self.assertRaises(TypeError):
            CNXHash.uuid2base64(1)
        with self.assertRaises(ValueError):
            CNXHash.uuid2base64('a')
        with self.assertRaises(TypeError):
            CNXHash.base642uuid(1)
        with self.assertRaises(ValueError):
            CNXHash.base642uuid('a')
        with self.assertRaises(IdentHashSyntaxError):
            CNXHash.validate(1)

    def test_similarity(self):
        self.assertTrue(self.cnxhash.similar(self.cnxhash.get_shortid()))
        self.assertFalse(self.cnxhash.similar(uuid.uuid4()))
        self.assertFalse(self.cnxhash.similar([]))
        self.assertTrue(self.cnxhash.similar(self.uuid))
        self.assertTrue(CNXHash.identifiers_similar(self.cnxhash,self.cnxhash.get_shortid()))
        self.assertTrue(CNXHash.identifiers_similar(self.cnxhash.get_shortid(),self.cnxhash))
        self.assertTrue(CNXHash.identifiers_similar(self.cnxhash.get_shortid(),self.uuid))

    def test_equality(self):
        self.assertTrue(self.cnxhash == self.cnxhash)
        self.assertTrue(self.uuid == self.cnxhash)
        self.assertTrue(CNXHash.identifiers_equal(self.uuid, self.cnxhash))
        self.assertTrue(CNXHash.identifiers_equal(self.cnxhash, str(self.cnxhash)))
        self.assertTrue(CNXHash.identifiers_equal(str(self.cnxhash), self.cnxhash))
        self.assertFalse(CNXHash.identifiers_equal(self.cnxhash,self.cnxhash.get_shortid()))
        self.assertTrue(CNXHash.identifiers_equal(self.cnxhash.get_shortid(),self.cnxhash.get_shortid()))
        self.assertFalse(CNXHash.identifiers_equal(self.cnxhash,[]))
