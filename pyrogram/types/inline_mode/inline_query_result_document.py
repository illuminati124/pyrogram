#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union, List

import pyrogram
from pyrogram import raw, types, utils
from .inline_query_result import InlineQueryResult


class InlineQueryResultDocument(InlineQueryResult):
    """Link to a file.
    
    Parameters:
        doc_url (``str``):
            A valid URL for the audio file.
            
        title (``str``):
            Title for the result.
            
        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.
            
        desc (``str``, *optional*):
            Description.
        
        thumb_url (``str``, *optional*):
            URL of the thumbnail for the result.
        caption (``str``, *optional*):
            Caption of the audio to be sent, 0-1024 characters.
            
        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.
            
        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.
            
        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.
            
        input_message_content (:obj:`~pyrogram.types.InputMessageContent`, *optional*):
            Content of the message to be sent instead of the audio.
    """

    def __init__(
        self,
        doc_url: str,
        title: str,
        id: str = None,
        desc: str = "",
        caption: str = "",
        parse_mode: Union[str, None] = object,
        thumb_url: str = None,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.doc_url = doc_url
        self.title = title
        self.desc = desc
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.thumb_url = thumb_url

    async def write(self, client: "pyrogram.Client"):
        docs = raw.types.InputWebDocument(
            url=self.doc_url,
            size=0,
            mime_type=self.mime_type,
            attributes=[]
        )

        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.desc,
            thumb=raw.types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            ) if self.thumb_url else None,
            content=docs,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities
                )
            )
        )
