# -*- coding: utf-8 -*-

# This file is part of Androguard.
#
# Copyright (C) 2012, Anthony Desnos <desnos at t0t0.fr>
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from struct import unpack

try:
    from .constants import UTF8_FLAG
except (ValueError, ImportError):
    from constants import UTF8_FLAG


class StringBlock(object):
    """
    StringBlock is a CHUNK inside an AXML File
    It contains all strings, which are used by referecing to ID's

    See http://androidxref.com/9.0.0_r3/xref/frameworks/base/libs/androidfw/include/androidfw/ResourceTypes.h#436
    """

    def __init__(self, buff, header, debug=False):
        """
        :param buff: buffer which holds the string block
        :param header: a instance of :class:`~ARSCHeader`
        """
        self.log = logging.getLogger("pyaxmlparser.stringblock")
        self.log.setLevel(logging.DEBUG if debug else logging.CRITICAL)
        self._cache = {}
        self.header = header
        # We already read the header (which was chunk_type and chunk_size
        # Now, we read the string_count:
        self.string_count = unpack("<i", buff.read(4))[0]
        # style_count
        self.style_offset_count = unpack("<i", buff.read(4))[0]

        # flags
        self.flags = unpack("<i", buff.read(4))[0]
        self.is_utf8 = (self.flags & UTF8_FLAG) != 0

        # string_pool_offset
        # The string offset is counted from the beginning of the string section
        self.stringsOffset = unpack("<i", buff.read(4))[0]
        # style_pool_offset
        # The styles offset is counted as well from the beginning of the string section
        self.stylesOffset = unpack("<i", buff.read(4))[0]

        # Check if they supplied a stylesOffset even if the count is 0:
        if self.style_offset_count == 0 and self.stylesOffset > 0:
            self.log.info(
                "Styles Offset given, but styleCount is zero. "
                "This is not a problem but could indicate packers."
            )

        self.string_offsets = []
        self.style_offsets = []
        self.char_buffer = b""
        self.styles = []

        # Next, there is a list of string following.
        # This is only a list of offsets (4 byte each)
        for i in range(self.string_count):
            self.string_offsets.append(unpack("<i", buff.read(4))[0])

        # And a list of styles
        # again, a list of offsets
        for i in range(self.style_offset_count):
            self.style_offsets.append(unpack("<i", buff.read(4))[0])

        # FIXME it is probably better to parse n strings and not calculate the size
        size = self.header.size - self.stringsOffset

        # if there are styles as well, we do not want to read them too.
        # Only read them, if no
        if self.stylesOffset != 0 and self.style_offset_count != 0:
            size = self.stylesOffset - self.stringsOffset

        if (size % 4) != 0:
            self.log.warning("Size of strings is not aligned by four bytes.")

        self.char_buffer = buff.read(size)

        if self.stylesOffset != 0 and self.style_offset_count != 0:
            size = self.header.size - self.stylesOffset

            if (size % 4) != 0:
                self.log.warning("Size of styles is not aligned by four bytes.")

            for i in range(0, size // 4):
                self.styles.append(unpack("<i", buff.read(4))[0])

    def __getitem__(self, idx):
        """
        Returns the string at the index in the string table
        """
        return self.get_string(idx)

    def __len__(self):
        """
        Get the number of strings stored in this table
        """
        return self.string_count

    def __iter__(self):
        """
        Iterable over all strings
        """
        for i in range(self.string_count):
            yield self.get_string(i)

    def get_string(self, idx):
        """
        Return the string at the index in the string table

        :param idx: index in the string table
        :return: str
        """
        if idx in self._cache:
            return self._cache[idx]

        if idx < 0 or not self.string_offsets or idx > self.string_count:
            return ""

        offset = self.string_offsets[idx]

        if self.is_utf8:
            self._cache[idx] = self.decode_utf8(offset)
        else:
            self._cache[idx] = self.decode_utf16(offset)

        return self._cache[idx]

    def get_style(self, idx):
        """
        Return the style associated with the index

        :param idx: index of the style
        :return:
        """
        return self.styles[idx]

    def decode_utf8(self, offset):
        """
        Decode an UTF-8 String at the given offset

        :param offset: offset of the string inside the data
        :return: str
        """
        # UTF-8 Strings contain two lengths, as they might differ:
        # 1) the UTF-16 length
        str_len, skip = self.decode_length(offset, 1)
        offset += skip

        # 2) the utf-8 string length
        encoded_bytes, skip = self.decode_length(offset, 1)
        offset += skip

        data = self.char_buffer[offset : offset + encoded_bytes]

        assert (
            self.char_buffer[offset + encoded_bytes] == 0
        ), "UTF-8 String is not null terminated! At offset={}".format(offset)

        return self.decode_bytes(data, "utf-8", str_len)

    def decode_utf16(self, offset):
        """
        Decode an UTF-16 String at the given offset

        :param offset: offset of the string inside the data
        :return: str
        """
        str_len, skip = self.decode_length(offset, 2)
        offset += skip

        # The len is the string len in utf-16 units
        encoded_bytes = str_len * 2

        data = self.char_buffer[offset : offset + encoded_bytes]

        assert (
            self.char_buffer[offset + encoded_bytes : offset + encoded_bytes + 2]
            == b"\x00\x00"
        ), "UTF-16 String is not null terminated! At offset={}".format(offset)

        return self.decode_bytes(data, "utf-16", str_len)

    def decode_bytes(self, data, encoding, str_len):
        """
        Generic decoding with length check.
        The string is decoded from bytes with the given encoding, then the length
        of the string is checked.
        The string is decoded using the "replace" method.

        :param data: bytes
        :param encoding: encoding name ("utf-8" or "utf-16")
        :param str_len: length of the decoded string
        :return: str
        """
        string = data.decode(encoding, "replace")
        if len(string) != str_len:
            self.log.warning("invalid decoded string length")
        return string

    def decode_length(self, offset, sizeof_char):
        """
        Generic Length Decoding at offset of string

        The method works for both 8 and 16 bit Strings.
        Length checks are enforced:
        * 8 bit strings: maximum of 0x7FFF bytes (See
        http://androidxref.com/9.0.0_r3/xref/frameworks/base/libs/androidfw/ResourceTypes.cpp#692)
        * 16 bit strings: maximum of 0x7FFFFFF bytes (See
        http://androidxref.com/9.0.0_r3/xref/frameworks/base/libs/androidfw/ResourceTypes.cpp#670)

        :param offset: offset into the string data section of the beginning of
        the string
        :param sizeof_char: number of bytes per char (1 = 8bit, 2 = 16bit)
        :returns: tuple of (length, read bytes)
        """
        sizeof_2chars = sizeof_char << 1
        fmt = "<2B" if sizeof_char == 1 else "<2H"
        high_bit = 0x80 << (8 * (sizeof_char - 1))

        length1, length2 = unpack(
            fmt, self.char_buffer[offset : (offset + sizeof_2chars)]
        )

        if (length1 & high_bit) != 0:
            length = ((length1 & ~high_bit) << (8 * sizeof_char)) | length2
            size = sizeof_2chars
        else:
            length = length1
            size = sizeof_char

        if sizeof_char == 1:
            assert (
                length <= 0x7FFF
            ), "length of UTF-8 string is too large! At offset={}".format(offset)
        else:
            assert (
                length <= 0x7FFFFFFF
            ), "length of UTF-16 string is too large!  At offset={}".format(offset)

        return length, size

    def show(self):
        """
        Print some information on stdout about the string table
        """
        print(
            "StringBlock(stringsCount=0x%x, "
            "stringsOffset=0x%x, "
            "stylesCount=0x%x, "
            "stylesOffset=0x%x, "
            "flags=0x%x"
            ")"
            % (
                self.string_count,
                self.stringsOffset,
                self.style_offset_count,
                self.stylesOffset,
                self.flags,
            )
        )

        if self.string_count > 0:
            print()
            print("String Table: ")
            for i, s in enumerate(self):
                print("{:08d} {}".format(i, repr(s)))

        if self.style_offset_count > 0:
            print()
            print("Styles Table: ")
            for i in range(self.style_offset_count):
                print("{:08d} {}".format(i, repr(self.get_style(i))))
