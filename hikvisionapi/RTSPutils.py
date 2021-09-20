from operator import mod
import ffmpeg
import os
import logging


def downloadRTSP(url: str, videoName: str, seconds: int = 9999999, debug: bool = False, force: bool = False, skipSeconds: bool = 0):
    """Downloads an RTSP livestream from url to videoName.

    Parameters:
        url (str): the RTSP link to a stream
        videoName (str): the filename of the downloaded stream
        seconds (int): the maximum number of seconds that should be recorded (default is 999999)
        debug (bool): Enables debug logging (default is False)
        force (bool): Forces saving of file (default is False)
        skipSeconds (int): the number of seconds that should be skipped when downloading (default is 0)
    """
    logging.info("Starting download from: " + url)
    try:
        if seconds:
            stream = ffmpeg.input(
                url,
                rtsp_transport="tcp",
                stimeout=1,
                t=seconds,
            )
        else:
            stream = ffmpeg.input(
                url,
                rtsp_transport="tcp",
                stimeout=1,
            )
        if skipSeconds:
            stream = ffmpeg.output(
                stream,
                videoName,
                ss=skipSeconds
            )
        else:
            stream = ffmpeg.output(
                stream,
                videoName
            )
    except AttributeError:
        raise Exception(
            "The version of ffmpeg used is wrong! Be sure to uninstall ffmpeg using pip and install ffmpeg-python or use a virtualenv! For more information see the README!")
    if os.path.exists(videoName):
        logging.debug(
            "The file %s exists, should have been downloaded from %s" % (videoName, url))
        if force is False:
            logging.warning("%s already exists" % videoName)
            return
        os.remove(videoName)
    if not debug:
        return ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    return ffmpeg.run(stream, capture_stdout=False, capture_stderr=False)


def downloadRTSPOnlyFrames(url: str, videoName: str, modulo: int, seconds: int = 9999999, debug: bool = False, force: bool = False, skipSeconds: int = 0):
    """Downloads an image for every `modulo` frame from an url and saves it to videoName.

    Parameters:
        url (str): The RTSP link to a stream
        videoName (str): The filename of the downloaded stream
                         should be in the format `{name}_%06d.jpg`
        modulo (int): 
        seconds (int): The maximum number of seconds that should be recorded (default is 9999999)
        debug (bool): Enables debug logging (default is False)
        force (bool): Forces saving of file (default is False)
        skipSeconds (int): The number of seconds that should be skipped when downloading (default is 0)
    """
    if videoName % 1 == videoName % 2:
        raise Exception("videoName cannot be formatted correctly")
    if modulo <= 0:
        raise Exception("modulo is not valid")
    logging.info("Trying to download from %s" % url)
    try:
        stream = ffmpeg.input(
            url,
            rtsp_transport="tcp",
            stimeout=1,
            t=seconds,
        )
        stream = ffmpeg.output(
            stream,
            videoName,
            vf="select=not(mod(n\,%s))" % (modulo),
            vsync="vfr",
            ss=skipSeconds
        )
    except AttributeError:
        raise Exception(
            "The version of ffmpeg used is wrong! Be sure to uninstall ffmpeg using pip and install ffmpeg-python or use a virtualenv! For more information see the README!")
    if os.path.exists(videoName):
        logging.debug(
            "The file %s exists, should have been downloaded from %s" % (videoName, url))
        if force is False:
            logging.warning("%s already exists" % videoName)
            return
        os.remove(videoName)
    if not debug:
        return ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
    return ffmpeg.run(stream, capture_stdout=False, capture_stderr=False)
