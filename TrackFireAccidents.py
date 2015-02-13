#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.

Usage
-----
lk_track.py [<video_source>]


Keys
----
ESC - exit
'''

import numpy as np
import cv2
import video
from common import anorm2, draw_str
import uuid
import random

from time import clock

lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 300,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

class App:
    def __init__(self, video_src):
        self.track_len = 1000
        self.detect_interval = 5
        self.tracks = []
        self.cam = video.create_capture(video_src)
        self.frame_idx = 0

    def run(self):
        while True:
            ret, frame = self.cam.read()
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            vis = frame.copy()

            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)

                d = abs(p0-p0r).reshape(-1, 2).max(-1)

                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    #if len(tr) > self.track_len:
                        #del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
                self.tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))
                checkFlag = 0
                for tr in self.tracks:
                    print "******************************************************"
                    #print np.int32(tr)
                    #print "******************************************************"
                    count = 0

                    print "length is", len(tr)
                    print tr[len(tr)-1][0], int(tr[0][0])-5,int(tr[0][0])+5, "<<<<<<<<<<<<<<<<<<<<<<<<<<"
                    print tr[len(tr)-1][1], int(tr[0][1])-5,int(tr[0][1])+5, ">>>>>>>>>>>>>>>>>>>>>>>>>>"
                    if int(tr[len(tr)-1][0]) not in range(int(tr[0][0])-5,int(tr[0][0])+5) and int(tr[len(tr)-1][1]) not in range(int(tr[0][1])-5,int(tr[0][1])+5):
                        #print "values::::::::::", self.poi.get(int(tr[0][0]))
                    #    if int(tr[0][0]) not in self.poi.keys():
                    #        self.poi[int(tr[0][0])]=[]
                        print int(tr[len(tr)-1][0])

                        self.poi[int(tr[0][0])] = int(tr[len(tr)-1][0]),int(tr[len(tr)-1][1])


                        for h in self.poi.values():
                            print "!#@!#@#@#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@", h, int(tr[len(tr)-1][0]),int(tr[len(tr)-1][1])
                            print "values length", len(self.poi.values())
                            if h[0] == int(tr[len(tr)-1][0]) and h[1] == int(tr[len(tr)-1][1]) and len(self.poi.values())>20:
                                checkFlag = checkFlag+1
                                print "apoi length", len(self.apoi)
                                self.apoi=(h[0],h[1])
                                print "apoooooooooooooiiiiiiiiiiii", self.apoi
                            print "no. of circles is", checkFlag


                        if checkFlag > 15:

                            #print "Danger!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
                            cv2.circle(vis,self.apoi, 30, (0,0,255), 1)
                            #apoi=""

                        print "moving object detected", tr
                        print "&&&&&&&&&&&&&&&&&", self.poi.values()
#                        print int(tr[len(tr)-1][0]),int(tr[len(tr)-1][1])

                   # for value in self.poi.values():
                   #     cv2.circle(vis,(value[0],value[1]), 20, (0,0,255), 1)

            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])

            self.frame_idx += 1
            self.prev_gray = frame_gray
            cv2.imshow('Video Surveillance', vis)

            ch = 0xFF & cv2.waitKey(1)

            if ch == 27:
                break

def main():
    import sys
    try: video_src = 'samples/CarCrashComp.mp4'
    except: video_src = 0

    print __doc__
    App(video_src).run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
