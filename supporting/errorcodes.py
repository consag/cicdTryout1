##
# Errorcodes
# @Since: 22-MAR-2019
# @Author: Jac. Beekers
# @Version: 20190322.0 - JBE - Initial

import logging
import supporting.errorcode as err

# Returncode, ErrorCode, ErrorMessage, Resolution, Area, Severity

OK=err.Errorcode(0,'0','No errors encounterued.','No action needed.','Result',logging.INFO)
##
# General errors, mostly related to environment and/or privileges
LOGDIR_NOTSET=err.Errorcode(1,'ENV-0001','LOGDIR not defined','Set the environment variable','Environment',logging.FATAL)
LOGDIR_NF=err.Errorcode(1,'ENV-0002','LOGDIR not found','Set the environment variable to an existing directory','Environment',logging.FATAL)
LOGDIR_NW=err.Errorcode(1,'ENV-0003','Cannot write to LOGDIR','Set the environment variable to a writeable directory','Environment',logging.FATAL)
FILE_NF=err.Errorcode(1,'ENV-0004', 'Cannot find file','Check the file\'s path and permissions','Environment', logging.ERROR)
FILE_NW=err.Errorcode(1,'ENV-0005', 'Cannot write to file','Check the file\'s path and permissions','Environment', logging.ERROR)
##
# General build-deploy related errors. Return code is 2
DEPLOYLIST_NF=err.Errorcode(2,'GENDEPLOY-0001','Deploylist not found','Check config directory and file name.','DatabaseArtifact',logging.FATAL)

# Database artifact errors. Return code will be 10
NO_DEPLOYLIST=err.Errorcode(10,'DBDEPLOY-0001','No dbdeploylist defined','Set the environment variable','DatabaseArtifact',logging.FATAL)
SOURCESQLDIR_NOTSET=err.Errorcode(10,'DBDEPLOY-0002','SourceSqlDir is not defined', 'Set the environment variable','DatabaseArtifact', logging.ERROR)
TARGETSQLDIR_NOTSET=err.Errorcode(10,'DBDEPLOY-0003','TargetSqlDir is not defined', 'Set the environment variable','DatabaseArtifact', logging.ERROR)
SQLFILE_NF=err.Errorcode(10,'DBDEPLOY-0004','SQL file not found', 'Check the deploy file content','DatabaseArtifact', logging.ERROR)

# Informatica artifact errors. Return code will be 20
NOT_IMPLEMENTED=err.Errorcode(20,'INFADEPLOY-0001','Result unknown. Function may not have been implemented completely','Ask your developer to implement the logic completely.','InformaticaArtifact',logging.WARNING)
INFACMD_FAILED=err.Errorcode(20,'INFADEPLOY-0002','infacmd command failed.','Check the log and/or ask your administrator.','InformaticaArtifact',logging.ERROR)