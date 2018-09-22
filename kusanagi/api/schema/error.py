"""
Python 3 SDK for the KUSANAGI(tm) Framework (http://kusanagi.io)

Copyright (c) 2016-2018 KUSANAGI S.L. All rights reserved.

Distributed under the MIT license.

For the full copyright and license information, please view the LICENSE
file that was distributed with this source code.

"""
from ...errors import KusanagiError

__license__ = "MIT"
__copyright__ = "Copyright (c) 2016-2018 KUSANAGI S.L. (http://kusanagi.io)"


class ServiceSchemaError(KusanagiError):
    """Base error class for Service schemas."""
