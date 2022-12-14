# Licensed to the .NET Foundation under one or more agreements.
# The .NET Foundation licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information.


import sys, os
#from iptest.util import get_env_var, get_temp_dir

#------------------------------------------------------------------------------

#--IronPython or something else?
is_cli =         sys.platform == 'cli'
is_ironpython =  is_cli
is_cpython    =  not is_ironpython
is_posix      =  sys.platform == 'posix'
is_osx        =  sys.platform == 'darwin'
is_netcoreapp =  False
is_netcoreapp21 = False
is_netcoreapp31 = False
is_mono = False

if is_ironpython:
    #We'll use System, if available, to figure out more info on the test
    #environment later
    import System
    import clr
    is_netcoreapp = clr.IsNetCoreApp
    is_netcoreapp21 = clr.FrameworkDescription.startswith(".NET Core 2.x")
    is_netcoreapp31 = clr.FrameworkDescription.startswith(".NET Core 3.1")
    is_net50 = clr.FrameworkDescription.startswith(".NET 5.0")
    is_net60 = clr.FrameworkDescription.startswith(".NET 6.0")
    if is_netcoreapp: clr.AddReference("System.Runtime.Extensions")
    is_posix = sys.platform == 'posix' or System.Environment.OSVersion.Platform == System.PlatformID.Unix
    is_osx = os.path.exists('/System/Library/CoreServices/SystemVersion.plist')
    is_mono = clr.IsMono

#--The bittedness of the Python implementation
is_cli32, is_cli64 = False, False
if is_ironpython: 
    is_cli32, is_cli64 = (System.IntPtr.Size == 4), (System.IntPtr.Size == 8)

is_32, is_64 = is_cli32, is_cli64
if not is_ironpython:
    cpu = os.environ["PROCESSOR_ARCHITECTURE"]
    if cpu.lower()=="x86":
        is_32 = True
    elif cpu.lower()=="amd64":
        is_64 = True
    

#--CLR version we're running on (if any)

is_net40 = False
is_net45 = False
is_net45Or46 = False
is_net46 = False
if is_cli:
    version = System.Environment.Version
    is_net40 = version.Major == 4
    is_net45 = is_net40 and version.Minor == 0 and version.Build == 30319 and version.Revision < 42000
    is_net45Or46 = is_net40 and version.Minor == 0 and version.Build == 30319
    is_net46 = is_net40 and version.Minor == 0 and version.Build == 30319 and version.Revision == 42000 

#--Newlines
if is_ironpython:
    newline = System.Environment.NewLine
else:
    import os
    newline = os.linesep

#--Build flavor of Python being tested
is_debug = False
if is_cli:
    is_debug = clr.IsDebug

#--Are we using peverify to check that all IL generated is valid?
is_peverify_run = False
if is_cli:
    is_peverify_run = is_debug and "-X:SaveAssemblies" in System.Environment.CommandLine    

#--We only run certain time consuming test cases in the stress lab
is_stress = False
# if get_env_var("THISISSTRESS")!=None: 
#     is_stress = True

#------------------------------------------------------------------------------
