import bpy
from bpy.app.handlers import persistent

@persistent
def load_handler_for_checkingupdate(_):
    print("Checking BlenderBIM Version!")
    import requests
    import addon_utils

    def findAddonVersion(addonName):
        for addon in addon_utils.modules():
            if addon.bl_info['name'] == addonName:
                return (addon.bl_info.get('version')[-1])

    def findStableVersion():
        r = requests.get('https://blenderbim.org/builds/')
        releaseList = []
        for l in str(r.text).split('\n'):
            if ("blenderbim" in l) and ("win" in l):
                releaseList.append(l)
        return(int(releaseList[-1].split("-")[1]))

    def findDailyVersion():
        gr = requests.get("https://api.github.com/repos/IfcOpenShell/IfcOpenShell/releases/latest")
        for n in gr.json()["assets"]:
            url = n["browser_download_url"]
            if ("blenderbim" in url) and ("py39" in url) and ("win" in url):
                return(int(url.split("/")[-2].split("-")[-1]))

    addonVersion = findAddonVersion("BlenderBIM")
    stableVersion = findStableVersion()
    dailyVersion = findDailyVersion()

    latest = stableVersion-addonVersion
    if latest > 0:
        print("New Stable Version Available")
    else:
        print("Latest Stable Version")


@persistent
def load_handler_for_startup(_):
    print("Checking Completed!")

# Add scene related startup scene and data settings here

def register():
    print("Registering to Change Defaults")
    bpy.app.handlers.load_factory_preferences_post.append(load_handler_for_checkingupdate)
    bpy.app.handlers.load_factory_startup_post.append(load_handler_for_startup)

def unregister():
    print("Unregistering to Change Defaults")
    bpy.app.handlers.load_factory_preferences_post.remove(load_handler_for_checkingupdate)
    bpy.app.handlers.load_factory_startup_post.remove(load_handler_for_startup)