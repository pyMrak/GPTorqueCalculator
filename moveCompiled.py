import shutil
import os



compiledMain = "dist/"
sourcePath = r"\\10.110.8.81\AET-SI-TO-Izmenjava\Andrej_Mrak\GPtorqueCalculator"

if os.path.exists(sourcePath):
    shutil.rmtree(sourcePath)

#os.mkdir(Paths.sourcePath)
shutil.move(compiledMain, sourcePath)


# for folder in ["icons", "exe", "DataProcessor/Text"]:
#     shutil.copytree(folder, Paths.sourcePath+'/'+folder, dirs_exist_ok=True)
#
# shutil.copy(Paths.configFile, Paths.getConfigFile(Paths.sourcePath))
# for file in []:
#     shutil.copy(file, Paths.sourcePath + "/" + file)

for folder in ["build"]:
    shutil.rmtree(folder)


