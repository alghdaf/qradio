#!/usr/bin/env python3
# Copyright (C) @subinps
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from utils import LOGGER
from contextlib import suppress
from config import Config
import calendar
import pytz
from datetime import datetime
import asyncio
import os
from pyrogram.errors.exceptions.bad_request_400 import (
    MessageIdInvalid, 
    MessageNotModified
)
from pyrogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton
)
from utils import (
    cancel_all_schedules,
    edit_config, 
    is_admin, 
    leave_call, 
    restart,
    restart_playout,
    stop_recording, 
    sync_to_db,
    update, 
    is_admin, 
    chat_filter,
    sudo_filter,
    delete_messages,
    seek_file
)
from pyrogram import (
    Client, 
    filters
)

IST = pytz.timezone(Config.TIME_ZONE)
if Config.DATABASE_URI:
    from utils import db

HOME_TEXT = "<b>مرحبًا  [{}](tg://user?id={}) \n\n أنا بوت تيليجرام للبث أخص أحدهم فما شأنك هنا؟ إذا احتجت شيئًا تواصل مع @OURPYBOT </b>"
admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(['start', f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    if len(message.command) > 1:
        if message.command[1] == 'help':
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"التشغيل", callback_data='help_play'),
                        InlineKeyboardButton(f"الإعدادات", callback_data=f"help_settings"),
                        InlineKeyboardButton(f"التسجيل", callback_data='help_record'),
                    ],
                    [
                        InlineKeyboardButton("الجدولة", callback_data="help_schedule"),
                        InlineKeyboardButton("التحكم", callback_data='help_control'),
                        InlineKeyboardButton("Admins", callback_data="help_admin"),
                    ],
                    [
                        InlineKeyboardButton(f"Misc", callback_data='help_misc'),
                        InlineKeyboardButton("إغلاق", callback_data="close"),
                    ],
                ]
                )
            await message.reply("تعلم كيفية استخدام qradio ،دليل المساعدة ، اختر من الخيارات أدناه.",
                reply_markup=reply_markup,
                disable_web_page_preview=True
                )
        elif 'sch' in message.command[1]:
            msg=await message.reply("التحقق من الجداول ..")
            you, me = message.command[1].split("_", 1)
            who=Config.SCHEDULED_STREAM.get(me)
            if not who:
                return await msg.edit("ضاع شيء في مكان ما.")
            del Config.SCHEDULED_STREAM[me]
            whom=f"{message.chat.id}_{msg.message_id}"
            Config.SCHEDULED_STREAM[whom] = who
            await sync_to_db()
            if message.from_user.id not in Config.ADMINS:
                return await msg.edit("طيب da")
            today = datetime.now(IST)
            smonth=today.strftime("%B")
            obj = calendar.Calendar()
            thisday = today.day
            year = today.year
            month = today.month
            m=obj.monthdayscalendar(year, month)
            button=[]
            button.append([InlineKeyboardButton(text=f"{str(smonth)}  {str(year)}",callback_data=f"sch_month_choose_none_none")])
            days=["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
            f=[]
            for day in days:
                f.append(InlineKeyboardButton(text=f"{day}",callback_data=f"day_info_none"))
            button.append(f)
            for one in m:
                f=[]
                for d in one:
                    year_=year
                    if d < int(today.day):
                        year_ += 1
                    if d == 0:
                        k="\u2063"   
                        d="none"   
                    else:
                        k=d    
                    f.append(InlineKeyboardButton(text=f"{k}",callback_data=f"sch_month_{year_}_{month}_{d}"))
                button.append(f)
            button.append([InlineKeyboardButton("إغلاق", callback_data="schclose")])
            await msg.edit(f"اختر اليوم من الشهر الذي تريد جدولة الدردشة الصوتية فيه. \n التاريخ هو {thisday} {smonth} {year}. اختيار التاريخ الذي يسبق اليوم سيعتبر العام المقبل {year+1}", reply_markup=InlineKeyboardMarkup(button))



        return
    buttons = [
        [
            InlineKeyboardButton('أعمل هنا', url='https://t.me/flrbi'),
            InlineKeyboardButton('🧩 المطور', url='https://instagram.com/alghdaf')
        ],
        [
            InlineKeyboardButton('👨🏼‍🦯 الدليل', callback_data='help_main'),
            InlineKeyboardButton('🗑 إغلاق', callback_data='close'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    k = await message.reply(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    await delete_messages([message, k])



@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("التشغيل", callback_data='help_play'),
                InlineKeyboardButton("الإعدادات", callback_data=f"help_settings"),
                InlineKeyboardButton("التسجيل", callback_data='help_record'),
            ],
            [
                InlineKeyboardButton("الجدولة", callback_data="help_schedule"),
                InlineKeyboardButton("التحكم", callback_data='help_control'),
                InlineKeyboardButton("Admins", callback_data="help_admin"),
            ],
            [
                InlineKeyboardButton("Misc", callback_data='help_misc'),
                InlineKeyboardButton("Config Vars", callback_data='help_env'),
                InlineKeyboardButton("إغلاق", callback_data="close"),
            ],
        ]
        )
    if message.chat.type != "private" and message.from_user is None:
        k=await message.reply(
            text="لا يمكنني مساعدتك هنا ، لأنك مشرف مجهول. ارجع الخاص",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(f"Help", url=f"https://telegram.dog/{Config.BOT_USERNAME}?start=help"),
                    ]
                ]
            ),)
        await delete_messages([message, k])
        return
    if Config.msg.get('help') is not None:
        await Config.msg['help'].delete()
    Config.msg['help'] = await message.reply_text(
        "تعلم كيفية استخدام Qradio ، قائمة التعليمات ، اختر من بين الخيارات أدناه.",
        reply_markup=reply_markup,
        disable_web_page_preview=True
        )
    #await delete_messages([message])
@Client.on_message(filters.command(['repo', f"repo@{Config.BOT_USERNAME}"]))
async def repo_(client, message):
    buttons = [
        [
            InlineKeyboardButton('🧩 المطور ', url='https://instagram.com/alghdaf'),
            InlineKeyboardButton('هنا حيث أعمل', url='https://t.me/flrbi'),     
        ],
        [
            InlineKeyboardButton("🎞 همم ", url='https://t.me/alghdaf'),
            InlineKeyboardButton('🗑 إغلاق', callback_data='close'),
        ]
    ]
    await message.reply("<b>By <a href=https://t.me/alghdaf>alghdaf.</a></b>", reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
    await delete_messages([message])

@Client.on_message(filters.command(['restart', 'update', f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def update_handler(client, message):
    if Config.HEROKU_APP:
        k = await message.reply("وجد مصدر التطبيق، يتم إعادة التشغيل للتحديث.")
        if Config.DATABASE_URI:
            msg = {"msg_id":k.message_id, "chat_id":k.chat.id}
            if not await db.is_saved("RESTART"):
                db.add_config("RESTART", msg)
            else:
                await db.edit_config("RESTART", msg)
            await sync_to_db()
    else:
        k = await message.reply("لم يتم العثور على تطبيق هيروكو، نحاول اعادة التشغيل.")
        if Config.DATABASE_URI:
            msg = {"msg_id":k.message_id, "chat_id":k.chat.id}
            if not await db.is_saved("RESTART"):
                db.add_config("RESTART", msg)
            else:
                await db.edit_config("RESTART", msg)
    try:
        await message.delete()
    except:
        pass
    await update()

@Client.on_message(filters.command(['logs', f"logs@{Config.BOT_USERNAME}"]) & admin_filter & chat_filter)
async def get_logs(client, message):
    m=await message.reply("Checking logs..")
    if os.path.exists("botlog.txt"):
        await message.reply_document('botlog.txt', caption="Bot Logs")
        await m.delete()
        await delete_messages([message])
    else:
        k = await m.edit("No log files found.")
        await delete_messages([message, k])

@Client.on_message(filters.command(['env', f"env@{Config.BOT_USERNAME}", "config", f"config@{Config.BOT_USERNAME}"]) & sudo_filter & chat_filter)
async def set_heroku_var(client, message):
    with suppress(MessageIdInvalid, MessageNotModified):
        m = await message.reply(".أتحقق من متغيرات الاتصال.")
        if " " in message.text:
            cmd, env = message.text.split(" ", 1)
            if "=" in env:
                var, value = env.split("=", 1)
            else:
                if env == "STARTUP_STREAM":
                    env_ = "STREAM_URL"
                elif env == "QUALITY":
                    env_ = "CUSTOM_QUALITY" 
                else:
                    env_ = env
                ENV_VARS = ["ADMINS", "SUDO", "CHAT", "LOG_GROUP", "STREAM_URL", "SHUFFLE", "ADMIN_ONLY", "REPLY_MESSAGE", 
                        "EDIT_TITLE", "RECORDING_DUMP", "RECORDING_TITLE", "IS_VIDEO", "IS_LOOP", "DELAY", "PORTRAIT", 
                        "IS_VIDEO_RECORD", "PTN", "CUSTOM_QUALITY"]
                if env_ in ENV_VARS:
                    await m.edit(f"القيمة الحالية للمتغير `{env}` هي `{getattr(Config, env_)}`")
                    await delete_messages([message])
                    return
                else:
                    await m.edit("هذه قيمة غير صالحة، عذرًا.")
                    await delete_messages([message, m])
                    return     
            
        else:
            await m.edit("لم تقدم أي قيمة لـ env ، يجب عليك اتباع التنسيق الصحيح.")
            await delete_messages([message, m])
            return

        if Config.DATABASE_URI and var in ["STARTUP_STREAM", "CHAT", "LOG_GROUP", "REPLY_MESSAGE", "DELAY", "RECORDING_DUMP", "QUALITY"]:      
            await m.edit("تم العثور على Mongodb ، إعداد متغيرات التكوين ...")
            await asyncio.sleep(2)  
            if not value:
                await m.edit(f"لم يتم تحديد قيمة لـ env. في محاولة لحذف القيمة الحالية {var}.")
                await asyncio.sleep(2)
                if var in ["STARTUP_STREAM", "CHAT", "DELAY"]:
                    await m.edit("هذا متغير إلزامي ولا يمكن حذفه.")
                    await delete_messages([message, m]) 
                    return
                await edit_config(var, False)
                await m.edit(f"حُذف بنجاح {var}")
                await delete_messages([message, m])           
                return
            else:
                if var in ["CHAT", "LOG_GROUP", "RECORDING_DUMP", "QUALITY"]:
                    try:
                        value=int(value)
                    except:
                        if var == "QUALITY":
                            if not value.lower() in ["low", "medium", "high"]:
                                await m.edit("يجب تحديد قيمة بين 10-100.")
                                await delete_messages([message, m])
                                return
                            else:
                                value = value.lower()
                                if value == "high":
                                    value = 100
                                elif value == "medium":
                                    value = 66.9
                                elif value == "low":
                                    value = 50
                        else:
                            await m.edit("يجب أن تعطيني ID إذا. يجب أن يكون عددًا صحيحًا.")
                            await delete_messages([message, m])
                            return
                    if var == "CHAT":
                        await leave_call()
                        Config.ADMIN_CACHE=False
                        if Config.IS_RECORDING:
                            await stop_recording()
                        await cancel_all_schedules()
                        Config.CHAT=int(value)
                        await restart()
                    await edit_config(var, int(value))
                    if var == "QUALITY":
                        if Config.CALL_STATUS:
                            data=Config.DATA.get('FILE_DATA')
                            if not data \
                                or data.get('dur', 0) == 0:
                                await restart_playout()
                                return
                            k, reply = await seek_file(0)
                            if k == False:
                                await restart_playout()
                    await m.edit(f"غُير بنجاح {var} إلى {value}")
                    await delete_messages([message, m])
                    return
                else:
                    if var == "STARTUP_STREAM":
                        Config.STREAM_SETUP=False
                    await edit_config(var, value)
                    await m.edit(f"غُير بنجاح {var} إلى {value}")
                    await delete_messages([message, m])
                    await restart_playout()
                    return
        else:
            if not Config.HEROKU_APP:
                buttons = [[InlineKeyboardButton('Heroku API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new'), InlineKeyboardButton('🗑 Close', callback_data='close'),]]
                await m.edit(
                    text="No heroku app found, this command needs the following heroku vars to be set.\n\n1. <code>HEROKU_API_KEY</code>: Your heroku account api key.\n2. <code>HEROKU_APP_NAME</code>: Your heroku app name.", 
                    reply_markup=InlineKeyboardMarkup(buttons)) 
                await delete_messages([message])
                return     
            config = Config.HEROKU_APP.config()
            if not value:
                await m.edit(f"بما أنه لم تُعطى لي قيمة، في محاولة لحذف القيمة الحالية للمتغير {var}.")
                await asyncio.sleep(2)
                if var in ["STARTUP_STREAM", "CHAT", "DELAY", "API_ID", "API_HASH", "BOT_TOKEN", "SESSION_STRING", "ADMINS"]:
                    await m.edit("هذه متغيرات إلزامية ولا يمكن حذفها.")
                    await delete_messages([message, m])
                    return
                if var in config:
                    await m.edit(f"حُذف بنجاح {var}")
                    await asyncio.sleep(2)
                    await m.edit("يتم الآن إعادة تشغيل التطبيق لإجراء تغييرات.")
                    if Config.DATABASE_URI:
                        msg = {"msg_id":m.message_id, "chat_id":m.chat.id}
                        if not await db.is_saved("RESTART"):
                            db.add_config("RESTART", msg)
                        else:
                            await db.edit_config("RESTART", msg)
                    del config[var]                
                    config[var] = None               
                else:
                    k = await m.edit(f"لم يتم العثةر على متغير بإسم {var}. لا شيء للتغيير...")
                    await delete_messages([message, k])
                return
            if var in config:
                await m.edit(f"متغير موجود بالفعل. تم تحريره الآن إلى {value}")
            else:
                await m.edit(f"لم يتم العثور على المتغير ، يتم الآن تعيين متغير جديد.")
            await asyncio.sleep(2)
            await m.edit(f" تم بنجاح تعيين {var} بالقيمة {value}, تتم الآن إعادة التشغيل لترى تأثيرات التغيير...")
            if Config.DATABASE_URI:
                msg = {"msg_id":m.message_id, "chat_id":m.chat.id}
                if not await db.is_saved("RESTART"):
                    db.add_config("RESTART", msg)
                else:
                    await db.edit_config("RESTART", msg)
            config[var] = str(value)




