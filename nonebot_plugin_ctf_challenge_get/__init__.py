from nonebot import on_command,get_driver
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message,Event
from nonebot.params import Arg,ArgStr, CommandArg, ArgPlainText,Received,Depends
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.plugin.plugin import PluginMetadata
from .Utils import get_ctfhub,get_adworld,review_adworld,get_BUUCTF
import string

default_start = list(get_driver().config.command_start)[0]

ctfhub = on_command("ctfhub", aliases={"ctfhub"}, priority=5)
adworld = on_command("adworld", aliases={"adworld"}, priority=5)
buuctf = on_command("buuctf", aliases={"buuctf"}, priority=5)


@ctfhub.handle()
async def handle_ctfhub(matcher: Matcher, args:Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("list_id", args)
    else:
        ctfhub_list = await get_ctfhub_list()
        await ctfhub.send(ctfhub_list)

# 获取ctfhublist
@ctfhub.got("list_id")
async def handle_list(list_id: str = ArgPlainText("list_id") ) -> str:
    if str.isdigit(list_id):
        list_id = int(list_id)
        if list_id>6 or list_id<1:
            await ctfhub.finish("查询的序号不存在")
    else:
        await ctfhub.finish("请重新输入正确的序号哦~")
    # if list_id==6:
    #     ctf_list = 
    ctfhub_list = await get_ctfhub_list(list_id)
    await ctfhub.finish(ctfhub_list)

async def get_ctfhub_list(list_id:int = 0)->str:
    if list_id:
        return get_ctfhub(list_id)
    return get_ctfhub(list_id)


@adworld.handle()
async def handle_aworld():
    nores,res = get_adworld()
    if nores:
        await adworld.send(nores)
    else:
        await adworld.send(res)

@adworld.got("info")
async def receive_(e:MessageEvent):
    msg = e.get_plaintext()
    if 'review' in msg:
        name = msg.replace('review','').strip()
        res = review_adworld(name)
        await adworld.finish(res)

async def buu_depend(event: MessageEvent):
    return get_BUUCTF()

@buuctf.handle()
async def handle_buuctf(matcher: Matcher, args:Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("list_id", args)
    else:
        buuctf_list = await get_buuctf_list()
        if buuctf_list:
            await ctfhub.send(buuctf_list)
        else:
            await ctfhub.finish('近期没有比赛噢~')

# 获取buuctflist
@buuctf.got("list_id")
async def handle_list(list_id: str = ArgPlainText("list_id") ) -> str:
    if str.isdigit(list_id):
        list_id = int(list_id)
        if list_id>6 or list_id<1:
            await buuctf.finish("查询的序号不存在")
    else:
        await buuctf.finish("请重新输入正确的序号哦~")
    # if list_id==6:
    #     ctf_list = 
    buuctf_list = await get_buuctf_list(list_id)
    await buuctf.finish(buuctf_list)

async def get_buuctf_list(list_id:int = 0)->str:
    if list_id:
        return get_BUUCTF(list_id)
    return get_BUUCTF(list_id)


__help_version__ = '0.1.1'
# New way of self registering (use PluginMetadata)
__plugin_meta__ = PluginMetadata(
    name='CTF Challenge Get',
    description='获取各平台赛事信息',
    usage=f'''
{default_start}ctfhub  # 获取ctfhub平台搜集的赛事
{default_start}adworld  # 获取攻防世界平台搜集的赛事
{default_start}buuctf  # 获取BUUCTF搜集的赛事

其他平台再等等啦~
''',
    extra={'version': '0.3.1'}
)
