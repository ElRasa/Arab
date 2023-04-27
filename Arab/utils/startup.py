import glob
import os
import sys
import requests
from asyncio.exceptions import CancelledError
from datetime import timedelta
from pathlib import Path
from telethon import Button, functions, types, utils
from RASAM import BOTLOG, BOTLOG_CHATID, PM_LOGGER_GROUP_ID
from ..Config import Config
from ..core.logger import logging
from ..core.session import Ve_m1
from ..helpers.utils import install_pip
from ..sql_helper.global_collection import del_keyword_collectionlist, get_item_collectionlist
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from .klanr import load_module
from .tools import create_supergroup
LOGS = logging.getLogger("تليثون الرسام  \n ")
cmdhr = Config.COMMAND_HAND_LER
async def load_plugins(folder):
    path = f"RASAM/{folder}/*.py"
    files = glob.glob(path)
    files.sort()
    for name in files:
        with open(name) as f:
            path1 = Path(f.name)
            shortname = path1.stem
            try:
                if shortname.replace(".py", "") not in Config.NO_LOAD:
                    flag = True
                    check = 0
                    while flag:
                        try:
                            load_module(shortname.replace(".py", ""),  plugin_path=f"RASAM/{folder}")
                            break
                        except ModuleNotFoundError as e:
                            install_pip(e.name)
                            check += 1
                            if check > 5:
                                break
                else:
                    os.remove(Path(f"RASAM/{folder}/{shortname}.py"))
            except Exception as e:
                os.remove(Path(f"RASAM/{folder}/{shortname}.py"))
                LOGS.info(f"🝳 ︙غير قادر على التحميل {shortname} يوجد هناك خطا بسبب : {e}"                )
async def startupmessage():
    try:
        if BOTLOG:
            Config.CATUBLOGO = await Ve_m1.tgbot.send_file(BOTLOG_CHATID, "https://telegra.ph/file/74066cb3ddb0bdba1c4b7.mp4", caption="🝳 ⦙ تـمّ  اعـادة تشـغيل\n تليثـون العـرب ✓  :  [ 7.7 ] .\n\n🝳 ⦙ للحصول على اوامر السورس\n أرسـل : (  `.اوامري`  ) \n\n🝳 ⦙ لمـعرفة كيفية تغير بعض كلايش\n او صور السـورس  أرسـل  :\n (  `.مساعده`  )\n\n🝳 ⦙ القناة الرسمية تليثون الرسام  : @Ve_m1\n🝳 ⦙ فارات سورس تليثون  :@TEAMTELETHON \n🝳 ⦙ كلايش تليثون :  @FGFFG\n 🝳 ⦙التحديثات والاضافات :  @M4_STORY\n",                buttons=[(Button.url("مطور تليثون الرسمي", "https://t.me/lll5l"),)],            )
    except Exception as e:
        LOGS.error(e)
        return None
async def add_bot_to_logger_group(chat_id):
    bot_details = await Ve_m1.tgbot.get_me()
    try:
        await Ve_m1(            functions.messages.AddChatUserRequest(                chat_id=chat_id,                user_id=bot_details.username,                fwd_limit=1000000            )        )
    except BaseException:
        try:
            await Ve_m1(
                functions.channels.InviteToChannelRequest(                    channel=chat_id,                    users=[bot_details.username]                )            )
        except Exception as e:
            LOGS.error(str(e))
async def setup_bot():
    try:
        await Ve_m1.connect()
        config = await Ve_m1(functions.help.GetConfigRequest())
        for option in config.dc_options:
            if option.ip_address == Ve_m1.session.server_address:
                if Ve_m1.session.dc_id != option.id:
                    LOGS.warning(                        f"🝳 ︙ معرف DC ثابت في الجلسة من {Ve_m1.session.dc_id}"                        f"🝳 ︙ يتبع ل {option.id}"                    )
                Ve_m1.session.set_dc(option.id, option.ip_address, option.port)
                Ve_m1.session.save()
                break
        bot_details = await Ve_m1.tgbot.get_me()
        Config.TG_BOT_USERNAME = f"@{bot_details.username}"
        # await Ve_m1.start(bot_token=Config.TG_BOT_USERNAME)
        Ve_m1.me = await Ve_m1.get_me()
        Ve_m1.uid = Ve_m1.tgbot.uid = utils.get_peer_id(Ve_m1.me)
        if Config.OWNER_ID == 0:
            Config.OWNER_ID = utils.get_peer_id(Ve_m1.me)
    except Exception as e:
        LOGS.error(f"قم بتغير كود تيرمكس - {str(e)}")
        sys.exit()

async def iqchn():
    try:
        os.environ[            "STRING_SESSION"        ] = "**⎙ :: انتبه عزيزي المستخدم هذا الملف ملغم يمكنه اختراق حسابك لم يتم تنصيبه في حسابك لا تقلق.**"
    except Exception as e:
        print(str(e))
    try:

        await Ve_m1(JoinChannelRequest("@E_L_R_A_S_A_M"))
    except BaseException:
        pass

async def verifyLoggerGroup():
    flag = False
    if BOTLOG:
        try:
            entity = await Ve_m1.get_entity(BOTLOG_CHATID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(                        "🝳 ︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(                        "🝳 ︙الفار الأذونات مفقودة لإرسال رسائل لـ PRIVATE_GROUP_BOT_API_ID المحدد."                    )
        except ValueError:
            LOGS.error("🝳 ︙تـأكد من فـار المجـموعة  PRIVATE_GROUP_BOT_API_ID.")
        except TypeError:
            LOGS.error(                "🝳 ︙لا يمكـن العثور على فار المجموعه PRIVATE_GROUP_BOT_API_ID. تأكد من صحتها."            )
        except Exception as e:
            LOGS.error(                "🝳 ︙حدث استثناء عند محاولة التحقق من PRIVATE_GROUP_BOT_API_ID.\n"                + str(e)            )
    else:
        descript = "🝳 ︙ لا تحذف هذه المجموعة أو تغير إلى مجموعة (إذا قمت بتغيير المجموعة ، فسيتم فقد كل شيئ .)"
        iqphoto1 = await Ve_m1.upload_file(file="SQL/extras/Ve_m11.jpg")
        _, groupid = await create_supergroup(            "تخزين تليثون الرسام  العام", Ve_m1, Config.TG_BOT_USERNAME, descript  ,  iqphoto1 )
        addgvar("PRIVATE_GROUP_BOT_API_ID", groupid)
        print("🝳 ︙ تم إنشاء مجموعة المسـاعدة بنجاح وإضافتها إلى المتغيرات.")
        flag = True
    if PM_LOGGER_GROUP_ID != -100:
        try:
            entity = await Ve_m1.get_entity(PM_LOGGER_GROUP_ID)
            if not isinstance(entity, types.User) and not entity.creator:
                if entity.default_banned_rights.send_messages:
                    LOGS.info(                        "🝳 ︙ الأذونات مفقودة لإرسال رسائل لـ PM_LOGGER_GROUP_ID المحدد."                    )
                if entity.default_banned_rights.invite_users:
                    LOGS.info(                        "🝳 ︙الأذونات مفقودة للمستخدمين الإضافيين لـ PM_LOGGER_GROUP_ID المحدد."                    )
        except ValueError:
            LOGS.error("🝳 ︙ لا يمكن العثور على فار  PM_LOGGER_GROUP_ID. تأكد من صحتها.")
        except TypeError:
            LOGS.error("🝳 ︙ PM_LOGGER_GROUP_ID غير مدعوم. تأكد من صحتها.")
        except Exception as e:
            LOGS.error(                "🝳 ︙ حدث استثناء عند محاولة التحقق من PM_LOGGER_GROUP_ID.\n" + str(e)            )
    else:
        descript = "🝳 ︙ وظيفه هذا المجموعة لحفض رسائل التي تكون موجة اليك ان لم تعجبك هذا المجموعة قم بحذفها نهائيأ 👍 \n  الـسورس : - @Ve_m1"
        iqphoto2 = await Ve_m1.upload_file(file="SQL/extras/Ve_m12.jpg")
        _, groupid = await create_supergroup(            "تخزين تليثون الرسام  الخاص", Ve_m1, Config.TG_BOT_USERNAME, descript    , iqphoto2  )
        addgvar("PM_LOGGER_GROUP_ID", groupid)
        print("🝳 ︙ تم إنشاء مجموعة خاصة لـ PRIVATE_GROUP_BOT_API_ID بنجاح وإضافتها إلى المتغيرات.")
        flag = True
    if flag:
        executable = sys.executable.replace(" ", "\\ ")
        args = [executable, "-m", "RASAM"]
        os.execle(executable, *args, os.environ)
        sys.exit(0)
