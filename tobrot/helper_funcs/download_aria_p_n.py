#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52

# the logging things
import logging
import sys
sys.setrecursionlimit(10**4)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

import aria2p
import asyncio
import os
from tobrot.helper_funcs.upload_to_tg import upload_to_tg, upload_to_gdrive
from tobrot.helper_funcs.create_compressed_archive import create_archive, unzip_me, unrar_me, untar_me
from tobrot.helper_funcs.extract_link_from_message import extract_link

from tobrot import (
    ARIA_TWO_STARTED_PORT,
    MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START,
    AUTH_CHANNEL,
    DOWNLOAD_LOCATION,
    EDIT_SLEEP_TIME_OUT,
    CUSTOM_FILE_NAME
)
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
	InlineKeyboardButton,
	InlineKeyboardMarkup,
	Message
)

async def aria_start():
    aria2_daemon_start_cmd = []
    # start the daemon, aria2c command
    aria2_daemon_start_cmd.append("aria2c")
    aria2_daemon_start_cmd.append("--allow-overwrite=true")
    aria2_daemon_start_cmd.append("--daemon=true")
    # aria2_daemon_start_cmd.append(f"--dir={DOWNLOAD_LOCATION}")
    # TODO: this does not work, need to investigate this.
    # but for now, https://t.me/TrollVoiceBot?start=858
    aria2_daemon_start_cmd.append("--enable-rpc")
    aria2_daemon_start_cmd.append("--follow-torrent=mem")
    aria2_daemon_start_cmd.append("--max-connection-per-server=10")
    aria2_daemon_start_cmd.append("--min-split-size=10M")
    aria2_daemon_start_cmd.append("--rpc-listen-all=false")
    aria2_daemon_start_cmd.append(f"--rpc-listen-port={ARIA_TWO_STARTED_PORT}")
    aria2_daemon_start_cmd.append("--rpc-max-request-size=1024M")
    aria2_daemon_start_cmd.append("--seed-ratio=0.0")
    aria2_daemon_start_cmd.append("--seed-time=1")
    aria2_daemon_start_cmd.append("--max-overall-upload-limit=1K")
    aria2_daemon_start_cmd.append("--split=10")
    aria2_daemon_start_cmd.append("--bt-tracker=udp://tracker.coppersurfer.tk:6969/announce,http://tracker.opentrackr.org:1337/announce,udp://9.rarbg.to:2710/announce,udp://9.rarbg.me:2710/announce,udp://exodus.desync.com:6969/announce,udp://tracker.cyberia.is:6969/announce,udp://tracker3.itzmx.com:6961/announce,udp://tracker.tiny-vps.com:6969/announce,udp://open.stealth.si:80/announce,http://tracker1.itzmx.com:8080/announce,udp://tracker.torrent.eu.org:451/announce,udp://retracker.lanta-net.ru:2710/announce,udp://tracker.moeking.me:6969/announce,udp://bt2.archive.org:6969/announce,http://tracker4.itzmx.com:2710/announce,udp://ipv4.tracker.harry.lu:80/announce,udp://bt1.archive.org:6969/announce,udp://explodie.org:6969/announce,https://trakx.herokuapp.com:443/announce,http://h4.trakx.nibba.trade:80/announce,udp://tracker.opentrackr.org:1337/announce,http://tracker3.itzmx.com:6961/announce,http://explodie.org:6969/announce,udp://zephir.monocul.us:6969/announce,udp://wassermann.online:6969/announce,udp://vibe.community:6969/announce,udp://valakas.rollo.dnsabr.com:2710/announce,udp://ultra.zt.ua:6969/announce,udp://u.wwwww.wtf:1/announce,udp://tracker2.dler.org:80/announce,udp://tracker0.ufibox.com:6969/announce,udp://tracker.zum.bi:6969/announce,udp://tracker.zerobytes.xyz:1337/announce,udp://tracker.zemoj.com:6969/announce,udp://tracker.vulnix.sh:6969/announce,udp://tracker.v6speed.org:6969/announce,udp://tracker.uw0.xyz:6969/announce,udp://tracker.swateam.org.uk:2710/announce,udp://tracker.skyts.net:6969/announce,udp://tracker.skynetcloud.site:6969/announce,udp://tracker.shkinev.me:6969/announce,udp://tracker.publictracker.xyz:6969/announce,udp://tracker.lelux.fi:6969/announce,udp://tracker.kamigami.org:2710/announce,udp://tracker.filemail.com:6969/announce,udp://tracker.dyne.org:6969/announce,udp://tracker.ds.is:6969/announce,udp://tracker.dler.org:6969/announce,udp://tracker.army:6969/announce,udp://tracker-udp.gbitt.info:80/announce,udp://teamspeak.value-wolf.org:6969/announce,udp://t3.leech.ie:1337/announce,udp://t2.leech.ie:1337/announce,udp://t1.leech.ie:1337/announce,udp://storage.groupees.com:6969/announce,udp://sd-161673.dedibox.fr:6969/announce,udp://rutorrent.frontline-mod.com:6969/announce,udp://retracker.sevstar.net:2710/announce,udp://retracker.netbynet.ru:2710/announce,udp://retracker.local.msn-net.ru:6969/announce,udp://retracker.akado-ural.ru:80/announce,udp://publictracker.xyz:6969/announce,udp://public.publictracker.xyz:6969/announce,udp://public-tracker.zooki.xyz:6969/announce,udp://opentracker.i2p.rocks:6969/announce,udp://opentor.org:2710/announce,udp://nagios.tks.sumy.ua:80/announce,udp://mts.tvbit.co:6969/announce,udp://movies.zsw.ca:6969/announce,udp://mail.realliferpg.de:6969/announce,udp://ln.mtahost.co:6969/announce,udp://line-net.ru:6969/announce,udp://koli.services:6969/announce,udp://kanal-4.de:6969/announce,udp://inferno.demonoid.is:3391/announce,udp://handrew.me:6969/announce,udp://git.vulnix.sh:6969/announce,udp://free-tracker.zooki.xyz:6969/announce,udp://forever-tracker.zooki.xyz:6969/announce,udp://fe.dealclub.de:6969/announce,udp://engplus.ru:6969/announce,udp://eliastre100.fr:6969/announce,udp://edu.uifr.ru:6969/announce,udp://drumkitx.com:6969/announce,udp://dpiui.reedlan.com:6969/announce,udp://discord.heihachi.pw:6969/announce,udp://daveking.com:6969/announce,udp://cutiegirl.ru:6969/announce,udp://code2chicken.nl:6969/announce,udp://chanchan.uchuu.co.uk:6969/announce,udp://cdn-2.gamecoast.org:6969/announce,udp://cdn-1.gamecoast.org:6969/announce,udp://bubu.mapfactor.com:6969/announce,udp://bms-hosxp.com:6969/announce,udp://blokas.io:6969/announce,udp://bitsparadise.info:6969/announce,udp://benouworldtrip.fr:6969/announce,udp://aruacfilmes.com.br:6969/announce,udp://api.bitumconference.ru:6969/announce,udp://adminion.n-blade.ru:6969/announce,udp://admin.videoenpoche.info:6969/announce,udp://adm.category5.tv:6969/announce,udp://aaa.army:8866/announce,udp://6ahddutb1ucc3cp.ru:6969/announce,udp://61626c.net:6969/announce,udp://47.ip-51-68-199.eu:6969/announce,https://w.wwwww.wtf:443/announce,https://tracker.tamersunion.org:443/announce,https://tracker.sloppyta.co:443/announce,https://tracker.nitrix.me:443/announce,https://tracker.lelux.fi:443/announce,https://tracker.imgoingto.icu:443/announce,https://tracker.hama3.net:443/announce,https://tracker.gbitt.info:443/announce,https://aaa.army:8866/announce,https://1337.abcvg.info:443/announce,http://vps02.net.orel.ru:80/announce,http://vpn.flying-datacenter.de:6969/announce,http://trun.tom.ru:80/announce,http://tracker2.dler.org:80/announce,http://tracker.zum.bi:6969/announce,http://tracker.zerobytes.xyz:1337/announce,http://tracker.ygsub.com:6969/announce,http://tracker.sloppyta.co:80/announce,http://tracker.skyts.net:6969/announce,http://tracker.noobsubs.net:80/announce,http://tracker.lelux.fi:80/announce,http://tracker.kamigami.org:2710/announce,http://tracker.gbitt.info:80/announce,http://tracker.bt4g.com:2095/announce,http://tracker.anonwebz.xyz:8080/announce,http://t.overflow.biz:6969/announce,http://t.nyaatracker.com:80/announce,http://rt.tace.ru:80/announce,http://retracker.sevstar.net:2710/announce,http://pow7.com:80/announce,http://opentracker.i2p.rocks:6969/announce,http://aaa.army:8866/announce,udp://www.midea123.z-media.com.cn:6969/announce,udp://tsundere.pw:6969/announce,udp://tracker6.dler.org:2710/announce,udp://tracker4.itzmx.com:2710/announce,udp://tracker2.itzmx.com:6961/announce,udp://tracker.kali.org:6969/announce,udp://tracker.fortu.io:6969/announce,udp://tracker.blacksparrowmedia.net:6969/announce,udp://tr.cili001.com:8070/announce,udp://tr.bangumi.moe:6969/announce,udp://qg.lorzl.gq:2710/announce,udp://open.lolicon.eu:7777/announce,udp://ns389251.ovh.net:6969/announce,udp://ns-1.x-fins.com:6969/announce,udp://jsb.by:8000/announce,udp://josueunhuit.com:6969/announce,udp://concen.org:6969/announce,udp://camera.lei001.com:6969/announce,udp://btt.royalquest.ru:2710/announce,udp://bt2.54new.com:8080/announce,udp://bt.firebit.org:2710/announce,udp://bioquantum.co.za:6969/announce,udp://bclearning.top:6969/announce,udp://anidex.moe:6969/announce,http://tracker2.itzmx.com:6961/announce,http://tracker.dler.org:6969/announce,http://t.acg.rip:6699/announce,http://open.acgnxtracker.com:80/announce,http://jsb.by:8000/announce,http://bobbialbano.com:6969/announce,wss://video.blender.org:443/tracker/socket,wss://tube.privacytools.io:443/tracker/socket,wss://tracker.sloppyta.co:443/announce,wss://tracker.files.fm:7073/announce,wss://peertube.cpy.re:443/tracker/socket,wss://open.tube:443/tracker/socket,wss://hub.bugout.link:443/announce,ws://tracker.sloppyta.co:80/announce,ws://tracker.files.fm:7072/announce,ws://tracker.btsync.cf:6969/announce,ws://hub.bugout.link:80/announce,udp://31.14.40.30:6969/announce,http://93.158.213.92:1337/announce,udp://151.80.120.114:2710/announce,udp://151.80.120.112:2710/announce,udp://208.83.20.20:6969/announce,udp://194.182.165.153:6969/announce,udp://176.113.71.60:6961/announce,udp://5.206.38.65:6969/announce,udp://185.181.60.67:80/announce,http://118.24.123.223:8080/announce,udp://89.234.156.205:451/announce,udp://37.235.174.46:2710/announce,udp://207.241.231.226:6969/announce,udp://51.15.40.114:80/announce,udp://207.241.226.111:6969/announce,udp://184.105.151.164:6969/announce,udp://93.158.213.92:1337/announce,http://176.113.71.60:6961/announce,udp://185.244.173.140:6969/announce,http://184.105.151.164:6969/announce,udp://212.47.227.58:6969/announce,udp://185.183.158.105:6969/announce,udp://159.69.208.124:6969/announce,udp://46.148.18.250:2710/announce,udp://193.150.6.253:6969/announce,udp://167.179.77.133:1/announce,udp://61.216.34.217:80/announce,udp://173.212.223.237:6969/announce,udp://165.227.0.51:6969/announce,udp://51.15.55.204:1337/announce,udp://134.209.1.127:6969/announce,udp://178.128.189.81:6969/announce,udp://45.77.100.109:6969/announce,udp://91.149.192.31:6969/announce,udp://75.127.14.224:2710/announce,udp://222.217.126.69:6969/announce,udp://85.94.179.157:6969/announce,udp://138.68.171.1:6969/announce,udp://195.123.209.147:6969/announce,udp://95.217.161.135:6969/announce,udp://51.158.154.106:2710/announce,udp://52.58.128.163:6969/announce,udp://195.169.149.121:6969/announce,udp://5.226.148.20:6969/announce,udp://125.227.84.132:6969/announce,udp://103.196.36.31:6969/announce,udp://62.171.179.41:80/announce,udp://62.138.2.239:6969/announce,udp://209.141.45.244:1337/announce,udp://199.195.249.193:1337/announce,udp://104.244.72.77:1337/announce,udp://199.187.121.233:6969/announce,udp://51.159.64.19:6969/announce,udp://163.172.156.194:6969/announce,udp://78.30.254.12:2710/announce,udp://212.1.226.176:2710/announce,udp://217.76.183.53:80/announce,udp://185.234.52.244:6969/announce,udp://217.12.210.229:6969/announce,udp://104.238.159.144:6969/announce,udp://51.81.46.170:6969/announce,udp://46.148.18.254:2710/announce,udp://193.34.92.5:80/announce,udp://213.108.129.160:6969/announce,udp://198.100.149.66:6969/announce,udp://195.201.94.195:6969/announce,udp://151.236.218.182:6969/announce,udp://178.159.40.252:6969/announce,udp://145.236.61.206:6969/announce,udp://188.40.91.149:6969/announce,udp://176.123.5.238:3391/announce,udp://192.99.37.155:6969/announce,udp://45.79.114.71:6969/announce,udp://51.77.58.98:6969/announce,udp://93.115.23.108:6969/announce,udp://148.251.53.72:6969/announce,udp://185.8.156.2:6969/announce,udp://178.32.217.118:6969/announce,udp://62.168.229.166:6969/announce,udp://46.101.244.237:6969/announce,udp://178.16.88.250:6969/announce,udp://144.76.35.202:6969/announce,udp://51.79.81.233:6969/announce,udp://144.76.82.110:6969/announce,udp://51.15.2.221:6969/announce,udp://185.83.214.123:6969/announce,udp://51.77.134.13:6969/announce,udp://51.68.34.33:6969/announce,udp://199.217.118.72:6969/announce,udp://61.19.251.235:6969/announce,udp://138.68.69.188:6969/announce,udp://212.195.37.201:6969/announce,udp://51.15.192.176:6969/announce,udp://54.207.36.253:6969/announce,udp://144.76.28.43:6969/announce,udp://37.228.115.250:6969/announce,udp://212.83.181.109:6969/announce,udp://66.209.59.221:6969/announce,udp://49.12.113.1:8866/announce,udp://35.205.255.125:6969/announce,udp://45.76.120.20:6969/announce,udp://51.68.199.47:6969/announce,http://95.107.48.115:80/announce,http://178.248.247.244:6969/announce,http://61.216.34.217:80/announce,http://165.227.0.51:6969/announce,http://51.15.55.204:1337/announce,http://47.240.12.145:6969/announce,http://222.217.126.69:6969/announce,http://51.158.154.106:2710/announce,http://189.68.241.4:6969/announce,http://195.201.31.194:80/announce,http://78.30.254.12:2710/announce,http://51.81.46.170:6969/announce,http://49.12.113.1:8866/announce,udp://47.105.62.206:6969/announce,udp://172.126.62.47:6969/announce,udp://61.216.34.217:2710/announce,udp://176.113.68.67:6961/announce,udp://45.33.83.49:6969/announce,udp://188.166.71.230:6969/announce,udp://67.224.119.27:6969/announce,udp://180.97.219.76:8070/announce,udp://51.15.3.74:6969/announce,udp://218.5.41.226:2710/announce,udp://198.50.195.216:7777/announce,udp://176.31.101.42:6969/announce,udp://47.97.100.153:6969/announce,udp://86.57.243.186:8000/announce,udp://109.190.50.33:6969/announce,udp://37.59.48.81:6969/announce,udp://61.164.110.198:6969/announce,udp://188.127.246.7:2710/announce,udp://2.59.132.201:8080/announce,udp://37.1.205.89:2710/announce,udp://41.242.80.100:6969/announce,udp://39.106.122.67:6969/announce,udp://91.121.145.207:6969/announce,http://176.113.68.67:6961/announce,http://211.20.122.232:6969/announce,http://54.39.179.91:6699/announce,http://54.37.106.164:80/announce,http://86.57.243.186:8000/announce,http://192.151.157.106:6969/announce")
    aria2_daemon_start_cmd.append(f"--bt-stop-timeout={MAX_TIME_TO_WAIT_FOR_TORRENTS_TO_START}")
    aria2_daemon_start_cmd.append("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36")
    aria2_daemon_start_cmd.append("--peer-agent=qBittorrent/4.2.5")
    #
    LOGGER.info(aria2_daemon_start_cmd)
    #
    process = await asyncio.create_subprocess_exec(
        *aria2_daemon_start_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    LOGGER.info(stdout)
    LOGGER.info(stderr)
    aria2 = aria2p.API(
        aria2p.Client(
            host="http://localhost",
            port=ARIA_TWO_STARTED_PORT,
            secret=""
        )
    )
    return aria2


def add_magnet(aria_instance, magnetic_link, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    try:
        download = aria_instance.add_magnet(
            magnetic_link,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    else:
        return True, "" + download.gid + ""


def add_torrent(aria_instance, torrent_file_path):
    if torrent_file_path is None:
        return False, "**FAILED** \n" + str(e) + " \nsomething wrongings when trying to add <u>TORRENT</u> file"
    if os.path.exists(torrent_file_path):
        # Add Torrent Into Queue
        try:
            download = aria_instance.add_torrent(
                torrent_file_path,
                uris=None,
                options=None,
                position=None
            )
        except Exception as e:
            return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
        else:
            return True, "" + download.gid + ""
    else:
        return False, "**FAILED** \nPlease try other sources to get workable link"


def add_url(aria_instance, text_url, c_file_name):
    options = None
    # if c_file_name is not None:
    #     options = {
    #         "dir": c_file_name
    #     }
    uris = [text_url]
    # Add URL Into Queue
    try:
        download = aria_instance.add_uris(
            uris,
            options=options
        )
    except Exception as e:
        return False, "**FAILED** \n" + str(e) + " \nPlease do not send SLOW links. Read /help"
    else:
        return True, "" + download.gid + ""


async def call_apropriate_function(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_unzip,
    is_unrar,
    is_untar,
    user_message
):
    if incoming_link.lower().startswith("magnet:"):
        sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name)
    elif incoming_link.lower().endswith(".torrent"):
        sagtus, err_message = add_torrent(aria_instance, incoming_link)
    else:
        sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name)
    if not sagtus:
        return sagtus, err_message
    LOGGER.info(err_message)
    # https://stackoverflow.com/a/58213653/4723940
    await check_progress_for_dl(
        aria_instance,
        err_message,
        sent_message_to_update_tg_p,
        None
    )
    if incoming_link.startswith("magnet:"):
        #
        err_message = await check_metadata(aria_instance, err_message)
        #
        await asyncio.sleep(1)
        if err_message is not None:
            await check_progress_for_dl(
                aria_instance,
                err_message,
                sent_message_to_update_tg_p,
                None
            )
        else:
            return False, "can't get metadata \n\n#stopped"
    await asyncio.sleep(1)
    file = aria_instance.get_download(err_message)
    to_upload_file = file.name
    com_g = file.is_complete
    #
    if is_zip:
        # first check if current free space allows this
        # ref: https://github.com/out386/aria-telegram-mirror-bot/blob/master/src/download_tools/aria-tools.ts#L194
        # archive the contents
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file
    #
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    if to_upload_file:
        if CUSTOM_FILE_NAME:
            os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        else:
            to_upload_file = to_upload_file

    if cstom_file_name:
        os.rename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name
    else:
        to_upload_file = to_upload_file
    #
    response = {}
    LOGGER.info(response)
    user_id = user_message.from_user.id
    #LOGGER.info(user_id)
    if com_g:
        final_response = await upload_to_tg(
            sent_message_to_update_tg_p,
            to_upload_file,
            user_id,
            response
        )
    LOGGER.info(final_response)
    try:
        message_to_send = ""
        for key_f_res_se in final_response:
            local_file_name = key_f_res_se
            message_id = final_response[key_f_res_se]
            channel_id = str(sent_message_to_update_tg_p.chat.id)[4:]
            private_link = f"https://t.me/c/{channel_id}/{message_id}"
            message_to_send += "👉 <a href='"
            message_to_send += private_link
            message_to_send += "'>"
            message_to_send += local_file_name
            message_to_send += "</a>"
            message_to_send += "\n"
        if message_to_send != "":
            mention_req_user = f"<a href='tg://user?id={user_id}'>Your Requested Files</a>\n\n"
            message_to_send = mention_req_user + message_to_send
            message_to_send = message_to_send + "\n\n" + "#uploads"
        else:
            message_to_send = "<i>FAILED</i> to upload files. 😞😞"
        await user_message.reply_text(
            text=message_to_send,
            quote=True,
            disable_web_page_preview=True
        )
    except:
        pass
    return True, None
#

async def call_apropriate_function_g(
    aria_instance,
    incoming_link,
    c_file_name,
    sent_message_to_update_tg_p,
    is_zip,
    cstom_file_name,
    is_unzip,
    is_unrar,
    is_untar,
    user_message
):
    if incoming_link.lower().startswith("magnet:"):
        sagtus, err_message = add_magnet(aria_instance, incoming_link, c_file_name)
    elif incoming_link.lower().endswith(".torrent"):
        sagtus, err_message = add_torrent(aria_instance, incoming_link)
    else:
        sagtus, err_message = add_url(aria_instance, incoming_link, c_file_name)
    if not sagtus:
        return sagtus, err_message
    LOGGER.info(err_message)
    # https://stackoverflow.com/a/58213653/4723940
    await check_progress_for_dl(
        aria_instance,
        err_message,
        sent_message_to_update_tg_p,
        None
    )
    if incoming_link.startswith("magnet:"):
        #
        err_message = await check_metadata(aria_instance, err_message)
        #
        await asyncio.sleep(1)
        if err_message is not None:
            await check_progress_for_dl(
                aria_instance,
                err_message,
                sent_message_to_update_tg_p,
                None
            )
        else:
            return False, "can't get metadata \n\n#stopped"
    await asyncio.sleep(1)
    file = aria_instance.get_download(err_message)
    to_upload_file = file.name
    com_gau = file.is_complete
    #
    if is_zip:
        # first check if current free space allows this
        # ref: https://github.com/out386/aria-telegram-mirror-bot/blob/master/src/download_tools/aria-tools.ts#L194
        # archive the contents
        check_if_file = await create_archive(to_upload_file)
        if check_if_file is not None:
            to_upload_file = check_if_file
    #
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    if to_upload_file:
        if CUSTOM_FILE_NAME:
            os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        else:
            to_upload_file = to_upload_file

    if cstom_file_name:
        os.rename(to_upload_file, cstom_file_name)
        to_upload_file = cstom_file_name
    else:
        to_upload_file = to_upload_file
    #
    response = {}
    LOGGER.info(response)
    user_id = user_message.from_user.id
    LOGGER.info(user_id)
    if com_gau:
        final_response = await upload_to_gdrive(
            to_upload_file,
            sent_message_to_update_tg_p,
            user_message,
            user_id
        )
#
async def call_apropriate_function_t(
    to_upload_file_g,
    sent_message_to_update_tg_p,
    is_unzip,
    is_unrar,
    is_untar
):
    #
    to_upload_file = to_upload_file_g
    if is_unzip:
        check_ifi_file = await unzip_me(to_upload_file_g)
        if check_ifi_file is not None:
            to_upload_file = check_ifi_file
    #
    if is_unrar:
        check_ife_file = await unrar_me(to_upload_file_g)
        if check_ife_file is not None:
            to_upload_file = check_ife_file
    #
    if is_untar:
        check_ify_file = await untar_me(to_upload_file_g)
        if check_ify_file is not None:
            to_upload_file = check_ify_file
    #
    response = {}
    LOGGER.info(response)
    user_id = sent_message_to_update_tg_p.reply_to_message.from_user.id
    final_response = await upload_to_gdrive(
        to_upload_file,
        sent_message_to_update_tg_p
    )
    LOGGER.info(final_response)
    #if to_upload_file:
        #if CUSTOM_FILE_NAME:
            #os.rename(to_upload_file, f"{CUSTOM_FILE_NAME}{to_upload_file}")
            #to_upload_file = f"{CUSTOM_FILE_NAME}{to_upload_file}"
        #else:
            #to_upload_file = to_upload_file

    #if cstom_file_name:
        #os.rename(to_upload_file, cstom_file_name)
        #to_upload_file = cstom_file_name
    #else:
        #to_upload_file = to_upload_file
    '''
    
    LOGGER.info(final_response)
    message_to_send = ""
    for key_f_res_se in final_response:
        local_file_name = key_f_res_se
        message_id = final_response[key_f_res_se]
        channel_id = str(AUTH_CHANNEL)[4:]
        private_link = f"https://t.me/c/{channel_id}/{message_id}"
        message_to_send += "👉 <a href='"
        message_to_send += private_link
        message_to_send += "'>"
        message_to_send += local_file_name
        message_to_send += "</a>"
        message_to_send += "\n"
    if message_to_send != "":
        mention_req_user = f"<a href='tg://user?id={user_id}'>Your Requested Files</a>\n\n"
        message_to_send = mention_req_user + message_to_send
        message_to_send = message_to_send + "\n\n" + "#uploads"
    else:
        message_to_send = "<i>FAILED</i> to upload files. 😞😞"
    await sent_message_to_update_tg_p.reply_to_message.reply_text(
        text=message_to_send,
        quote=True,
        disable_web_page_preview=True
    )
    return True, None
    '''


# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164
async def check_progress_for_dl(aria2, gid, event, previous_message):
    #g_id = event.reply_to_message.from_user.id
    try:
        file = aria2.get_download(gid)
        complete = file.is_complete
        is_file = file.seeder
        if not complete:
            if not file.error_message:
                msg = ""
                # sometimes, this weird https://t.me/c/1220993104/392975
                # error creeps up
                # TODO: temporary workaround
                downloading_dir_name = "N/A"
                try:
                    # another derp -_-
                    # https://t.me/c/1220993104/423318
                    downloading_dir_name = str(file.name)
                except:
                    pass
                #
                if is_file is None :
                   msgg = f"Conn: {file.connections} <b>|</b> GID: <code>{gid}</code>"
                else :
                   msgg = f"P: {file.connections} | S: {file.num_seeders} <b>|</b> GID: <code>{gid}</code>"
                msg = f"\n`{downloading_dir_name}`"
                msg += f"\n<b>Speed</b>: {file.download_speed_string()}"
                msg += f"\n<b>Status</b>: {file.progress_string()} <b>of</b> {file.total_length_string()} <b>|</b> {file.eta_string()} <b>|</b> {msgg}"
                #msg += f"\nSize: {file.total_length_string()}"

                #if is_file is None :
                   #msg += f"\n<b>Conn:</b> {file.connections}, GID: <code>{gid}</code>"
                #else :
                   #msg += f"\n<b>Info:</b>[ P : {file.connections} | S : {file.num_seeders} ], GID: <code>{gid}</code>"

                #msg += f"\nStatus: {file.status}"
                #msg += f"\nETA: {file.eta_string()}"
                #msg += f"\nGID: <code>{gid}</code>"
                inline_keyboard = []
                ikeyboard = []
                ikeyboard.append(InlineKeyboardButton("Cancel 🚫", callback_data=(f"cancel {gid}").encode("UTF-8")))
                inline_keyboard.append(ikeyboard)
                reply_markup = InlineKeyboardMarkup(inline_keyboard)
                #msg += reply_markup
                LOGGER.info(msg)
                if msg != previous_message:
                    await event.edit(msg, reply_markup=reply_markup)
                    previous_message = msg
            else:
                msg = file.error_message
                await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
                await event.edit(f"`{msg}`")
                return False
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await check_progress_for_dl(aria2, gid, event, previous_message)
        else:
            await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
            await event.edit(f"Downloaded Successfully: `{file.name}` 🤒")
            return True
    except aria2p.client.ClientException:
        pass
    except MessageNotModified:
        pass
    except RecursionError:
        file.remove(force=True)
        await event.edit(
            "Download Auto Canceled :\n\n"
            "Your Torrent/Link is Dead.".format(
                file.name
            )
        )
        return False
    except Exception as e:
        LOGGER.info(str(e))
        if " not found" in str(e) or "'file'" in str(e):
            await event.edit("Download Canceled :\n<code>{}</code>".format(file.name))
            return False
        else:
            LOGGER.info(str(e))
            await event.edit("<u>error</u> :\n<code>{}</code> \n\n#error".format(str(e)))
            return False
# https://github.com/jaskaranSM/UniBorg/blob/6d35cf452bce1204613929d4da7530058785b6b1/stdplugins/aria.py#L136-L164


async def check_metadata(aria2, gid):
    file = aria2.get_download(gid)
    LOGGER.info(file)
    if not file.followed_by_ids:
        # https://t.me/c/1213160642/496
        return None
    new_gid = file.followed_by_ids[0]
    LOGGER.info("Changing GID " + gid + " to " + new_gid)
    return new_gid
