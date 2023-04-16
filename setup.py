from cx_Freeze import setup, Executable

build_exe_options = {"packages":["pygame"],"include_files" : ["assets/", "powerups/", "constants.py", "musicplayer.py", "player.py", "render.py", "timer.py", "utils.py", "world_map.py", "level_data.csv", "tutorial_data.csv"]}

setup(name = "Ten Second Time",
      version = "0.1",
      description = "Ten Second Time Game",
      options = { "build_exe" : build_exe_options },
      executables = [Executable("main.py", target_name="tensecondtime.exe")]) # Program name
