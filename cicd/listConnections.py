#  MIT License
#
#  Copyright (c) 2019 Jac. Beekers
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

#  MIT License
#
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#
#

import logging, datetime, supporting
from supporting import errorcodes
from cicd.informatica import infaSettings
from cicd.informatica import infaConstants
from supporting import generalSettings
from cicd.informatica import manageConnection
import sys, argparse

now = datetime.datetime.now()
result = errorcodes.OK


def parse_the_arguments(argv):
    """Parses the provided arguments and exits on an error.
    Use the option -h on the command line to get an overview of the required and optional arguments.
     """
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outputfile", required=False, action="store", dest="output_file",
                        help="File the connections should be written to. Default value is >" + infaConstants.DEFAULT_CONNECTIONSFILE + "<.")
    args = parser.parse_args()

    if args.output_file is None:
        args.output_file = infaConstants.DEFAULT_CONNECTIONSFILE

    return args


def main(argv):
    """List the connections as available in the Informatica domain.
    Usage: listConnections.py [-h] [-o OUTPUT_FILE]
    If no output file is provided, the default will be taken from infaConstants.DEFAULT_CONNECTIONSFILE
    """
    thisproc = "MAIN"
    mainProc = 'listConnections'

    resultlogger = supporting.configurelogger(mainProc)
    logger = logging.getLogger(mainProc)

    args = parse_the_arguments(argv)

    generalSettings.getenvvars()

    supporting.log(logger, logging.DEBUG, thisproc, 'Started')
    supporting.log(logger, logging.DEBUG, thisproc, 'logDir is >' + generalSettings.logDir + "<.")

    output_file = args.output_file

    infaSettings.getinfaenvvars()
    infaSettings.outinfaenvvars()

    connection = manageConnection.ManageConnection(Tool="ListConnections",
                                                   Domain=infaSettings.sourceDomain,
                                                   OnError=errorcodes.INFACMD_LIST_CONN_FAILED,
                                                   OutputFile=output_file
                                                   )
    result = manageConnection.ManageConnection.manage(connection)
    if result.rc == errorcodes.OK.rc:
        result = connection.parseConnectionListOutput(output_file)
        if result.rc == errorcodes.OK.rc:
            result = connection.writeConnectionList(output_file)
        else:
            supporting.log(logger, logging.DEBUG, thisproc,
                           'parseConnectionListOutput completed with return code >' + str(result.rc)
                           + '< and result code >' + result.code + "<.")
    else:
        with open(output_file, 'r') as f:
            for line in f:
                result.message += line.rstrip()

    supporting.log(logger, logging.DEBUG, thisproc, 'Completed with return code >' + str(result.rc)
                   + '< and result code >' + result.code + "<.")
    supporting.exitscript(resultlogger, result)


if __name__ == '__main__':
    main(sys.argv[1:])
