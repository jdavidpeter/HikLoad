import os
import xml.dom.minidom as minidom
from xml.etree import ElementTree
import subprocess
import xmltodict
import ffmpeg
from config import getConfig


def getXmlString(elem):
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


def findRec(node, element, result):
    for item in node.getChildren():
        result.append(item)
        findRec(item, element, result)
    return result


def downloadRTSP(url, name="", camera=""):
    """Downloads an RTSP livestream to a specific location.
    name, camera are optional
    """
    if(name != None and camera != None):
        if exists(name, camera) is True:
            return
    else:
        name = url
        camera = ""
    print("Trying to download from: " + url)
    stream = ffmpeg.output(ffmpeg.input(url), camera + name + ".mp4", reorder_queue_size="0",
                           timeout=0, stimeout=100, rtsp_flags="listen", rtsp_transport="tcp")
    ffmpeg.run(stream, capture_stdout=False, capture_stderr=False)


def chdir(newpath):
    """Changes current directory to downloadPath"""
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    os.chdir(newpath)


def exists(name, camera):
    """Returns true if file already exists"""
    f = camera + name + ".mp4"
    if os.path.isfile(f):
        return True
    return False


def getList(response):
    """Returns a list of [url, name, camera] from a response"""
    obj = xmltodict.parse(getXmlString(response))
    ret = []
    try:
        for i in obj["ns0:CMSearchResult"]["ns0:matchList"]["ns0:searchMatchItem"]:
            url = i["ns0:mediaSegmentDescriptor"]["ns0:playbackURI"].replace(
                "rtsp://", "rtsp://" + getConfig('user') + ":" + getConfig(
                    "password") + "@")
            camera = url.split('/')[5]
            arguments = url.split('?')[1]
            name = arguments.split('&')[2]
            name = name.replace("name=", "")
            ret.append([url, name, camera])
    except:
        print("Could not get a list of videos from the server.")
        print("Maybe the server is down or maybe the user/password is incorrect?")
    return ret
