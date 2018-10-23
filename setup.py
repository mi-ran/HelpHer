import cx_Freeze

exe = [cx_Freeze.Executable("main.py")] 
  
cx_Freeze.setup( name = "search", version = "1.0", options = {"build_exe": {"packages": ["errno", "os", "re", "stat", "subprocess","collections", "pprint","shutil", "humanize","pycallgraph"], "include_files": []}}, executables = exe ) 
