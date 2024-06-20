#This simple script is meant to patch and disinfect already infected scenes with the leukocyte antivirus (aka the chinese virus)
#It kills the scriptJob responsible for infecting the file when saving and removes the propagation nodes.
#Finally it prompts the user for a complete cleanup of the userSetup.py for total disinfection.

#Use with obvious caution, if you have custom code in userSetup.py, clean that up manually.

#@TheFuchsen - Angel Canales Jun 2024
#github: https://github.com/TheFuchsen
#Twitter because I refuse to call it X: https://x.com/TheFuchsen

import maya.cmds as mc
import os

def killAntiLeuko():
    allJobs = mc.scriptJob(listJobs=True)
    for job in allJobs:
        if "SceneSaved" in job and "leukocyte.antivirus()" in job:
            jobNumber = int(job.split(":")[0]) 
            mc.scriptJob(kill=jobNumber, force=True)
            print("Leukocyte Antivirus killed.")
            return
    print(end="Leukocyte Antivirus is not running. ") 

def leukoPatch():
    sceneNodes=mc.ls()
    quarantine=[]
    for node in sceneNodes:
        if node =="vaccine_gene":
            quarantine.append(node)
        elif node=="breed_gene":
            quarantine.append(node)
    
    if quarantine:
        killAntiLeuko()
        mc.delete(quarantine)
        print("The scene was cleaned. Save your file before continuing.")
        mc.confirmDialog(
        title="LeukoPatch by TheFuchsen",
        message="La Escena fue limpiada. Guarda el archivo antes de continuar.\n\nThe scene was cleaned. Save your file before continuing.",
        button=["Aceptar"],
        defaultButton="Aceptar",
    )
        cleanUserSetup()
    else:
        killAntiLeuko()
        print("No infection was detected.")
        mc.confirmDialog(
        title="LeukoPatch by TheFuchsen",
        message="No se ha detectado infección en la escena.\n\nNo infection was detected in the scene.",
        button=["Aceptar"],
        defaultButton="Aceptar",
    )
        cleanUserSetup()

def cleanUserSetup():
    userSetupPath = os.path.expanduser("~") + "/maya/scripts/userSetup.py"
    try:
        infected_lines = {
            "import vaccine",
            "cmds.evalDeferred('leukocyte = vaccine.phage()')",
            "cmds.evalDeferred('leukocyte.occupation()')",
        }
        with open(userSetupPath, "r") as f:
            lines = f.readlines()
        infected = any(line.strip().startswith(infected_line) for line in lines for infected_line in infected_lines)

        if infected:
            result = mc.confirmDialog(
                title="LeukoPatch by TheFuchsen",
                message="El archivo userSetup.py está infectado. Se recomienda parchar userSetup.py antes de continuar.\nEsta acción eliminará y reemplazará tu archivo userSetup.py por un archivo con función vacía y protegido contra escritura para prevenir futuras infecciones.\n\n"
                        "userSetup.py is infected. It is recommended to patch userSetup.py file before continuing.\nThis action will delete and replace your userSetup.py file with an empty function and protected against write in order to prevent future infections.\n\n"
                        "¿Estás seguro de que deseas continuar?\n\n"
                        "Are you sure you want to continue?",
                button=["Aceptar / OK", "Cancelar / Cancel"],
                defaultButton="Cancelar / Cancel",
                cancelButton="Cancelar / Cancel",
                dismissString="Cancelar / Cancel"
            )

            if result == "Aceptar / OK":
                try:
                    os.remove(userSetupPath) #Esto elimina el archivo original (user setup.py)
                    with open(userSetupPath, "w") as f:
                        f.write("def emptyFunc():\n    pass") #Esto crea un archivo con una función vacia
                    os.chmod(userSetupPath, 0o444) #Finalmente lo fijamos como archivo Read-only, para prevenir reinfección
                    print("userSetup.py purgado y reemplazado por un archivo protegido.")
                    mc.inViewMessage(
                        amg="El archivo 'userSetup.py' ha sido purgado y reemplazado por un archivo protegido.\n\n"
                            "The file userSetup.py has been purged and replaced with a protected file.", pos='midCenter', fade=True
                            )
                    
                except FileNotFoundError:
                    print("userSetup.py no encontrado o ya está protegido.")
                    print("userSetup.py was not found or is already protected.")
                    mc.inViewMessage(
                        amg="userSetup.py no encontrado o ya está protegido. No se requiere limpieza.\n\n"
                            "userSetup.py was not found or is already protected. No cleanup needed.", pos='midCenter', fade=True
                            )
                    
                except Exception as e:
                    print("Error al limpiar userSetup.py:", e)
                    print("Error when cleaning userSetup.py:", e)
                    mc.inViewMessage(
                        amg="Error al limpiar userSetup.py:\n\n"
                            "Error when cleaning userSetup.py:\n\n"
                            "Exception: {e}", pos='midCenter', fade=True
                            )
            else:
                print("Limpieza de userSetup.py cancelada.")
                print("userSetup.py cleanup was canceled.")
                mc.inViewMessage(
                    amg="impieza de userSetup.py cancelada.\n\n"
                        "userSetup.py cleanup was canceled.", pos='midCenter', fade=True
                    )
        else:
            print("userSetup.py se encuentra limpio. No se requieren acciones.")
            print("userSetup.py is clean. No action needed.")
            mc.confirmDialog(
            title="LeukoPatch by TheFuchsen",
            message="No se ha detectado infección en userSetup.py. No se requieren más acciones.\n\nNo infection was detected in userSetup.py. No further action required.",
            button=["Aceptar"],
            defaultButton="Aceptar",
            )
    except FileNotFoundError:
        print("userSetup.py no encontrado o está protegido.")
        print("userSetup.py was not found or is protected.")
        mc.inViewMessage(
            amg="userSetup.py no encontrado o ya está protegido. No se requiere limpieza.\n\n"
                "userSetup.py was not found or is already protected. No cleanup needed.", pos='midCenter', fade=True
                )
        
    except Exception as e:
        print("Error al limpiar userSetup.py:", e)
        print("Error when cleaning userSetup.py:", e)
        mc.inViewMessage(
            amg="Error al leer userSetup.py:\n\n"
                "Error reading userSetup.py:\n\n"
                "Exception: {e}", pos='midCenter', fade=True
                        )
def onMayaDroppedPythonFile(*args, **kwargs):  
    leukoPatch()
