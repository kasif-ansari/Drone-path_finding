#!/usr/bin/python3
#
#  Copyright (C) 1997-2016 JDE Developers Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see http://www.gnu.org/licenses/.
#  Authors :
#       Aitor Martinez Fernandez <aitor.martinez.fernandez@gmail.com>
#       Francisco Miguel Rivas Montero <franciscomiguel.rivas@urjc.es>
#  Rosified by:
#       Francisco Perez Salgado <f.perez475@gmail.com>
#


# General imports
import sys


# Practice imports
from MyAlgorithm import MyAlgorithm
from interfaces.camera import ListenerCamera
from interfaces.motors import PublisherMotors

if __name__ == "__main__":

    camera = ListenerCamera("/depth_camera/rgb/image_raw")
    motors = PublisherMotors("/F1ROS/cmd_vel", 4, 0.3)
    algorithm=MyAlgorithm(camera, motors)
   
    algorithm.run()
    time.sleep(0.07)
    arr=algorithm.getcoordinates()
    print(arr[-1])