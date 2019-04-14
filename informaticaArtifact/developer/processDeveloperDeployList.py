"""
    Process deploy list for database artifacts
    @Since: 23-MAR-2019
    @Author: Jac. Beekers
    @Version: 20190324.0 - JBE - Initial
"""

import supporting.errorcodes as err
import supporting, logging
import informaticaArtifact.developer as developer
import informaticaArtifact
import supporting.errorcodes as errorcodes
import supporting.deploylist
import informaticaArtifact.infaSettings as infaSettings
import supporting.generalSettings as generalSettings
from supporting.generalSettings import completePath

logger = logging.getLogger(__name__)
entrynr =0

def processList(deployFile):
    thisproc = "processList"
    latestResult = err.OK
    supporting.log(logger, logging.DEBUG, thisproc, "deployfile is >" + deployFile +"<.")
    result, deployItems = supporting.deploylist.getWorkitemList(deployFile)
    if result.rc == 0:
        for deployEntry in deployItems:
            latestResult = processEntry(deployEntry)
        return latestResult
    else:
        supporting.log(logger, logging.ERROR, thisproc, "Could not get deploylist")
        return errorcodes.FILE_NF

def processEntry(deployEntry):
    thisproc = "processEntry"
    result = err.OK
    supporting.log(logger, logging.DEBUG, thisproc, "Started to work on deploy entry >" + deployEntry + "<.")

    parts = deployEntry.split(':')
    if not len(parts) == 2 and not len(parts) == 4:
        supporting.log(logger, logging.DEBUG, thisproc, "Insufficient entries found. Expected 2 or 4, got >" + str(len(parts)) +"<.")

    type = parts[0]
    object = parts[1]
    if len(parts) == 4:
        exportcontrol = completePath(generalSettings.configDir + "/" + parts[2], generalSettings.sourceDir)
        importcontrol = completePath(generalSettings.configDir + "/" + parts[3], generalSettings.sourceDir)

    supporting.log(logger, logging.DEBUG, thisproc, 'Type is >' + type + '< and object is >' + object + '<')
    if type == 'PROJECT':
        result = developer.export_infadeveloper(
            Domain=infaSettings.sourceDomain,
            Repository=infaSettings.sourceModelRepository,
            Project=object,
            FilePath=generalSettings.artifactDir + "/" + object +".xml",
            OverwriteExportFile=infaSettings.overwriteExportFile,
            ExportRefData=infaSettings.sourceExportRefData
        )
    elif type == 'CONTROLFILE':
        result = developer.export_infadeveloper(
            Domain = infaSettings.sourceDomain,
            Repository = infaSettings.sourceModelRepository,
            Project=object,
            FilePath=generalSettings.artifactDir + "/" + object +".xml",
            OverwriteExportFile = infaSettings.overwriteExportFile,
            ControlFilePath = exportcontrol
        )
    else:
        result = errorcodes.NOT_IMPLEMENTED

    supporting.log(logger, logging.DEBUG, thisproc,
                   "Completed with rc >" + str(result.rc) + "< and code >" + result.code + "<.")
    return result
