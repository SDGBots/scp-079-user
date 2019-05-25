# SCP-079-USER - Invite and help other bots
# Copyright (C) 2019 SCP-079 <https://scp-079.org>
#
# This file is part of SCP-079-USER.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging

from pyrogram import Filters, Message

from .. import glovar
from .ids import init_group_id


# Enable logging
logger = logging.getLogger(__name__)


def is_class_c(_, message: Message) -> bool:
    # Check if the user who sent the message is Class C personnel
    try:
        uid = message.from_user.id
        gid = message.chat.id
        if init_group_id(gid):
            if uid in glovar.admin_ids.get(gid, set()) or uid in glovar.bot_ids or message.from_user.is_self:
                return True
    except Exception as e:
        logger.warning(f"Is class c error: {e}", exc_info=True)

    return False


def is_class_d(_, message: Message) -> bool:
    # Check if the user who sent the message is Class D personnel
    try:
        uid = message.from_user.id
        if uid in glovar.bad_ids["users"]:
            return True

        if message.forward_from:
            fid = message.forward_from.id
            if fid in glovar.bad_ids["users"]:
                return True

        if message.forward_from_chat:
            cid = message.forward_from_chat.id
            if cid in glovar.bad_ids["channels"]:
                return True
    except Exception as e:
        logger.warning(f"Is class d error: {e}", exc_info=True)


def is_class_e(_, message: Message) -> bool:
    # Check if the user who sent this message is Class E personnel
    try:
        gid = message.chat.id
        uid = message.from_user.id
        if uid in glovar.except_ids["users"]:
            return True

        for gid in glovar.admin_ids:
            if uid in glovar.admin_ids[gid]:
                return True

        if gid in glovar.except_ids["tmp"].get(uid, set()):
            return True

        if message.forward_from:
            fid = message.forward_from.id
            if fid in glovar.except_ids["users"]:
                return True

            for gid in glovar.admin_ids:
                if uid in glovar.admin_ids[gid]:
                    return True

            if gid in glovar.except_ids["tmp"].get(fid, set()):
                return True

        if message.forward_from_chat:
            cid = message.forward_from_chat.id
            if cid in glovar.except_ids["channels"]:
                return True
    except Exception as e:
        logger.warning(f"Is class e error: {e}", exc_info=True)

    return False


def is_declared_message(_, message: Message) -> bool:
    # Check if the message is declared by other bots
    try:
        if isinstance(message, int):
            gid = _
            mid = message
        else:
            gid = message.chat.id
            mid = message.message_id

        if mid in glovar.declared_message_ids.get(gid, set()):
            return True
    except Exception as e:
        logger.warning(f"Is declared message error: {e}", exc_info=True)

    return False


def is_exchange_channel(_, message: Message) -> bool:
    # Check if the message is sent from the exchange channel
    cid = message.chat.id
    if glovar.should_hide:
        if cid == glovar.hide_channel_id:
            return True
    elif cid == glovar.exchange_channel_id:
        return True

    return False


def is_hide_channel(_, message: Message) -> bool:
    # Check if the message is sent from the hide channel
    cid = message.chat.id
    if cid == glovar.hide_channel_id:
        return True

    return False


def is_new_group(_, message: Message) -> bool:
    # Check if the bot joined a new group
    try:
        new_users = message.new_chat_members
        for user in new_users:
            if user.is_self:
                return True
    except Exception as e:
        logger.warning(f"Is new group error: {e}", exc_info=True)

    return False


def is_test_group(_, message: Message) -> bool:
    # Check if the message is sent from the test group
    try:
        cid = message.chat.id
        if cid == glovar.test_group_id:
            return True
    except Exception as e:
        logger.warning(f"Is test group error: {e}", exc_info=True)

    return False


class_c = Filters.create(
    name="Class C",
    func=is_class_c
)

class_d = Filters.create(
    name="Class D",
    func=is_class_d
)

class_e = Filters.create(
    name="Class E",
    func=is_class_e
)

declared_message = Filters.create(
    name="Declared message",
    func=is_declared_message
)

exchange_channel = Filters.create(
    name="Exchange Channel",
    func=is_exchange_channel
)

hide_channel = Filters.create(
    name="Hide Channel",
    func=is_hide_channel
)

new_group = Filters.create(
    name="New Group",
    func=is_new_group
)

test_group = Filters.create(
    name="Test Group",
    func=is_test_group
)