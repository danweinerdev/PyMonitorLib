import fcntl
import grp
import os
import platform
import pwd
import select
import subprocess


def CloseDescriptor(fd):
    """
    Close a given descriptor. If the object has its own 'close' method that
    will be used otherwise everything will be passed to 'os.close'.

    :param fd: File descriptor or 'closeable' object.
    :return: None
    """
    try:
        if hasattr(fd, 'close'):
            fd.close()
        else:
            os.close(fd)
    except (IOError, OSError):
        pass


def Command(command, stderr=True, cwd=None):
    """
    Execute an external command with the given working directory. The result will
    be the STDOUT data and the return code. If 'stderr' is set to true the STDERR
    output will be piped to STDOUT otherwise it will be ignored.

    :param command: Command parameters to execute.
    :param stderr: Boolean indicating whether STDERR should be piped to STDOUT.
    :param cwd: Current working directory.
    :return: Tuple of process exitcode and STDOUT data.
    """
    process = None
    output = []
    try:
        process = subprocess.Popen(command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT if stderr else os.devnull,
            bufsize=1)

        while True:
            if process.poll() is not None:
                break
            for line in iter(process.stdout.readline, b''):
                if len(line.strip()) > 0:
                    output.append(line.strip())
    except KeyboardInterrupt:
        pass
    except OSError:
        raise

    return process.poll(), output


def GetGroupId(group):
    """
    On a Linux system attempt to get the GID value for a give 'group'. This uses
    a system call to obtain this data.

    :param group: Group name to lookup.
    :return: GID value if the group is found, otherwise None
    """
    if isinstance(group, int):
        return group
    if platform.system() != 'Linux':
        raise RuntimeError('GID lookup not support outside of Linux')
    try:
        return grp.getgrnam(group).gr_gid
    except KeyError:
        return None


def GetUserId(user):
    """
    On a Linux system attempt to get the UID value for a give 'user'. This uses
    a system call to obtain this data.

    :param user: User name to lookup.
    :return: UID value if the user is found, otherwise None
    """
    if isinstance(user, int):
        return user
    if platform.system() != 'Linux':
        raise RuntimeError('UID lookup not support outside of Linux')
    try:
        return pwd.getpwnam(user).pw_uid
    except KeyError:
        return None


def RedirectStream(source, target=None):
    """
    Redirect a source file descriptor to a new target file descriptor. If no target
    is specified the source will be redirected to the /dev/null object.

    :param source: Source file descriptor
    :param target: Target file descriptor. If None is provided /dev/null is used.
    :return: None
    """
    if target is None:
        target = os.open(os.devnull, os.O_RDWR)
    else:
        target = target.fileno()
    os.dup2(target, source.fileno())


def Select(rds, wrts, timeout, logger=None):
    """
    Select on the given sockets for events at the given timeout period. This is a wrapper
    around the system call select for handling a set of file descriptors. The function will
    return None in the event of a failure of the resulting list of descriptors which an
    event occurred on.

    :param rds: Set of reader descriptors.
    :param wrts: Set of writer descriptors.
    :param timeout: Timeout value to wait for an event.
    :param logger: Optional logger instance in the event of errors.
    :return: None if a failure occurred, or the descriptors which an event occurred.
    """
    if not isinstance(rds, list):
        rds = [rds]
    if not isinstance(wrts, list):
        wrts = [wrts]

    try:
        res = select.select(rds, wrts, [], float(timeout))
    except select.error as e:
        if logger:
            logger.error('Select error: {}'.format(e))
        return None
    except os.error as e:
        if logger:
            logger.error('OSError: [{}] {}'.format(e.errno, os.strerror(e.errno)))
        return None
    except KeyboardInterrupt:
        return []

    return res


def SetNonBlocking(fd):
    """
    Set file descriptors to non-blocking.

    :param fd: File descriptor object
    :return: None
    """
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)


def SetProcessOwner(user, group, logger=None):
    """
    Set the given user and group as the process owner. The current process owner
    must have access to set the new user/group combination. This is usually only
    used in the event root needs to drop privileges to a non-privileged user after
    a fork has occurred.

    :param user: Integer representing the new user owner.
    :param group: Integer representing the new group owner.
    :param logger: Optional logger instance in the event of errors.
    :return: None
    """
    try:
        if user is not None:
            os.setuid(user)
    except OSError as e:
        if logger:
            logger.error("Failed to set process user '{}': [{}] {}".format(
                user, e.errno, os.strerror(e.errno)))
    try:
        if group is not None:
            os.setgid(group)
    except OSError as e:
        if logger:
            logger.error("Failed to set process group '{}': [{}] {}".format(
                group, e.errno, os.strerror(e.errno)))


def SetProcessUmask(umask, logger=None):
    """
    Set the process umask.

    :param umask: Selected umask.
    :param logger: Optional logger instance in the event of errors.
    :return: None
    """
    try:
        os.umask(umask)
    except OSError as e:
        if logger:
            logger.error('Failed to set umask: [{}] {}'.format(
                e.errno, os.strerror(e.errno)))
