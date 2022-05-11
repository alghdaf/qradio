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
try:
   import os
   import heroku3
   from dotenv import load_dotenv
   from ast import literal_eval as is_enabled

except ModuleNotFoundError:
    import os
    import sys
    import subprocess
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)


class Config:
    #Telegram API Stuffs
    load_dotenv()  # load enviroment variables from .env file
    ADMIN = os.environ.get("ADMINS", '')
    SUDO = [int(admin) for admin in (ADMIN).split()] # Exclusive for heroku vars configuration.
    ADMINS = [int(admin) for admin in (ADMIN).split()] #group admins will be appended to this list.
    API_ID = int(os.environ.get("API_ID", ''))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")     
    SESSION = os.environ.get("SESSION_STRING", "")

    #Stream Chat and Log Group
    CHAT = int(os.environ.get("CHAT", ""))
    LOG_GROUP=os.environ.get("LOG_GROUP", "")

    #Stream 
    STREAM_URL=os.environ.get("STARTUP_STREAM", "https://www.youtube.com/watch?v=zcrUCvBD16k")
   
    #Database
    DATABASE_URI=os.environ.get("DATABASE_URI", None)
    DATABASE_NAME=os.environ.get("DATABASE_NAME", "qradio")


    #heroku
    API_KEY=os.environ.get("HEROKU_API_KEY", None)
    APP_NAME=os.environ.get("HEROKU_APP_NAME", None)


    #Optional Configuration
    SHUFFLE=is_enabled(os.environ.get("SHUFFLE", 'True'))
    ADMIN_ONLY=is_enabled(os.environ.get("ADMIN_ONLY", "True"))
    REPLY_MESSAGE=os.environ.get("REPLY_MESSAGE", False)
    EDIT_TITLE = os.environ.get("EDIT_TITLE", False)
    #others
    
    RECORDING_DUMP=os.environ.get("RECORDING_DUMP", False)
    RECORDING_TITLE=os.environ.get("RECORDING_TITLE", False)
    TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")    
    IS_VIDEO=is_enabled(os.environ.get("IS_VIDEO", 'False'))
    IS_LOOP=is_enabled(os.environ.get("IS_LOOP", 'True'))
    DELAY=int(os.environ.get("DELAY", '10'))
    PORTRAIT=is_enabled(os.environ.get("PORTRAIT", 'False'))
    IS_VIDEO_RECORD=is_enabled(os.environ.get("IS_VIDEO_RECORD", 'False'))
    DEBUG=is_enabled(os.environ.get("DEBUG", 'False'))
    PTN=is_enabled(os.environ.get("PTN", "False"))

    #Quality vars
    E_BITRATE=os.environ.get("BITRATE", False)
    E_FPS=os.environ.get("FPS", False)
    CUSTOM_QUALITY=os.environ.get("QUALITY", "100")

    #Search filters for cplay
    FILTERS =  [filter.lower() for filter in (os.environ.get("FILTERS", "video document")).split(" ")]


    #Dont touch these, these are not for configuring player
    GET_FILE={}
    DATA={}
    STREAM_END={}
    SCHEDULED_STREAM={}
    DUR={}
    msg = {}

    SCHEDULE_LIST=[]
    playlist=[]
    CONFIG_LIST = ["ADMINS", "IS_VIDEO", "IS_LOOP", "REPLY_PM", "ADMIN_ONLY", "SHUFFLE", "EDIT_TITLE", "CHAT", 
    "SUDO", "REPLY_MESSAGE", "STREAM_URL", "DELAY", "LOG_GROUP", "SCHEDULED_STREAM", "SCHEDULE_LIST", 
    "IS_VIDEO_RECORD", "IS_RECORDING", "WAS_RECORDING", "RECORDING_TITLE", "PORTRAIT", "RECORDING_DUMP", "HAS_SCHEDULE", 
    "CUSTOM_QUALITY"]

    STARTUP_ERROR=None

    ADMIN_CACHE=False
    CALL_STATUS=False
    YPLAY=False
    YSTREAM=False
    CPLAY=False
    STREAM_SETUP=False
    LISTEN=False
    STREAM_LINK=False
    IS_RECORDING=False
    WAS_RECORDING=False
    PAUSE=False
    MUTED=False
    HAS_SCHEDULE=None
    IS_ACTIVE=None
    VOLUME=111
    CURRENT_CALL=None
    BOT_USERNAME=None
    USER_ID=None

    if LOG_GROUP:
        LOG_GROUP=int(LOG_GROUP)
    else:
        LOG_GROUP=None
    if not API_KEY or \
       not APP_NAME:
       HEROKU_APP=None
    else:
       HEROKU_APP=heroku3.from_key(API_KEY).apps()[APP_NAME]


    if EDIT_TITLE in ["NO", 'False']:
        EDIT_TITLE=False
        LOGGER.info("Title Editing turned off")
    if REPLY_MESSAGE:
        REPLY_MESSAGE=REPLY_MESSAGE
        REPLY_PM=False
        LOGGER.info("Reply Message Found, dsEbled PM MSG")
    else:
        REPLY_MESSAGE=False
        REPLY_PM=False

    if E_BITRATE:
       try:
          BITRATE=int(E_BITRATE)
       except:
          LOGGER.error("Invalid bitrate specified.")
          E_BITRATE=False
          BITRATE=48000
       if not BITRATE >= 48000:
          BITRATE=48000
    else:
       BITRATE=48000
    
    if E_FPS:
       try:
          FPS=int(E_FPS)
       except:
          LOGGER.error("Invalid FPS specified")
          E_FPS=False
       if not FPS >= 30:
          FPS=30
    else:
       FPS=30
    try:
       CUSTOM_QUALITY=int(CUSTOM_QUALITY)
       if CUSTOM_QUALITY > 100:
          CUSTOM_QUALITY = 100
          LOGGER.warning("maximum quality allowed is 100, invalid quality specified. Quality set to 100")
       elif CUSTOM_QUALITY < 10:
          LOGGER.warning("Minimum Quality allowed is 10., Qulaity set to 10")
          CUSTOM_QUALITY = 10
       if  66.9  < CUSTOM_QUALITY < 100:
          if not E_BITRATE:
             BITRATE=48000
       elif 50 < CUSTOM_QUALITY < 66.9:
          if not E_BITRATE:
             BITRATE=36000
       else:
          if not E_BITRATE:
             BITRATE=24000
    except:
       if CUSTOM_QUALITY.lower() == 'high':
          CUSTOM_QUALITY=100
       elif CUSTOM_QUALITY.lower() == 'medium':
          CUSTOM_QUALITY=66.9
       elif CUSTOM_QUALITY.lower() == 'low':
          CUSTOM_QUALITY=50
       else:
          LOGGER.warning("Invalid QUALITY specified.Defaulting to High.")
          CUSTOM_QUALITY=100



    #help strings 
    PLAY_HELP="""__إليك عزيزي / عزيزتي تعليمات.__

1. قم بتشغيل مقطع فيديو من رابط YouTube.
الأمر: ** / play **
__يمكنك استخدام هذا كرد على رابط YouTube أو تمرير الرابط على طول الأمر. أو كرد على رسالة للبحث عن ذلك في YouTube .__

2. التشغيل من ملف تيليجرام.
الأمر: ** / play **
__بالرد على الوسائط المدعومة (فيديو ومستندات أو ملف صوتي) .__
ملاحظة: __للكل من الحالتين / يمكن أيضًا استخدام fplay بواسطة المشرفين لتشغيل الأغنية على الفور دون انتظار انتهاء قائمة الانتظار .__

4. البث المباشر
الأمر: ** / stream**
__مرر عنوان URL من يوتيوب للبث المباشر أو أي عنوان مباشر لتشغيله كبث .__

5. استيراد قائمة تشغيل قديمة.
الأمر: ** / import **
__ بالرد على ملف قائمة تشغيل تم تصديره مسبقًا. __

6. تشغيل من قناة تيليجرام
الأمر: ** / cplay **
__استخدام `/ cplay channel username أو channel id` لتشغيل جميع الملفات من القناة المحددة.
سيتم تشغيل ملفات الفيديو والمستندات بشكل افتراضي. يمكنك إضافة نوع الملف أو إزالته باستخدام var.
على سبيل المثال، لبث الصوت والفيديو والمستندات من القناة ، استخدم `/ env FILTERS video document audio`.  إذا كنت بحاجة إلى صوت فقط ، `/ env FILTERS video audio` وهكذا.
لإعداد الملفات من قناة كـ STARTUP_STREAM ، بحيث تتم إضافة الملفات تلقائيًا إلى قائمة التشغيل عند بدء تشغيل الروبوت. استخدم `/ env STARTUP_STREAM اسم مستخدم القناة أو معرف القناة`

لاحظ أنه بالنسبة للقنوات العامة ، يجب استخدام اسم مستخدم للقنوات مع "@" وبالنسبة للقنوات الخاصة ، يجب استخدام معرف القناة.
للقنوات الخاصة ، تأكد من أن كل من حساب الروبوت وحساب المستخدم المشغل عضو او مشرف في القناة .__
"""
    SETTINGS_HELP="""
** يمكنك بسهولة تخصيص لاعب حسب احتياجاتك. التكوينات التالية متوفرة: **

🔹 الأمر: ** /settings**

التكوينات المتوفرة:

** وضع المشغل ** - __هذا يسمح لك بتشغيل المشغل كإذاعة على مدار الساعة طوال أيام الأسبوع أو فقط عندما تكون هناك أغنية في قائمة الانتظار.
إذا تم تعطيله ، فسيغادر اللاعب من المكالمة عندما تكون قائمة التشغيل فارغة.
وإلا فسيتم بث STARTUP_STREAM عندما يكون معرف قائمة التشغيل فارغًا .__

** الفيديو ** - __هذا يسمح لك بالتبديل بين الصوت والفيديو.
إذا تم تعطيله ، فسيتم تشغيل ملفات الفيديو كصوت .__

** المسؤولين فقط ** - __تفعيل هذا سيقيد المستخدمين غير الإداريين من استخدام أمر التشغيل .__

** تعديل العنوان ** - __تفعيل هذا الخيار سيعدل عنوان دردشة الفيديو الخاص بك إلى اسم الأغاني الجاري تشغيلها .__

** المشغل العشوائي ** - __تفعيل هذا سيؤدي إلى تبديل قائمة التشغيل عشوائيًا كلما قمت باستيراد قائمة تشغيل أو باستخدام / yplay __

** الرد التلقائي ** - __اختر ما إذا كنت تريد الرد على الرسائل الخاصة على الفضوليين والمزعجين في حساب المستخدم المشغل.
يمكنك إعداد رسالة رد مخصصة باستخدام متغير"REPLY_MESSAGE" .__
"""
    SCHEDULER_HELP="""قريبا بإذن الله Qradio سيُمكنك من جدولة بث في اي مدة على مدار العام!!
"""
    RECORDER_HELP="""
    __ مع QRadio يمكنك بسهولة تسجيل جميع محادثات الفيديو الخاصة بك.
افتراضيًا ، تتيح لك Telegram التسجيل لمدة أقصاها 4 ساعات.
،وفي محاولة للتغلب على هذا وتخطي الحدود (: أعددت إلى أن يتم إعادة بدء التسجيل تلقائيًا بعد 4 ساعات__

الأمر: ** /record**

التكوينات المتوفرة:
1. Record Video: __في حالة التمكين ، سيتم تسجيل كل من الفيديو والصوت في البث الجميل، وإلا فسيتم تسجيل الصوت فقط .__

2. Video dimension: __أو بُعد الفيديو ومنه يكون الاختيار بين الأبعاد الرأسية والأفقية للتسجيل__

3. Custom Recording Title: __ قم بإعداد عنوان تسجيل مخصص لتسجيلاتك. استخدم الأمر / rtitle لتكوين هذا.
لإيقاف العنوان المخصص ، استخدم `/rtitle False` __

4. Recording Dumb: __به يمكنك إعداد إعادة توجيه جميع التسجيلات الخاصة بك إلى قناة ، وسيكون هذا مفيدًا لأنه بخلاف ذلك يتم إرسال التسجيلات إلى الرسائل المحفوظة في حساب البث او المشغل.
الإعداد باستخدام "RECORDING_DUMP` config .__

⚠️ إذا بدأت التسجيل باستخدام QRadio ، فتأكد من إيقافه من QRadio وليس من الححساب المشغل او ادارة البث.
"""

    CONTROL_HELP="""__QRadio يسمح لك بالتحكم في مجالس القرآن او أيًا يكن بسهولة__
1. لتخطي أغنية.
الأمر: ** /skip **
__يمكنك تمرير رقم أكبر من 2 لتخطي الأغنية صاحبة هذا الموضع أو الترتيب في قائمة التشغيل .__

2. لإيقاف المشغل مؤقتًا.
الأمر: ** / pause **

3. لاستئناف المشغل.
الأمر: ** /resume **

4. لتغيير مستوى الصوت.
الأمر: ** /volume **
__مرر الصوت بين 1-200 .__

5. لمغادرة المجلس.
الأمر: ** /leave **

6. للتبديل في قائمة التشغيل عشوائيًا.
الأمر: ** /shuffle **

7. لمسح قائمة التشغيل الحالية.
الأمر: ** /clearplaylist **

8. للتخطي من الفيديو.
الأمر: ** /seek **
__ يمكنك تمرير عدد من الثواني ليتم تخطيها. مثال: / ابحث عن 10 لتخطي 10 ثوانٍ. / طلب -10 للإرجاع 10 ثوانٍ .__

9. لكتم صوت المشغل.
الأمر: ** /vcmute **

10. لإعادة صوت المشغل.
الأمر: ** /vcunmute **

11. لتظهر قائمة التشغيل.
الأمر: ** /playlist **
__استخدم /player لإظهار أزرار التحكم__
"""

    ADMIN_HELP = """
__QRadio يسمح بالتحكم في المسؤولين ، أي يمكنك إضافة مدراء وإزالتهم بسهولة.
يوصى باستخدام قاعدة بيانات MongoDb للحصول على تجربة أفضل ، وإلا فسيتم إعادة تعيين جميع المسؤولين بعد إعادة التشغيل .__

الأمر: ** /vcpromote **
__يمكنك ترقية أي مسؤول باسم المستخدم أو معرف المستخدم الخاص به أو بالرد على رسالة المستخدمين .__

الأمر: ** /vcdemote **
__إزالة مسؤول من قائمة المسؤولين__

الأمر: ** /Refresh **
__تحديث قائمة إدارة الدردشة__
"""

    MISC_HELP = """
الأمر: ** /export **
__QRadio يسمح لك بتصدير قائمة التشغيل الحالية لاستخدامها في المستقبل .__
__ سيتم إرسال ملف json إليك ويمكن استخدام نفس الأمر مع أمر الاستيراد / .__

الأمر: ** /logs **
__للمطورين، إذا حدث خطأ ما في المشغل ، يمكنك بسهولة التحقق من السجلات باستخدام / logs__
 
الأمر: ** /env **
__إعداد متغيرات التكوين الخاصة بك باستخدام الأمر env .__
__مثال: لإعداد__ `REPLY_MESSAGE` __use__` / env REPLY_MESSAGE = مرحبًا ، تحقق 82 بدلاً من إرسال رسائل غير مرغوب فيها في PM`__
__يمكنك حذف config var عن طريق إدخال قيمة لذلك ، على سبيل المثال: __ `/ env LOG_GROUP =` __ هذا سيحذف تهيئة LOG_GROUP الحالية.

الأمر: ** /config **
__تشابه مع استخدام / env **

الأمر: ** /update **
__تحديث برنامج الروبوت بأحدث التغييرات__

نصيحة: __يمكنك بسهولة تغيير تهيئة الدردشة عن طريق إضافة حساب المستخدم وحساب الروبوت إلى أي مجموعة أخرى وأي أمر في مجموعة جديدة دون الحاجة للتلاعب في المتغيرات__
"""
    ENV_HELP="""
** هذا القسم للمطورين...**
هذه هي المتغيرات القابلة للتكوين المتاحة ويمكنك تعيين كل واحد منهم باستخدام الأمر env 


** متغيرات إلزامية **

1. `API_ID` : __Get From [my.telegram.org](https://my.telegram.org/)__

2. `API_HASH` : __Get from [my.telegram.org](https://my.telegram.org)__

3. `BOT_TOKEN` : __[@Botfather](https://telegram.dog/BotFather)__

4. `SESSION_STRING` : __Generate From here [GenerateStringName](https://repl.it/@subinps/getStringName)__

5. `CHAT` : __ID of Channel/Group where the bot plays Music.__

6. `STARTUP_STREAM` : __This will be streamed on startups and restarts of bot. 
You can use either any STREAM_URL or a direct link of any video or a Youtube Live link. 
You can also use YouTube Playlist.Find a Telegram Link for your playlist from [PlayList Dumb](https://telegram.dog/ourpybot) 
You can also use the files from a channel as startup stream. For that just use the channel id or channel username of channel as STARTUP_STREAM value.
For more info on channel play , read help from player section.__

**اختيارية**

1. `DATABASE_URI`: __MongoDB database Url, get from [mongodb](https://cloud.mongodb.com). This is an optional var, but it is recomonded to use this to experiance the full features.__

2. `HEROKU_API_KEY`: __Your heroku api key. Get one from [here](https://dashboard.heroku.com/account/applications/authorizations/new)__

3. `HEROKU_APP_NAME`: __Your heroku app's name.__

4. `FILTERS`: __Filters for channel play file search. Read help about cplay in player section.__

**Other Optional Vars**
1. `LOG_GROUP` : __Group to send Playlist, if CHAT is a Group__

2. `ADMINS` : __ID of users who can use admin commands.__

3. `REPLY_MESSAGE` : __A reply to those who message the USER account in PM. Leave it blank if you do not need this feature. (Configurable through buttons if mongodb added. Use /settings)__

4. `ADMIN_ONLY` : __Pass `True` If you want to make /play command only for admins of `CHAT`. By default /play is available for all.(Configurable through buttons if mongodb added. Use /settings)__

5. `DATABASE_NAME`: __Database name for your mongodb database.mongodb__

6. `SHUFFLE` : __Make it `False` if you dont want to shuffle playlists. (Configurable through buttons)__

7. `EDIT_TITLE` : __Make it `False` if you do not want the bot to edit video chat title according to playing song. (Configurable through buttons if mongodb added. Use /settings)__

8. `RECORDING_DUMP` : __A Channel ID with the USER account as admin, to dump video chat recordings.__

9. `RECORDING_TITLE`: __A custom title for your videochat recordings.__

10. `TIME_ZONE` : __Time Zone of your country, by default IST__

11. `IS_VIDEO_RECORD` : __Make it `False` if you do not want to record video, and only audio will be recorded.(Configurable through buttons if mongodb added. Use /record)__

12. `IS_LOOP` ; __Make it `False` if you do not want 24 / 7 Video Chat. (Configurable through buttons if mongodb added.Use /settings)__

13. `IS_VIDEO` : __Make it `False` if you want to use the player as a musicplayer without video. (Configurable through buttons if mongodb added. Use /settings)__

14. `PORTRAIT`: __Make it `True` if you want the video recording in portrait mode. (Configurable through buttons if mongodb added. Use /record)__

15. `DELAY` : __Choose the time limit for commands deletion. 10 sec by default.__

16. `QUALITY` : __Customize the quality of video chat, use one of `high`, `medium`, `low` . __

17. `BITRATE` : __Bitrate of audio (Not recommended to change).__

18. `FPS` : __Fps of video to be played (Not recommended to change.)__

"""
