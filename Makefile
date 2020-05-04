PROG := AviUtlAutoInstaller
SRCS := main.py

# 実行対象のPython
PYTHON := python.exe

# pyinstaller関連設定
PYINST := pyinstaller.exe
FLAGS := --clean

# workpath
WORKDIR := obj
# distpath
OUTDIR := bin

.PHONY: all run debug clean

all : $(PROG)

$(PROG) : 
	@mkdir.exe -p release
	$(PYINST) $(FLAGS) --workpath ./release/$(WORKDIR) --distpath ./release/$(OUTDIR) release.spec

run :
	@$(PYTHON) $(SRCS)

debug :
	@mkdir.exe -p debug
	$(PYINST) $(FLAGS) --workpath ./debug/$(WORKDIR) --distpath ./debug/$(OUTDIR) debug.spec

clean :
	@rm.exe -rf ./release ./debug __pycache__/ */__pycache__/

