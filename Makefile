PROG := AviUtlAutoInstaller
SRCS := src/main.py

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
	@mkdir -p release
	$(PYINST) $(FLAGS) --workpath ./release/$(WORKDIR) --distpath ./release/$(OUTDIR) spec/release.spec

run :
	@$(PYTHON) $(SRCS)

debug :
	@mkdir -p debug
	$(PYINST) $(FLAGS) --workpath ./debug/$(WORKDIR) --distpath ./debug/$(OUTDIR) spec/debug.spec

clean :
	@rm -rf ./release ./debug src/__pycache__/ src/*/__pycache__/

