# Configure docplex to use a local solver
import os
import shutil
import sys
from docplex.cp.config import set_default, LOCAL_CONTEXT

DEFAULT_STUDENT_PARAMETERS = {
    'Presolve': 'Off',
    'Workers': 1
}

CPOPTIMIZER_EXEC = "cpoptimizer"
INSA_CPOPTIMIZER_PATH = \
  '/Applications/BigData/CPLEX_Studio129/cpoptimizer/bin/x86-64_osx'


def setup(**kargs):
    # Default parameters for students:
    for k, v in DEFAULT_STUDENT_PARAMETERS.items():
        kargs.setdefault(k, v)

    # Update log output (does not work... )
    LOCAL_CONTEXT['log_output'] = sys.stdout

    # Set default parameters
    LOCAL_CONTEXT['params'].update(**kargs)

    # Switch to local context
    set_default(LOCAL_CONTEXT)
    if not shutil.which(CPOPTIMIZER_EXEC):
        #If you work on your local machine, change this line
        #if sys.platform == 'darwin':  # OS X Mo, temporaire
        #    os.environ['PATH'] += \
        #      ':/Users/msiala/Applications/CPLEX_Studio129/cpoptimizer/bin/x86-64_osx'
        #else:
        os.environ['PATH'] += ':' + INSA_CPOPTIMIZER_PATH
