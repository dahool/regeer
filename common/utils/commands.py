"""
This code is extracted from transifex project (http://www.transifex.org/)
Although I added some methods

"""
import os
#import subprocess
import popen2

def get_command_output(cmd):
    
    if os.name == "posix":
        dout, din = popen2.popen2('{ ' + cmd + '; } 2>&1')
    else:
        dout, din = popen2.popen2(cmd + ' 2>&1')
    res = dout.readlines()
    dout.close()
    din.close()
    return res

def python_to_args(**kwargs):
    """
    Converts python function arguments to command line arguments for
    use with subprocess module.

    python_to_args(baz=value, bar=True, q=True, f='foo')

    Returns:
        [   "-q", "-ffoo",
            "--bar", "--baz=value",
            "bar","buzz" ]
    """
    kwarglist = []
    for k,v in kwargs.iteritems():
        if len(k) > 1:
            k = k.replace('_','-')
            if v is True:
                kwarglist.append("--%s" % k)
            elif v is not None and type(v) is not bool:
                kwarglist.append("--%s=%s" % (k,v))
        else:
            if v is True:
                kwarglist.append("-%s" % k)
            elif v is not None and type(v) is not bool:
                kwarglist.append("-%s" % k)
                kwarglist.append(str(v))
    return kwarglist

class CommandError(Exception):
    def __init__(self, command, status, stderr=None):
        self.stderr = stderr
        self.status = status
        self.command = command

    def __str__(self):
        return repr("%s returned exit status %d" %
                    (str(self.command), self.status))

def run_command(command, *args, **kw):
    """
    Handles executing the command on the shell and consumes and returns
    the returned information (stdout)

    ``command``
        The command argument list to execute

    ``cwd``
        Use cwd as the working dir.

    ``with_extended_output``
        Whether to return a (status, stdout, stderr) tuple.

    ``with_exceptions``
        Whether to raise an exception when command returns a non-zero status.

    ``with_raw_output``
        Whether to avoid stripping off trailing whitespace.

    ``convert_args``
        Converts python arguments to command line arguments.

    Returns
        str(output)                     # extended_output = False (Default)
        tuple(int(status), str(stdout), str(stderr)) # extended_output = True
    """
    _input= kw.pop('_input', None)
    cwd = kw.pop('cwd', os.getcwd())

    with_extended_output = kw.pop('with_extended_output', False)
    with_exceptions = kw.pop('with_exceptions', True)
    with_raw_output = kw.pop('with_raw_output', False)

    # if command is a string split to a list
    if isinstance(command, basestring):
        command = command.split()

    # if more kwargs are given, convert them to command line args
    if kw:
        kwarglist = python_to_args(**kw)
    else:
        kwarglist = []
    command += kwarglist + list(args)

    # If stdin is a string, create a pipe so we can write the contents
    if _input:
        stdin = subprocess.PIPE
    else:
        stdin = None

    # Start the process
    os.chdir(cwd)
    return get_command_output(' '.join(command))
#    proc = subprocess.Popen(command,
#                            cwd=cwd,
#                            stdin=stdin,
#                            stderr=subprocess.PIPE,
#                            stdout=subprocess.PIPE,
#                            shell=True)

    # Write the contents to the pipe
#    if _input:
#        proc.stdin.write(_input)
#
#    # Wait for the process to return
#    stdout_value, stderr_value = proc.communicate()
#    status = proc.returncode
#
#    # Strip off trailing whitespace by default
#    if not with_raw_output:
#        stdout_value = stdout_value.rstrip()
#        stderr_value = stderr_value.rstrip()
#
#    if with_exceptions and status != 0:
#        raise CommandError(command, status, stderr_value)
#
#    # Allow access to the command's status code
#    if with_extended_output:
#        return (status, stdout_value, stderr_value)
#    else:
#        return stdout_value