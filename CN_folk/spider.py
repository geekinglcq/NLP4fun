# -*- coding:utf-8 -*-

import re
import os
import json
import time
import binascii
import codecs

from http.cookiejar import LWPCookieJar
from bs4 import BeautifulSoup
import requests

default_timeout = 10


class Spider(object):

    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'  # NOQA
        }
        self.cookies = {'appver': '1.5.2'}
        self.playlist_class_dict = {}
        self.session = requests.Session()


    def httpRequest(self,
                    method,
                    action,
                    query=None,
                    urlencoded=None,
                    callback=None,
                    timeout=None):
        connection = json.loads(
            self.rawHttpRequest(method, action, query, urlencoded, callback, timeout)
        )
        return connection

    def rawHttpRequest(self,
                       method,
                       action,
                       query=None,
                       urlencoded=None,
                       callback=None,
                       timeout=None):
        if method == 'GET':
            url = action if query is None else action + '?' + query
            connection = self.session.get(url,
                                          headers=self.header,
                                          timeout=default_timeout)

        elif method == 'POST':
            connection = self.session.post(action,
                                           data=query,
                                           headers=self.header,
                                           timeout=default_timeout)

        connection.encoding = 'UTF-8'
        return connection.text

    # get playlist detail 
    def playlist_detail(self, playlist_id):
        action = 'http://music.163.com/api/playlist/detail?id={}'.format(
            playlist_id)
        try:
            data = self.httpRequest('GET', action)
            return data['result']['tracks']
        except requests.exceptions.RequestException as e:
            print(e)
            return []

   
    # get the top-50 songs of the artists
    def artists(self, artist_id):
        action = 'http://music.163.com/api/artist/{}'.format(artist_id)
        try:
            data = self.httpRequest('GET', action)
            return data['hotSongs']
        except requests.exceptions.RequestException as e:
            print(e)
            return []

    # get the comments of the song
    def song_comments(self, music_id, offset=0, total='fasle', limit=100):
        action = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}/?rid=R_SO_4_{}&\
            offset={}&total={}&limit={}'.format(music_id, music_id, offset, total, limit)
        try:
            comments = self.httpRequest('GET', action)
            return comments
        except requests.exceptions.RequestException as e:
            print(e)
            return []

    # get the lyric of the song
    def song_lyric(self, music_id):
        action = 'http://music.163.com/api/song/lyric?os=osx&id={}&lv=-1&kv=-1&tv=-1'.format(  # NOQA
            music_id)
        try:
            data = self.httpRequest('GET', action)
            if 'lrc' in data and data['lrc']['lyric'] is not None:
                lyric_info = data['lrc']['lyric']
            else:
                lyric_info = '未找到歌词'
            return lyric_info
        except requests.exceptions.RequestException as e:
            print(e)
            return []
    
    def download_lyric_comments_of_playlist(self, playlist_id):
        playlist_detail = self.playlist_detail(playlist_id)
        songids = list()
        id2name = {}
        for i in playlist_detail:
            songids.append(i['id'])
            id2name[i['id']] = i['name']
        os.mkdir('%s'%(playlist_id))
        print(len(songids))
        lf = codecs.open('%s/lyrics.txt'%(playlist_id),'w','utf-8')
        cf = codecs.open('%s/comments.txt'%(playlist_id),'w','utf-8')
        for song in songids:
            print('handling the song-"%s"'%(id2name[song]))
            lyric = self.song_lyric(song)
            lf.write(lyric)
            comments = self.song_comments(song)
            for comment in comments['hotComments']:
                cf.write(comment['content']+'\n')
        lf.close()
        cf.close()

if __name__ == '__main__':
    sp = Spider()
    sp.download_lyric_comments_of_playlist(10139384)
    sp.download_lyric_comments_of_playlist(86682746)    

        