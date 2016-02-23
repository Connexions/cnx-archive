# -*- coding: utf-8 -*-
# ###
# Copyright (c) 2016, Rice University
# This software is subject to the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
# ###
"""\
Logic used to acquire data from the archive database.

"""
import os

from cnxarchive.database import db_connect
from cnxarchive.utils import (
    join_ident_hash,
    split_ident_hash,
    IdentHashMissingVersion,
    )

from cnxarchive.scripts.export_epub.exceptions import *


here = os.path.abspath(os.path.dirname(__file__))
SQL_DIR = os.path.join(here, 'sql')


def _get_sql(filename):
    """Returns the contents of the sql file from the given ``filename``."""
    with open(os.path.join(SQL_DIR, filename), 'r') as f:
        return f.read()


def verify_id_n_version(id, version):
    """Given an ``id`` and ``version``, verify the identified content exists.

    """
    stmt = _get_sql('verify-id-and-version.sql')
    args = dict(id=id, version=version)

    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            cursor.execute(stmt, args)
            try:
                valid = cursor.fetchone()[0]
            except TypeError:
                raise NotFound(join_ident_hash(id, version))
    return True


def get_id_n_version(ident_hash):
    """From the given ``ident_hash`` return the id and version."""
    try:
        id, version = split_ident_hash(ident_hash)
    except IdentHashMissingVersion:
        # XXX Don't import from views... And don't use httpexceptions
        from pyramid.httpexceptions import HTTPNotFound
        from cnxarchive.views import get_latest_version
        try:
            version = get_latest_version(ident_hash)
        except HTTPNotFound:
            raise NotFound(ident_hash)
        id, version = split_ident_hash(join_ident_hash(ident_hash, version))
    else:
        verify_id_n_version(id, version)

    return id, version


__all__ = (
    'get_id_n_version',
    )
