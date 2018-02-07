import paramiko
import socket
import getpass
from . import easySSHScript
from inspect import getfile as libpath
from time import sleep as wait
from os import remove as __remove__
from random import randint as __random__


class EasySSHPythonElement:

    # Constant

    __type_usable = dict(int=int, float=float, complex=complex, bool=bool, bytes=bytes, str=str,
                         list=list, tuple=tuple, dict=dict, set=set)

    # Basic Setting

    def __init__(self, python, parent, point: str):
        super.__setattr__(self, '_EasySSHPythonElement__python', python)
        super.__setattr__(self, '_EasySSHPythonElement__parent', parent)
        super.__setattr__(self, '_EasySSHPythonElement__point', point)
        super.__setattr__(self, '_EasySSHPythonElement__default', ['_EasySSHPythonElement__python',
                                                                   '_EasySSHPythonElement__parent',
                                                                   '_EasySSHPythonElement__point',
                                                                   '_EasySSHPythonElement__default'])

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        return EasySSHPythonElement(self.__python, self.__addr__, item)

    def __setattr__(self, key, value):
        if key in self.__default:
            return super.__setattr__(self.__python, key, value)

        command = '%s = %s' % (self.__to__(key), EasySSHPython.__ele2str__(value))
        self.__python.__command__(command)

        return EasySSHPythonElement(self.__python, None, key)

    def __delattr__(self, item):
        if item in self.__dict__:
            del self.__dict__[item]
        self.__python.__command__('del %s' % self.__to__(item))

    def __getitem__(self, item):
        return EasySSHPythonElement(self.__python, None, '%s[%s]' % (self.__addr__,
                                                                     EasySSHPython.__ele2str__(item)))

    def __setitem__(self, key, value):
        self.__python.__command__('%s[%s] = %s' % (self.__addr__,
                                                   EasySSHPython.__ele2str__(key),
                                                   EasySSHPython.__ele2str__(value)))

    def __call__(self, *args, **kwargs):
        args_str = ''
        for arg in args:
            args_str = '%s, %s' % (args_str, EasySSHPython.__ele2str__(arg))
        for key, value in kwargs.items():
            args_str = '%s, %s=%s' % (args_str, key, EasySSHPython.__ele2str__(value))
        if len(args_str) != 0:
            args_str = args_str[2:]

        return EasySSHPythonElement(self.__python, None, '%s(%s)' % (self.__addr__, args_str))

    def __between__(self, target, operator: str):
        return EasySSHPythonElement(self.__python, None, '%s %s %s' % (self.__addr__, operator,
                                                                       EasySSHPython.__ele2str__(target)
                                                                       if type(target) is EasySSHPythonElement
                                                                       else target.__repr__()))

    def __put__(self, target, await: bool = False, track: bool = True, seconds=0.001):
        self.__python.__command__(self.__between__(target, operator='='), await=await)
        if not await and track:
            self.__python.__track__(seconds=seconds)
        return self

    def __to__(self, toward: str) -> str:
        return '%s.%s' % (self.__addr__, toward)

    def __type__(self):
        return self.__python.__command__('type(%s)' % self.__addr__, await=True)[8:-2]

    def __cast__(self, vtype: str, value):
        if vtype in self.__type_usable:
            return self.__type_usable[vtype](value)
        return self

    # Usable Function

    def __invert__(self):
        return self.__cast__(self.__type__(), self.__python.__command__(self.__addr__, await=True))

    def __run__(self, track: bool = False, seconds=0.001):
        self.__python.__command__(self.__addr__, await=not track)
        if track:
            self.__python.__track__(seconds=seconds)
        return self

    @property
    def __addr__(self) -> str:
        return ('%s.%s' % (self.__parent, self.__point)) if self.__parent is not None else self.__point

    def __download__(self, path: str = None):
        ssh = self.__python.__ssh__
        lpath = '_download_%d.bin' % __random__(0, 65535)
        path = '%s/%s' % ((ssh.path if path is None else path), lpath)

        self.__python.__command__('%s.__upload__(%s, \'%s\')' % (
            self.__python.__base__, self.__addr__, path))

        sftp = ssh.sftp_open()
        sftp.get(path, lpath)

        data = easySSHScript.__download__(lpath)
        self.__python.__command__('%s.__remove__(\'%s\')' % (self.__python.__base__, path))
        return data

    def __upload__(self, data, path: str = None):
        ssh = self.__python.__ssh__
        lpath = '_download_%d.bin' % __random__(0, 65535)
        path = '%s/%s' % ((ssh.path if path is None else path), lpath)
        easySSHScript.__upload__(data, lpath)

        try:
            sftp = ssh.sftp_open()
            sftp.put(lpath, path)

            self.__python.__command__('%s = %s.__download__(\'%s\')' % (
                self.__addr__, self.__python.__base__, path))
        finally:
            __remove__(lpath)

    # Operator - Not called

    def __add__(self, other):
        return self.__between__(other, operator='+')

    def __sub__(self, other):
        return self.__between__(other, operator='-')

    def __mul__(self, other):
        return self.__between__(other, operator='*')

    def __truediv__(self, other):
        return self.__between__(other, operator='/')

    def __floordiv__(self, other):
        return self.__between__(other, operator='//')

    def __matmul__(self, other):
        return self.__between__(other, operator='@')

    def __mod__(self, other):
        return self.__between__(other, operator='%')

    def __pow__(self, other):
        return self.__between__(other, operator='**')

    def __and__(self, other):
        return self.__between__(other, operator='&')

    def __or__(self, other):
        return self.__between__(other, operator='|')

    def __xor__(self, other):
        return self.__between__(other, operator='^')

    def __lshift__(self, other):
        return self.__between__(other, operator='<<')

    def __rshift__(self, other):
        return self.__between__(other, operator='>>')

    def __lt__(self, other):
        return self.__between__(other, operator='<')

    def __le__(self, other):
        return self.__between__(other, operator='<=')

    def __gt__(self, other):
        return self.__between__(other, operator='>')

    def __ge__(self, other):
        return self.__between__(other, operator='>=')

    def __eq__(self, other):
        return self.__between__(other, operator='==')

    def __ne__(self, other):
        return self.__between__(other, operator='!=')

    def __iter__(self):
        return EasySSHPythonElementIterator(self.__python, self.__addr__)

    # Use __iter__ instead
    # def __next__(self):
    #    pass

    # Operator - Instantly called

    def __abs__(self):
        return abs(~EasySSHPythonElement(self.__python, self.__addr__, '__abs__').__call__())

    def __int__(self):
        return int(~EasySSHPythonElement(self.__python, self.__addr__, '__int__').__call__())

    def __float__(self):
        return float(~EasySSHPythonElement(self.__python, self.__addr__, '__float__').__call__())

    def __complex__(self):
        return complex(~EasySSHPythonElement(self.__python, self.__addr__, '__complex__').__call__())

    def __bool__(self):
        return bool(~EasySSHPythonElement(self.__python, self.__addr__, '__bool__').__call__())

    # Use ~ (__invert__) instead
    # def __str__(self):
    #    return str(~EasySSHPythonElement(self.__python, self.__addr__, '__str__').__call__())

    # def __hash__(self):
    #    return int(~EasySSHPythonElement(self.__python, self.__addr__, '__hash__').__call__())

    def __bytes__(self):
        return bytes(~EasySSHPythonElement(self.__python, self.__addr__, '__bytes__').__call__())

    def __index__(self):
        return int(~EasySSHPythonElement(self.__python, self.__addr__, '__index__').__call__())

    def __len__(self):
        return int(~EasySSHPythonElement(self.__python, self.__addr__, '__len__').__call__())

    def __contains__(self, item):
        return bool(~EasySSHPythonElement(self.__python, self.__addr__, '__contains__').__call__(item))

    def __neg__(self):
        vtype = self.__type__()
        value = ~EasySSHPythonElement(self.__python, self.__addr__, '__neg__').__call__()
        return self.__cast__(vtype, value)

    def __pos__(self):
        vtype = self.__type__()
        value = ~EasySSHPythonElement(self.__python, self.__addr__, '__pos__').__call__()
        return self.__cast__(vtype, value)


class EasySSHPythonElementIterator:

    num_stack = -1

    def __init__(self, python, parent):
        self.__python = python

        if EasySSHPythonElementIterator.num_stack < 0:
            EasySSHPythonElementIterator.num_stack = 0
            self.__python.__iter_stack = []
            self.__python.__iter_value = []

        self.__python.__iter_stack.append(EasySSHPythonElement(python, parent, '__iter__').__call__()).__run__()
        self.__python.__iter_value.append(None).__run__()

        self.__num = EasySSHPythonElementIterator.num_stack
        self.__value = self.__python.__iter_value[self.__num]
        EasySSHPythonElementIterator.num_stack += 1

    def __next__(self):
        msg = self.__python.__command__('_EasySSHPythonElementIterator__iter_value[%d] = '
                                        '_EasySSHPythonElementIterator__iter_stack[%d].__next__()'
                                        % (self.__num, self.__num))
        if msg.startswith('Traceback'):
            raise StopIteration
        return self.__value


class EasySSHPython(EasySSHPythonElement):

    # Basic Setting

    def __init__(self, ssh, session, stdin, track: bool):
        super(EasySSHPython, self).__init__(self, None, '')
        super.__setattr__(self, '_EasySSHPython__ssh', ssh)
        super.__setattr__(self, '_EasySSHPython__base', None)
        super.__setattr__(self, '_EasySSHPython__session', session)
        super.__setattr__(self, '_EasySSHPython__stdin', stdin)
        super.__setattr__(self, '_EasySSHPython__track', track)
        super.__setattr__(self, '_EasySSHPython__prefix', 'python3')
        super.__setattr__(self, '_EasySSHPython__stdout', '')
        super.__setattr__(self, '_EasySSHPython__stdptr', 0)
        super.__setattr__(self, '_EasySSHPython__stdend', False)
        super.__setattr__(self, '_EasySSHPython__default', ['_EasySSHPython__ssh',
                                                            '_EasySSHPython__base',
                                                            '_EasySSHPython__session',
                                                            '_EasySSHPython__stdin',
                                                            '_EasySSHPython__prefix',
                                                            '_EasySSHPython__default',
                                                            '_EasySSHPython__stdout',
                                                            '_EasySSHPython__stdptr',
                                                            '_EasySSHPython__stdend',
                                                            '_EasySSHPython__default'])

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        return EasySSHPythonElement(self, None, item)

    def __setattr__(self, key, value):
        if key in self.__default:
            return super.__setattr__(self, key, value)

        command = '%s = %s' % (key, self.__ele2str__(value))
        self.__command__(command)

        return EasySSHPythonElement(self, None, key)

    def __delattr__(self, item):
        if item in self.__dict__:
            del self.__dict__[item]
        self.__command__('del %s' % item)

    def __read__(self, crawl: bool = False, seconds=0.001) -> str:
        while True:
            self.__stdout += self.__session.recv(4096).decode('utf-8')
            if self.__stdout[-4:] in ('>>> ', '... '):
                self.__stdend = True
                prefix = 0
                if len(self.__stdout) >= self.__stdptr - 2:
                    prefix = self.__stdptr
                self.__stdout = self.__stdout[prefix:-6]
                break
            if self.__stdout.endswith('`9`4\r\n'):
                self.__stdend = True
                prefix = 0
                if len(self.__stdout) >= self.__stdptr - 2:
                    prefix = self.__stdptr
                    #if self.__stdout[:self.__stdptr - 2] == self.__prefix[:self.__stdptr - 2]:
                    #    prefix = self.__stdptr
                self.__stdout = self.__stdout[prefix:-7]
                break
            if not crawl:
                break
            wait(seconds)

        if not self.__stdend:
            return self.__stdout

        stdout = self.__stdout
        self.__stdout = ''

        return stdout

    def __readline__(self):
        try:
            out = None
            if not self.__eof__():
                out = self.__read__(crawl=False)
                len_out = len(out)
                if len_out > self.__stdptr:
                    out = out[self.__stdptr:]
                    self.__stdptr = len_out
                else:
                    out = ''
            return out
        except paramiko.ssh_exception.NoValidConnectionsError:
            return None
        except paramiko.ssh_exception.SSHException:
            return None
        except socket.error:
            return None
        except KeyboardInterrupt:
            self.__del__()
            return None

    def __track__(self, seconds=0.001, break_msg: str = None):
        while True:
            out = self.__readline__()
            if out is None:
                return
            if len(out) > 0:
                print(out, end='')
            if break_msg is not None:
                if break_msg in out:
                    return
            wait(seconds)

    def __eof__(self) -> bool:
        return self.__stdend

    def __bool__(self):
        return self.__session is not None

    @property
    def __ssh__(self):
        return self.__dict__['_EasySSHPython__ssh']

    @property
    def __base__(self) -> str:
        return self.__dict__['_EasySSHPython__base']

    @staticmethod
    def __ele2str__(arg) -> str:
        if type(arg) is EasySSHPythonElement:
            arg = arg.__addr__
        elif type(arg) is list:
            arg = EasySSHPython.__liple__(arg, '[', ']')
        elif type(arg) is tuple:
            arg = EasySSHPython.__liple__(arg, '(', ')')
        elif type(arg) is set:
            arg = EasySSHPython.__liple__(arg, '{', '}')
        elif type(arg) is dict:
            arg = EasySSHPython.__sect__(arg, '{', '}')
        elif type(arg) is str:
            arg = '\'%s\'' % arg
        else:
            arg = str(arg)
        return arg

    @staticmethod
    def __liple__(arg, prefix, suffix) -> str:
        argsum = ''
        for sp in arg:
            argsum = '%s, %s' % (argsum, EasySSHPython.__ele2str__(sp))
        if len(argsum) != 0:
            argsum = argsum[2:]
        return '%s%s%s' % (prefix, argsum, suffix)

    @staticmethod
    def __sect__(arg, prefix, suffix) -> str:
        argsum = ''
        for key, value in arg.items():
            argsum = '%s, %s: %s' % (argsum, EasySSHPython.__ele2str__(key), EasySSHPython.__ele2str__(value))
        if len(argsum) != 0:
            argsum = argsum[2:]
        return '%s%s%s' % (prefix, argsum, suffix)

    def close(self):
        self.__del__()

    def __del__(self):
        if not self:
            return False

        self.__session.close()
        self.__session = None
        self.__stdin = None
        self.__stdout = None
        return True

    # Usable Function

    def __import__(self, import_class: str, import_from: str = None, import_as: str = None):
        command = 'import %s' % import_class
        if import_from is not None:
            command = 'from %s %s' % (import_from, command)
        if import_as is not None:
            command = '%s as %s' % (command, import_as)

        return self.__command__(command)

    def __def__(self, def_name: str, *args, **kwargs):
        command = '%s(' % def_name

        args_str = ''
        for arg in args:
            args_str = '%s, %s' % (args_str, self.__ele2str__(arg))
        for key, value in kwargs.items():
            args_str = '%s, %s=%s' % (args_str, key, self.__ele2str__(value))
        if len(args_str) != 0:
            args_str = args_str[2:]

        return self.__command__('%s%s)' % (command, args_str))

    def __command__(self, command: str, await: bool = True) -> str:
        if not self:
            return str(False)

        try:
            if self.__track:
                print('*' * 16 + ' COM ' + '*' * 16)
                print(command)
            self.__stdend = False
            self.__prefix = '%s\n' % command
            self.__stdptr = len(self.__prefix) + 1
            self.__stdptr += 2 * ((self.__stdptr + 2) // 80)
            if (self.__stdptr + 2) % 82 == 0:
                self.__stdptr += 244
            self.__stdin.write(self.__prefix)
            self.__stdin.flush()
            msg = self.__read__(crawl=True) if await else str(True)
            if self.__track and await:
                if len(msg) > 0:
                    print(msg)
        except paramiko.ssh_exception.NoValidConnectionsError:
            return str(False)
        except paramiko.ssh_exception.SSHException:
            return str(False)
        except socket.error:
            return str(False)
        except KeyboardInterrupt:
            self.__del__()
            return str(False)

        return msg

    def __script__(self, lpath: str, path: str = None):
        ssh = self.__ssh
        name = '_script_%d' % __random__(0, 65535)
        path = '%s/%s.py' % ((ssh.path if path is None else path), name)

        sftp = ssh.sftp_open()
        sftp.put(lpath, path)

        self.__import__(name)
        self.__command__('%s.__remove__(\'%s\')' % (name, path))
        return name


class EasySSH:

    # Basic Setting

    def __init__(self, host: str, username: str, password: str = None, port: int = 22, connect: bool = False):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__port = port

        self.__terminal = None
        self.__sftp = None
        self.__pythons = list()

        self.__is_root = False

        self.__cd = None

        self.__errmsg = None
        self.__stdout = None

        if connect:
            self.connect()

    def __get_password(self):
        return self.__password if self.__password is not None else getpass.getpass('Password: ')

    @staticmethod
    def __path_backward(path: str, prev: int = 0):
        dotting = False

        if len(path) >= 1:
            if path[0] == '/':
                path = path[1:]

        if len(path) >= 1:
            if path[0] == '.':
                dotting = True
                if len(path) >= 2:
                    if path[1] == '.':
                        prev += 1
                        path = path[1:]
                path = path[1:]

        if len(path) >= 1:
            if path[0] == '/':
                path = path[1:]

        return EasySSH.__path_backward(path, prev) if dotting else (path, prev)

    @staticmethod
    def __path_cut(path: str, prev: int):
        arr = path.split('/')[1:-prev]

        path = ''
        for d in arr:
            path = '%s/%s' % (path, d)
        return path

    # Usable Function

    @property
    def errmsg(self) -> str:
        return self.__errmsg

    @property
    def path(self) -> str:
        return self.__cd

    def connect(self):
        if self.__terminal is not None:
            self.__errmsg = '[EasySSH] Already connected'
            return False

        self.__pythons = list()
        self.__is_root = False
        self.__cd = None

        self.__terminal = paramiko.SSHClient()
        self.__terminal.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            self.__terminal.connect(hostname=self.__host,
                                    username=self.__username,
                                    password=self.__get_password(),
                                    port=self.__port,
                                    timeout=5)
        except paramiko.ssh_exception.AuthenticationException:
            self.__errmsg = '[EasySSH] Authentication failed'
            return False
        except socket.error:
            self.__errmsg = '[EasySSH] Socket error'
            return False

        self.cd(('/home/%s' % self.__username) if self.__username != 'root' else '/')
        return True

    def cd(self, path: str):
        self.__cd = self.get_route(path)
        return self.__cd

    def command(self, command: str, sudo: bool = False, read: bool = True):
        sess = self.python(command='%s;echo \'`9`4\' ' % command, sudo=sudo, read=read, contain=False)
        if sess is not None:
            sess.__del__()
            msg = self.__stdout
            if sudo:
                prefix = msg.index('[sudo]')
                suffix = msg.index(':')
                if prefix < suffix:
                    msg = msg[suffix + 4:]
            return msg
        return None,

    def close(self):
        for python in self.__pythons:
            python.__del__()
        self.__pythons = None

        if self.__sftp is not None:
            self.__sftp.close()
            self.__sftp = None

        if self.__terminal is None:
            self.__errmsg = '[EasySSH] Already disconnected'
            return False

        self.__terminal.close()
        self.__terminal = None
        return True

    def python(self, args: str = None, sudo: bool = False, track: bool = False, read: bool = True,
               command: str = 'python3', contain: bool = True):
        if self.__terminal is None:
            self.__errmsg = '[EasySSH] Already disconnected'
            return None
        try:
            session = self.__terminal.get_transport().open_session()
            session.get_pty()

            command = ('%s %s' % (command, args)) if args is not None else command
            if sudo:
                command = 'sudo %s' % command
            if self.__cd is not None:
                command = 'cd %s;%s' % (self.__cd, command)

            session.exec_command(command)
            stdin = session.makefile('wb', -1)
            if sudo:
                stdin.write('%s\n' % self.__get_password())
                stdin.flush()
            python = EasySSHPython(self, session, stdin, track)
            if read:
                self.__stdout = python.__read__(crawl=True)
            if contain:
                self.__pythons.append(python)
                python.__dict__['_EasySSHPython__base'] = python.__script__(libpath(easySSHScript))
        except paramiko.ssh_exception.NoValidConnectionsError:
            self.__errmsg = '[EasySSH] Socket error'
            return None
        except paramiko.ssh_exception.SSHException:
            self.__errmsg = '[EasySSH] SSH error'
            return None
        except socket.error:
            self.__errmsg = '[EasySSH] Socket error'
            return None
        except KeyboardInterrupt:
            self.__errmsg = '[EasySSH] Impulsively disconnected'
            self.close()
            return None

        return python

    def sftp_open(self):
        if self.__sftp is not None:
            self.__errmsg = '[EasySSH] Already connected'
            return self.__sftp
        if self.__terminal is None:
            self.__errmsg = '[EasySSH] Already disconnected'
            return None

        try:
            self.__sftp = self.__terminal.open_sftp()
            return self.__sftp
        except paramiko.SFTP_FAILURE:
            self.__errmsg = '[EasySSH] Connecting failed'
            return None
        except socket.error:
            self.__errmsg = '[EasySSH] Socket error'
            return None

    def sftp_close(self):
        if self.__sftp is None:
            self.__errmsg = '[EasySSH] Already disconnected'
            return None
        if self.__terminal is None:
            self.__errmsg = '[EasySSH] Already disconnected'
            return None

        self.__sftp.close()
        self.__sftp = None

    def get_route(self, path: str = None):
        if path is None:
            return self.__cd

        if path.endswith('/'):
            path = path[:len(path) - 1]

        if path.startswith('/'):
            return path

        if self.__cd is None:
            self.__errmsg = '[EasySSH] Default directory not exists'
            return None

        path, back = self.__path_backward(path)
        cd = self.__path_cut(self.__cd, back) if back > 0 else self.__cd

        return '%s/%s' % (cd, path)
