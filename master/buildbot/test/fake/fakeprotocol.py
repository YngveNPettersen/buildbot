# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from buildbot.buildslave.protocols import base
from twisted.internet import defer


class FakeConnection(base.Connection):

    def __init__(self, master, buildslave):
        base.Connection.__init__(self, master, buildslave)
        self._connected = True
        self.remoteCalls = []
        self.builders = {}  # { name : isBusy }

        # users of the fake can add to this as desired
        self.info = {
            'slave_commands': [],
            'version': '0.8.2',
            'basedir': '/sl',
            'system': 'nt',
        }

    def remotePrint(self, message):
        self.remoteCalls.append(('remotePrint', message))
        return defer.succeed(None)

    def remoteGetSlaveInfo(self):
        self.remoteCalls.append(('remoteGetSlaveInfo',))
        return defer.succeed(self.slaveInfo)

    def remoteSetBuilderList(self, builders):
        self.remoteCalls.append(('remoteSetBuilderList', builders[:]))
        self.builders = dict((b, False) for b in builders)
        return defer.succeed(None)

    def remoteStartCommand(self, remoteCommand, builderName, commandId, commandName, args):
        self.remoteCalls.append(('remoteStartCommand', remoteCommand, builderName,
                                 commandId, commandName, args))
        return defer.succeed(None)

    def remoteShutdown(self):
        self.remoteCalls.append(('remoteShutdown',))
        return defer.succeed(None)

    def remoteStartBuild(self, builderName):
        self.remoteCalls.append(('remoteStartBuild', builderName))
        return defer.succeed(None)

    def remoteInterruptCommand(self, builderName, commandId, why):
        self.remoteCalls.append(('remoteInterruptCommand', builderName, commandId, why))
        return defer.succeed(None)
